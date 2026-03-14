from flask import request
from flask_restful import Resource
from app.repository.book_repo import MongoBookRepository
from app.schemas.book import BookCreate

class BookListResource(Resource):
    def __init__(self, db):
        self.repo = MongoBookRepository(db)

    def get(self):
        """
        Get all books
        ---
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
            description: Success
        """
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        books = self.repo.get_all(limit, offset)
        for b in books: b['_id'] = str(b['_id'])
        return books, 200

    def post(self):
        """
        Create a book
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                title:
                  type: string
                author:
                  type: string
                year:
                  type: integer
        responses:
          201:
            description: Created
        """
        data = request.get_json()
        book_in = BookCreate(**data)
        new_book = self.repo.create(book_in.model_dump())
        new_book['_id'] = str(new_book['_id'])
        return new_book, 201

class BookResource(Resource):
    def __init__(self, db):
        self.repo = MongoBookRepository(db)

    def get(self, book_id):
        """
        Get book by ID
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Success
          404:
            description: Not Found
        """
        book = self.repo.get_by_id(book_id)
        if not book: return {"message": "Not found"}, 404
        book['_id'] = str(book['_id'])
        return book, 200

    def delete(self, book_id):
        """
        Delete book
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          204:
            description: Deleted
        """
        if self.repo.delete(book_id): return '', 204
        return {"message": "Not found"}, 404