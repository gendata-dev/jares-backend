from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship

from src.schema import TableBase
from src.survey.schema import Survey  # noqa


class Routine(TableBase):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("llms.id"), nullable=False)
    routine_name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    active_status = Column(Boolean, default=True, nullable=False)
    day_of_the_week = Column(String(20), nullable=False)
    start_time = Column(Integer, nullable=False)

    groups = relationship("Group", back_populates="routines")
    surveys = relationship("Survey", back_populates="routines")
    llms = relationship("Llm", back_populates="routines")
    call_logs = relationship("CallLog", back_populates="routines")
