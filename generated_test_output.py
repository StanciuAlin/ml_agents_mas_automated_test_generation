import sys
import os
sys.path.insert(0, os.path.abspath('evaluation'))
from logic_to_test_deadcode import analyze_user_access, calculate_average

def test_analyze_user_access_denied():
    assert analyze_user_access(17, True, False) == "Minimum requirements not met"
    assert analyze_user_access(20, False, False) == "Minimum requirements not met"
    assert analyze_user_access(20, True, True) == "Access Denied"

def test_calculate_average_empty_list():
    with pytest.raises(ValueError):
        calculate_average([])

def test_calculate_average_single_element():
    assert calculate_average([5]) == 5

def test_calculate_average_multiple_elements():
    assert calculate_average([1, 2, 3, 4, 5]) == 3.0