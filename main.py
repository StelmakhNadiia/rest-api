from fastapi import FastAPI
from api.books import router as books_router

app = FastAPI()

app.include_router(books_router)


@app.get("/")
async def root():
    return {"message": "Library API is running"}