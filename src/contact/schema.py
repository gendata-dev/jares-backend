from sqlalchemy import Column, Integer, String, ForeignKey, Text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from src.schema import TableBase, PrimaryKey
from src.routine.schema import Routine  # noqa


class Contact(TableBase):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    phone = Column(String(20), nullable=False)
    region = Column(String(50), nullable=False)
    preferred_call_time = Column(Text, nullable=True)

    contact_crops = relationship("ContactCrop", back_populates="contacts")
    contact_equipments = relationship("ContactEquipment", back_populates="contacts")
    contact_groups = relationship("ContactGroup", back_populates="contacts")
    call_logs = relationship("CallLog", back_populates="contacts")
    answers = relationship("Answer", back_populates="contacts")


class Crop(TableBase):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    contact_crops = relationship("ContactCrop", back_populates="crops")


class Equipment(TableBase):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    contact_equipments = relationship("ContactEquipment", back_populates="equipments")


class ContactCrop(TableBase):
    """관계 테이블"""

    __tablename__ = "contact_crops"

    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)

    contacts = relationship("Contact", back_populates="contact_crops")
    crops = relationship("Crop", back_populates="contact_crops")

    __table_args__ = tuple(PrimaryKeyConstraint(contact_id, crop_id))


class ContactEquipment(TableBase):
    """관계 테이블"""

    __tablename__ = "contact_equipments"

    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipments.id"), nullable=False)

    contacts = relationship("Contact", back_populates="contact_equipments")
    equipments = relationship("Equipment", back_populates="contact_equipments")

    __table_args__ = tuple(PrimaryKeyConstraint(contact_id, equipment_id))


class ContactGroup(TableBase):
    """관계 테이블"""

    __tablename__ = "contact_groups"

    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    contacts = relationship("Contact", back_populates="contact_groups")
    groups = relationship("Group", back_populates="contact_groups")

    __table_args__ = tuple(PrimaryKeyConstraint(contact_id, group_id))


class ContactRead(BaseModel):
    id: PrimaryKey


class ContactCreate(BaseModel):
    name: str
    phone: str
    region: str
    # <HHMM> like 1930
    preferredCallTime: str
    # groupId: list[int]


class ContactUpdate(BaseModel):
    pass


class ContactDelete(BaseModel):
    pass
