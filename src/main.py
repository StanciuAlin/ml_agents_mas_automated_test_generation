from agent_logic import generate_test_code


def run_experiment():
    # An example function to test - in a real scenario, this would be your actual codebase
    code_to_test = """
        def calculate_discount(price, discount_percent):
            if not 0 <= discount_percent <= 100:
                raise ValueError("Invalid discount")
            return price * (1 - discount_percent / 100)
    """

    print("Generating tests locally on M4...")
    test_result = generate_test_code(code_to_test)

    print("\n--- GENERATED TEST ---")
    print(test_result)

    # Save to a temporary file for syntax checking
    with open("generated_test_output.py", "w") as f:
        f.write(test_result)
    print("\nResult saved to generated_test_output.py")


if __name__ == "__main__":
    run_experiment()
