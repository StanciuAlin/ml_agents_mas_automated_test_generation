import re
from agent_logic import generate_test_code, refine_test_code
from utils import get_system_specs, read_code_content, run_pytest_programmatically


def clean_markdown_code(text: str) -> str:
    """Curăță tag-urile de tip markdown doar dacă ele există în output."""
    text = text.strip()
    if text.startswith("```python"):
        pattern = r"```python\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
    return text.replace("```python", "").replace("```", "").strip()


def automate_test_generation_multi_agent():
    # Definim fișierul țintă din folderul evaluation
    target_file = "evaluation/logic_to_test_deadcode.py"
    code_to_test = read_code_content(target_file)
    if not code_to_test:
        print("❌ Could not read target file.")
        return

    # Detectare și afișare specificații hardware locale (M4 Mac Mini)
    specs = get_system_specs()
    print(f"🖥️ Hardware detected: {specs['cpu']} with {specs['ram']} RAM")
    print("=" * 60)

    # 🚀 PASUL 1: Agentul 1 (Coder) generează prima versiune a suitei de teste
    print("🚀 [AGENT 1: CODER] Generating initial test suite...")
    test_result = generate_test_code(code_to_test)
    test_code_clean = clean_markdown_code(test_result)

    max_iterations = 3
    current_iteration = 1
    success = False

    while current_iteration <= max_iterations:
        print(
            f"\n🔄 [ITERATION {current_iteration}/{max_iterations}] Saving and executing tests...")

        # Injectăm dinamic calea către folderul evaluation în sys.path al fișierului generat.
        # Acest pas garantează că pytest va găsi modulul indiferent de halucinațiile de import ale LLM-ului.
        header = (
            "import sys\n"
            "import os\n"
            "sys.path.insert(0, os.path.abspath('evaluation'))\n"
            "from logic_to_test_deadcode import analyze_user_access, calculate_average\n\n"
        )

        final_file_content = header + test_code_clean

        # Salvăm codul complet în fișierul final pentru execuție
        with open("generated_test_output.py", "w", encoding="utf-8") as f:
            f.write(final_file_content)

        # 🕵️‍♂️ PASUL 2: Agentul 2 (Executor/Critic) rulează testele programatic prin pytest
        print("🕵️‍♂️ [AGENT 2: EXECUTOR] Running pytest on generated code...")
        is_ok, execution_logs = run_pytest_programmatically(
            "generated_test_output.py")

        if is_ok:
            print("✨ [SUCCESS] All generated tests passed successfully!")
            print(execution_logs)
            success = True
            break
        else:
            print(
                "⚠️ [CRITIC ALERT] Test execution failed! Captured errors from pytest.")

            if current_iteration == max_iterations:
                print("❌ Reached maximum iterations. Stopping refinement.")
                break

            # 🔧 PASUL 3: Agentul 3 (Refiner) analizează traceback-ul și corectează codul
            print("🔧 [AGENT 3: REFINER] Analyzing logs and fixing test code...")
            refined_result = refine_test_code(
                code_to_test, test_code_clean, execution_logs)
            test_code_clean = clean_markdown_code(refined_result)
            current_iteration += 1

    print("=" * 60)
    if success:
        print("🎉 Multi-Agent pipeline completed successfully! File saved: generated_test_output.py")
    else:
        print("⚠️ Pipeline finished but tests are still failing. Review generated_test_output.py manually.")


if __name__ == "__main__":
    automate_test_generation_multi_agent()
