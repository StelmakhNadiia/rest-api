from flask import request
from flask_restful import Resource
from services.book_service import (
    get_books_service,
    get_book_service,
    create_book_service,
    remove_book_service
)

class BooksResource(Resource):
    def get(self):
        """
        Отримати список всіх книг
        ---
        tags:
          - Books
        parameters:
          - name: limit
            in: query
            type: integer
            default: 10
          - name: offset
            in: query
            type: integer
            default: 0
        responses:
          200:
            description: Список книг успішно отримано
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        """
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
        return get_books_service(limit, offset)

    def post(self):
        """
        Додати нову книгу
        ---
        tags:
          - Books
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/BookInput'
        responses:
          201:
            description: Книга створена
            schema:
              $ref: '#/definitions/Book'
        """
        data = request.get_json()
        return create_book_service(data), 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Книга знайдена
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Книгу не знайдено
        """
        book = get_book_service(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return book

    def delete(self, book_id):
        """
        Видалити книгу
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          204:
            description: Книга видалена
          404:
            description: Книгу не знайдено
        """
        book = remove_book_service(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return "", 204