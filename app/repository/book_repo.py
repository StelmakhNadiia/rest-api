from uuid import UUID, uuid4
from app.models.book import books_db

class BookRepository:
    async def get_all(self):
        return books_db

    async def get_by_id(self, book_id: UUID):
        for book in books_db:
            if str(book["id"]) == str(book_id):
                return book
        return None

    async def create(self, book_data: dict):
        new_book = {
            "id": uuid4(),
            **book_data
        }
        books_db.append(new_book)
        return new_book

    async def delete(self, book_id: UUID):
        for i, book in enumerate(books_db):
            if str(book["id"]) == str(book_id):
                books_db.pop(i)
                return True
        return False