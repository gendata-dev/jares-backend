from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.schema import TableBase


class Question(TableBase):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    question_list = Column(JSON, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    answers = relationship("Answer", back_populates="questions")
    surveys = relationship(
        "Survey",
        back_populates="questions",
        primaryjoin="Question.survey_id == Survey.id",
    )



class Survey(TableBase):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    current_question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    survey_name = Column(String(50), nullable=False)

    routines = relationship("Routine", back_populates="surveys")
    questions = relationship(
        "Question",
        back_populates="surveys",
        primaryjoin="Question.survey_id == Survey.id",
    )
    current_questions = relationship(
        "Question",
        uselist=False,
        primaryjoin="Survey.current_question_id == Question.id",
    )



class Llm(TableBase):
    __tablename__ = "llms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(50), nullable=False)
    reference_file = Column(Text, nullable=True)
    main_goals = Column(Text, nullable=True)
    prompt_1 = Column(Text, nullable=True)
    prompt_2 = Column(Text, nullable=True)
    prompt_3 = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now(), nullable=True)

    routines = relationship("Routine", back_populates="llms")
