import json
from typing import Any, Dict
from typing import TypeVar, Type

from pydantic import BaseModel

_T = TypeVar('_T')


class BaseSchema(BaseModel):
    def to_model_instance(self, model: Type[_T]) -> _T:
        return model(**self.model_dump())

    def to_json_dict(self, *args, **kwargs) -> Dict[str, Any]:
        return self.model_dump(mode="json", *args, **kwargs)

    def convert_to(self, schema_cls: Type[_T], **fields) -> _T:
        return schema_cls(**{
            **self.model_dump(),
            **fields
        })
