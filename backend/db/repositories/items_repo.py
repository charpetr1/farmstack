# backend/db/repositories/items_repo.py
from datetime import datetime
from bson import ObjectId
from db.mongo import items_collection

async def create_item(text: str, list_id: ObjectId, user_id: ObjectId):
    doc = {
        "text": text,
        "completed": False,
        "list_id": list_id,
        "user_id": user_id,
        "created_at": datetime.utcnow(),
    }
    result = await items_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc

async def get_items_for_list(list_id: ObjectId, user_id: ObjectId, skip: int = 0, limit: int = 20):
    cursor = items_collection.find({"list_id": list_id, "user_id": user_id}).skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    total = await items_collection.count_documents({"list_id": list_id, "user_id": user_id})
    return items, total

async def update_item(item_id: ObjectId, user_id: ObjectId, data: dict):
    result = await items_collection.update_one(
        {"_id": item_id, "user_id": user_id},
        {"$set": data},
    )
    return result.modified_count == 1

async def delete_item(item_id: ObjectId, user_id: ObjectId):
    result = await items_collection.delete_one({"_id": item_id, "user_id": user_id})
    return result.deleted_count == 1
