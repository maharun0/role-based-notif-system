import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.services.connection_manager import manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket) -> None:
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as exc:
        logger.warning("WebSocket error for user_id=%d: %s", user_id, exc)
        manager.disconnect(user_id)
