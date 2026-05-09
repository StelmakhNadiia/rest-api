from pydantic import BaseModel
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