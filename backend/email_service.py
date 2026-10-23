import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

def send_email(recipient, subject, body):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SMTP_FROM") or smtp_user

    if not smtp_user or not smtp_password or not sender_email:
        raise RuntimeError(
            "SMTP_USER, SMTP_PASSWORD, and SMTP_FROM must be configured in .env"
        )

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_password)
        server.send_message(message)

    return {
        "success": True,
        "recipient": recipient,
        "subject": subject,
    }