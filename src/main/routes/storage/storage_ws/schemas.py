from enum import Enum
from typing import Optional, Union

from pydantic import field_validator

from src.core.db import BaseSchema
from src.core.utils.types import JsonDict


class StorageRequestType(Enum):
    ENQUEUE_REQUEST = 1
    ENQUEUE_RESPONSE = 2


class StorageRequest(BaseSchema):
    request_type: StorageRequestType
    message_id: str
    target_user_id: int
    data: JsonDict

    # noinspection PyNestedDecorators
    @field_validator('request_type', mode="before")
    @classmethod
    def set_message_type(cls, value: Union[int, StorageRequestType]) -> StorageRequestType:
        return StorageRequestType(value) if isinstance(value, int) else value
