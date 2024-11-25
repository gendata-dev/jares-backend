from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from schema import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    sessions = relationship("Session", back_populates="users")


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    last_accessed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="sessions")
