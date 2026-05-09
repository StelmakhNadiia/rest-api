from fastapi import FastAPI
from api.books import router as books_router

from database.db import Base, engine
from models.book_model import Book

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(books_router)


@app.get("/")
async def root():
    return {"message": "Library API is running"}