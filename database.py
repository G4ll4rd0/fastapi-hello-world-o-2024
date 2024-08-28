'''
File to connect to database
'''
from sqlalchemy import create_engine # pylint: disable=import-error
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # pylint: disable=import-error

SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
