from typing import TypeVar, Optional, Type, Tuple, Dict, Any, ClassVar, Generic

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from src.core.db.base.schema import BaseSchema
from src.core.db.exceptions import DoesNotExistError
from src.core.db.sqlalchemy_to_pydantic import sqlalchemy_to_pydantic

Base = declarative_base()
_schemaBaseT = TypeVar('_schemaBaseT', bound=BaseSchema)


class CustomModelMeta(DeclarativeMeta):
    def __new__(cls, name: str, bases: Tuple[type], attrs: Dict[str, Any]) -> 'CustomModelMeta':
        model_cls = super().__new__(cls, name, bases, attrs)

        setattr(cls, "DoesNotExist", type("DoesNotExist", (DoesNotExistError,), {}))
        return model_cls


class BaseModel(Base, Generic[_schemaBaseT], metaclass=CustomModelMeta):  # type: ignore
    __abstract__: ClassVar[bool] = True
    __secured_fields__: ClassVar[Tuple[str, ...]] = tuple()

    class DoesNotExist(DoesNotExistError):  # Only for type checking; Will be replaced by metaclass
        pass

    @classmethod
    def as_pydantic_scheme(
            cls,
            exclude: Optional[Tuple[str]] = None,
            bases: Optional[Tuple[Type[_schemaBaseT], ...]] = None,
            **model_kwargs
    ) -> Type[_schemaBaseT]:
        return sqlalchemy_to_pydantic(
            db_model=cls,
            exclude=cls.__secured_fields__ + (exclude if exclude is not None else tuple()),
            bases=bases,
            **model_kwargs
        )

    def to_scheme(self, scheme_cls: Type[_schemaBaseT], **fields) -> _schemaBaseT:
        return scheme_cls.parse_obj({
            **self.__dict__,
            **fields
        })
