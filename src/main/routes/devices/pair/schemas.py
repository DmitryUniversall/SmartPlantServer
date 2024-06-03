from typing import Optional

from src.core.db import BaseSchema


class PairDeviceRequestPayload(BaseSchema):
    device_id: Optional[int] = None
    device_username: Optional[str] = None
