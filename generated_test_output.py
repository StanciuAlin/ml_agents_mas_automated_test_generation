import sys
import os
sys.path.insert(0, os.path.abspath('evaluation'))
from logic_to_test_deadcode import analyze_user_access, calculate_average

def test_analyze_user_access_denied():
    assert analyze_user_access(17, True, False) == "Minimum requirements not met"
    assert analyze_user_access(20, False, False) == "Minimum requirements not met"
    assert analyze_user_access(20, True, True) == "Access Denied"