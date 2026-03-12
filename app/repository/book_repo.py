from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.book import Book  

class BookRepository:
    def get_all(self, db: Session, limit: int, offset: int, sort_by: str):
        """
        Отримання книг із бази даних з використанням Limit-Offset пагінації.
        """
        
        return db.query(Book).order_by(getattr(Book, sort_by)).offset(offset).limit(limit).all()

    def get_by_id(self, db: Session, book_id: UUID) -> Optional[Book]:
        """Пошук книги в БД за ID."""
        return db.query(Book).filter(Book.id == book_id).first()

    def create(self, db: Session, book_data: dict) -> Book:
        """Створення нової книги в PostgreSQL."""
        db_book = Book(**book_data)
        db.add(db_book)
        db.commit()      # Зберігаємо в базу
        db.refresh(db_book) # Отримуємо об'єкт з уже присвоєним ID
        return db_book

    def delete(self, db: Session, book_id: UUID) -> bool:
        """Ідемпотентне видалення."""
        db_book = self.get_by_id(db, book_id)
        if db_book:
            db.delete(db_book)
            db.commit()
            return True
        return False