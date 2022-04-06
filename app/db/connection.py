from motor.motor_asyncio import AsyncIOMotorClient

from app import config


class Database:
    client: AsyncIOMotorClient


db = Database()

async def connect_to_mongodb():
    db.client = AsyncIOMotorClient(
        config.MONGO_URL,
    )


async def close_mongodb_connection():
    db.client.close()

async def get_db():
    return db.client[config.MONGO_DB]
