import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.api.deps import DBSession
from src.core.constants import RoleName
from src.db.models import Notification, NotificationRecipient, User
from src.schemas.notification import (
    MarkReadRequest,
    NotificationCreate,
    NotificationOut,
    NotificationRecipientOut,
    UnreadCountOut,
)
from src.services.notification_service import create_notification

logger = logging.getLogger(__name__)
router = APIRouter(tags=["notifications"])


@router.get("/users/{user_id}/notifications/unread-count", response_model=UnreadCountOut)
async def unread_count(user_id: int, db: DBSession) -> dict:
    result = await db.execute(
        select(func.count()).where(
            NotificationRecipient.user_id == user_id,
            NotificationRecipient.is_read == False,  # noqa: E712
        )
    )
    return {"unread_count": result.scalar_one()}


@router.get("/users/{user_id}/notifications", response_model=list[NotificationRecipientOut])
async def list_notifications(
    user_id: int,
    db: DBSession,
    is_read: bool | None = None,
    search: str | None = None,
) -> list[NotificationRecipient]:
    stmt = (
        select(NotificationRecipient)
        .where(NotificationRecipient.user_id == user_id)
        .options(selectinload(NotificationRecipient.notification))
        .order_by(NotificationRecipient.delivered_at.desc())
    )
    if is_read is not None:
        stmt = stmt.where(NotificationRecipient.is_read == is_read)
    if search:
        matched_ids = (
            select(Notification.id)
            .where(
                Notification.title.ilike(f"%{search}%")
                | Notification.message.ilike(f"%{search}%")
            )
            .scalar_subquery()
        )
        stmt = stmt.where(NotificationRecipient.notification_id.in_(matched_ids))
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("/notifications", response_model=NotificationOut, status_code=201)
async def create(payload: NotificationCreate, db: DBSession) -> Notification:
    result = await db.execute(
        select(User).where(User.id == payload.created_by).options(selectinload(User.role))
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role.name != RoleName.ADMIN:
        raise HTTPException(status_code=403, detail="Only Admin users can create notifications")
    return await create_notification(db, payload)


@router.patch("/notifications/{notification_id}/read", response_model=NotificationRecipientOut)
async def mark_read(
    notification_id: int,
    body: MarkReadRequest,
    db: DBSession,
) -> NotificationRecipient:
    result = await db.execute(
        select(NotificationRecipient)
        .where(
            NotificationRecipient.notification_id == notification_id,
            NotificationRecipient.user_id == body.user_id,
        )
        .options(selectinload(NotificationRecipient.notification))
    )
    recipient = result.scalar_one_or_none()
    if recipient is None:
        raise HTTPException(status_code=404, detail="Notification not found for this user")

    recipient.is_read = body.is_read
    recipient.read_at = datetime.now(timezone.utc) if body.is_read else None
    await db.commit()
    await db.refresh(recipient)
    return recipient
