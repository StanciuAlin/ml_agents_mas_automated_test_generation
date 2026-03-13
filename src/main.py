from agent_logic import generate_test_code
from utils import get_system_specs, read_code_content


def automate_test_generation():

    target_file = "logic_to_test_deadcode.py"
    code_to_test = read_code_content(target_file)
    if not code_to_test:
        return

    specs = get_system_specs()
    print(f"Hardware detected: {specs['cpu']} with {specs['ram']} RAM")

    test_result = generate_test_code(code_to_test)

    print("\n--- GENERATED TEST ---")
    print(test_result)

    # Clean up code block markers if present
    test_result = test_result.strip("```python").strip("```")

    # Save to a temporary file for syntax checking
    with open("generated_test_output.py", "w") as f:
        f.write(test_result)
    print("\nResult saved to generated_test_output.py")


if __name__ == "__main__":
    automate_test_generation()
