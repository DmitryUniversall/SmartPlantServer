from src.core.db import BaseSchema
from src.main.components.auth.models.user import UserPrivate


class GetMeResponsePayload(BaseSchema):
    user: UserPrivate
