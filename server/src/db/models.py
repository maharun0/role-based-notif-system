from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="role")
    notification_roles: Mapped[list["NotificationRole"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    role: Mapped["Role"] = relationship(back_populates="users")
    notifications_created: Mapped[list["Notification"]] = relationship(back_populates="creator")
    recipients: Mapped[list["NotificationRecipient"]] = relationship(back_populates="user")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    audience_type: Mapped[str] = mapped_column(String(20), nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    creator: Mapped["User"] = relationship(back_populates="notifications_created")
    notification_roles: Mapped[list["NotificationRole"]] = relationship(
        back_populates="notification", cascade="all, delete-orphan"
    )
    recipients: Mapped[list["NotificationRecipient"]] = relationship(
        back_populates="notification", cascade="all, delete-orphan"
    )


class NotificationRole(Base):
    __tablename__ = "notification_roles"
    __table_args__ = (UniqueConstraint("notification_id", "role_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    notification_id: Mapped[int] = mapped_column(ForeignKey("notifications.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

    notification: Mapped["Notification"] = relationship(back_populates="notification_roles")
    role: Mapped["Role"] = relationship(back_populates="notification_roles")


class NotificationRecipient(Base):
    __tablename__ = "notification_recipients"
    __table_args__ = (
        UniqueConstraint("notification_id", "user_id"),
        Index("ix_notification_recipients_user_is_read", "user_id", "is_read"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    notification_id: Mapped[int] = mapped_column(ForeignKey("notifications.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    notification: Mapped["Notification"] = relationship(back_populates="recipients")
    user: Mapped["User"] = relationship(back_populates="recipients")
