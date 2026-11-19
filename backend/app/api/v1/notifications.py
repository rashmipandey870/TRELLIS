"""TRELLIS In-App Notifications API Router."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_uow
from app.models.notifications import Notification
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", summary="Get notifications for authenticated user")
def list_user_notifications(
    limit: int = 20,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[dict[str, Any]]:
    notifs = (
        db.execute(
            select(Notification)
            .where(Notification.recipient_id == user.id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        .scalars()
        .all()
    )
    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.notification_type,
            "link": n.link,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat(),
        }
        for n in notifs
    ]


@router.post("/{notification_id}/read", summary="Mark single notification as read")
def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    _uow: Any = Depends(get_uow),
) -> dict[str, str]:
    notif = db.get(Notification, notification_id)
    if not notif or notif.recipient_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found.")

    notif.is_read = True
    db.commit()
    return {"message": "Notification marked as read."}


@router.post("/mark-all-read", summary="Mark all notifications as read")
def mark_all_read(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    _uow: Any = Depends(get_uow),
) -> dict[str, str]:
    db.execute(
        update(Notification)
        .where(Notification.recipient_id == user.id)
        .values(is_read=True)
    )
    db.commit()
    return {"message": "All notifications marked as read."}
