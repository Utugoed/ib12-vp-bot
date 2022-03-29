from motor.motor_asyncio import AsyncIOMotorClient

from app.config import MONGO_DB, MONGO_URL


class Database:
    client: AsyncIOMotorClient


db = Database()
db.client = AsyncIOMotorClient(
        MONGO_URL,
    )

async def get_db():
    return db.client[MONGO_DB]
