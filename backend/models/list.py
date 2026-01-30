# backend/models/list.py
from dataclasses import dataclass
from datetime import datetime
from bson import ObjectId

@dataclass
class TodoList:
    id: ObjectId
    name: str
    user_id: ObjectId
    created_at: datetime