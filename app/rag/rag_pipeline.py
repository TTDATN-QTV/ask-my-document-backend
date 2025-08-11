# app/rag/rag_pipeline.py
from typing import List
from app.rag.retriever import FaissRetriever

class RAGPipeline:
    def __init__(self, index_path: str, metadata_path: str, llm_client):
        """
        llm_client: 1 object have method `generate(prompt: str) -> str`
        """
        self.retriever = FaissRetriever(index_path, metadata_path)
        self.llm_client = llm_client

    def run(self, query: str, top_k: int = 5) -> str:
        # 1. Get context from FAISS
        context_chunks: List[str] = self.retriever.retrieve(query, top_k=top_k)
        context_text = "\n".join(context_chunks)

        # 2. Construct prompt
        prompt = (
            "You are an assistant answering based on the provided documents.\n"
            "Context:\n"
            f"{context_text}\n\n"
            "Question:\n"
            f"{query}\n\n"
            "Answer:"
        )

        # 3. Call LLM
        answer = self.llm_client.generate(prompt)
        return answer

def generate_answer(query: str, index_path: str, metadata_path: str, llm_client, top_k: int = 5) -> str:
    """
    Utility function to create RAGPipeline and generate an answer.
    """
    pipeline = RAGPipeline(index_path, metadata_path, llm_client)
    return pipeline.run(query, top_k=top_k)
