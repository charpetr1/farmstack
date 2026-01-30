# backend/api/items.py
import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import Request
from bson import ObjectId
from jose import JWTError, jwt

from schemas.item import ItemCreate, ItemUpdate, ItemOut, PaginatedItems
from db.repositories.items_repo import (
    create_item,
    get_items_for_list,
    update_item,
    delete_item,
)
from db.repositories.users_repo import get_user_by_id
from db.repositories.lists_repo import get_list_by_id
from db.mongo import items_collection

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

async def get_current_user(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_id(ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/list/{list_id}", response_model=PaginatedItems)
async def list_items(
    list_id: str,
    current_user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    list_doc = await get_list_by_id(ObjectId(list_id), current_user["_id"])
    if not list_doc:
        raise HTTPException(status_code=404, detail="List not found")

    skip = (page - 1) * page_size
    docs, total = await get_items_for_list(ObjectId(list_id), current_user["_id"], skip=skip, limit=page_size)
    items = [
        ItemOut(
            id=str(doc["_id"]),
            text=doc["text"],
            completed=doc["completed"],
            list_id=str(doc["list_id"]),
            user_id=str(doc["user_id"]),
            created_at=doc["created_at"],
        )
        for doc in docs
    ]
    return PaginatedItems(items=items, total=total, page=page, page_size=page_size)

@router.post("/list/{list_id}", response_model=ItemOut, status_code=201)
async def create_item_endpoint(list_id: str, payload: ItemCreate, current_user=Depends(get_current_user)):
    list_doc = await get_list_by_id(ObjectId(list_id), current_user["_id"])
    if not list_doc:
        raise HTTPException(status_code=404, detail="List not found")

    doc = await create_item(text=payload.text, list_id=ObjectId(list_id), user_id=current_user["_id"])
    return ItemOut(
        id=str(doc["_id"]),
        text=doc["text"],
        completed=doc["completed"],
        list_id=str(doc["list_id"]),
        user_id=str(doc["user_id"]),
        created_at=doc["created_at"],
    )

@router.patch("/{item_id}", response_model=ItemOut)
async def update_item_endpoint(item_id: str, payload: ItemUpdate, current_user=Depends(get_current_user)):
    data = {k: v for k, v in payload.dict().items() if v is not None}
    if not data:
        raise HTTPException(status_code=400, detail="No data to update")

    ok = await update_item(ObjectId(item_id), current_user["_id"], data)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")

    doc = await items_collection.find_one({"_id": ObjectId(item_id), "user_id": current_user["_id"]})
    return ItemOut(
        id=str(doc["_id"]),
        text=doc["text"],
        completed=doc["completed"],
        list_id=str(doc["list_id"]),
        user_id=str(doc["user_id"]),
        created_at=doc["created_at"],
    )

@router.delete("/{item_id}", status_code=204)
async def delete_item_endpoint(item_id: str, current_user=Depends(get_current_user)):
    ok = await delete_item(ObjectId(item_id), current_user["_id"])
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return None