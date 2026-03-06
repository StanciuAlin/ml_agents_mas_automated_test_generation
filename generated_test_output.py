
import pytest

def calculate_discount(price, discount_percent):
    if not 0 <= discount_percent <= 100:
        raise ValueError("Invalid discount")
    return price * (1 - discount_percent / 100)


def test_calculate_discount_valid_input():
    assert calculate_discount(100, 10) == 90
    assert calculate_discount(200, 50) == 100
    assert calculate_discount(50, 0) == 50

def test_calculate_discount_invalid_discount_percent():
    with pytest.raises(ValueError):
        calculate_discount(100, 105)
    with pytest.raises(ValueError):
        calculate_discount(100, -5)

def test_calculate_discount_zero_price():
    assert calculate_discount(0, 10) == 0

def test_calculate_discount_full_discount():
    assert calculate_discount(100, 100) == 0
