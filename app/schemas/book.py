from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from app.models.book import BookStatus

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: str
    status: BookStatus = BookStatus.AVAILABLE
    year: int = Field(..., gt=0)

class BookRead(BookCreate):
    id: UUID