import logging

from fastapi import APIRouter
from sqlalchemy import select

from src.api.deps import DBSession
from src.db.models import Role
from src.schemas.role import RoleOut

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleOut])
async def list_roles(db: DBSession) -> list[Role]:
    result = await db.execute(select(Role))
    return list(result.scalars().all())
