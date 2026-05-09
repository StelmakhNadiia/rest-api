from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from api.books import BooksResource, BookResource

app = Flask(__name__)
api = Api(app)

template = {
    "swagger": "2.0",
    "info": {
        "title": "Library API",
        "version": "1.0.0",
        "description": "API для керування книгами"
    },
    "definitions": {
        "Book": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "example": "65f12345"},
                "title": {"type": "string", "example": "Кобзар"},
                "author": {"type": "string", "example": "Тарас Шевченко"},
                "description": {"type": "string", "example": "Збірка поетичних творів"},
                "status": {"type": "string", "enum": ["available", "borrowed"], "example": "available"},
                "year": {"type": "integer", "example": 1840}
            }
        },
        "BookInput": {
            "type": "object",
            "required": ["title", "author", "year"],
            "properties": {
                "title": {"type": "string", "example": "Назва книги"},
                "author": {"type": "string", "example": "Автор"},
                "description": {"type": "string", "example": "Короткий опис"},
                "status": {"type": "string", "enum": ["available", "borrowed"], "default": "available"},
                "year": {"type": "integer", "example": 2024}
            }
        }
    }
}

swagger = Swagger(app, template=template)

api.add_resource(BooksResource, "/books/")
api.add_resource(BookResource, "/books/<string:book_id>")

@app.route("/")
def root():
    return {"message": "Library API is running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)