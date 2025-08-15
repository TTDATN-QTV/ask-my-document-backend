from app.utils.llm_client import get_default_llm

def test_mock_llm_generate():
    llm = get_default_llm()
    prompt = "Hello, what is Python?"
    result = llm.generate(prompt)
    assert "[MOCK LLM]" in result
    assert "Python" in result or "Prompt received" in result