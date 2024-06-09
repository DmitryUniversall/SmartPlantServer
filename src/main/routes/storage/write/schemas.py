from src.core.db import BaseSchema
from src.core.utils.types import JsonDict


class StorageWriteRequestPayload(BaseSchema):
    target_user_id: int
    data: JsonDict


class WriteRequestPayload(StorageWriteRequestPayload):
    pass


class WriteResponsePayload(StorageWriteRequestPayload):
    response_to_request_uuid: str


class StorageWriteResponsePayload(BaseSchema):
    request_uuid: str
