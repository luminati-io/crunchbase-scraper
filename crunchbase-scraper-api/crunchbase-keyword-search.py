import requests
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

DEFAULT_OUTPUT_FILENAME_FORMAT = "crunchbase_keywords_{timestamp}.json"


class CrunchbaseKeywordSearcher:
    """Searches Crunchbase organizations by keywords using Bright Data API."""

    API_BASE_URL = "https://api.brightdata.com/datasets/v3"
    DATASET_ID = "gd_l1vijqt9jfj7olije"
    POLLING_INTERVAL = 5
    REQUEST_TIMEOUT = 30

    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("API token required")

        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def search_by_keywords(
        self,
        keywords: List[Dict[str, str]],
        output_filename: Optional[str] = None,
    ) -> bool:
        """Execute keyword search and save results."""
        if not keywords:
            logging.warning("No keywords provided")
            return False

        start_time = datetime.now()
        logging.info(f"Starting search for {len(keywords)} keywords")

        # Initiate search request
        search_response = self._trigger_search(keywords)
        if not search_response or "snapshot_id" not in search_response:
            return False

        snapshot_id = search_response["snapshot_id"]
        last_status = None

        # Monitor search progress
        while True:
            status = self._check_status(snapshot_id)
            elapsed = (datetime.now() - start_time).total_seconds()

            if status != last_status:
                self._log_status_change(status, elapsed)
                last_status = status

            if status == "ready":
                return self._handle_successful_search(snapshot_id, output_filename)

            if status in ["failed", "error", None]:
                return False

            time.sleep(self.POLLING_INTERVAL)

    def _trigger_search(self, keywords: List[Dict[str, str]]) -> Optional[Dict]:
        """Initiate keyword search through API."""
        try:
            response = requests.post(
                f"{self.API_BASE_URL}/trigger",
                headers=self.headers,
                params={
                    "dataset_id": self.DATASET_ID,
                    "include_errors": "true",
                    "type": "discover_new",
                    "discover_by": "keyword",
                },
                json=keywords,
                timeout=self.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._log_request_error("search trigger", e)
            return None

    def _check_status(self, snapshot_id: str) -> Optional[str]:
        """Check current search status."""
        try:
            response = requests.get(
                f"{self.API_BASE_URL}/progress/{snapshot_id}",
                headers=self.headers,
                timeout=self.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            return response.json().get("status")
        except requests.exceptions.RequestException as e:
            self._log_request_error("status check", e)
            return "error"

    def _fetch_data(self, snapshot_id: str) -> Optional[List[Dict]]:
        """Retrieve search results."""
        try:
            response = requests.get(
                f"{self.API_BASE_URL}/snapshot/{snapshot_id}",
                headers=self.headers,
                params={"format": "json"},
                timeout=self.REQUEST_TIMEOUT * 2,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._log_request_error("data fetch", e)
            return None

    def _handle_successful_search(self, snapshot_id: str, filename: str) -> bool:
        """Process and save successful search results."""
        data = self._fetch_data(snapshot_id)
        if data is None:
            return False

        return self._save_data(
            data,
            filename
            or DEFAULT_OUTPUT_FILENAME_FORMAT.format(
                timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
            ),
        )

    def _save_data(self, data: List[Dict], filename: str) -> bool:
        """Save results to JSON file."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved {len(data)} records to {filename}")
            return True
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Data save failed: {e}")
            return False

    def _log_status_change(self, status: str, elapsed: float):
        """Handle status update logging."""
        if status == "running":
            logging.info(f"Status: running ({elapsed:.1f}s elapsed)")
        elif status == "ready":
            logging.info(f"Completed in {elapsed:.1f} seconds")
        elif status in ["failed", "error"]:
            logging.error(f"Failed after {elapsed:.1f} seconds")
        else:
            logging.info(f"Status: {status} ({elapsed:.1f}s)")

    def _log_request_error(self, operation: str, error: Exception):
        """Standardize API error logging."""
        logging.error(f"API {operation} error: {error}")
        if hasattr(error, "response") and error.response:
            logging.error(
                f"Response {error.response.status_code}: {error.response.text[:500]}"
            )


def main() -> None:
    """Example execution with configuration."""
    config = {
        "api_token": "API_TOKEN",  # Replace with actual token
        "keywords": [{"keyword": "AI"}, {"keyword": "Venture Capital"}],
        "output_file": None,  # Optional custom filename
    }

    try:
        searcher = CrunchbaseKeywordSearcher(config["api_token"])
        success = searcher.search_by_keywords(config["keywords"], config["output_file"])
        logging.info("Search completed" if success else "Search failed")

    except Exception as e:
        logging.exception(f"Critical error: {e}")


if __name__ == "__main__":
    main()
