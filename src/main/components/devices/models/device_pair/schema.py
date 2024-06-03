from datetime import datetime

from pydantic import field_validator

from src.core.db import BaseSchema
from src.main.components.auth.models.user import UserInternal


class DevicePair(BaseSchema):
    id: int
    user: UserInternal
    device: UserInternal
    created_at: datetime

    # noinspection PyNestedDecorators
    @field_validator('user')
    @classmethod
    def validate_user(cls, user: UserInternal) -> UserInternal:
        if user.is_device:
            raise ValueError(f"Only user (user with is_device=False) can be used for `user` field in {cls.__name__}")
        return user

    # noinspection PyNestedDecorators
    @field_validator('device')
    @classmethod
    def validate_device(cls, user: UserInternal) -> UserInternal:
        if not user.is_device:
            raise ValueError(f"Only device (user with is_device=True) can be used for `device` field in {cls.__name__}")
        return user
