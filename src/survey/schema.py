from sqlalchemy import Column, Integer, String, JSON, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from schema import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_list = Column(JSON, nullable=False)

    answers = relationship("Answer", back_populates="question")
    calls = relationship("Call", back_populates="start_question")


class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, nullable=False)
    survey_name = Column(String(50), nullable=False)

    routines = relationship("Routine", back_populates="survey")
    calls = relationship("Call", back_populates="survey")
    answers = relationship("Answer", back_populates="survey")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    answer_list = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("Contact", back_populates="answers")
    survey = relationship("Survey", back_populates="answers")
    question = relationship("Question", back_populates="answers")
