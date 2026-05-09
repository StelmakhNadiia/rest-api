from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from schemas.book_schema import BookCreate, Book
from database.mongo import get_books_collection
from services import book_service

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[Book])
async def get_all_books(
        limit: int = Query(10, ge=1),
        offset: int = Query(0, ge=0),
        collection = Depends(get_books_collection)
):
    return await book_service.get_books_service(collection, limit, offset)

@router.get("/{book_id}", response_model=Book)
async def get_book_by_id(book_id: str, collection = Depends(get_books_collection)):
    book = await book_service.get_book_service(collection, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=201)
async def add_book(book: BookCreate, collection = Depends(get_books_collection)):
    return await book_service.create_book_service(collection, book)

@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: str, collection = Depends(get_books_collection)):
    book = await book_service.remove_book_service(collection, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")