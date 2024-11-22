from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
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
