from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from schemas.book_schema import BookCreate, Book , BookPaginationResponse
from services.book_service import (
    get_books_service,
    get_book_service,
    create_book_service,
    remove_book_service
)
from database.db import get_db

router = APIRouter(prefix="/books", tags=["Books"])



@router.get("/", response_model=BookPaginationResponse)
async def get_all_books(
        limit: int = Query(10, ge=1),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    return await get_books_service(db, limit, offset)

@router.get("/{book_id}", response_model=Book)
async def get_book_by_id(
        book_id: UUID,
        db: Session = Depends(get_db)
):
    book = await get_book_service(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post("/", response_model=Book, status_code=201)
async def add_book(
        book: BookCreate,
        db: Session = Depends(get_db)
):
    return await create_book_service(db, book)


@router.delete("/{book_id}", status_code=204)
async def delete_book(
        book_id: UUID,
        db: Session = Depends(get_db)
):
    await remove_book_service(db, book_id)
    return