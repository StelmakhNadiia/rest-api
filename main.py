from fastapi import FastAPI
from app.api.book_router import router as book_router
from app.core.database import engine, Base 
import app.models.book 

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library REST API",
    description="Лабораторна робота №2",
    version="1.0.0"
)

app.include_router(book_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Library API"}