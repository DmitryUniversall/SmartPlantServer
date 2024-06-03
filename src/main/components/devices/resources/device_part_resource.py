from http import HTTPStatus
from typing import Optional, List

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.components.auth.models.user import UserInternal, UserModel
from src.main.components.devices.exceptions.generics import (
    InvalidUserDeviceHTTPException,
    DeviceAlreadyHasOwnerHTTPException
)
from src.main.components.devices.models.device_pair import DevicePairModel
from src.main.db import AsyncDatabaseManagerST
from src.main.resources import BaseResource, BaseResourceSTMeta

_db_manager = AsyncDatabaseManagerST()


# TODO: override update methods for safety
class DevicePairResourceST(BaseResource[DevicePairModel], metaclass=BaseResourceSTMeta):
    __model_cls__ = DevicePairModel

    async def _fetch_by_id(self, session: AsyncSession, pair_id: int) -> Optional[DevicePairModel]:
        # .options(joinedload(DevicePairModel.user), joinedload(DevicePairModel.device_user))
        query = select(DevicePairModel).filter(DevicePairModel.id == pair_id)
        result = await session.execute(query)
        return result.scalar()

    async def _fetch_device_owner(self, session: AsyncSession, device_id: int) -> Optional[UserModel]:
        subquery = select(DevicePairModel.user_id).where(DevicePairModel.device_id == device_id).scalar_subquery()
        stmt = select(UserModel).where(UserModel.id == subquery)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def _fetch_user_devices(self, session: AsyncSession, user_id: int) -> List[UserModel]:
        subquery = select(DevicePairModel.device_id).where(DevicePairModel.user_id == user_id).subquery()
        # FIXME: Argument 1 to "in_" of "SQLCoreOperations" has incompatible type "Subquery"; expected "Iterable[Any] | BindParameter[Any] | InElementRole"
        stmt = select(UserModel).where(UserModel.id.in_(subquery))  # type: ignore
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def _delete_pair_by_device_id(self, session: AsyncSession, device_id: int) -> None:
        stmt = delete(DevicePairModel).where(DevicePairModel.device_id == device_id)
        await session.execute(stmt)
        await session.commit()

    async def get_user_devices(self, user_id: int) -> List[UserModel]:
        async with _db_manager.session() as session:
            return await self._fetch_user_devices(session, user_id)

    async def get_owner(self, device_id: int) -> Optional[UserModel]:
        async with _db_manager.session() as session:
            return await self._fetch_device_owner(session, device_id)

    async def create_device_pair(self, user: UserInternal, device: UserInternal) -> DevicePairModel:
        if user.is_device or not device.is_device:
            raise InvalidUserDeviceHTTPException(status_code=HTTPStatus.BAD_REQUEST, message="Unable to pair devices: Invalid user or device specified")

        if await self.get_owner(device_id=device.id):
            raise DeviceAlreadyHasOwnerHTTPException(status_code=HTTPStatus.BAD_REQUEST, message="This device already has owner, so is cannot be paired with any other user")

        device_pair = DevicePairModel(user_id=user.id, device_id=device.id)  # type: ignore
        await self.save(device_pair)
        return device_pair

    async def unpair_device(self, device_id: int) -> None:
        async with _db_manager.session() as session:
            await self._delete_pair_by_device_id(session, device_id)

    async def is_same_network(self, user_id_1: int, user_id_2: int) -> bool:
        """
        Check if the two user IDs (can be user and device) are in the same network.

        They are in the same network if:
        1) One of them is a user that has DevicePair with the second.
        2) Both belong to the same user.

        :param user_id_1: `int`
            The ID of the first user or device.

        :param user_id_2: `int`
            The ID of the second user or device.

        :return: `bool`
            Returns `True` if the two IDs are in the same network, otherwise `False`.
        """

        async with _db_manager.session() as session:
            stmt_1 = select(DevicePairModel).where(
                (DevicePairModel.user_id == user_id_1) & (DevicePairModel.device_id == user_id_2)
            )
            stmt_2 = select(DevicePairModel).where(
                (DevicePairModel.user_id == user_id_2) & (DevicePairModel.device_id == user_id_1)
            )

            result_1 = await session.execute(stmt_1)
            result_2 = await session.execute(stmt_2)

            if result_1.scalars().first() or result_2.scalars().first():
                return True

            # Check if both user_id_1 and user_id_2 are associated with the same user via DevicePair
            stmt_3 = select(DevicePairModel.user_id).where(
                (DevicePairModel.device_id == user_id_1) | (DevicePairModel.device_id == user_id_2)
            ).group_by(DevicePairModel.user_id).having(func.count(DevicePairModel.user_id) == 2)

            result_3 = await session.execute(stmt_3)
            if result_3.scalars().first():
                return True

            return False
