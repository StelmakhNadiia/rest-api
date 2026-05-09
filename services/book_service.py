from repository import book_repository
from schemas.book_schema import BookCreate

async def get_books_service(collection, limit: int, offset: int):
    return await book_repository.get_books(collection, limit, offset)

async def get_book_service(collection, book_id: str):
    return await book_repository.get_book(collection, book_id)

async def create_book_service(collection, book: BookCreate):
    return await book_repository.create_book(collection, book)

async def remove_book_service(collection, book_id: str):
    return await book_repository.delete_book(collection, book_id)