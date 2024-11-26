from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.schema import TableBase


class Question(TableBase):
	__tablename__ = "questions"

	id = Column(Integer, primary_key=True, autoincrement=True)
	question_list = Column(JSON, nullable=False)

	answers = relationship("Answer", back_populates="questions")
    # calls = relationship("Call", back_populates="questions")


class Survey(TableBase):
	__tablename__ = "surveys"

	id = Column(Integer, primary_key=True, autoincrement=True)
	question_id = Column(Integer, nullable=False)
	survey_name = Column(String(50), nullable=False)
    
	routines = relationship("Routine", back_populates="surveys")
	answers = relationship("Answer", back_populates="surveys")


class Model(TableBase):
	__tablename__ = "models"
    
	id = Column(Integer, primary_key=True, autoincrement=True)
	model_name = Column(String(50), nullable=False)
	reference_file = Column(Text, nullable=True)
	main_goals = Column(Text, nullable=True)
	prompt_1 = Column(Text, nullable=True)
	prompt_2 = Column(Text, nullable=True)
	prompt_3 = Column(Text, nullable=True)
	created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
	updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now(), nullable=True)

	routines = relationship("Routine", back_populates="models")
