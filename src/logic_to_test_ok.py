# src/logic_to_test_ok.py

def calculate_discount(price, discount_percent):
    if not 0 <= discount_percent <= 100:
        raise ValueError("Invalid discount")
    return price * (1 - discount_percent / 100)
