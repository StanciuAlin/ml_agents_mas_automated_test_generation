# Multi-Agent Systems for Automated Test Generation

**Topic:** Using Multi-Agent Systems (MAS) for Automated Test Generation (Based on TestGenEval)

## 1. Project Objective

The goal of this project is to design, implement, and evaluate a **Multi-Agent System** capable of
generating high-quality unit tests for Python codebases where different specialized agents
collaborate to **write**, **execute**, and **refine** test cases to maximize **code coverage** and minimize **hallucinations**.

## 2. Methodology & Architecture (Local-First Approach)

To ensure data privacy and cost-efficiency, the project will be developed and executed **locally** on **Apple Silicon (M4)** hardware using:

- **Inference Engine:** `Ollama`.
- **Local LLMs:** `Qwen 2.5 Coder 7B` (specialized for programming) and `Llama 3.1 8B`.
- **Orchestration:** `LangGraph` to manage agent states and communication.
- **Dataset:** `TestGenEval`, focusing on repository-level unit test generation.

## 3. Proposed Multi-Agent Workflow

- **The Architect Agent:** Analyzes the source code and defines the test requirements.
- **The Coder Agent:** Generates the Python unit tests (using pytest or unittest).
- **The Executor Agent (The "Critic"):** Runs the generated tests in a sandboxed environment. If the tests fail, it captures the traceback.
- **The Refiner Agent:** Receives the error logs and iterates on the code until the tests pass.

## 4. Evaluation Metrics

- **Pass Rate:** Percentage of generated tests that execute without errors.
- **Code Coverage:** Using coverage.py to measure how much of the source code is exercised.
- **Comparative Analysis:** Performance of a **Single-Agent (Baseline)** vs. the **Multi-Agent System**.
