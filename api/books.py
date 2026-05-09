from flask import request
from flask_restful import Resource
from flasgger import swag_from

from services.book_service import (
    get_books_service,
    get_book_service,
    create_book_service,
    remove_book_service
)


class BooksResource(Resource):

    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'limit',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 10
            },
            {
                'name': 'offset',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 0
            }
        ],
        'responses': {
            200: {
                'description': 'List of books'
            }
        }
    })
    def get(self):
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
        return get_books_service(limit, offset)

    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string'},
                        'author': {'type': 'string'},
                        'description': {'type': 'string'},
                        'status': {
                            'type': 'string',
                            'enum': ['available', 'borrowed']
                        },
                        'year': {'type': 'integer'}
                    }
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Book created'
            }
        }
    })
    def post(self):
        data = request.get_json()
        return create_book_service(data), 201


class BookResource(Resource):

    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            200: {'description': 'Book found'},
            404: {'description': 'Book not found'}
        }
    })
    def get(self, book_id):
        book = get_book_service(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return book

    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            204: {'description': 'Book deleted'},
            404: {'description': 'Book not found'}
        }
    })
    def delete(self, book_id):
        book = remove_book_service(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return "", 204