import os
import requests

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

def get_default_llm():
    return HuggingFaceLLM()
