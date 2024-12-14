from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel

from src.schema import TableBase, PrimaryKey
from src.routine.schema import Routine  # noqa


class Survey(TableBase):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    routines = relationship("Routine", back_populates="surveys")


class SurveyQuestionCategory(TableBase):
    """관계 테이블"""

    __tablename__ = "survey_question_categories"

    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    question_category_id = Column(
        Integer, ForeignKey("question_categories.id"), nullable=False
    )

    __table_args__ = tuple(PrimaryKeyConstraint(survey_id, question_category_id))


class SurveyRead(BaseModel):
    id: PrimaryKey
    name: str
    questionCategories: list[dict]


class SurveyCreate(BaseModel):
    name: str
    questionCategories: list[PrimaryKey]
