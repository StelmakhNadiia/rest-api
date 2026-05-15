from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from typing import List, Optional  

class BookStatus(str, Enum):
    available = "available"
    borrowed = "borrowed"

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    status: BookStatus
    year: int = Field(..., ge=0)

class BookRead(BookCreate):
    id: UUID

    class Config:
        from_attributes = True 

class BookPaginationResponse(BaseModel):
    items: List[BookRead]
    next_cursor: Optional[str] = None 
    limit: int