from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.schemas.book import BookCreate, BookRead, BookCursorPage
from app.services.book_service import BookService
from app.core.database import get_db

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.get("/", response_model=BookCursorPage)
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    return await service.get_books(db=db, limit=limit, cursor=cursor)

@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: UUID, db: Session = Depends(get_db)):
    book = await service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@router.post("/", response_model=BookRead, status_code=201)
async def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    return await service.add_book(db, book_in.model_dump())

@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: UUID, db: Session = Depends(get_db)):
    await service.remove_book(db, book_id)
    return None