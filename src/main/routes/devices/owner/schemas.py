from typing import Optional

from src.core.db import BaseSchema
from src.main.components.auth.models.user import UserPublic


class OwnerResponsePayload(BaseSchema):
    owner: Optional[UserPublic] = None
