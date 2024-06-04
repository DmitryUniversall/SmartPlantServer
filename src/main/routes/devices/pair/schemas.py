from src.core.db import BaseSchema
from src.main.components.auth.models.user import UserPublic


class PairDeviceResponsePayload(BaseSchema):
    device_user: UserPublic
