"""TRELLIS Email & Calendar Notification Service (Phase 3.1).

Supports:
- SMTP with STARTTLS or local MailHog (port 1025)
- MIME multipart messages with HTML + plain text fallback
- RFC 5545 iCalendar (.ics) attachments for meeting invites
- Asynchronous dispatch via Celery tasks with exponential backoff retries
"""

from __future__ import annotations

import email.message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from app.core.celery_app import celery_app
from app.core.config import settings


def send_smtp_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str = "",
    ics_data: str | None = None,
) -> bool:
    """Send an email synchronously via configured SMTP server."""
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    msg["To"] = to_email

    alt_part = MIMEMultipart("alternative")
    if text_content:
        alt_part.attach(MIMEText(text_content, "plain", "utf-8"))
    alt_part.attach(MIMEText(html_content, "html", "utf-8"))
    msg.attach(alt_part)

    if ics_data:
        ics_part = MIMEText(ics_data, "calendar", "utf-8")
        ics_part.add_header("Content-Disposition", "attachment", filename="invite.ics")
        ics_part.add_header("method", "REQUEST")
        msg.attach(ics_part)

    try:
        if settings.SMTP_TLS:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                server.starttls()
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        else:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        return True
    except Exception as e:
        # In test or dev without live SMTP, gracefully return False
        return False


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_async_task(
    self: Any,
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str = "",
    ics_data: str | None = None,
) -> bool:
    """Celery background task for asynchronous email delivery with retries."""
    success = send_smtp_email(to_email, subject, html_content, text_content, ics_data)
    if not success and settings.TRELLIS_ENV not in ("dev", "test"):
        try:
            self.retry(countdown=60 * (2 ** self.request.retries))
        except Exception:
            return False
    return success


def dispatch_email_notification(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str = "",
    ics_data: str | None = None,
) -> None:
    """Dispatch email via Celery async queue if available, otherwise synchronous."""
    if settings.TRELLIS_ENV in ("test", "dev"):
        # Synchronous in testing / dev
        send_smtp_email(to_email, subject, html_content, text_content, ics_data)
    else:
        try:
            send_email_async_task.delay(to_email, subject, html_content, text_content, ics_data)
        except Exception:
            send_smtp_email(to_email, subject, html_content, text_content, ics_data)
