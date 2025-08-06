# app/routes/upload.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def dummy_upload():
    return {"msg": "Upload route placeholder"}
