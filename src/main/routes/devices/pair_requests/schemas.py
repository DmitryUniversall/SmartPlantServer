from enum import Enum
from typing import List

from pydantic import field_serializer

from src.core.db import BaseSchema
from src.core.utils.types import JsonDict
from src.main.components.devices.models.device_pair_request import DevicePairRequest


class PairRequestRespondAction(Enum):
    ACCEPT = "accept"
    REJECT = "reject"


class PairRequestsResponsePayload(BaseSchema):
    class Config:
        arbitrary_types_allowed = True

    pair_requests: List[DevicePairRequest]

    @field_serializer("pair_requests")
    def pair_requests_serializer(self, requests: List[DevicePairRequest]) -> List[JsonDict]:
        return [request.serialize() for request in requests]
