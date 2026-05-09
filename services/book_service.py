from repository.book_repository import (
    get_all_books,
    get_book,
    create_book,
    delete_book
)

def get_books_service(limit, offset):
    return get_all_books(limit, offset)

def get_book_service(book_id: str):
    return get_book(book_id)

def create_book_service(book_data):
    return create_book(book_data)

def remove_book_service(book_id: str):
    return delete_book(book_id)