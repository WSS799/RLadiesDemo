import time
import json
import logging
from anthropic import Anthropic
from jinja2 import Template
from .prompts import SYSTEM_PROMPT_TEMPLATE, CLASSIFICATION_USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

class ClassificationEngine:
    def __init__(self, api_key: str, model: str, profile: dict):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.profile = profile
        template = Template(SYSTEM_PROMPT_TEMPLATE)
        self.system_prompt = template.render(**profile)

    def classify_document(self, document: dict) -> dict:
        user_prompt = CLASSIFICATION_USER_PROMPT_TEMPLATE.format(
            title=document["title"],
            document_type=document["document_type"],
            publication_date=document["publication_date"],
            abstract=document["abstract"]
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=self.system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            raw_text = response.content[0].text
            try:
                # Handle cases where the LLM might have wrapped JSON in markdown codeblocks
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].strip()

                classification_data = json.loads(raw_text)
            except json.JSONDecodeError:
                classification_data = {
                    "classification": "PARSE_ERROR",
                    "rationale": raw_text
                }
        except Exception as e:
            logger.error(f"API Error classifying document {document.get('document_number')}: {e}")
            classification_data = {
                "classification": "PARSE_ERROR",
                "rationale": str(e)
            }

        result = document.copy()
        result.update(classification_data)
        return result

    def classify_batch(self, documents: list[dict]) -> list[dict]:
        results = []
        for doc in documents:
            classified = self.classify_document(doc)
            if classified.get("classification") != "IRRELEVANT":
                results.append(classified)
            time.sleep(0.5)  # Rate limiting

        priority_map = {"CRITICAL": 0, "IMPORTANT": 1, "INFORMATIONAL": 2, "PARSE_ERROR": 3}
        results.sort(key=lambda x: priority_map.get(x.get("classification"), 99))

        return results
