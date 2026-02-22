from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from fastapi import HTTPException

app = FastAPI() 


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    description: Optional[str] = None 


books = [
    {"id": 1, "title": "Kobzar", "author": "Taras Shevchenko", "year": 1840},
]


@app.get("/books", response_model=List[Book])
async def get_books(): 
    return books

@app.post("/books", response_model=Book, status_code=201)
async def create_book(book: Book):
    books.append(book.dict())
    return book

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index] = updated_book.dict()
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(index)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")