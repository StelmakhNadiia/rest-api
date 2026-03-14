from typing import List, Optional
from pydantic_mongo import PydanticObjectId

class MongoBookRepository:
    def __init__(self, db):
        self.collection = db.books

    async def get_all(self, limit: int, offset: int) -> List[dict]:
        cursor = self.collection.find({}).skip(offset).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_by_id(self, book_id: str) -> Optional[dict]:
        return await self.collection.find_one({"_id": PydanticObjectId(book_id)})

    async def create(self, book_data: dict) -> dict:
        result = await self.collection.insert_one(book_data)
        book_data["_id"] = result.inserted_id
        return book_data

    async def delete(self, book_id: str) -> bool:
        response = await self.collection.delete_one({"_id": PydanticObjectId(book_id)})
        return response.deleted_count > 0