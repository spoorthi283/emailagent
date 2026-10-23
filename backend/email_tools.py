
from email_service import send_email


def send_email_tool(
    recipient: str,
    subject: str,
    body: str
) -> dict:
    """Send an email using the configured SMTP account."""

    send_email(
        recipient=recipient,
        subject=subject,
        body=body
    )

    return {
        "success": True,
        "message": f"Email accepted for sending to {recipient}"
    }
