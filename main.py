from fastapi import FastAPI
from app import auth, book_router
from main import app

app = FastAPI(title="Library API with JWT")


app.include_router(auth.router)
app.include_router(book_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to protected Library API"}