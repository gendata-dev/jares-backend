from pydantic import BaseModel, conint
from sqlalchemy.orm import DeclarativeBase
from typing import Generic, TypeVar, List, Optional


PrimaryKey = conint(gt=0, lt=2147483647)
T = TypeVar("T")


class TableBase(DeclarativeBase):
    pass


class MetaData(BaseModel):
    itemsPerPage: Optional[int] = None
    totalItems: Optional[int] = None
    pageIndex: Optional[int] = None
    totalPages: Optional[int] = None


class GenericResponse(BaseModel, Generic[T]):
    items: List[T]
    meta: Optional[MetaData] = None

    @classmethod
    def create(cls, items: List[T], meta: Optional[MetaData] = None):
        """
        python과 DB는 명명 규칙이 snake case로 동일하지만
        js, ts의 경우 camel case를 사용한다
        google json style guide의 경우 camel case를 사용하는 것을 권고하기 떄문에
        일관적인 response형태를 위해 snake to camel 함수를 적용시킴
        client에 친화적인 API 구현방식
        """
        converted_item = [cls.snake_to_camel_dict(item) for item in items]
        return cls(items=converted_item, meta=meta)

    @classmethod
    def snake_to_camel_dict(cls, input_dict: dict) -> dict:
        result = dict()
        for key, value in input_dict.items():
            new_key = cls.snake_to_camel(key)

            if isinstance(value, dict):
                result[new_key] = cls.snake_to_camel_dict(value)
            elif isinstance(value, list):
                result[new_key] = [
                    cls.snake_to_camel_dict(v) if isinstance(v, dict) else v
                    for v in value
                ]
            else:
                result[new_key] = value

        return result

    @classmethod
    def snake_to_camel(cls, snake_str: str) -> str:
        parts = snake_str.split("_")
        return parts[0] + "".join(part.capitalize() for part in parts[1:])