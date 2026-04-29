import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self, api_key: str, sender_email: str):
        self.client = SendGridAPIClient(api_key)
        self.sender_email = sender_email

    def send(self, to_email: str, subject: str, html_content: str) -> bool:
        message = Mail(
            from_email=self.sender_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        try:
            response = self.client.send(message)
            return response.status_code in [200, 202]
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
