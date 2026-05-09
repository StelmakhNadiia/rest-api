from sqlalchemy.orm import Session
from models.book_model import Book


async def get_books(db: Session, limit: int, offset: int):
    return db.query(Book).offset(offset).limit(limit).all()


async def get_book_by_id(db: Session, book_id):
    return db.query(Book).filter(Book.id == book_id).first()


async def add_book(db: Session, book_data):
    book = Book(**book_data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


async def delete_book(db: Session, book_id):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book:
        db.delete(book)
        db.commit()

    return True
async def get_books(db: Session, limit: int, offset: int):
    items = db.query(Book).offset(offset).limit(limit).all()
    total = db.query(Book).count()  #  скільки всього книг
    return items, total