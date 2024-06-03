import asyncio
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from src.core.utils.types import JsonDict
from src.main.components.auth.models.user import UserInternal, UserPublic


class DevicePairReqeustState(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class DevicePairRequest:
    def __init__(self, user: UserInternal, device: UserInternal) -> None:
        self.uuid: str = uuid4().hex
        self.created_at: datetime = datetime.now()
        self.user = user
        self.device = device
        self._state = DevicePairReqeustState.PENDING
        self._state_changed_event: asyncio.Event = asyncio.Event()

    @property
    def state(self) -> DevicePairReqeustState:
        return self._state

    @state.setter
    def state(self, value: DevicePairReqeustState) -> None:
        self._state_changed_event.set()
        self._state_changed_event.clear()
        self._state = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value: UserInternal) -> None:
        if value.is_device:
            raise ValueError(f"Only user (user with is_device=False) can be used for `user` in DevicePairRequest")

        self._user = value

    @property
    def device(self) -> UserInternal:
        return self._device

    @device.setter
    def device(self, value: UserInternal) -> None:
        if not value.is_device:
            raise ValueError(f"Only device (user with is_device=True) can be used for `device` in DevicePairRequest")

        self._device = value

    async def wait_for_state_change(self, timeout: Optional[float]) -> None:
        await asyncio.wait_for(self._state_changed_event.wait(), timeout=timeout)

    def serialize(self) -> JsonDict:
        return {
            "uuid": self.uuid,
            "user": self.user.convert_to(UserPublic).to_json_dict(),
            "device": self.device.convert_to(UserPublic).to_json_dict(),
            "created_at": self.created_at.timestamp()
        }
