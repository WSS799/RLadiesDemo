import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

@dataclass
class Settings:
    anthropic_api_key: str
    sendgrid_api_key: str
    sender_email: str
    recipient_email: str
    classification_model: str = "claude-sonnet-4-20250514"
    enrichment_model: str = "claude-sonnet-4-20250514"
    federal_register_base_url: str = "https://www.federalregister.gov/api/v1"
    lookback_days: int = 7
    profiles_dir: Path = Path(__file__).parent / "profiles"

def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
        sendgrid_api_key=os.environ.get("SENDGRID_API_KEY", ""),
        sender_email=os.environ.get("SENDER_EMAIL", ""),
        recipient_email=os.environ.get("RECIPIENT_EMAIL", "")
    )
