# app/services/document_service.py
from pathlib import Path
from fastapi import UploadFile

from app.config import UPLOAD_DIR, INDEX_DIR
from app.utils.pdf_parser import extract_text
from app.rag.retriever import build_faiss_index

def save_upload_file(file: UploadFile, upload_dir: Path = UPLOAD_DIR) -> Path:
    """
    Save the uploaded file to the given upload_dir with original filename.
    Automatically uses separate folders for prod/test depending on APP_ENV.
    """
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path

def split_text_to_docs(text: str, chunk_size: int = 500) -> list[str]:
    """
    Split text into smaller chunks (docs) of max length chunk_size.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def create_faiss_index_and_save(docs: list[str], index_path: Path, metadata_path: Path):
    """
    Build FAISS index from docs and save both index and metadata to disk.
    """
    build_faiss_index(docs, index_path, metadata_path)

def process_and_index_document(file_path: Path):
    """
    Extract text from PDF, split into chunks, and build FAISS index.
    Saves index/metadata into environment-specific INDEX_DIR.
    Handles unreadable/empty PDFs gracefully.
    """
    try:
        text = extract_text(file_path)
    except Exception:
        # Catch all PDF reading errors and return business logic message
        raise ValueError("Empty or no text extracted from PDF.")

    if not text or not text.strip():
        raise ValueError("Empty or no text extracted from PDF.")

    chunks = split_text_to_docs(text)
    if not chunks or all(not c.strip() for c in chunks):
        raise ValueError("Empty or no text extracted from PDF.")

    index_path = INDEX_DIR / f"{file_path.stem}.faiss"
    metadata_path = INDEX_DIR / f"{file_path.stem}.pkl"
    create_faiss_index_and_save(chunks, index_path, metadata_path)
    return index_path, metadata_path, chunks
