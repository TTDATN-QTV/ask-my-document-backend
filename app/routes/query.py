# app/routes/query.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def dummy_query():
    return {"msg": "Query route placeholder"}
