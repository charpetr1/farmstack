from fastapi import FastAPI

from db.indexes import create_indexes
from api import auth_router, lists_router, items_router

app = FastAPI(title="farmstack API")

# ============================
# API ROUTES
# ============================
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(lists_router, prefix="/api/lists", tags=["lists"])
app.include_router(items_router, prefix="/api/items", tags=["items"])

# ============================
# HEALTHCHECK
# ============================
@app.get("/health")
def health():
    return {"status": "ok"}

# ============================
# CREATE INDEXES
# ============================
@app.on_event("startup")
async def startup_event():
    await create_indexes()
