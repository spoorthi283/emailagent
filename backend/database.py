
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(
    os.getenv("DATABASE_PATH", "emails.db")
)


def get_connection():
    connection = sqlite3.connect(
        DB_PATH,
        timeout=10
    )
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS email_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                status TEXT NOT NULL,
                error TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_contact(name: str, email: str):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO contacts (name, email)
            VALUES (?, ?)
            ON CONFLICT(email)
            DO UPDATE SET name = excluded.name
        """, (name.strip(), email.strip().lower()))


def find_contacts(name: str):
    with get_connection() as conn:
        return conn.execute("""
            SELECT name, email
            FROM contacts
            WHERE LOWER(name) = LOWER(?)
        """, (name.strip(),)).fetchall()


def log_email(
    recipient,
    subject,
    body,
    status,
    error=None
):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO email_logs
            (recipient, subject, body, status, error)
            VALUES (?, ?, ?, ?, ?)
        """, (recipient, subject, body, status, error))


def get_email_history(limit=50):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT *
            FROM email_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]
