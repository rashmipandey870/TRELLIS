"""TRELLIS Celery Application Configuration for asynchronous task execution."""

from __future__ import annotations

import os

from celery import Celery

from app.core.config import settings

redis_url = settings.REDIS_URL or os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")

celery_app = Celery(
    "trellis",
    broker=redis_url,
    backend=redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
)
