import time
import requests
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FederalRegisterCollector:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def collect(self, days: int = 7) -> list[dict]:
        target_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        url = f"{self.base_url}/documents.json"

        params = {
            "conditions[agencies][]": "food-and-drug-administration",
            "per_page": 100,
            "order": "newest",
            "conditions[publication_date][gte]": target_date,
            "fields[]": ["title", "abstract", "type", "publication_date", "html_url", "pdf_url", "document_number", "agencies", "subtype"]
        }

        all_documents = []

        while url:
            try:
                response = requests.get(url, params=params if url == f"{self.base_url}/documents.json" else None)
                if response.status_code != 200:
                    logger.error(f"API returned status {response.status_code}: {response.text}")
                    return []

                data = response.json()

                for doc in data.get("results", []):
                    parsed_doc = {
                        "title": doc.get("title", ""),
                        "abstract": doc.get("abstract", "") or "",
                        "document_type": doc.get("type", ""),
                        "publication_date": doc.get("publication_date", ""),
                        "html_url": doc.get("html_url", ""),
                        "pdf_url": doc.get("pdf_url", "") or "",
                        "document_number": doc.get("document_number", "")
                    }
                    all_documents.append(parsed_doc)

                url = data.get("next_page_url")
                if url:
                    time.sleep(2)  # Respect rate limits
            except Exception as e:
                logger.error(f"Failed to collect documents: {e}")
                break

        return all_documents

    def filter_relevant_types(self, documents: list[dict]) -> list[dict]:
        allowed_types = ["Notice", "Rule", "Proposed Rule", "Presidential Document"]
        excluded_keywords = ["Petition", "Meeting", "Tobacco", "Food Additive", "GRAS", "Animal Drug", "Veterinary"]

        filtered = []
        for doc in documents:
            if doc["document_type"] not in allowed_types:
                continue

            title = doc["title"].lower()
            if any(keyword.lower() in title for keyword in excluded_keywords):
                continue

            filtered.append(doc)

        return filtered
