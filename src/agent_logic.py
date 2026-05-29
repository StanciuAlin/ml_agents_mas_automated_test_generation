from utils import get_coder_agent_ollama, get_coder_agent_openai


# Schimbat implicit pe ollama pentru rulare locală pe M4
def get_coder_agent(api_choice="ollama"):
    if api_choice == "ollama":
        return get_coder_agent_ollama()
    else:
        return get_coder_agent_openai()


def generate_test_code(source_code: str):
    llm = get_coder_agent(api_choice="ollama")

    prompt = (
        "You are an expert Python QA Engineer.\n"
        "Your task is to write a pytest suite for the provided code.\n\n"
        "CRITICAL REQUIREMENTS:\n"
        "1. Do NOT copy or include the original functions in your response.\n"
        "2. Do NOT write any import statements. The framework will inject them dynamically.\n"
        "3. Carefully analyze the logic. If a branch is DEAD CODE (unreachable), do NOT expect it to be executed. Test the actual behavioral output of the function.\n"
        "4. Return ONLY valid, raw Python test functions (e.g., def test_...).\n"
        "5. Import all Python libraries needed for the test functions (e.g., import pytest).\n"
        "6. Do NOT wrap your response in markdown code blocks like ```python. Just return raw text code.\n\n"
        f"CODE TO TEST:\n{source_code}"
    )

    response = llm.invoke(prompt)
    return response.content


def refine_test_code(source_code: str, failed_test_code: str, error_log: str):
    llm = get_coder_agent(api_choice="ollama")

    prompt = (
        "You are an expert Python QA Engineer. Your previous pytest code failed execution.\n\n"
        f"ORIGINAL CODE UNDER TEST:\n{source_code}\n\n"
        f"YOUR PREVIOUS TEST CODE THAT FAILED:\n{failed_test_code}\n\n"
        f"PYTEST ERROR LOG (TRACEOUT):\n{error_log}\n\n"
        "CRITICAL INSTRUCTIONS FOR FIXING:\n"
        "1. Look closely at the AssertionError. You miscalculated the expected return value because of dead code or logic confusion. Correct your assertions to match what the original code actually outputs.\n"
        "2. Do NOT include the original functions or any import lines.\n"
        "3. Be sure that all functions from the imported code file are properly tested and cover all branches.\n"
        "4. Do NOT use markdown blocks like ```python. Return ONLY the raw, corrected python test functions.\n"
    )

    response = llm.invoke(prompt)
    return response.content
