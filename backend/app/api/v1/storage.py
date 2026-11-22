"""Storage download and token verification router for TRELLIS (WS3 / Phase B)."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.services.storage_service import storage_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/storage", tags=["Storage & Downloads"])


@router.get("/download/{token_or_name}", summary="Download authenticated or signed file")
def download_file(token_or_name: str) -> FileResponse:
    """Download stored file by resolving either signed token or direct stored name."""
    if ":" in token_or_name:
        is_valid, stored_name = storage_service.verify_signed_token(token_or_name)
        if not is_valid or not stored_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Download authorization token is invalid or has expired.",
            )
    else:
        stored_name = token_or_name

    file_path = storage_service.get_file_path(stored_name)
    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested file not found in storage.",
        )

    # Infer original human-readable filename
    display_name = stored_name.split("_", 1)[-1] if "_" in stored_name else stored_name
    return FileResponse(
        path=str(file_path),
        filename=display_name,
        media_type="application/octet-stream",
    )
