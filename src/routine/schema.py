from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime

from src.schema import TableBase, PrimaryKey


class Routine(TableBase):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    language_model_id = Column(
        Integer, ForeignKey("language_models.id"), nullable=False
    )
    name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    active_status = Column(Boolean, default=True, nullable=False)
    day_of_the_week = Column(String(20), nullable=False)
    # start_time = Column(Integer, nullable=False)

    groups = relationship("Group", back_populates="routines")
    surveys = relationship("Survey", back_populates="routines")
    language_models = relationship(
        "LanguageModel", cascade="", back_populates="routines"
    )
    call_logs = relationship("CallLog", back_populates="routines")


class RoutineCreate(BaseModel):
    group_id: PrimaryKey
    survey_id: PrimaryKey
    llm_id: PrimaryKey
    name: str
    start_date: datetime
    end_date: datetime
    active_status: bool
    # TODO: BE ENUM
    day_of_week: str
    # start_time: int


class RoutineRead(BaseModel):
    id: PrimaryKey
    group_id: PrimaryKey
    survey_id: PrimaryKey
    llm_id: PrimaryKey
    name: str
    start_date: datetime
    end_date: datetime
    active_status: bool
    day_of_week: str
