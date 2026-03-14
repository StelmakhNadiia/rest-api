from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID
from app.repository.book_repo import BookRepository

class BookService:
    def __init__(self):
        self.repository = BookRepository()

    async def get_books(self, db: Session, limit: int, cursor: Optional[UUID] = None):
        items = self.repository.get_all(db=db, limit=limit, cursor=cursor)
        
        next_cursor = None
        if len(items) == limit:
            next_cursor = items[-1].id
            
        return {
            "items": items,
            "next_cursor": next_cursor
        }

    async def get_book_by_id(self, db: Session, book_id: UUID):
        return self.repository.get_by_id(db, book_id)

    async def add_book(self, db: Session, book_data: dict):
        return self.repository.create(db, book_data)

    async def remove_book(self, db: Session, book_id: UUID) -> bool:
        return self.repository.delete(db, book_id)