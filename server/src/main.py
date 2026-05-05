import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.logger_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Application starting up")
    yield
    logger.info("Application shutting down")


app = FastAPI(title="Role-Based Notification System", lifespan=lifespan)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "message": "Hello from the notification server!"}
