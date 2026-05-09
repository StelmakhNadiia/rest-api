from database.mongo import books_collection
from bson import ObjectId, errors


async def get_all_books(limit: int, offset: int):

    books_cursor = books_collection.find().skip(offset).limit(limit)
    books = await books_cursor.to_list(length=limit)
    for book in books:
        book["id"] = str(book["_id"])
        del book["_id"]
    return books


async def get_book(book_id: str):
    try:
        book = await books_collection.find_one({"_id": ObjectId(book_id)})
    except errors.InvalidId:
        return None

    if not book:
        return None

    book["id"] = str(book["_id"])
    del book["_id"]
    return book


async def create_book(book_data):

    book_dict = book_data.dict() if hasattr(book_data, "dict") else book_data
    result = await books_collection.insert_one(book_dict)
    book_dict["id"] = str(result.inserted_id)

    if "_id" in book_dict:
        del book_dict["_id"]
    return book_dict


async def delete_book(book_id: str):
    try:
        obj_id = ObjectId(book_id)
    except errors.InvalidId:
        return None

    book = await books_collection.find_one({"_id": obj_id})
    if not book:
        return None

    await books_collection.delete_one({"_id": obj_id})
    book["id"] = str(book["_id"])
    del book["_id"]
    return book