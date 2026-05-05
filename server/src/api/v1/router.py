from fastapi import APIRouter

from src.api.v1 import notifications, roles, users

router = APIRouter(prefix="/api/v1")
router.include_router(users.router)
router.include_router(notifications.router)
router.include_router(roles.router)
