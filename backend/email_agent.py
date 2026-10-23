import os
import json

from dotenv import load_dotenv
from openai import AzureOpenAI

from database import find_contacts
from email_service import send_email

load_dotenv()


def get_ai_client():
    api_key = os.getenv("LLM_API_KEY")
    endpoint = os.getenv("LLM_ENDPOINT", "").strip()
    api_version = os.getenv("LLM_API_VERSION")

    if not api_key or not endpoint or not api_version:
        raise RuntimeError(
            "Check LLM_API_KEY, LLM_ENDPOINT, and LLM_API_VERSION in .env"
        )

    return AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint.rstrip("/"),
        api_version=api_version,
    )


def process_prompt(prompt: str) -> dict:
    client = get_ai_client()
    deployment = os.getenv("LLM_MODEL")

    if not deployment:
        raise RuntimeError("LLM_MODEL is missing in .env")

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": """
You are an AI email assistant.

Return only a valid JSON object with these fields:
- action: "send_email" or "none"
- recipient_name: contact name, or null
- subject: email subject, or null
- body: email body, or null

Only use action "send_email" when the user explicitly asks to send
an email. Do not invent email addresses. If the recipient is unclear,
use action "none". Create a professional subject and body.
""",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Azure OpenAI returned an empty response.")

    result = json.loads(content)

    if result.get("action") != "send_email":
        return {
            "success": True,
            "message": "Prompt processed. No email was sent.",
            "details": result,
        }

    recipient_name = result.get("recipient_name")
    subject = result.get("subject")
    body = result.get("body")

    if not recipient_name or not subject or not body:
        return {
            "success": False,
            "message": "Missing recipient, subject, or email body.",
        }

    contacts = find_contacts(recipient_name)

    if not contacts:
        return {
            "success": False,
            "message": f"No saved contact found for {recipient_name}.",
        }

    contact = contacts[0]

    # Support either dictionary rows or SQLite Row objects.
    recipient_email = contact["email"]

    # FIX: Pass positional arguments matching send_email(recipient, subject, body).
    email_result = send_email(recipient_email, subject, body)

    return {
        "success": True,
        "message": f"Email sent successfully to {recipient_name}.",
        "recipient": recipient_email,
        "subject": subject,
        "body": body,
        "email_result": email_result,
    }
