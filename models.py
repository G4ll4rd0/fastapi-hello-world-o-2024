'''
Models used in books API
'''
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String # pylint: disable=import-error

from database import Base # pylint: disable=import-error


@dataclass
class Books(Base):
    '''
    Model for Books DB
    '''
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(Integer)
