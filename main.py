from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from pymongo import MongoClient
import os
from app.api.book_resource import BookListResource, BookResource

app = Flask(__name__)
api = Api(app)

swagger = Swagger(app)


MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_admin:password@mongo_db:27017")
client = MongoClient(MONGO_URL)
db = client.books


api.add_resource(BookListResource, '/books', resource_class_args=[db])
api.add_resource(BookResource, '/books/<string:book_id>', resource_class_args=[db])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)