from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Type, Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import BaseModel
from src.main.db import AsyncDatabaseManagerST

_modelT = TypeVar("_modelT", bound=BaseModel)
_db_manager = AsyncDatabaseManagerST()


class BaseResource(ABC, Generic[_modelT]):  # TODO: Add validators and methods-events (like on_create and etc.)
    @property
    @abstractmethod
    def __model_cls__(self) -> Type[_modelT]:
        ...

    async def _fetch_by_id(self, session: AsyncSession, object_id: int) -> Optional[_modelT]:
        stmt = select(self.__model_cls__).filter(self.__model_cls__.id == object_id)
        result = await session.execute(stmt)
        return result.scalar()

    async def _delete_by_id(self, session: AsyncSession, object_id: int) -> None:
        stmt = delete(self.__model_cls__).where(self.__model_cls__.id == object_id)
        await session.execute(stmt)
        await session.commit()

    async def _update_by_id(self, session: AsyncSession, object_id: int, **fields) -> _modelT:
        result = await session.execute(
            update(self.__model_cls__)
            .where(self.__model_cls__.id == object_id)
            .values(**fields)
            .returning(self.__model_cls__)
        )

        if (updated := result.scalar_one_or_none()) is None:
            raise self.__model_cls__.DoesNotExist(f"Not found {self.__model_cls__.__name__} with id={object_id}")

        return updated

    async def save(self, model_obj: _modelT) -> None:
        async with _db_manager.session() as session:
            session.add(model_obj)
            await session.commit()

    async def get_by_id(self, object_id: int) -> _modelT:
        async with _db_manager.session() as session:
            if (obj := await self._fetch_by_id(session, object_id)) is not None:
                return obj
            raise self.__model_cls__.DoesNotExist(f"Not found {self.__model_cls__.__name__} with id={object_id}")

    async def delete(self, model_obj: _modelT) -> None:
        async with _db_manager.session() as session:
            await session.delete(model_obj)
            await session.commit()

    async def delete_by_id(self, object_id: int) -> None:
        async with _db_manager.session() as session:
            await self._delete_by_id(session, object_id)

    async def update(self, model_obj: _modelT, **fields) -> _modelT:
        for key, value in fields.items():
            setattr(model_obj, key, value)

        await self.save(model_obj)
        return model_obj

    async def update_by_id(self, object_id: int, **fields) -> None:
        async with _db_manager.session() as session:
            await self._update_by_id(session, object_id, **fields)
