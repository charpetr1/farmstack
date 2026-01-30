# backend/schemas/list.py
from pydantic import BaseModel
from datetime import datetime
from typing import List

class ListBase(BaseModel):
    name: str

class ListCreate(ListBase):
    pass

class ListOut(BaseModel):
    id: str
    name: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class PaginatedLists(BaseModel):
    items: List[ListOut]
    total: int
    page: int
    page_size: int
