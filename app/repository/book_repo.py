from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.book import Book

class BookRepository:
    def get_all(self, db: Session, limit: int, cursor: Optional[UUID] = None):
        query = db.query(Book).order_by(Book.id)
        if cursor:
            query = query.filter(Book.id > cursor)
        return query.limit(limit).all()

    def get_by_id(self, db: Session, book_id: UUID) -> Optional[Book]:
        return db.query(Book).filter(Book.id == book_id).first()

    def create(self, db: Session, book_data: dict) -> Book:
        db_book = Book(**book_data)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    def delete(self, db: Session, book_id: UUID) -> bool:
        db_book = self.get_by_id(db, book_id)
        if db_book:
            db.delete(db_book)
            db.commit()
            return True
        return False