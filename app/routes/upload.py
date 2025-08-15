# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import document_service

# Try to import PdfReadError from either pypdf or PyPDF2; fall back to a dummy class.
try:
    from pypdf.errors import PdfReadError  # type: ignore
except Exception:
    try:
        from PyPDF2.errors import PdfReadError  # type: ignore
    except Exception:
        class PdfReadError(Exception):  # fallback
            pass

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf"}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Validate extension
    ext = file.filename.lower().rsplit(".", 1)
    if len(ext) < 2 or f".{ext[1]}" not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    try:
        # Save and process
        saved_path = document_service.save_upload_file(file)
        index_path, metadata_path, chunks = document_service.process_and_index_document(saved_path)

        # If downstream returns empty chunks
        if not chunks or all(not c.strip() for c in chunks):
            raise HTTPException(status_code=422, detail="Empty or no text extracted from PDF.")

        return {
            "status": "success",
            "filename": file.filename,
            "chunks": len(chunks),
            "index_path": str(index_path),
            "metadata_path": str(metadata_path),
            "message": "File uploaded and indexed successfully."
        }

    # Mapping business logic/PDF reading errors to 422 for test pass instead of 500
    except ValueError as e:
        # Example: "No text found in document"
        raise HTTPException(status_code=422, detail=str(e))
    except PdfReadError as e:
        raise HTTPException(status_code=422, detail=f"Invalid or unreadable PDF: {e}")
    except HTTPException:
        raise
    except Exception as e:
        # "Unexpected error occurred" => 500
        raise HTTPException(status_code=500, detail=str(e))
