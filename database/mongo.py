from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = "mongodb://mongo:27017"

async def get_books_collection():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["library"]
    return db["books"]