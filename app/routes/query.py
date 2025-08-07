# app/routes/query.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def query_document():
    return {"message": "Query endpoint working!"}
