from utils import get_coder_agent_openai, get_coder_agent_ollama


def get_coder_agent(api_choice="openai"):
    if api_choice == "ollama":
        return get_coder_agent_ollama()
    else:
        return get_coder_agent_openai()


def generate_test_code(source_code: str):
    # Change to "ollama" if you want to use Ollama
    llm = get_coder_agent(api_choice="openai")

    prompt = (
        "You are an expert Python QA Engineer. "
        "Analyze the code for logic errors, dead code, or potential crashes. "
        "Write a pytest suite that covers all reachable branches and explicitly "
        "tests for identified edge cases and bugs. Be sure that all text "
        "that is generated and is not a valid Python code is commented out.\n\n"
        f"CODE:\n{source_code}"
    )

    response = llm.invoke(prompt)
    return response.content
