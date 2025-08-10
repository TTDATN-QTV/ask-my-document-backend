from app.rag.retriever import FaissRetriever
import os

def test_retriever_returns_results():
    index_path = "data/index/mock_index.faiss"
    meta_path = "data/index/mock_index.pkl"

    assert os.path.exists(index_path), "FAISS index file missing"
    assert os.path.exists(meta_path), "Metadata file missing"

    retriever = FaissRetriever(index_path, meta_path)
    results = retriever.retrieve("What is Python?", top_k=2)

    assert isinstance(results, list), "Results should be a list"
    assert len(results) > 0, "No results returned"
    assert any("Python" in r or "programming" in r for r in results), \
        "Relevant content not found in results"

    print("Retriever test passed. Sample results:", results)
