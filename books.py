'''
Main file for Books API
'''
from dataclasses import dataclass

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session # pylint: disable=import-error

import models # pylint: disable=import-error
from database import SessionLocal, engine # pylint: disable=import-error

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    '''Get DB Session

    Yields:
        Session: DB Session
    '''
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()

@dataclass
class Book(BaseModel):
    '''
    Base Model to use in API
    '''
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    '''_summary_

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    '''
    return db.query(models.Books).all()


@app.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
    '''_summary_

    Args:
        book (Book): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    '''

    book_model = models.Books()
    book_model.title = book.title # type: ignore
    book_model.author = book.author # type: ignore
    book_model.description = book.description # type: ignore
    book_model.rating = book.rating # type: ignore

    db.add(book_model)
    db.commit()

    return book


@app.put("/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    '''_summary_

    Args:
        book_id (int): _description_
        book (Book): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    '''

    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )

    book_model.title = book.title # type: ignore
    book_model.author = book.author # type: ignore
    book_model.description = book.description # type: ignore
    book_model.rating = book.rating # type: ignore

    db.add(book_model)
    db.commit()

    return book


@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    '''_summary_

    Args:
        book_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
    '''

    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )

    db.query(models.Books).filter(models.Books.id == book_id).delete()

    db.commit()
