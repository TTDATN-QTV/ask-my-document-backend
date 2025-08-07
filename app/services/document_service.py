import os
import uuid
from pathlib import Path

from app.utils.pdf_parser import extract_text_from_pdf
from app.rag.retriever import build_faiss_index

UPLOAD_DIR = Path("data/uploads")
INDEX_DIR = Path("data/index")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DIR.mkdir(parents=True, exist_ok=True)

def save_uploaded_file(file) -> Path:
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.pdf"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path

def process_and_index_document(file_path: Path):
    text = extract_text_from_pdf(file_path)
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    build_faiss_index(chunks, INDEX_DIR / f"{file_path.stem}.index")
