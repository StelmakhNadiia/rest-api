from fastapi import FastAPI, Body, HTTPException, Depends, Query
from typing import List
from database.mongo import users_collection, books_collection
from schemas.user_schema import UserSchema
from schemas.book_schema import BookCreate, Book
from services import book_service
from auth.auth_handler import create_tokens, get_password_hash, verify_password, decode_jwt
from auth.auth_bearer import JWTBearer
from rate_limiter import rate_limit


app = FastAPI(
    title="Library API with JWT",
    dependencies=[Depends(rate_limit)]
)


@app.post("/user/signup", tags=["User"])
async def create_user(user: UserSchema = Body(...)):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = {
        "email": user.email,
        "password": get_password_hash(user.password)
    }
    await users_collection.insert_one(user_dict)
    return create_tokens(user.email)


@app.post("/user/login", tags=["User"])
async def user_login(user: UserSchema = Body(...)):
    user_in_db = await users_collection.find_one({"email": user.email})
    if user_in_db and verify_password(user.password, user_in_db["password"]):
        return create_tokens(user.email)
    raise HTTPException(status_code=401, detail="Invalid login details")


@app.post("/user/refresh", tags=["User"])
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    payload = decode_jwt(refresh_token)
    if payload:
        return create_tokens(payload["user_id"])
    raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

@app.get("/books/", response_model=List[Book], tags=["Books"])
async def get_all_books(
        limit: int = Query(10, ge=1),
        offset: int = Query(0, ge=0)
):

    return await book_service.get_books_service(limit, offset)

@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
async def get_book_by_id(book_id: str):

    book = await book_service.get_book_service(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books/", response_model=Book, status_code=201, dependencies=[Depends(JWTBearer())], tags=["Books"])
async def add_book(book: BookCreate):

    return await book_service.create_book_service(book)

@app.delete("/books/{book_id}", status_code=204, dependencies=[Depends(JWTBearer())], tags=["Books"])
async def delete_book(book_id: str):

    book = await book_service.remove_book_service(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return None

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Library API with JWT is running"}