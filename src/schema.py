from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from typing import Generic, TypeVar, List, Optional


class TableBase(DeclarativeBase):
    pass


T = TypeVar("T", bound=BaseModel)


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
