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
        return cls(items=items, meta=meta)
