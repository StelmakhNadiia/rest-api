from app.repository.book_repo import BookRepository
from typing import Optional
from app.models.book import BookStatus

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def list_books(self, status: Optional[BookStatus], author: Optional[str], sort_by: Optional[str]):
        books = await self.repo.get_all()
        
        if status:
            books = [b for b in books if b["status"] == status]
        if author:
            books = [b for b in books if author.lower() in b["author"].lower()]
        
        if sort_by in ["title", "year"]:
            books = sorted(books, key=lambda x: x[sort_by])
            
        return books

    async def get_book(self, book_id):
        return await self.repo.get_by_id(book_id)

    async def add_book(self, data):
        return await self.repo.create(data)

    async def remove_book(self, book_id):
        return await self.repo.delete(book_id)