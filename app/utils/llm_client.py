class MockLLM:
    """
    Mock LLM client for testing/demo.
    """
    def generate(self, prompt: str) -> str:
        # Trả về prompt kèm nhãn mock để dễ nhận biết trong test
        return f"[MOCK LLM] Prompt received:\n{prompt}"

def get_default_llm():
    """
    Returns the default LLM client (mock for MVP/demo).
    """
    return MockLLM()