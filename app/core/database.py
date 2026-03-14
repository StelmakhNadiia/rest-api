import motor.motor_asyncio
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_admin:password@mongo_db:27017")

async def get_db():
    # Створюємо клієнт прямо тут
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    return client.books