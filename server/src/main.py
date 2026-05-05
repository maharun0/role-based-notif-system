import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.router import router as api_router
from src.api.v1.websocket import router as ws_router
from src.logger_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Application starting up")
    yield
    logger.info("Application shutting down")


app = FastAPI(title="Role-Based Notification System", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(ws_router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
