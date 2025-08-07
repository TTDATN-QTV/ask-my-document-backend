# app/routes/upload.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def upload_document():
    return {"message": "Upload endpoint working!"}
