import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[user_id] = websocket
        logger.info("WebSocket connected: user_id=%d", user_id)

    def disconnect(self, user_id: int) -> None:
        self._connections.pop(user_id, None)
        logger.info("WebSocket disconnected: user_id=%d", user_id)

    async def send(self, user_id: int, data: dict) -> None:
        ws = self._connections.get(user_id)
        if ws is None:
            return
        try:
            await ws.send_json(data)
        except Exception:
            self.disconnect(user_id)


manager = ConnectionManager()
