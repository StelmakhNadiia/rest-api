from database.mongo import books_collection
from bson import ObjectId, errors

def get_all_books(limit: int, offset: int):

    books_cursor = books_collection.find().skip(offset).limit(limit)
    books = []
    for book in books_cursor:
        book["id"] = str(book["_id"])
        del book["_id"]
        books.append(book)
    return books

def get_book(book_id: str):
    try:
        book = books_collection.find_one({"_id": ObjectId(book_id)})
    except errors.InvalidId:
        return None

    if not book:
        return None

    book["id"] = str(book["_id"])
    del book["_id"]
    return book

def create_book(book_dict):
    result = books_collection.insert_one(book_dict)
    book_dict["id"] = str(result.inserted_id)
    if "_id" in book_dict:
        del book_dict["_id"]
    return book_dict

def delete_book(book_id: str):
    try:
        obj_id = ObjectId(book_id)
    except errors.InvalidId:
        return None

    book = books_collection.find_one({"_id": obj_id})
    if not book:
        return None

    books_collection.delete_one({"_id": obj_id})
    book["id"] = str(book["_id"])
    del book["_id"]
    return book