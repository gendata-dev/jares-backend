from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import DBConfig

DB_URL = DBConfig.SQLALCHEMY_DATABASE_URI

# TODO: it's for test need to delete in prod
# import logging
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
engine = create_engine(DB_URL, echo=True)

# engine = create_engine(DB_URL)


def get_db():
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_db)]
