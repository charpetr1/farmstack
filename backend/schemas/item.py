# backend/schemas/item.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ItemBase(BaseModel):
    text: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None

class ItemOut(BaseModel):
    id: str
    text: str
    completed: bool
    list_id: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class PaginatedItems(BaseModel):
    items: List[ItemOut]
    total: int
    page: int
    page_size: int