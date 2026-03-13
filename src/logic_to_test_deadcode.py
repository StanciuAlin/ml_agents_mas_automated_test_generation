# src/logic_to_test_deadcode.py

def analyze_user_access(age, has_id, is_blocked):
    if age >= 18 and has_id:
        if is_blocked:
            return "Access Denied"
        return "Access Granted"

    # Dead Code: age > 200 is already covered by the first condition, so this branch is never reached
    if age > 200:
        return "Special Access"

    return "Minimum requirements not met"


def calculate_average(numbers):
    # Edge case: empty list will cause a crash due to division by zero
    if not numbers:
        raise ValueError("List cannot be empty")
    total = sum(numbers)
    return total / len(numbers)
