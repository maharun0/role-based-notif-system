from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator

from src.core.constants import AudienceType


class NotificationCreate(BaseModel):
    title: str
    message: str
    audience_type: AudienceType
    role_ids: list[int] = []
    created_by: int

    @model_validator(mode="after")
    def validate_role_ids(self) -> "NotificationCreate":
        if self.audience_type == AudienceType.BY_ROLE and not self.role_ids:
            raise ValueError("role_ids required when audience_type is BY_ROLE")
        return self


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    message: str
    audience_type: str
    created_by: int
    created_at: datetime


class NotificationRecipientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    notification_id: int
    user_id: int
    is_read: bool
    read_at: datetime | None
    delivered_at: datetime
    notification: NotificationOut


class MarkReadRequest(BaseModel):
    user_id: int
    is_read: bool


class UnreadCountOut(BaseModel):
    unread_count: int
