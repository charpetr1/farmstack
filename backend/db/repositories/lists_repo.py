# backend/db/repositories/lists_repo.py
from datetime import datetime
from bson import ObjectId
from db.mongo import lists_collection

async def create_list(name: str, user_id: ObjectId):
    doc = {
        "name": name,
        "user_id": user_id,
        "created_at": datetime.utcnow(),
    }
    result = await lists_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc

async def get_lists_for_user(user_id: ObjectId, skip: int = 0, limit: int = 20):
    cursor = lists_collection.find({"user_id": user_id}).skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    total = await lists_collection.count_documents({"user_id": user_id})
    return items, total

async def get_list_by_id(list_id: ObjectId, user_id: ObjectId):
    return await lists_collection.find_one({"_id": list_id, "user_id": user_id})

async def delete_list(list_id: ObjectId, user_id: ObjectId):
    result = await lists_collection.delete_one({"_id": list_id, "user_id": user_id})
    return result.deleted_count == 1