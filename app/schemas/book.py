from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from pydantic_mongo import PydanticObjectId

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None
    year: int = Field(..., gt=0, lt=2027)

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
   
    id: PydanticObjectId = Field(alias="_id")

    model_config = ConfigDict(
        populate_by_name=True, 
        json_encoders={PydanticObjectId: str} 
    )