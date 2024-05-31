from enum import Enum
from typing import Optional, Union

from pydantic import field_validator

from src.core.db import BaseSchema
from src.core.utils.types import JsonDict


class StorageRequestMSGType(Enum):
    ENQUEUE_REQUEST = 1
    ENQUEUE_RESPONSE = 2


class StorageRequest(BaseSchema):
    request_type: StorageRequestMSGType
    message_id: str
    target_device_id: str
    data: Optional[JsonDict] = None

    # noinspection PyNestedDecorators
    @field_validator('msg_type', mode="before")
    @classmethod
    def set_message_type(cls, value: Union[int, StorageRequestMSGType]) -> StorageRequestMSGType:
        return StorageRequestMSGType(value) if isinstance(value, int) else value
