from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings import settings

client = AsyncIOMotorClient(settings.MONGO_DB_URL)
db = client[settings.MONGO_DB_NAME]
