from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID

from schemas.book_schema import BookCreate, BookRead, BookPaginationResponse
from services.book_service import BookService
from database.db import get_db


router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=BookPaginationResponse)
async def get_all_books(
    limit: int = Query(10, ge=1),
    cursor: str | None = None,
    db: Session = Depends(get_db)
):
    return await BookService.get_books_paginated(db, limit, cursor)


@router.post("/", response_model=BookRead, status_code=201)
async def add_book(book: BookCreate, db: Session = Depends(get_db)):
   return await BookService.create_new_book(db, book)

@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: UUID,
    db: Session = Depends(get_db)
):
    success = await BookService.remove_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")