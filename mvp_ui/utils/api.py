import requests

API_URL = "http://localhost:8000"

def upload_pdf(file):
    files = {"file": (file.name, file, "application/pdf")}
    return requests.post(f"{API_URL}/documents/upload", files=files)

def ask_question(query, top_k, file_id):
    payload = {"query": query, "top_k": top_k, "file_id": file_id}
    return requests.post(f"{API_URL}/documents/query", json=payload)