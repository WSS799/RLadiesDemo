import json
import logging
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
from src.classify.prompts import ENRICHMENT_SYSTEM_PROMPT, ENRICHMENT_USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

class EnrichmentEngine:
    def __init__(self, api_key: str, model: str):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def fetch_full_text(self, html_url: str) -> str:
        if not html_url:
            return "Full text unavailable."

        try:
            response = requests.get(html_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            content_area = soup.find(id="fulltext_content_area")
            if not content_area:
                content_area = soup.find("div", class_="main-content")

            if content_area:
                text = content_area.get_text(separator=' ', strip=True)
            else:
                text = soup.get_text(separator=' ', strip=True)

            return text[:15000]
        except Exception as e:
            logger.warning(f"Failed to fetch full text for {html_url}: {e}")
            return "Full text unavailable."

    def enrich(self, classified_doc: dict) -> dict:
        if classified_doc.get("classification") != "CRITICAL":
            return classified_doc

        full_text = self.fetch_full_text(classified_doc.get("html_url", ""))

        user_prompt = ENRICHMENT_USER_PROMPT_TEMPLATE.format(
            title=classified_doc.get("title"),
            document_type=classified_doc.get("document_type"),
            publication_date=classified_doc.get("publication_date"),
            full_text=full_text
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=ENRICHMENT_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}]
            )

            raw_text = response.content[0].text
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].strip()

            impact_brief = json.loads(raw_text)
            classified_doc["impact_brief"] = impact_brief
        except Exception as e:
            logger.error(f"Enrichment error for {classified_doc.get('document_number')}: {e}")
            classified_doc["impact_brief"] = {"error": "Failed to generate impact brief", "details": str(e)}

        return classified_doc

    def enrich_batch(self, classified_docs: list[dict]) -> list[dict]:
        enriched_docs = []
        for doc in classified_docs:
            if doc.get("classification") == "CRITICAL":
                enriched_docs.append(self.enrich(doc))
            else:
                enriched_docs.append(doc)
        return enriched_docs
