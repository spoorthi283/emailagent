
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import (
    init_db,
    add_contact,
    get_email_history,
    log_email,
)
from email_agent import process_prompt
from models import PromptRequest, ContactRequest

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Email Automation Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {"message": "AI Email Automation Agent is running"}


@app.post("/api/agent")
def run_agent(request: PromptRequest):
    try:
        result = process_prompt(request.prompt)

        # Record successful email activity when supported by database.py.
        if result.get("success") and result.get("recipient"):
            log_email(
                result["recipient"],
                result.get("subject", ""),
                result.get("body", ""),
                "sent",
            )

        return result

    except Exception:
        logger.exception("Agent request failed")
        raise HTTPException(
            status_code=500,
            detail="Could not process the request. Check backend logs.",
        )


@app.post("/api/contacts")
def create_contact(request: ContactRequest):
    try:
        result = add_contact(request.name, request.email)
        return {
            "success": True,
            "message": "Contact saved successfully.",
            "result": result,
        }
    except Exception:
        logger.exception("Contact creation failed")
        raise HTTPException(
            status_code=500,
            detail="Could not save contact. Check backend logs.",
        )


@app.get("/api/history")
def email_history():
    try:
        return get_email_history()
    except Exception:
        logger.exception("Could not retrieve email history")
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve email history.",
        )
