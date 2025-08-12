# app/rag/retriever.py
import os
from pathlib import Path
import faiss
import pickle
from typing import List
from sentence_transformers import SentenceTransformer

# ==== Config: dynamic data folder based on APP_ENV ====
APP_ENV = os.getenv("APP_ENV", "dev")  # default dev
DATA_DIR = Path(f"data_{APP_ENV}") if APP_ENV != "dev" else Path("data")
INDEX_DIR = DATA_DIR / "index"

class FaissRetriever:
    def __init__(self, index_path: Path, metadata_path: Path):
        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError(f"FAISS index or metadata not found: {index_path}, {metadata_path}")

        self.index = faiss.read_index(str(index_path))

        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

        self.embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        query_emb = self.embed_model.encode([query])
        distances, indices = self.index.search(query_emb, top_k)

        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.metadata[idx])
        return results


def build_faiss_index(docs: list[str], index_path: Path, metadata_path: Path):
    index_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(docs)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, str(index_path))

    with open(metadata_path, "wb") as f:
        pickle.dump(docs, f)


# ==== Default mock paths for quick retrieval ====
INDEX_PATH = INDEX_DIR / "mock_index.faiss"
META_PATH = INDEX_DIR / "mock_index.pkl"

def get_relevant_context(query: str, top_k: int = 5):
    retriever = FaissRetriever(INDEX_PATH, META_PATH)
    return retriever.retrieve(query, top_k)
