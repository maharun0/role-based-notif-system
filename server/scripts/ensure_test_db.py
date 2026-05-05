"""Ensure notifications_test exists (init scripts only run on first volume create)."""

import asyncio
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncpg

from src.logger_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

_TEST_DB = "notifications_test"


async def main() -> None:
    host = os.getenv("PGHOST", "localhost")
    port = int(os.getenv("PGPORT", "5432"))
    user = os.getenv("PGUSER", "postgres")
    password = os.getenv("PGPASSWORD", "postgres")

    conn = await asyncpg.connect(
        host=host, port=port, user=user, password=password, database="postgres"
    )
    try:
        exists = await conn.fetchval(
            "select 1 from pg_database where datname = $1", _TEST_DB
        )
        if not exists:
            await conn.execute("CREATE DATABASE notifications_test")
            logger.info("Created database: %s", _TEST_DB)
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
