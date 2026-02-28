from fastapi import FastAPI
from app.api.book_router import router as book_router

app = FastAPI(
    title="Library REST API",
    description="Лабораторна робота №1",
    version="1.0.0"
)


app.include_router(book_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Library API"}