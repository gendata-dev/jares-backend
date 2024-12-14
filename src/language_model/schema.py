from sqlalchemy import Column, Integer, String, ARRAY, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.schema import TableBase, PrimaryKey


class LanguageModel(TableBase):
    __tablename__ = "language_models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # TODO: NEED UNIQUE
    name = Column(String(50), nullable=False)
    reference_file = Column(Text, nullable=True)
    main_goals = Column(Text, nullable=True)
    prompts = Column(ARRAY(Text), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now(), nullable=True)

    routines = relationship("Routine", back_populates="language_models")


class LanguageModelCreate(BaseModel):
    name: str
    referenceFile: str
    mainGoals: str
    prompts: list[str]


class LanguageModelRead(BaseModel):
    id: PrimaryKey
    name: str
    referenceFile: str
    mainGoals: str
    prompts: list[str]
    createdAt: datetime
    updatedAt: Optional[datetime] = None


class LanguageModelDelete(BaseModel):
    languageModelIds: list[PrimaryKey]
