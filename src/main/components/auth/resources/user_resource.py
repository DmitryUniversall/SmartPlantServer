import hashlib
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.components.auth.models.user import UserModel
from src.main.db import AsyncDatabaseManagerST
from src.main.resources import BaseResource, BaseResourceSTMeta

_db_manager: AsyncDatabaseManagerST = AsyncDatabaseManagerST()


class UserResourceST(BaseResource[UserModel], metaclass=BaseResourceSTMeta):
    __model_cls__ = UserModel

    def hash_password(self, password: str, encoding: str = "utf-8") -> str:
        return hashlib.sha256(password.encode(encoding=encoding)).hexdigest()

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

    async def create_user(self, username: str, password: str, **fields) -> UserModel:
        user = UserModel(
            username=username,  # type: ignore
            password=self.hash_password(password),  # type: ignore
            **fields  # type: ignore
        )

        await self.save(user)
        return user

    async def get_by_username(self, username: str, **fields) -> UserModel:
        if (user := await self._get_by_username(username, **fields)) is not None:
            return user
        raise UserModel.DoesNotExist("User not found")
