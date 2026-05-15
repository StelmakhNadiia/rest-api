from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from models.book_model import BookModel
from schemas.book_schema import BookCreate


def get_books(db: Session, limit: int, cursor: str | None):
    query = db.query(BookModel)
    
    if cursor:
        try:
            
            cursor_uuid = uuid.UUID(cursor)
            query = query.filter(BookModel.id > cursor_uuid)
        except ValueError:
            pass 
            
    return query.order_by(BookModel.id).limit(limit).all()

def get_book(db: Session, book_id: UUID):
    return db.query(BookModel).filter(BookModel.id == book_id).first()

def create_book(db: Session, book: BookCreate):
    new_book = BookModel(
        id=uuid.uuid4(),
        title=book.title,
        author=book.author,
        description=book.description,
        status=book.status,
        year=book.year
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def delete_book(db: Session, book_id: UUID):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False