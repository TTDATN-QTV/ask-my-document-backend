import os
import requests
from langchain.llms import CTransformers
from transformers import AutoTokenizer

class HuggingFaceLLM:
    def __init__(self, model="deepset/roberta-base-squad2"):
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self.token = os.getenv("HF_TOKEN")
        if not self.token:
            raise RuntimeError("HF_TOKEN environment variable not set.")

    def generate(self, question: str, context_docs: list[str]) -> str:
        headers = {"Authorization": f"Bearer {self.token}"}
        context_text = "\n".join(context_docs)
        payload = {
            "inputs": {
                "question": question,
                "context": context_text
            }
        } 
        response = requests.post(self.api_url, headers=headers, json=payload)
        try:
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            return f"[HF ERROR] {str(e)} | Raw response: {response.text}"

        if isinstance(result, dict) and "answer" in result:
            return result["answer"]
        elif isinstance(result, dict) and "error" in result:
            return f"[HF ERROR] {result['error']}"
        else:
            return str(result)

class LocalLLM:
    def __init__(self, model_path="models/llama-2-7b-chat.ggmlv3.q4_1.bin"):
        self.llm = CTransformers(
            model=model_path,
            model_type="llama",
            config={
                "max_new_tokens": 256,
                "temperature": 0.01
            }
        )

    def generate(self, question: str, context_docs: list[str]) -> str:
        context_text = truncate_context(context_docs, question, max_tokens=512)
        prompt = (
            "Answer the user's question **only** using the provided context below.\n"
            "If the answer is not in the context, reply \"I don't know\".\n"
            f"Context: {context_text}\n"
            f"Question: {question}\n"
            "Helpful answer:"
        )
        return self.llm(prompt)

tokenizer = AutoTokenizer.from_pretrained("hf-internal-testing/llama-tokenizer")

def truncate_context(context_docs, question, max_tokens=512):
    prompt_template = (
        "Use the following pieces of information to answer the user's question.\n"
        "If you don't know the answer, just say that you don't know, don't try to make up an answer.\n"
        "Context: {context}\n"
        "Question: {question}\n"
        "Only return the helpful answer below and nothing else.\n"
        "Helpful answer:"
    )
    context = ""
    for doc in context_docs:
        temp_context = context + doc + "\n"
        prompt = prompt_template.format(context=temp_context, question=question)
        num_tokens = len(tokenizer.encode(prompt))
        if num_tokens > max_tokens:
            break
        context = temp_context
    return context

def get_default_llm():
    return LocalLLM()
