from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, String, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel

from src.schema import TableBase, PrimaryKey
from src.survey.schema import Survey  # noqa


class QuestionCategory(TableBase):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=False, unique=True)
    # TODO: Q-A implement NEED FIX
    question_list = Column(ARRAY(String(100)))


# DEPRECATED
class Question(TableBase):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("question_categories.id"), nullable=False)
    # TODO: Q-A implement NEED FIX
    question_list = Column(String(100), nullable=False)
    # TODO: optional
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    # is_deleted = bool

    answers = relationship("Answer", back_populates="questions")
    # surveys = relationship(
    #     "Survey",
    #     back_populates="questions",
    #     primaryjoin="Question.survey_id == Survey.id",
    # )
    # question_categories = relationship("QuestionCategory", back_populates="questions")


class QuestionRead(BaseModel):
    id: PrimaryKey
    category: str
    questionList: list[str]


class QuestionCreate(BaseModel):
    category: str
    questionList: list[str]
