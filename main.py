import contextlib
from fastapi import FastAPI
from api.books import router as books_router

from database.db import Base, engine

from models.book_model import BookModel 

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
   
app = FastAPI(
    title="Library API",
    lifespan=lifespan
)


app.include_router(books_router)

@app.get("/")
async def root():
    return {"message": "Library API is running"}