from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from src.schema import TableBase, PrimaryKey


class Group(TableBase):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    routines = relationship("Routine", back_populates="groups")
    contact_groups = relationship("ContactGroup", back_populates="groups")


class GroupCreate(BaseModel):
    name: str


class GroupRead(BaseModel):
    id: PrimaryKey
    name: str


class GroupList(BaseModel):
    groupIds: list[PrimaryKey]
