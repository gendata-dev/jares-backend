from fastapi import Depends
from typing import Annotated, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from src.config import DBConfig


db_conn: Optional[Engine]

# TODO: echo for test need to delete in prod
def connect_db():
    DB_URL = DBConfig.SQLALCHEMY_DATABASE_URI
    global db_conn
    db_conn = create_engine(DB_URL, echo=True)


def disconnect_db():
    global db_conn
    if db_conn:
        db_conn.dispose()


def get_db():
    with Session(bind=db_conn) as session:
        try:
            yield session
        finally:
            session.close()


DbSession = Annotated[Session, Depends(get_db)]
