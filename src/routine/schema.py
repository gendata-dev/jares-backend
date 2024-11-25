from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship

from schema import Base


class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    routine_name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    active_status = Column(Boolean, default=True, nullable=False)
    day_of_the_week = Column(String(20), nullable=False)
    start_time = Column(Integer, nullable=False)

    group = relationship("Group", back_populates="routines")
    survey = relationship("Survey", back_populates="routines")
    model = relationship("Model", back_populates="routines")
    calls = relationship("Call", back_populates="routines")
