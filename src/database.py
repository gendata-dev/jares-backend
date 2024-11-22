from sqlalchemy import create_engine

from config import DBConfig

DB_URL = DBConfig.SQLALCHEMY_DATABASE_URI
engine = create_engine(DB_URL)
