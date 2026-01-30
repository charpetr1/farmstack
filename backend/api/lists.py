# backend/api/lists.py
import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from jose import JWTError, jwt
from fastapi import Request

from schemas.list import ListCreate, ListOut, PaginatedLists
from db.repositories.lists_repo import (
    create_list,
    get_lists_for_user,
    get_list_by_id,
    delete_list,
)
from db.repositories.users_repo import get_user_by_id

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

@router.get("/", response_model=PaginatedLists)
async def list_lists(
    current_user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    skip = (page - 1) * page_size
    docs, total = await get_lists_for_user(current_user["_id"], skip=skip, limit=page_size)
    items = [
        ListOut(
            id=str(doc["_id"]),
            name=doc["name"],
            user_id=str(doc["user_id"]),
            created_at=doc["created_at"],
        )
        for doc in docs
    ]
    return PaginatedLists(items=items, total=total, page=page, page_size=page_size)

@router.post("/", response_model=ListOut, status_code=201)
async def create_list_endpoint(payload: ListCreate, current_user=Depends(get_current_user)):
    doc = await create_list(name=payload.name, user_id=current_user["_id"])
    return ListOut(
        id=str(doc["_id"]),
        name=doc["name"],
        user_id=str(doc["user_id"]),
        created_at=doc["created_at"],
    )

@router.delete("/{list_id}", status_code=204)
async def delete_list_endpoint(list_id: str, current_user=Depends(get_current_user)):
    ok = await delete_list(ObjectId(list_id), current_user["_id"])
    if not ok:
        raise HTTPException(status_code=404, detail="List not found")
    return None