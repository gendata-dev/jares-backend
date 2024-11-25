from pydantic import BaseModel
from pydantic.generics import GenericModel
from sqlalchemy.orm import declarative_base
from typing import Generic, TypeVar, List, Optional

TableBase = declarative_base()


T = TypeVar("T")


class MetaData(BaseModel):
    itemsPerPage: Optional[int] = None
    totalItems: Optional[int] = None
    pageIndex: Optional[int] = None
    totalPages: Optional[int] = None


class GenericResponse(GenericModel, Generic[T]):
    data: Optional[MetaData]
    items: List[T]
