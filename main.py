from fastapi import FastAPI
from api.books import router as books_router

from database.db import Base, engine
from models.book_model import BookModel

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(books_router)


@app.get("/")
async def root():
    return {"message": "Library API is running"}