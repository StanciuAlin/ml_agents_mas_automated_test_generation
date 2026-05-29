from agent_logic import generate_test_code
import pandas as pd
import os
import sys
import time

# Adăugăm rădăcina proiectului în path pentru importuri
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_evaluation(num_samples=1):
    DATA_PATH = "evaluation/testgeneval/data/test-00000-of-00001.parquet"
    INPUT_CODE_DIR = "evaluation/input_python_code"
    GENERATED_TESTS_DIR = "evaluation/generated_tests"

    if not os.path.exists(INPUT_CODE_DIR):
        os.makedirs(INPUT_CODE_DIR)
    if not os.path.exists(GENERATED_TESTS_DIR):
        os.makedirs(GENERATED_TESTS_DIR)

    if not os.path.exists(DATA_PATH):
        print(f"❌ Nu am găsit dataset-ul la {DATA_PATH}")
        return

    df = pd.read_parquet(DATA_PATH)
    print(f"✅ Loaded dataset. Processing the first {num_samples} samples...")

    total_start = time.time()

    for i in range(num_samples):
        row = df.iloc[i]
        task_id = str(row['instance_id']).replace("/", "_").replace(".", "_")
        source_code = row['code_src']

        # DEFINIM NUMELE MODULULUI AICI (înainte de utilizare)
        source_module_name = f"src_{task_id}"

        print(f"\n[{i+1}/{num_samples}] Task: {task_id}")
        task_start = time.time()

        # 1. Salvăm codul sursă
        source_file_path = os.path.join(
            INPUT_CODE_DIR, f"{source_module_name}.py")
        with open(source_file_path, "w") as f:
            f.write(source_code)

        # 2. Generăm testele
        print(f"🤖 Generating tests...")
        try:
            generated_tests_raw = generate_test_code(source_code)

            # 3. Curățare și corectare importuri
            generated_tests = generated_tests_raw.replace(
                "```python", "").replace("```", "").strip()

            # Acum source_module_name este garantat să existe
            generated_tests = generated_tests.replace(
                "from your_module", f"from {source_module_name}")
            generated_tests = generated_tests.replace(
                "from module", f"from {source_module_name}")

            # 4. Salvăm testele
            test_file_path = os.path.join(
                GENERATED_TESTS_DIR, f"test_{task_id}.py")
            with open(test_file_path, "w") as f:
                f.write("import pytest\nimport sys\nimport os\n")
                input_abs_path = os.path.abspath(INPUT_CODE_DIR)
                f.write(f"sys.path.append('{input_abs_path}')\n\n")
                f.write(generated_tests)

            duration = time.time() - task_start
            print(f"⏱️ Timp execuție task: {duration:.2f}s")
            print(f"✨ Saved Test: {test_file_path}")

        except Exception as e:
            print(f"❌ Eroare la procesarea task-ului {task_id}: {e}")

    total_duration = time.time() - total_start
    print(f"\nGATA! Timp total: {total_duration:.2f}s")


if __name__ == "__main__":
    run_evaluation(1)
