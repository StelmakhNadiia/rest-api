from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.schemas.book import BookCreate, BookRead
from app.services.book_service import BookService
from app.models.book import BookStatus
from app.core.database import get_db

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.get("/", response_model=List[BookRead])
async def get_books(
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = Query("title", pattern="^(title|year)$"),
    limit: int = Query(10, ge=1, le=100), 
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return await service.get_books(
        db=db,
        status=status, 
        author=author, 
        sort_by=sort_by, 
        limit=limit, 
        offset=offset
    )

@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: UUID, db: Session = Depends(get_db)):
    book = await service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Книгу не знайдено"
        )
    return book

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    return await service.add_book(db, book_in.model_dump())

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: Session = Depends(get_db)):
    await service.remove_book(db, book_id)
    return None