from pathlib import Path
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
