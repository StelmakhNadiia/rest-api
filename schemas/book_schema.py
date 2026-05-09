from pydantic import BaseModel, EmailStr
from enum import Enum


class BookStatus(str, Enum):
    available = "available"
    borrowed = "borrowed"


class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    status: BookStatus
    year: int


class Book(BookCreate):
    id: str

class UserSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str