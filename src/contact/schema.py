from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from schema import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(50), nullable=False)

    contacts = relationship("Contact", back_populates="group")
    routines = relationship("Routine", back_populates="group")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    name = Column(String(10), nullable=False)
    phone = Column(String(20), nullable=False)
    region = Column(String(50), nullable=False)
    call_time = Column(Text, nullable=True)

    group = relationship("Group", back_populates="contacts")
    contact_crops = relationship("ContactCrop", back_populates="contacts")
    contact_equipments = relationship("ContactEquipment", back_populates="contacts")
    answers = relationship("Answer", back_populates="users")
    calls = relationship("Call", back_populates="receivers")


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)

    contact_crops = relationship("ContactCrop", back_populates="crops")


class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)

    contact_equipments = relationship("ContactEquipment", back_populates="equipments")


class ContactCrop(Base):
    __tablename__ = "contact_crops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)

    contact = relationship("Contact", back_populates="contact_crops")
    crop = relationship("Crop", back_populates="contact_crops")


class ContactEquipment(Base):
    __tablename__ = "contact_equipments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipments.id"), nullable=False)

    contact = relationship("Contact", back_populates="contact_equipments")
    equipment = relationship("Equipment", back_populates="contact_equipments")
