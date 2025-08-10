# app/rag/retriever.py
import os
import faiss
import pickle
from typing import List
from sentence_transformers import SentenceTransformer

class FaissRetriever:
    def __init__(self, index_path: str, metadata_path: str):
        if not os.path.exists(index_path) or not os.path.exists(metadata_path):
            raise FileNotFoundError("FAISS index or metadata not found")

        # Load FAISS index
        self.index = faiss.read_index(index_path)

        # Load metadata (contains text chunks)
        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

        # Model embedding (must match the model used during indexing)
        self.embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Return the most relevant text chunks"""
        query_emb = self.embed_model.encode([query])
        distances, indices = self.index.search(query_emb, top_k)

        results = []
        for idx in indices[0]:
            if idx != -1:  # No match found
                results.append(self.metadata[idx])
        return results
