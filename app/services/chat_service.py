# app/services/chat_service.py
from app.rag.retriever import get_relevant_context_for_file
from app.rag.rag_pipeline import generate_answer

def handle_query(user_query: str, top_k: int = 2, file_ids: list = None) -> dict:
    """
    Process a user's query:
    1. Retrieve relevant context from FAISS index
    2. Pass context + query to LLM for generating answer
    """

    if not user_query.strip():
        raise ValueError("Query cannot be empty.")
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")
    if not file_ids or not isinstance(file_ids, list):
        raise ValueError("file_ids is required and must be a list.")

    # Get context for all file_ids but limit to top_k
    context_docs = []
    for file_id in file_ids:
        context_docs += get_relevant_context_for_file(user_query, file_id, top_k=top_k)
    # Limit total number of context_docs
    context_docs = context_docs[:top_k]

    answer = generate_answer(user_query, [c["content"] for c in context_docs])

    return {
        "query": user_query,
        "context": context_docs,
        "answer": answer
    }
