from datetime import datetime
from enum import Enum
from typing import Union

from pydantic import Field, field_validator

from src.core.db import BaseSchema
from src.core.utils.types import JsonDict


class DataMessageType(Enum):
    REQUEST = 1
    RESPONSE = 2


class StorageDataMessage(BaseSchema):
    data_type: DataMessageType
    request_uuid: str
    target_user_id: int
    sender_user_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    data: JsonDict

    # noinspection PyNestedDecorators
    @field_validator('data_type', mode="before")
    @classmethod
    def set_token_type(cls, value: Union[str, DataMessageType]) -> DataMessageType:
        return DataMessageType(value) if isinstance(value, str) else value
