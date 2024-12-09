from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from src.schema import TableBase, PrimaryKey
from src.routine.schema import Routine  # noqa
from src.contact.schema import Contact  # noqa


class Group(TableBase):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(50), nullable=False, unique=True)

    routines = relationship("Routine", back_populates="groups")
    contact_groups = relationship("ContactGroup", back_populates="groups")


class GroupCreate(BaseModel):
    groupName: str


class GroupRead(BaseModel):
    id: PrimaryKey
    groupName: str


class GroupList(BaseModel):
    groupIds: list[PrimaryKey]
