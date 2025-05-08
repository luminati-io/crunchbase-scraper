from seleniumbase import SB
from bs4 import BeautifulSoup
import json
import re
import html.entities


def extract_crunchbase_info(html_content):
    """
    Extracts structured company data from Crunchbase HTML content.

    Args:
        html_content (str): Raw HTML from Crunchbase page

    Returns:
        dict: Structured company information with cleaned values
    """
    result = {
        "description": None,
        "website_url": None,
        "founding_date": None,
        "email": None,
        "phone": None,
        "company_overview": None,
        "headquarters_location": None,
        "operating_status": None,
        "employee_count": None,
        "founder_names": [],
        "industry_categories": [],
    }

    soup = BeautifulSoup(html_content, "lxml")
    json_script = soup.find("script", {"id": "ng-state", "type": "application/json"})
    json_text = json_script.string if json_script else html_content

    def extract_data(pattern, text=json_text, default=None):
        """Helper to extract first regex match from text"""
        match = re.search(pattern, text)
        return match.group(1) if match else default

    # Core company information
    result.update(
        {
            "description": extract_data(r'"target_short_description"\s*:\s*"([^"]+)"'),
            "website_url": extract_data(r'"website"\s*:\s*{\s*"value"\s*:\s*"([^"]+)"'),
            "founding_date": extract_data(
                r'"started_on"\s*:\s*{\s*"value"\s*:\s*"([^"]+)"'
            ),
            "email": extract_data(r'"contact_email"\s*:\s*"([^"]+)"'),
            "phone": extract_data(r'"phone_number"\s*:\s*"([^"]+)"'),
            "company_overview": extract_data(r'"description"\s*:\s*"([^"]+)"'),
            "operating_status": extract_data(r'"operating_status"\s*:\s*"([^"]+)"'),
            "employee_count": extract_data(r'"num_employees_enum"\s*:\s*"([^"]+)"'),
        }
    )

    # Location information
    if location_data := extract_data(
        r'"location_identifiers"\s*:\s*\[(.*?)\]', json_text
    ):
        location_parts = {}
        for match in re.finditer(
            r'"location_type"\s*:\s*"([^"]+)".*?"value"\s*:\s*"([^"]+)"', location_data
        ):
            location_parts[match.group(1)] = match.group(2)
        result["headquarters_location"] = ", ".join(
            location_parts.get(key, "") for key in ("city", "region", "country")
        )

    # Founders information
    if founders := extract_data(r'"founder_identifiers"\s*:\s*\[(.*?)\]', json_text):
        result["founder_names"] = re.findall(r'"value"\s*:\s*"([^"]+)"', founders)

    # Industry categories (fallback to HTML if JSON not found)
    if categories := extract_data(r'"categories"\s*:\s*\[(.*?)\]', json_text):
        result["industry_categories"] = re.findall(
            r'"value"\s*:\s*"([^"]+)"', categories
        )
    else:
        result["industry_categories"] = [
            div.text.strip() for div in soup.select("div.chip-text")
        ]

    # Normalize employee count format
    if result["employee_count"]:
        count_match = re.match(
            r"(?:c_)?0*(\d+)[_-]0*(\d+|max)", result["employee_count"]
        )
        if count_match:
            lower_bound = int(count_match.group(1))
            upper_bound = count_match.group(2)
            result["employee_count"] = (
                f"{lower_bound}+"
                if upper_bound == "max"
                else f"{lower_bound}-{int(upper_bound)}"
            )

    return clean_string_values(result)


def clean_string_values(data):
    """
    Recursively cleans string values by handling:
    - Escaped characters
    - Unicode sequences
    - HTML entities
    - Whitespace normalization

    Args:
        data: Input data structure (dict, list, or str)

    Returns:
        Cleaned data structure
    """
    if isinstance(data, dict):
        return {k: clean_string_values(v) for k, v in data.items()}
    if isinstance(data, list):
        return [clean_string_values(v) for v in data]
    if isinstance(data, str):
        cleaned = data.replace("\\n", "\n").replace("\\r", "\r")
        try:
            cleaned = cleaned.encode("utf-8").decode("unicode_escape")
        except UnicodeDecodeError:
            pass
        cleaned = re.sub(
            r"&([a-z]+|#[0-9]+);",
            lambda m: chr(html.entities.name2codepoint.get(m.group(1), 0)),
            cleaned,
        )
        return re.sub(r"\s+", " ", cleaned).strip()
    return data


def fetch_crunchbase_data(url):
    """
    Executes browser automation to fetch and process Crunchbase data

    Args:
        url (str): Valid Crunchbase organization URL

    Returns:
        dict: Structured company data
    """
    with SB(uc=True, headless=False, locale="en") as browser:
        browser.open(url)
        browser.wait_for_ready_state_complete()
        browser.wait_for_element_present('script[id="ng-state"]', timeout=20)

        # Handle cookie consent if present
        browser.click_if_visible("#onetrust-accept-btn-handler", timeout=5)
        browser.sleep(2)  # Allow dynamic content to load

        return extract_crunchbase_info(browser.get_page_source())


def main():
    """Entry point with error handling and output"""
    target_url = "https://www.crunchbase.com/organization/databricks"

    try:
        print(f"🔄 Fetching data from: {target_url}")
        company_data = fetch_crunchbase_data(target_url)

        # Save as JSON
        with open("company_data.json", "w", encoding="utf-8") as f:
            json.dump(company_data, f, indent=2, ensure_ascii=False)

        print("✅ Data successfully retrieved")
    except Exception as e:
        print(f"❌ Error processing {target_url}: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
