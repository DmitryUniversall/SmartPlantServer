from typing import List

from src.core.db import BaseSchema
from src.main.components.auth.models.user import UserPublic


class DevicesResponsePayload(BaseSchema):
    devices: List[UserPublic]
