from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import psutil
import subprocess
import platform
import os


def get_coder_agent_ollama():
    # Optimized for Mac M4: temperature 0 for precision in code
    # The model "qwen2.5-coder:7b" is designed for coding tasks, providing better code generation capabilities.
    return ChatOllama(
        model="qwen2.5-coder:7b",
        temperature=0
    )


def get_coder_agent_openai():
    return ChatOpenAI(
        base_url="http://127.0.0.1:1234/v1",  # Address from LM Studio
        api_key="lm-studio",
        model="qwen2.5-coder-7b-instruct",  # Model name from LM Studio
        temperature=0
    )


def read_code_content(file_name):
    """
    Citeste continutul unui fisier de cod raportat la radacina proiectului.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))  # folderul src
    project_root = os.path.dirname(current_dir)  # folderul ml_agents_project

    # Daca ai trimis deja o cale care incepe cu evaluation, o lipim direct de radacina
    if file_name.startswith("evaluation"):
        file_path = os.path.join(project_root, file_name)
    else:
        # Altfel, presupunem ca e in src
        file_path = os.path.join(current_dir, file_name)

    try:
        if not os.path.exists(file_path):
            print(f"[WARNING]: File {file_path} not found.")
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"[ERROR]: Error reading file {file_path}: {e}")
        return None


def get_system_specs():
    try:
        cpu_model = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
    except:
        cpu_model = platform.processor()

    # Get total RAM in bytes and convert to GB
    total_ram_bytes = psutil.virtual_memory().total
    total_ram_gb = round(total_ram_bytes / (1024 ** 3))

    return {
        "cpu": cpu_model,
        "ram": f"{total_ram_gb} GB"
    }


def run_pytest_programmatically(test_file_path="generated_test_output.py"):
    """
    Agentul 2 (Critic/Executor): Execută fișierul de test generat și returnează (success_boolean, logs)
    """
    try:
        # Rulăm pytest direct pe fișierul generat și capturăm rezultatul text
        result = subprocess.run(
            ["uv", "run", "pytest", test_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            return True, "All tests passed successfully!"
        else:
            # Combinăm stdout și stderr pentru a oferi context maxim agentului Refiner
            return False, result.stdout + "\n" + result.stderr
    except Exception as e:
        return False, f"Execution failed due to environment error: {str(e)}"
