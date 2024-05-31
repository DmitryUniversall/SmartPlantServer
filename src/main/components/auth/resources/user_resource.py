import hashlib
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils.singleton import SingletonMeta
from src.main.components.auth.models.user import UserModel
from src.main.db import AsyncDatabaseManagerST

_db_manager: AsyncDatabaseManagerST = AsyncDatabaseManagerST()


class UserResourceST(metaclass=SingletonMeta):
    def hash_password(self, password: str, encoding: str = "utf-8") -> str:
        return hashlib.sha256(password.encode(encoding=encoding)).hexdigest()

    async def _fetch_user_by_id(self, session: AsyncSession, user_id: int) -> Optional[UserModel]:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        return result.scalar()

    async def _get_by_id(self, user_id: int) -> Optional[UserModel]:
        async with _db_manager.session() as session:
            return await self._fetch_user_by_id(session, user_id)

    async def _fetch_user_by_credentials(self, session: AsyncSession, username: str, **fields) -> Optional[UserModel]:
        query = select(UserModel).filter(
            UserModel.username == username,
            *(getattr(UserModel, name) == value for name, value in fields.items())
        )

        result = await session.execute(query)
        return result.scalar()

    async def _get_by_username(self, username: str, **fields) -> Optional[UserModel]:
        async with _db_manager.session() as session:
            return await self._fetch_user_by_credentials(session, username, **fields)

    async def _save_user(self, user: UserModel) -> None:
        async with _db_manager.session() as session:
            session.add(user)
            await session.commit()

    async def _delete_user(self, user: UserModel) -> None:
        async with _db_manager.session() as session:
            await session.delete(user)
            await session.commit()

    async def create_user(self, username: str, password: str, **fields) -> UserModel:
        user = UserModel(
            username=username,  # type: ignore
            password=self.hash_password(password),  # type: ignore
            **fields  # type: ignore
        )

        await self._save_user(user)
        return user

    async def get_by_id(self, user_id: int) -> UserModel:
        if (user := await self._get_by_id(user_id)) is not None:
            return user
        raise UserModel.DoesNotExist("User not found")

    async def get_by_username(self, username: str, **fields) -> UserModel:
        if (user := await self._get_by_username(username, **fields)) is not None:
            return user
        raise UserModel.DoesNotExist("User not found")

    async def update_user(self, user: UserModel, **fields) -> UserModel:
        for key, value in fields.items():
            setattr(user, key, value)

        await self._save_user(user)
        return user

    async def delete_user(self, user: UserModel) -> None:
        await self._delete_user(user)
