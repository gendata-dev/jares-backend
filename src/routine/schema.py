from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Date,
    ARRAY,
)
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import date
from typing import Optional

from src.schema import TableBase, PrimaryKey


# TODO: NEED TO ADD CONSTRAINT 'execution_days'
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
    execution_days = Column(ARRAY(String(3)), nullable=False)
    execution_count = Column(Integer, default=0)
    # start_time = Column(Integer, nullable=False)

    groups = relationship("Group", back_populates="routines")
    surveys = relationship("Survey", back_populates="routines")
    language_models = relationship(
        "LanguageModel", cascade="", back_populates="routines"
    )
    call_logs = relationship("CallLog", back_populates="routines")


class RoutineCreate(BaseModel):
    groupId: PrimaryKey
    surveyId: PrimaryKey
    languageModelId: PrimaryKey
    name: str
    startDate: date
    endDate: date
    activeStatus: bool
    # TODO: BE ENUM
    executionDays: list[str]

    # start_time: int


class RoutineRead(BaseModel):
    id: PrimaryKey
    name: str
    groupId: PrimaryKey
    groupName: Optional[str] = None
    surveyId: PrimaryKey
    surveyName: Optional[str] = None
    languageModelId: PrimaryKey
    languageModelName: Optional[str] = None
    startDate: date
    endDate: date
    activeStatus: bool
    executionDays: list[str]


class RoutineDelete(BaseModel):
    routineIds: list[PrimaryKey]
