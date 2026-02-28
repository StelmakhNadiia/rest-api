from typing import List, Optional, Dict
from uuid import UUID
from app.repository.book_repo import BookRepository
from app.models.book import BookStatus

class BookService:
    def __init__(self):
        self.repository = BookRepository()

    async def get_books(
        self, 
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None,
        sort_by: Optional[str] = None
    ) -> List[Dict]:
        """Отримання книг із застосуванням фільтрації та сортування."""
        books = await self.repository.get_all()

        # 1. Фільтрація
        if status:
            books = [b for b in books if b["status"] == status]
        if author:
            books = [b for b in books if author.lower() in b["author"].lower()]

        # 2. Сортування (по Назві або Року випуску)
        if sort_by == "title":
            books = sorted(books, key=lambda x: x["title"].lower())
        elif sort_by == "year":
            books = sorted(books, key=lambda x: x["year"])

        return books

    async def get_book_by_id(self, book_id: UUID) -> Optional[Dict]:
        return await self.repository.get_by_id(book_id)

    async def add_book(self, book_data: Dict) -> Dict:
        
        return await self.repository.create(book_data)

    async def remove_book(self, book_id: UUID) -> bool:
        return await self.repository.delete(book_id)