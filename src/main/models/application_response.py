from typing import Optional, TypeVar, Generic

from pydantic import field_serializer

from src.core.db import BaseSchema
from src.core.utils.types import JsonDict

_contentT = TypeVar("_contentT")


class ApplicationResponsePayload(BaseSchema, Generic[_contentT]):
    ok: bool = True
    application_status_code: int
    message: str
    data: Optional[_contentT] = None

    # noinspection PyNestedDecorators
    @field_serializer('data')
    @classmethod
    def serialize_data(cls, value: Optional[_contentT]) -> Optional[JsonDict]:
        if value is None:
            return None

        return value.model_dump() if isinstance(value, BaseSchema) else value
