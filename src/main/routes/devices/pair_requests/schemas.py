from typing import Union, List

from pydantic import field_validator, field_serializer

from src.core.db import BaseSchema
from enum import Enum

from src.core.utils.types import JsonDict
from src.main.components.devices.models.device_pair_request import DevicePairRequest


class PairRequestRespondAction(Enum):
    ACCEPT = "accept"
    REJECT = "reject"


class PairRequestRespondPayload(BaseSchema):
    action: PairRequestRespondAction
    request_uuid: str

    # noinspection PyNestedDecorators
    @field_validator('action', mode="before")
    @classmethod
    def set_token_type(cls, value: Union[str, PairRequestRespondAction]) -> PairRequestRespondAction:
        return PairRequestRespondAction(value) if isinstance(value, str) else value


class PairRequestsResponsePayload(BaseSchema):
    class Config:
        arbitrary_types_allowed = True

    pair_requests: List[DevicePairRequest]

    @field_serializer("pair_requests")
    def pair_requests_serializer(self, requests: List[DevicePairRequest]) -> List[JsonDict]:
        return [request.serialize() for request in requests]
