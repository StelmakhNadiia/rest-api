from fastapi import APIRouter, HTTPException, Query, Depends, Request
from typing import Any, Dict
from schemas.book_schema import BookCreate, Book
from database.mongo import get_books_collection
from services import book_service

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=Dict[str, Any])
async def get_all_books(
        request: Request,
        limit: int = Query(10, ge=1),
        offset: int = Query(0, ge=0),
        collection = Depends(get_books_collection)
):
    
    books, total_count = await book_service.get_books_service(collection, limit, offset)
    
   
    base_url = str(request.url).split('?')[0]
    
   
    next_page = None
    if offset + limit < total_count:
        next_page = f"{base_url}?limit={limit}&offset={offset + limit}"
        
   
    prev_page = None
    if offset > 0:
        prev_offset = max(0, offset - limit)
        prev_page = f"{base_url}?limit={limit}&offset={prev_offset}"

    return {
        "count": total_count,
        "next": next_page,
        "prev": prev_page,
        "results": books
    }

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