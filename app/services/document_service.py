# app/services/document_service.py
from pathlib import Path
from fastapi import UploadFile
import uuid

from app.config import UPLOAD_DIR, INDEX_DIR
from app.utils.pdf_parser import extract_text
from app.rag.retriever import build_faiss_index

def save_upload_file(file: UploadFile, upload_dir: Path = UPLOAD_DIR) -> Path:
    """
    Save the uploaded file to the given upload_dir with original filename.
    Automatically uses separate folders for prod/test depending on APP_ENV.
    """
    file_id = str(uuid.uuid4())
    ext = Path(file.filename).suffix
    file_path = upload_dir / f"{file_id}{ext}"
    upload_dir.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path, file_id

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

def process_and_index_document(file_path: Path, file_id: str):
    """
    Extract text from PDF, split into chunks, and build FAISS index.
    Index/metadata are saved using file_id.
    """
    text = extract_text(file_path)

    if not text or not text.strip():
        raise ValueError("Empty or no text extracted from PDF.")

    chunks = split_text_to_docs(text)
    if not chunks or all(not c.strip() for c in chunks):
        raise ValueError("Empty or no text extracted from PDF.")

    index_path = INDEX_DIR / f"{file_id}.faiss"
    metadata_path = INDEX_DIR / f"{file_id}.pkl"
    create_faiss_index_and_save(chunks, index_path, metadata_path)
    return index_path, metadata_path, chunks
