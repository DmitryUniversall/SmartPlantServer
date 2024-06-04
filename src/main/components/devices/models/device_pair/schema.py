from datetime import datetime
from typing import Union

from pydantic import field_validator

from src.core.db import BaseSchema
from src.main.components.auth.models.user import UserInternal, UserModel


class DevicePair(BaseSchema):
    id: int
    user: UserInternal
    device: UserInternal
    created_at: datetime

    # noinspection PyNestedDecorators
    @field_validator('user', mode="before")
    @classmethod
    def validate_user(cls, user: Union[UserModel, UserInternal]) -> UserInternal:
        user_internal = user.to_schema(UserInternal) if isinstance(user, UserModel) else user
        if user_internal.is_device:
            raise ValueError(f"Only user (user with is_device=False) can be used for `user` field in {cls.__name__}")
        return user_internal

    # noinspection PyNestedDecorators
    @field_validator('device', mode="before")
    @classmethod
    def validate_device(cls, user: Union[UserModel, UserInternal]) -> UserInternal:
        user_internal = user.to_schema(UserInternal) if isinstance(user, UserModel) else user
        if not user_internal.is_device:
            raise ValueError(f"Only device (user with is_device=True) can be used for `device` field in {cls.__name__}")
        return user_internal
