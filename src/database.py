from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from src.config import DBConfig

DB_URL = DBConfig.SQLALCHEMY_DATABASE_URI


db_conn: Optional[Engine]


def connect_db():
    global db_conn
    # TODO: echo for test need to delete in prod
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
