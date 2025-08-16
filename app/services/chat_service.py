# app/services/chat_service.py
from app.rag.retriever import get_relevant_context_for_file
from app.rag.rag_pipeline import generate_answer

def handle_query(user_query: str, top_k: int = 3, file_id: str = None) -> dict:
    """
    Process a user's query:
    1. Retrieve relevant context from FAISS index
    2. Pass context + query to LLM for generating answer
    """

    if not user_query.strip():
        raise ValueError("Query cannot be empty.")
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")
    if not file_id:
        raise ValueError("file_id is required.")

    context_docs = get_relevant_context_for_file(user_query, file_id, top_k=top_k)
    answer = generate_answer(user_query, context_docs)

    return {
        "query": user_query,
        "context": context_docs,
        "answer": answer
    }
