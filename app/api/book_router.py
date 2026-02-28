from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from app.schemas.book import BookCreate, BookRead
from app.services.book_service import BookService
from app.models.book import BookStatus

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.get("/", response_model=List[BookRead])
async def get_books(
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = Query(None, regex="^(title|year)$")
):
    """Ендпоїнт для отримання всіх книг з фільтрацією та сортуванням."""
    return await service.get_books(status=status, author=author, sort_by=sort_by)

@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: UUID):
    """Отримання книги за ID. Повертає 404, якщо не знайдено."""
    book = await service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Книгу не знайдено"
        )
    return book

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate):
    """Додавання нової книги. Валідація через Pydantic."""
    return await service.add_book(book_in.model_dump())

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    """
    Ідемпотентне видалення. 
    Навіть якщо книги немає, повертаємо 204 (успішно, без контенту).
    """
    await service.remove_book(book_id)
    return None