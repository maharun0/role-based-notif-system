import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from src.core.constants import RoleName
from src.db.models import Role, User
from src.db.session import AsyncSessionLocal
from src.logger_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

_ROLES = [
    RoleName.ADMIN,
    RoleName.MANAGER,
    RoleName.EDITOR,
    RoleName.VIEWER,
    RoleName.SUPPORT,
]

_USERS = [
    {"name": "Alice Admin", "email": "alice@example.com", "role": RoleName.ADMIN},
    {"name": "Bob Manager", "email": "bob@example.com", "role": RoleName.MANAGER},
    {"name": "Carol Editor", "email": "carol@example.com", "role": RoleName.EDITOR},
    {"name": "Dave Viewer", "email": "dave@example.com", "role": RoleName.VIEWER},
    {"name": "Eve Support", "email": "eve@example.com", "role": RoleName.SUPPORT},
    {"name": "Frank Manager", "email": "frank@example.com", "role": RoleName.MANAGER},
]


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        role_map: dict[str, Role] = {}
        for role_name in _ROLES:
            result = await session.execute(select(Role).where(Role.name == role_name))
            role = result.scalar_one_or_none()
            if role is None:
                role = Role(name=role_name)
                session.add(role)
                logger.info("Created role: %s", role_name)
            else:
                logger.info("Role already exists: %s", role_name)
            role_map[role_name] = role

        await session.flush()

        for user_data in _USERS:
            result = await session.execute(select(User).where(User.email == user_data["email"]))
            if result.scalar_one_or_none() is None:
                role = role_map[user_data["role"]]
                session.add(User(name=user_data["name"], email=user_data["email"], role_id=role.id))
                logger.info("Created user: %s (%s)", user_data["name"], user_data["email"])
            else:
                logger.info("User already exists: %s", user_data["email"])

        await session.commit()
        logger.info("Seeding complete")


if __name__ == "__main__":
    asyncio.run(seed())
