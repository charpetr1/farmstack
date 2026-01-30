# backend/db/indexes.py

from db.mongo import users_collection, lists_collection, items_collection

async def create_indexes():
    # Users
    await users_collection.create_index("email", unique=True)

    # Lists
    await lists_collection.create_index("user_id")

    # Items
    await items_collection.create_index("list_id")
    await items_collection.create_index("user_id")
