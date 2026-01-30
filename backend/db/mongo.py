# backend/db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client.get_default_database()


users_collection = db["users"]
lists_collection = db["lists"]
items_collection = db["items"]


