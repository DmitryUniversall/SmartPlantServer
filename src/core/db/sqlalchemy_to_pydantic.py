from typing import TYPE_CHECKING, Container, Optional, TypeVar, Type, Tuple

from pydantic import ConfigDict, create_model

from src.core.exceptions import NotFoundError

if TYPE_CHECKING:
    from .base import BaseModel, BaseSchema  # type: ignore

_schemaBaseT = TypeVar('_schemaBaseT', bound='BaseSchema')


def sqlalchemy_to_pydantic(
        db_model: Type['BaseModel'],
        *,
        exclude: Optional[Container[str]] = None,
        config: Optional[ConfigDict] = None,
        bases: Optional[Tuple[Type[_schemaBaseT], ...]] = None,
        **model_kwargs
) -> Type[_schemaBaseT]:
    table = db_model.metadata.tables[db_model.__tablename__]
    fields = {}

    for column in table.columns:
        column_name = column.name
        if exclude is not None and column_name in exclude:
            continue

        if hasattr(column.type, "impl") and hasattr(column.type.impl, "python_type"):
            python_type = column.type.impl.python_type
        elif hasattr(column.type, "python_type"):
            python_type = column.type.python_type
        else:
            raise NotFoundError(f"Column has no type impl or python_type (Column {column})")

        fields[column_name] = (python_type, ...) if not column.nullable else (Optional[python_type], None)

    return create_model(  # type: ignore
        db_model.__name__,
        __config__=config,
        __base__=bases,
        **model_kwargs,
        **fields
    )
