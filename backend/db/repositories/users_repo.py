# backend/db/repositories/users_repo.py
from datetime import datetime
from bson import ObjectId
from db.mongo import users_collection

async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

async def get_user_by_id(user_id: ObjectId):
    return await users_collection.find_one({"_id": user_id})

async def create_user(email: str, hashed_password: str):
    doc = {
        "email": email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
    }
    result = await users_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc