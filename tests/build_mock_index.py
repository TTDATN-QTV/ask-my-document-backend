import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

INDEX_DIR = "data/index"
FAISS_PATH = os.path.join(INDEX_DIR, "mock_index.faiss")
META_PATH = os.path.join(INDEX_DIR, "mock_index.pkl")

def build_mock_index():
    os.makedirs(INDEX_DIR, exist_ok=True)

    docs = [
        "Python is a programming language.",
        "FastAPI is a modern, fast web framework for Python.",
        "FAISS is a library for efficient similarity search.",
        "Streamlit is used for building data apps quickly.",
    ]

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    with open(META_PATH, "wb") as f:
        pickle.dump(docs, f)

    faiss.write_index(index, FAISS_PATH)
    print(f"Mock index saved to {FAISS_PATH}")
    print(f"Metadata saved to {META_PATH}")

if __name__ == "__main__":
    build_mock_index()
