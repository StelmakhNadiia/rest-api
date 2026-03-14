from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List
from app.schemas.book import BookCreate, BookRead
from app.repository.book_repo import MongoBookRepository
from app.core.database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookRead])
async def get_books(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db = Depends(get_db)
):
    repo = MongoBookRepository(db)
    return await repo.get_all(limit, offset)

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db = Depends(get_db)):
    repo = MongoBookRepository(db)
    return await repo.create(book_in.model_dump())

@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: str, db = Depends(get_db)):
    repo = MongoBookRepository(db)
    book = await repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db = Depends(get_db)):
    repo = MongoBookRepository(db)
    deleted = await repo.delete(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None