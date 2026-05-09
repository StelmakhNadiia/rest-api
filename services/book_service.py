from repository import book_repository

async def get_books_service(limit, offset):
    return await book_repository.get_all_books(limit, offset)

async def get_book_service(book_id):
    return await book_repository.get_book(book_id)

async def create_book_service(book_data):
    return await book_repository.create_book(book_data)

async def remove_book_service(book_id):
    return await book_repository.delete_book(book_id)