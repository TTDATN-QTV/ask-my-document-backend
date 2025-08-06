# app/main.py
from fastapi import FastAPI
from app.routes import upload, query

def create_app() -> FastAPI:
    app = FastAPI(
        title="Ask My Document",
        description="Upload documents and ask questions using RAG pipeline.",
        version="0.1.0",
    )

    app.include_router(upload.router, prefix="/upload", tags=["Upload"])
    app.include_router(query.router, prefix="/query", tags=["Query"])

    return app

app = create_app()
