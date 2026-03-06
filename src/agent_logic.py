from langchain_ollama import ChatOllama


def get_coder_agent():
    # Optimized for Mac M4: temperature 0 for precision in code
    # The model "qwen2.5-coder:7b" is designed for coding tasks, providing better code generation capabilities.
    return ChatOllama(
        model="qwen2.5-coder:7b",
        temperature=0
    )


def generate_test_code(source_code: str):
    llm = get_coder_agent()
    prompt = (
        "You are an expert Python QA Engineer. "
        "Write a pytest suite for the following code. "
        "Return ONLY the python code, no explanations.\n\n"
        f"CODE:\n{source_code}"
    )
    response = llm.invoke(prompt)
    return response.content
