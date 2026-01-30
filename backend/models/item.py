# backend/models/item.py
from dataclasses import dataclass
from datetime import datetime
from bson import ObjectId

@dataclass
class Item:
    id: ObjectId
    text: str
    completed: bool
    list_id: ObjectId
    user_id: ObjectId
    created_at: datetime