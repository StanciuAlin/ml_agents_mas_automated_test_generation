import re
from agent_logic import generate_test_code, refine_test_code
from utils import get_system_specs, read_code_content, run_pytest_programmatically


def clean_markdown_code(text: str) -> str:
    text = text.strip()
    if text.startswith("```python"):
        pattern = r"```python\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
    return text.replace("```python", "").replace("```", "").strip()


def automate_test_generation_multi_agent():
    target_file = "evaluation/logic_to_test_deadcode.py"
    # target_file = "evaluation/logic_to_test_ok.py"

    code_to_test = read_code_content(target_file)
    if not code_to_test:
        print("❌ Could not read target file.")
        return

    specs = get_system_specs()
    print(f"Hardware detected: {specs['cpu']} with {specs['ram']} RAM")
    print("=" * 60)

    print("[AGENT 1: CODER] Generating initial test suite...")
    test_result = generate_test_code(code_to_test)
    test_code_clean = clean_markdown_code(test_result)

    max_iterations = 3
    current_iteration = 1
    success = False

    while current_iteration <= max_iterations:
        print(
            f"\n[ITERATION {current_iteration}/{max_iterations}] Saving and executing tests...")

        header = (
            "import sys\n"
            "import os\n"
            "sys.path.insert(0, os.path.abspath('evaluation'))\n"
            "from logic_to_test_deadcode import analyze_user_access, calculate_average\n\n"
        )

        final_file_content = header + test_code_clean

        with open("generated_test_output.py", "w", encoding="utf-8") as f:
            f.write(final_file_content)

        print("[AGENT 2: EXECUTOR] Running pytest on generated code...")
        is_ok, execution_logs = run_pytest_programmatically(
            "generated_test_output.py")

        if is_ok:
            print("✨ [SUCCESS] All generated tests passed successfully!")
            print(execution_logs)
            success = True
            break
        else:
            print(
                "[CRITIC ALERT] Test execution failed! Captured errors from pytest.")

            if current_iteration == max_iterations:
                print("❌ Reached maximum iterations. Stopping refinement.")
                break

            print("[AGENT 3: REFINER] Analyzing logs and fixing test code...")
            refined_result = refine_test_code(
                code_to_test, test_code_clean, execution_logs)
            test_code_clean = clean_markdown_code(refined_result)
            current_iteration += 1

    print("=" * 60)
    if success:
        print("Multi-Agent pipeline completed successfully! File saved: generated_test_output.py")
    else:
        print("Pipeline finished but tests are still failing. Review generated_test_output.py manually.")


if __name__ == "__main__":
    automate_test_generation_multi_agent()
