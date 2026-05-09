from sqlalchemy.orm import Session

from repository.book_repository import (
    get_books,
    get_book_by_id,
    add_book,
    delete_book
)


async def get_books_service(db: Session, limit: int, offset: int):
    return await get_books(db, limit, offset)


async def get_book_service(db: Session, book_id):
    return await get_book_by_id(db, book_id)


async def create_book_service(db: Session, book_data):
    book = book_data.model_dump()
    return await add_book(db, book)


async def remove_book_service(db: Session, book_id):
    return await delete_book(db, book_id)

async def get_books_service(db: Session, limit: int, offset: int):
    items, total = await get_books(db, limit, offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}