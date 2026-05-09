from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID

from models.book_model import BookModel
from schemas.book_schema import BookCreate
from repository import book_repository as repo

class BookService:
    @staticmethod
    async def get_books_paginated(
        db: Session, 
        limit: int = 10, 
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        за допомогою курсорної пагінації.
        """
       
        items = repo.get_all_books(db, limit=limit, cursor=cursor)
        
       
        next_cursor = None
        if len(items) == limit:
           
            next_cursor = str(items[-1].id)
            
        return {
            "items": items,
            "next_cursor": next_cursor,
            "limit": limit
        }

    @staticmethod
    async def get_book_by_id(db: Session, book_id: str):
        return repo.get_book(db, book_id)

    @staticmethod
    async def create_new_book(db: Session, book_data: BookCreate):
       
        return repo.create_book(db, book_data)

    @staticmethod
    async def remove_book(db: Session, book_id: str) -> bool:
        return await repo.delete_book(db, book_id)