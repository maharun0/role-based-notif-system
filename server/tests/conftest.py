from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.core.constants import RoleName
from src.db.base import Base
from src.db.models import Role, User
from src.db.session import get_session
from src.main import app


@pytest_asyncio.fixture
async def engine():
    _engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield _engine
    await _engine.dispose()


@pytest_asyncio.fixture
async def seeded_client(engine) -> AsyncGenerator[tuple[AsyncClient, dict], None]:
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        roles: dict[str, Role] = {}
        for name in RoleName:
            r = Role(name=name)
            session.add(r)
            roles[name] = r
        await session.flush()

        user_defs = [
            ("Alice Admin", "alice@example.com", RoleName.ADMIN),
            ("Bob Manager", "bob@example.com", RoleName.MANAGER),
            ("Carol Editor", "carol@example.com", RoleName.EDITOR),
            ("Dave Viewer", "dave@example.com", RoleName.VIEWER),
            ("Eve Support", "eve@example.com", RoleName.SUPPORT),
            ("Frank Manager", "frank@example.com", RoleName.MANAGER),
        ]
        users: list[User] = []
        for uname, email, role_name in user_defs:
            u = User(name=uname, email=email, role_id=roles[role_name].id)
            session.add(u)
            users.append(u)
        await session.commit()
        for u in users:
            await session.refresh(u)

    seed = {
        "alice": users[0],
        "bob": users[1],
        "carol": users[2],
        "dave": users[3],
        "eve": users[4],
        "frank": users[5],
    }

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac, seed

    app.dependency_overrides.clear()
