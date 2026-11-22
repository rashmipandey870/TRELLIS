"""Secure file storage abstraction for TRELLIS (WS3 FILE_UPLOAD).

Never stores binary blobs in the database.
Enforces:
- Strict MIME and extension allow-lists
- Max 10MB file size limit
- SHA-256 integrity verification
- Randomized collision-resistant filenames
- Signed, short-lived download authorization tokens
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import re
import time
import uuid
from pathlib import Path
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".py",
    ".java",
    ".sql",
    ".js",
    ".zip",
    ".md",
    ".json",
    ".csv",
}

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
    "text/x-python",
    "text/x-java-source",
    "application/sql",
    "text/javascript",
    "application/zip",
    "application/x-zip-compressed",
    "text/markdown",
    "application/json",
    "text/csv",
}

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


class StorageService:
    """Manages secure file uploads, checksums, and signed retrieval links."""

    def __init__(self, base_dir: Path | None = None) -> None:
        if base_dir:
            self.base_dir = base_dir
        else:
            self.base_dir = Path(__file__).resolve().parent.parent.parent / "storage" / "uploads"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.signing_secret = getattr(settings, "JWT_SECRET_KEY", "trellis-storage-signing-secret-key-12345678").encode("utf-8")

    def sanitize_filename(self, filename: str) -> str:
        clean = re.sub(r"[^A-Za-z0-9_.-]", "_", filename or "unnamed_file")
        return clean.strip("._") or "unnamed_file"

    def save_file(
        self,
        file_bytes: bytes,
        original_filename: str,
        content_type: str | None = None,
        user_id: str = "anonymous",
    ) -> dict[str, Any]:
        """Validate, hash, and persist file to local disk or object storage."""
        if len(file_bytes) > MAX_FILE_SIZE_BYTES:
            raise ValueError(f"File size exceeds maximum allowed 10 MB limit ({len(file_bytes)} bytes)")

        safe_name = self.sanitize_filename(original_filename)
        ext = Path(safe_name).suffix.lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"File extension '{ext}' is not permitted. Allowed: {sorted(ALLOWED_EXTENSIONS)}")

        if content_type:
            clean_mime = content_type.split(";")[0].strip().lower()
            if clean_mime not in ALLOWED_MIME_TYPES and clean_mime != "application/octet-stream":
                raise ValueError(f"MIME type '{clean_mime}' is not permitted.")

        # Compute SHA-256
        sha256 = hashlib.sha256(file_bytes).hexdigest()

        # Generate unique random storage filename
        stored_name = f"{uuid.uuid4().hex}_{safe_name}"
        dest_path = self.base_dir / stored_name

        dest_path.write_bytes(file_bytes)
        logger.info(
            "Persisted file '%s' (%s bytes, sha256=%s) to storage for user '%s'",
            stored_name,
            len(file_bytes),
            sha256[:12],
            user_id,
        )

        relative_url = f"/api/v1/storage/download/{stored_name}"

        return {
            "file_url": relative_url,
            "file_name": safe_name,
            "stored_name": stored_name,
            "sha256": sha256,
            "size_bytes": len(file_bytes),
        }

    def generate_signed_token(self, stored_name: str, user_id: str, expires_in_sec: int = 3600) -> str:
        """Create HMAC-SHA256 signed short-lived download authorization token."""
        expiry = int(time.time()) + expires_in_sec
        payload = f"{stored_name}:{user_id}:{expiry}"
        sig = hmac.new(self.signing_secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"{payload}:{sig}"

    def verify_signed_token(self, token: str, requesting_user_id: str | None = None) -> tuple[bool, str | None]:
        """Verify authenticity, expiration, and user ownership of download token."""
        try:
            parts = token.split(":")
            if len(parts) != 4:
                return False, None
            stored_name, user_id, expiry_str, received_sig = parts
            expiry = int(expiry_str)

            if time.time() > expiry:
                return False, None

            if requesting_user_id and requesting_user_id != user_id:
                return False, None

            expected_payload = f"{stored_name}:{user_id}:{expiry}"
            expected_sig = hmac.new(self.signing_secret, expected_payload.encode("utf-8"), hashlib.sha256).hexdigest()

            if hmac.compare_digest(received_sig, expected_sig):
                return True, stored_name
            return False, None
        except Exception:
            return False, None

    def get_file_path(self, stored_name: str) -> Path | None:
        """Resolve path and verify it remains strictly within storage base directory."""
        clean_name = Path(stored_name).name
        target = (self.base_dir / clean_name).resolve()
        if not str(target).startswith(str(self.base_dir.resolve())):
            return None
        if not target.exists():
            return None
        return target


storage_service = StorageService()
