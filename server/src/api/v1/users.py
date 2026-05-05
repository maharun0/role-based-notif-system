import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.api.deps import DBSession
from src.db.models import User
from src.schemas.user import UserOut

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
async def list_users(db: DBSession) -> list[User]:
    result = await db.execute(select(User).options(selectinload(User.role)))
    return list(result.scalars().all())


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: DBSession) -> User:
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.role))
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
