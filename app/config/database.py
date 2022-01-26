import motor.motor_asyncio

from app.config.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DB_URL)
db = client[settings.MONGO_DB_DATABASE]



