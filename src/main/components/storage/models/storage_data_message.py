from datetime import datetime
from enum import Enum

from pydantic import Field

from src.core.db import BaseSchema
from src.core.utils.types import JsonDict


class DataMessageType(Enum):
    REQUEST = 1
    RESPONSE = 2


class StorageDataMessage(BaseSchema):
    created_at: datetime = Field(default_factory=datetime.now)
    data_type: DataMessageType
    message_id: str
    target_user_id: int
    sender_user_id: int
    data: JsonDict
