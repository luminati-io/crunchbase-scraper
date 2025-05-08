import requests
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

DEFAULT_OUTPUT_FILENAME_FORMAT = "crunchbase_organizations_{timestamp}.json"


class CrunchbaseOrganizationsCollector:
    """Collects Crunchbase organization data via Bright Data Datasets API."""

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

    def collect_organizations(
        self,
        organization_urls: List[Dict[str, str]],
        output_filename: Optional[str] = None,
    ) -> bool:
        if not organization_urls:
            logging.warning("No organization URLs provided")
            return False

        start_time = datetime.now()
        logging.info(f"Starting collection for {len(organization_urls)} organizations")

        # Trigger initial collection request
        collection_response = self._trigger_collection(organization_urls)
        if not collection_response or "snapshot_id" not in collection_response:
            return False

        snapshot_id = collection_response["snapshot_id"]
        last_status = None

        # Poll for completion status
        while True:
            status = self._check_status(snapshot_id)
            elapsed = (datetime.now() - start_time).total_seconds()

            if status != last_status:
                self._log_status_change(status, elapsed)
                last_status = status

            if status == "ready":
                return self._handle_successful_collection(snapshot_id, output_filename)

            if status in ["failed", "error", None]:
                return False

            time.sleep(self.POLLING_INTERVAL)

    def _trigger_collection(self, urls: List[Dict[str, str]]) -> Optional[Dict]:
        """Initiate data collection job through API."""
        try:
            response = requests.post(
                f"{self.API_BASE_URL}/trigger",
                headers=self.headers,
                params={"dataset_id": self.DATASET_ID, "include_errors": "true"},
                json=urls,
                timeout=self.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._log_request_error("collection trigger", e)
            return None

    def _check_status(self, snapshot_id: str) -> Optional[str]:
        """Retrieve current job status from API."""
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
        """Retrieve collected data from completed job."""
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

    def _handle_successful_collection(self, snapshot_id: str, filename: str) -> bool:
        """Process and save successfully collected data."""
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
        """Persist collected data to JSON file."""
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
        """Handle API error logging consistently."""
        logging.error(f"API {operation} error: {error}")
        if hasattr(error, "response") and error.response:
            logging.error(
                f"Response {error.response.status_code}: {error.response.text[:500]}"
            )


def main() -> None:
    """Execution entry point with example configuration."""
    config = {
        "api_token": "API_TOKEN",  # Replace with actual token
        "organizations": [
            {"url": "https://www.crunchbase.com/organization/apple"},
            {"url": "https://www.crunchbase.com/organization/brightdata"},
        ],
        "output_file": None,  # Optional custom filename
    }

    try:
        collector = CrunchbaseOrganizationsCollector(config["api_token"])
        success = collector.collect_organizations(
            config["organizations"], config["output_file"]
        )
        logging.info("Process completed" if success else "Process failed")

    except Exception as e:
        logging.exception(f"Critical error: {e}")


if __name__ == "__main__":
    main()