import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constants import AudienceType
from src.db.models import Notification, NotificationRecipient, NotificationRole, User
from src.schemas.notification import NotificationCreate
from src.services.connection_manager import manager

logger = logging.getLogger(__name__)


async def create_notification(db: AsyncSession, payload: NotificationCreate) -> Notification:
    # Persist the notification first so we can fan out stable foreign keys.
    notification = Notification(
        title=payload.title,
        message=payload.message,
        audience_type=payload.audience_type,
        created_by=payload.created_by,
    )
    db.add(notification)
    await db.flush()

    if payload.audience_type == AudienceType.BY_ROLE:
        # Keep the role targeting snapshot for auditing/debugging.
        for role_id in payload.role_ids:
            db.add(NotificationRole(notification_id=notification.id, role_id=role_id))

    # Audience expansion happens at send-time into explicit recipient rows.
    if payload.audience_type == AudienceType.ALL:
        result = await db.execute(select(User))
    else:
        result = await db.execute(select(User).where(User.role_id.in_(payload.role_ids)))
    users = result.scalars().all()

    for user in users:
        # Each user gets an independent read state.
        db.add(NotificationRecipient(notification_id=notification.id, user_id=user.id, is_read=False))

    # Collect IDs before commit (objects expire after commit)
    user_ids = [u.id for u in users]

    await db.commit()
    await db.refresh(notification)

    ws_payload = {
        "id": notification.id,
        "title": notification.title,
        "message": notification.message,
        "audience_type": notification.audience_type,
        "created_by": notification.created_by,
        "created_at": notification.created_at.isoformat(),
        "is_read": False,
    }
    for user_id in user_ids:
        # Best-effort realtime push; API remains the source of truth.
        await manager.send(user_id, ws_payload)

    logger.info("Notification created: id=%d, audience=%s, recipients=%d",
                notification.id, payload.audience_type, len(user_ids))
    return notification
