from typing import List, Optional, Dict
from uuid import UUID
from sqlalchemy.orm import Session
from app.repository.book_repo import BookRepository
from app.models.book import BookStatus

class BookService:
    def __init__(self):
        self.repository = BookRepository()

    async def get_books(
        self,
        db: Session,  
        limit: int,
        offset: int,
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None,
        sort_by: str = "title"
    ) -> List:
        """Отримання книг через репозиторій з пагінацією на рівні БД."""
        
        return self.repository.get_all(
            db=db, 
            limit=limit, 
            offset=offset, 
            sort_by=sort_by
        )

    async def get_book_by_id(self, db: Session, book_id: UUID):
        return self.repository.get_by_id(db, book_id)

    async def add_book(self, db: Session, book_data: Dict):
        return self.repository.create(db, book_data)

    async def remove_book(self, db: Session, book_id: UUID) -> bool:
        return self.repository.delete(db, book_id)