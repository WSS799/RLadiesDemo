import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

class DigestBuilder:
    def __init__(self):
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.template = self.env.get_template('weekly_digest.html')

    def build(self, classified_docs: list[dict], subscriber_name: str) -> str:
        critical_items = [doc for doc in classified_docs if doc.get("classification") == "CRITICAL"]
        important_items = [doc for doc in classified_docs if doc.get("classification") == "IMPORTANT"]
        informational_items = [doc for doc in classified_docs if doc.get("classification") == "INFORMATIONAL"]

        dates = [doc["publication_date"] for doc in classified_docs if doc.get("publication_date")]
        if dates:
            oldest = min(dates)
            newest = max(dates)
            date_range = f"{oldest} to {newest}"
        else:
            date_range = datetime.now().strftime("%Y-%m-%d")

        html_content = self.template.render(
            subscriber_name=subscriber_name,
            date_range=date_range,
            critical_items=critical_items,
            important_items=important_items,
            informational_items=informational_items,
            total_critical=len(critical_items),
            total_important=len(important_items),
            total_informational=len(informational_items)
        )
        return html_content
