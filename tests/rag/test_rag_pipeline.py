from app.rag.rag_pipeline import RAGPipeline
import os

class MockLLM:
    def generate(self, prompt: str) -> str:
        return f"[MOCK ANSWER] Prompt received:\n{prompt}"

def test_pipeline_runs_with_mock_llm():
    index_path = "data/index/mock_index.faiss"
    meta_path = "data/index/mock_index.pkl"

    assert os.path.exists(index_path), "FAISS index file missing"
    assert os.path.exists(meta_path), "Metadata file missing"

    pipeline = RAGPipeline(index_path, meta_path, llm_client=MockLLM())
    answer = pipeline.run("What is FastAPI?", top_k=2)

    assert isinstance(answer, str), "Pipeline output should be a string"
    assert "[MOCK ANSWER]" in answer, "Mock LLM response not detected"
    assert "FastAPI" in answer or "Prompt received" in answer, \
        "Expected keyword not found in answer"

    print("Pipeline test passed. Sample answer:", answer)
