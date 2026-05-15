from bson import ObjectId
from schemas.book_schema import BookCreate


async def get_books(collection, limit: int, offset: int):
    total_count = await collection.count_documents({})

    cursor = collection.find().skip(offset).limit(limit)
    books = []
    async for book in cursor:
        book["id"] = str(book["_id"])
        del book["_id"]
        books.append(book)
        
    return books, total_count


async def get_book(collection, book_id: str):
    if not ObjectId.is_valid(book_id):
        return None

    book = await collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        return None

    book["id"] = str(book["_id"])
    del book["_id"]
    return book


async def create_book(collection, book: BookCreate):
    book_dict = book.model_dump()
    result = await collection.insert_one(book_dict)
    book_dict["id"] = str(result.inserted_id)
    if "_id" in book_dict:
        del book_dict["_id"]
    return book_dict


async def delete_book(collection, book_id: str):
    if not ObjectId.is_valid(book_id):
        return None

    book = await collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        return None

    await collection.delete_one({"_id": ObjectId(book_id)})
    book["id"] = str(book["_id"])
    del book["_id"]
    return book