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
    Read the content of a code file located in the src folder.
    """
    # Construim calea relativă la folderul src
    file_path = os.path.join("src", file_name)

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
