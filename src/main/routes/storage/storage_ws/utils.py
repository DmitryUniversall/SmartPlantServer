from enum import Enum
from typing import Any, Dict

from fastapi.websockets import WebSocket


class StorageMessageType(Enum):
    RESPONSE = 1
    DATA = 2


async def send_storage_data_message_ws(websocket: WebSocket, data: Dict[str, Any]) -> None:
    await websocket.send_json({
        "msg_type": StorageMessageType.DATA.value,
        "data": data
    })
