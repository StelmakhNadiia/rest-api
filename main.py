from fastapi import FastAPI
from api.books import router as books_router


app = FastAPI(
    title="Library Management API",
    description="API для керування книгами в бібліотеці",
    version="1.0.0"
)


app.include_router(books_router)

@app.get("/")
async def root():
    """Ендпоінт для перевірки, чи працює сервіс"""
    return {"message": "Library API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)