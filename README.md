# Crunchbase Scraper

This repository provides two approaches for extracting business intelligence data from Crunchbase:

1. **Basic Scraper Script:** Lightweight, browser-automated scraper for limited data collection.
2. **Bright Data Crunchbase Scraper API:** A robust, scalable, and maintenance-free solution for high-volume and reliable data extraction.

## Table of Contents
- [Basic Crunchbase Scraper](#1-basic-crunchbase-scraper)
    - [Features](#features)
    - [Prerequisites](#prerequisites)
    - [Implementation](#implementation)
    - [Sample Output](#sample-output)
    - [Limitations & Challenges](#significant-limitations--challenges)
- [Bright Data Crunchbase Scraper API](#2-bright-data-crunchbase-scraper-api)
    - [Key Benefits](#key-benefits)
    - [Getting Started](#getting-started)
    - [API Methods](#api-methods)
      - [A. Collect Crunchbase Data by URL](#a-collect-crunchbase-data-by-url)
      - [B. Discover Crunchbase Data by Keyword](#b-discover-crunchbase-data-by-keyword)
- [API Configuration & Delivery Options](#api-configuration--delivery-options)
- [No-Code Scraper Interface](#no-code-scraper-interface)
- [Alternative: Pre-Collected Crunchbase Datasets](#alternative-pre-collected-crunchbase-datasets)
- [Resources & Support](#resources--support)


## 1. Basic Crunchbase Scraper

A Python implementation demonstrating how to extract fundamental company data from Crunchbase profiles.

<img width="800" alt="Bright Data Platform Interface" src="https://github.com/user-attachments/assets/03b5a4c6-ba43-4595-bab8-96161740e197" />

### Features

This script collects publicly available data points, including:

- Company fundamentals (description, website, founding date)
- Contact information (email, phone)
- Operational metrics (status, employee count, location)
- Leadership information (founders)
- Industry classifications

### Prerequisites

* Python 3.x installed
* SeleniumBase library: `pip install seleniumbase`

### Implementation

1. **Get the Code:** Access the script file here: [free-crunchbase-scraper/crunchbase-scraper.py](https://github.com/triposat/Crunchbase-Scraper/blob/main/free-crunchbase-scraper/crunchbase-scraper.py)
2. **Set Target URL:** Open the script and modify the `target_url` variable to the specific Crunchbase company profile you wish to scrape.
    
    ```python
    target_url = "https://www.crunchbase.com/organization/your-target-company"
    ```
    
3. **Run the Script:** Execute the script from your terminal: `python crunchbase-scraper.py`


💡 **Note:** This script uses [SeleniumBase](https://seleniumbase.io/), an advanced Selenium wrapper with built-in tools for handling CAPTCHAs and other browser challenges. Learn more: [Web Scraping with SeleniumBase](https://brightdata.com/blog/web-data/web-scraping-with-seleniumbase) and [SeleniumBase with Proxies](https://brightdata.com/blog/proxy-101/seleniumbase-with-proxies).


### Sample Output

The script extracts structured data in the following format:

```jsonc
{
  "description": "Bright Data offers a platform for ethical web data collection and analysis.",
  "website_url": "[https://brightdata.com](https://brightdata.com/)",
  "founding_date": "2018-07-01",
  "email": "[sales@brightdata.com](mailto:sales@brightdata.com)",
  "phone": "(888) 538-9204",
  "company_overview": "Bright Data is a data collection platform that helps businesses gather publicly available web data...",
  "headquarters_location": "New York, United States, North America",
  "operating_status": "active",
  "employee_count": "251-500",
  "founder_names": [
    "Derry Shribman",
    "Ofer Vilenski"
  ],
  "industry_categories": [
    "Business Intelligence",
    "Cloud Data Services", "/* ... */"
  ]
}
```

### Significant Limitations & Challenges

This approach encounters significant [web scraping challenges](https://brightdata.com/blog/web-data/web-scraping-challenges) that make it unsuitable for production-scale data collection:

- **IP Blocking & Rate Limiting:** Crunchbase actively monitors and limits requests from individual IP addresses. Your IP will likely be blocked quickly after some scraping attempts.
- **Sophisticated Anti-Bot Measures:** Crunchbase employs advanced security, including CAPTCHAs (like [Cloudflare Turnstile](https://brightdata.com/products/web-unlocker/captcha-solver/cloudflare-turnstile)) and behavioral analysis, specifically designed to detect and block automated scripts.

  <img width="800" alt="Crunchbase CAPTCHA Challenge" src="https://github.com/user-attachments/assets/44cb5a79-e943-454b-9354-28b78ef67b57" />

- **Dynamic Website Structure:** Crunchbase frequently updates its website layout and code. Any change can break the script, requiring constant, time-consuming maintenance.
- **Scalability Issues:** This method cannot scale to handle multiple URLs efficiently or process large volumes of data.
- **Maintenance Overhead:** You are responsible for managing infrastructure, handling blocks, updating the script, and ensuring compliance.


## 2. Bright Data Crunchbase Scraper API
The [Bright Data Crunchbase Scraper API](https://brightdata.com/products/web-scraper/crunchbase) provides a robust, scalable, and hassle-free way to extract comprehensive data from Crunchbase without dealing with the complexities of scraping.

### Key Benefits

- **Bypasses Technical Challenges:** Automatically handles IP blocks, CAPTCHAs, and rate limits using advanced proxy rotation and web unlocking technology.
- **Enterprise Scalability:** Designed for high-volume data collection.
- **High Reliability:** Ensures consistent data delivery with enterprise-grade uptime.
- **Developer-Friendly:** Simple API integration eliminates complex scraper development and maintenance.
- **Structured Data Format:** Delivers clean, normalized data ready for analysis.
- **Regulatory Compliance:** Adheres to data privacy regulations, including GDPR and CCPA.
- **Flexible Pricing:** Pay-as-you-go model based on successful data delivery.
- **Dedicated Support:** Access 24/7 expert technical support.
- **Implementation Options:** Use the API programmatically or through the [No-Code Scraper](https://brightdata.com/products/web-scraper/no-code) interface.

### Getting Started

1. **Create Account:** Sign up for a [Bright Data account](https://brightdata.com/) *(New users receive $5 credits after adding a payment method)*.
2. **Generate API Token:** Obtain your unique [API key](https://docs.brightdata.com/general/account/api-token) from your dashboard.
3. **Implementation Guide:** For detailed configuration steps for both API methods and No-Code interface, see:
[setup-bright-data-crunchbase-scraper.md](https://github.com/triposat/Crunchbase-Scraper/blob/main/setup-bright-data-crunchbase-scraper.md)


### API Methods

The API offers two primary data collection approaches:

### A. Collect Crunchbase Data by URL

Retrieves comprehensive profile information for specific Crunchbase company URLs.

**Input Parameters:**

| Parameter | Required | Description |
| --- | --- | --- |
| `url` | Yes | The full Crunchbase company URL. |

**Example Request (Python):**

```python
config = {
    "api_token": "YOUR_API_TOKEN",  # Replace with actual token
    "organizations": [
        {"url": "https://www.crunchbase.com/organization/apple"},
        {"url": "https://www.crunchbase.com/organization/brightdata"},
    ],
    "output_file": "crunchbase-company-profiles.json", # Optional custom filename
}
# ... rest of the script uses this config
```

- Replace `"YOUR_API_TOKEN"` with your actual Bright Data API token.
- Modify the `organizations` list with your target Crunchbase URLs.
- See the full runnable script: [crunchbase-scraper-api/crunchbase-profile-fetcher.py](https://github.com/triposat/Crunchbase-Scraper/blob/main/crunchbase-scraper-api/crunchbase-profile-fetcher.py)

**Example Request (cURL):**

```bash
curl -X POST \
  "https://api.brightdata.com/datasets/v3/trigger?dataset_id=gd_l1vijqt9jfj7olije&include_errors=true" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"url":"https://www.crunchbase.com/organization/apple"},{"url":"https://www.crunchbase.com/organization/brightdata"}]'
```


**Sample Output Snippet:**

The API returns comprehensive, structured data. Below is a small fraction of the available fields for a single company:

```jsonc
{
  "companyName": "Bright Data",
  "legalName": "Bright Data",
  "website": "https://brightdata.com",
  "description": "Offers a platform for ethical web data collection and analysis...",
  "foundedDate": "2014-01-01",
  "location": {"city": "New York", "state": "New York", "country": "United States"},
  "companyType": "For-Profit",
  "operatingStatus": "Active",
  "ipoStatus": "Private (Acquired)",
  "employeeSizeRange": "251-500",
  "industries": ["Business Intelligence", "Cloud Data Services", "..."],
  "keyPersonnel": {
    "ceo": {"name": "Or Lenchner", "...": "..."},
    "founders": [{"name": "Derry Shribman", "...": "..."}, {"name": "Ofer Vilenski", "...": "..."}]
  },
  "webTraffic": {"monthlyVisits": 865525, "source": "Semrush", "...": "..."},
  "technology": {"activeTechCount": 19, "exampleTechUsed": ["Cloudflare Hosting", "..."]},
  "products": {"totalActive": 23, "exampleProductNames": ["Residential Proxies", "..."]},
  "acquisitionDetails": {"acquiredBy": "EMK Capital", "priceUSD": 200000000, "...": "..."},
  "intellectualProperty": {"patentsGranted": 199, "trademarksRegistered": 18}
  // Additional data fields available
}
```

View complete sample response: [crunchbase-data/crunchbase-company-profiles.json](https://github.com/triposat/Crunchbase-Scraper/blob/main/crunchbase-data/crunchbase-company-profiles.json)

### B. Discover Crunchbase Data by Keyword

Identifies companies associated with specific keywords or industries (e.g., "AI", "Venture Capital", "SaaS").

<img width="800" alt="Discover by Keyword Interface Example" src="https://github.com/user-attachments/assets/56e59e94-19fa-4977-84a0-4b70c794cb20" />

**Input Parameter:**

| Parameter | Required | Description |
| --- | --- | --- |
| `keyword` | Yes | The keyword(s) to search for related companies. |

**Example Request (Python):**

```python
config = {
    "api_token": "YOUR_API_TOKEN",  # Replace with actual token
    "keywords": [
        {"keyword": "AI"},
        {"keyword": "Venture Capital"},
        {"keyword": "SaaS"}
        # Add more keywords as needed
    ],
    "output_file": "crunchbase-keyword-results.json", # Optional: Customize output filename
}
# ... (script uses this config to make the API call)
```

- Replace `"YOUR_API_TOKEN"`.
- Modify the `keywords` list.
- See the full runnable script: [`crunchbase-scraper-api/crunchbase-keyword-search.py`](https://github.com/triposat/Crunchbase-Scraper/blob/main/crunchbase-scraper-api/crunchbase-keyword-search.py)

**Example Request (cURL):**

```bash
curl -X POST \
  "https://api.brightdata.com/datasets/v3/trigger?dataset_id=gd_l1vijqt9jfj7olije&include_errors=true&type=discover_new&discover_by=keyword" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"keyword":"AI"},{"keyword":"Venture Capital"}]'

```

**Sample Output Snippet:**

The response includes data for *multiple* companies matching the keyword search. This shows the structure for one result:

```jsonc
{
  "companyName": "Airbus", // Example result for "AI" keyword
  "legalName": "Airbus Defense and Space Holdings, Inc.",
  "website": "https://us.airbus.com",
  "description": "Airbus designs, manufactures, and delivers aerospace products...",
  "foundedDate": "2014-01-01",
  "location": {
    "city": "Herndon",
    "state": "Virginia",
    "country": "United States"
  },
  "companyType": "For-Profit",
  "operatingStatus": "Active",
  "ipoStatus": "Private",
  "employeeSizeRange": "10001+",
  "industries": [
    "Aerospace",
    "Commercial",
    "Manufacturing"
  ],
  // ... includes similar detailed fields as the 'Collect by URL' method
}
```

View complete sample response: [crunchbase-data/crunchbase-keyword-results.json](https://github.com/triposat/Crunchbase-Scraper/blob/main/crunchbase-data/crunchbase-keyword-results.json)

### API Configuration & Delivery Options

Customize your data collection jobs using additional parameters within the API request:

| Parameter | Type | Description | Example |
| --- | --- | --- | --- |
| `limit` | `integer` | Sets the maximum number of results per input (URL or keyword). | `limit=50` |
| `include_errors` | `boolean` | Includes detailed error information in the response if issues occur. | `include_errors=true` |
| `format` | `enum` | Specifies the desired output format (`json`, `csv`, `ndjson`). | `format=csv` |
| `notify` | `url` | Provides a webhook URL to receive notifications upon job completion. | `notify=https://...` |

Data can be delivered directly to your preferred [external storage](https://docs.brightdata.com/scraping-automation/web-scraper-api/overview#via-deliver-to-external-storage%3A) or via a [webhook](https://docs.brightdata.com/scraping-automation/web-data-apis/web-scraper-api/overview#via-webhook%3A).

For comprehensive documentation on the Web Scraper API and triggering collections, see:

- [Bright Data Web Scraper API Documentation](https://docs.brightdata.com/scraping-automation/web-scraper-api/overview)
- [Trigger Collection API Reference](https://docs.brightdata.com/api-reference/web-scraper-api/trigger-a-collection)



### No-Code Scraper Interface

For users who prefer a visual, point-and-click approach, Bright Data also offers the [No-Code Scraper](https://brightdata.com/products/web-scraper/no-code). This interface allows you to configure and launch Crunchbase data collection tasks using the same powerful underlying infrastructure, without writing any code. See the [Setup Guide](https://github.com/triposat/Crunchbase-Scraper/blob/main/setup-bright-data-crunchbase-scraper.md) for guidance.

## Alternative: Pre-Collected Crunchbase Datasets

If you require immediate access to large amounts of structured Crunchbase data without running scraping jobs yourself, consider Bright Data's pre-collected [Crunchbase Datasets](https://brightdata.com/products/datasets/crunchbase).

- **Ready-to-Use:** Access validated and structured Crunchbase data instantly.
- **Comprehensive Coverage:** Datasets include over 100 data points per company profile.
- **Regular Updates:** Choose from various data freshness options (daily, weekly, monthly, or custom).
- **Flexible Purchase Options:** Acquire the entire dataset or specific subsets tailored to your needs and budget.
- **Easy Integration:** Integrate datasets seamlessly via API or direct download.
- **Sample Data Available:** Request a sample to evaluate data quality and fit.


## Resources & Support

- **Bright Data Documentation:**
    - [Crunchbase Scraper API Product Page](https://brightdata.com/products/web-scraper/crunchbase)
    - [Web Scraper API Documentation](https://docs.brightdata.com/scraping-automation/web-scraper-api/overview)
    - [API Reference: Trigger Collection](https://docs.brightdata.com/api-reference/web-scraper-api/trigger-a-collection)
    - [Datasets Product Page](https://brightdata.com/products/datasets)
    - [Getting Your API Token](https://docs.brightdata.com/general/account/api-token)
- **Guides & Blog Posts:**
    - [How to Scrape Crunchbase (Comprehensive Guide)](https://brightdata.com/blog/web-data/how-to-scrape-crunchbase)
    - [Web Scraping Without Getting Blocked](https://brightdata.com/blog/web-data/web-scraping-without-getting-blocked)
    - [Setup Guide for Bright Data Crunchbase Scraper (in this repo)](https://github.com/triposat/Crunchbase-Scraper/blob/main/setup-bright-data-crunchbase-scraper.md)
- **Technical Support:** Contact the Bright Data support team 24/7 via your account dashboard or email at [support@brightdata.com](mailto:support@brightdata.com).
