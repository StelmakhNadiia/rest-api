from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from typing import Optional, List
from app.models.book import BookStatus

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None
    status: BookStatus = BookStatus.AVAILABLE
    year: int = Field(..., gt=0, lt=2027)

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class BookCursorPage(BaseModel):
    items: List[BookRead]
    next_cursor: Optional[UUID] = None