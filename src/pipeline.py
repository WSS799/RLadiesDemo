import os
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from config.settings import load_settings
from src.collect.federal_register import FederalRegisterCollector
from src.classify.engine import ClassificationEngine
from src.enrich.impact_brief import EnrichmentEngine
from src.deliver.email_builder import DigestBuilder
from src.deliver.sender import EmailSender

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self):
        self.settings = load_settings()

        self.profiles = []
        if self.settings.profiles_dir.exists():
            for yaml_file in self.settings.profiles_dir.glob("*.yaml"):
                with open(yaml_file, 'r') as f:
                    self.profiles.append(yaml.safe_load(f))

        self.collector = FederalRegisterCollector(self.settings.federal_register_base_url)
        self.enricher = EnrichmentEngine(self.settings.anthropic_api_key, self.settings.enrichment_model)
        self.digest_builder = DigestBuilder()
        self.sender = EmailSender(self.settings.sendgrid_api_key, self.settings.sender_email)

    def run(self):
        logger.info("Step 1: Collecting documents from Federal Register...")
        raw_documents = self.collector.collect(self.settings.lookback_days)

        logger.info("Step 2: Filtering relevant document types...")
        filtered_documents = self.collector.filter_relevant_types(raw_documents)
        logger.info(f"Step 3: Collected {len(filtered_documents)} valid documents after filtering (from {len(raw_documents)} raw).")

        all_results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for profile in self.profiles:
            subscriber_name = profile.get("subscriber_name", "Subscriber")
            subscriber_email = profile.get("subscriber_email", self.settings.recipient_email)
            logger.info(f"Step 4: Processing for {subscriber_name}")

            # Initialize classification engine for this specific profile
            classifier = ClassificationEngine(
                api_key=self.settings.anthropic_api_key,
                model=self.settings.classification_model,
                profile=profile
            )

            logger.info(f"  a. Classifying {len(filtered_documents)} documents...")
            classified_docs = classifier.classify_batch(filtered_documents)

            logger.info("  b. Enriching CRITICAL documents...")
            enriched_docs = self.enricher.enrich_batch(classified_docs)

            logger.info("  c. Building HTML digest...")
            html_content = self.digest_builder.build(enriched_docs, subscriber_name)

            critical_count = sum(1 for d in enriched_docs if d.get("classification") == "CRITICAL")
            important_count = sum(1 for d in enriched_docs if d.get("classification") == "IMPORTANT")
            informational_count = sum(1 for d in enriched_docs if d.get("classification") == "INFORMATIONAL")

            dates = [doc["publication_date"] for doc in enriched_docs if doc.get("publication_date")]
            date_range = f"{min(dates)} to {max(dates)}" if dates else datetime.now().strftime("%Y-%m-%d")
            subject = f"RegWatch Digest: {date_range} | {critical_count} Critical Items"

            logger.info("  d. Sending email...")
            success = self.sender.send(subscriber_email, subject, html_content)

            if success:
                logger.info(f"  e. SUCCESS: {subscriber_name}: {critical_count} critical, {important_count} important, {informational_count} informational items sent.")
            else:
                logger.error(f"  e. FAILED to send email for {subscriber_name}.")

            all_results[subscriber_name] = enriched_docs

        logger.info("Step 5: Saving raw results...")
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        with open(data_dir / f"run_{timestamp}.json", "w") as f:
            json.dump(all_results, f, indent=2)

if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
