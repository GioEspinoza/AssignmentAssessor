from backend.aa_logic import is_in_range
from backend.aa_logic import is_positive_float
from backend.aa_logic import valid_due_date
from backend.aa_logic import valid_comp_date
from backend.aa_logic import round_down_to_two_decimals
from datetime import datetime


def test_in_range():
    assert is_in_range("3", 1, 5) == True
    assert is_in_range("1", 1, 5) == True
    assert is_in_range("0", 1, 5) == False
    assert is_in_range("6", 1, 5) == False
    assert is_positive_float("") == False
    assert is_positive_float("abc") == False


def test_pos_int():
    assert is_positive_float("5") == True
    assert is_positive_float("8") == True
    assert is_positive_float("-1") == False
    assert is_positive_float("-7") == False
    assert is_positive_float("") == False
    assert is_positive_float("abc") == False


def test_due():
    test_day = datetime.today().strftime("%m-%d-%Y")

    assert valid_due_date(test_day) == True
    assert valid_due_date("12-31-2099") == True
    assert valid_due_date("01-01-1010") == False


def test_comp():
    test_day = datetime.today().strftime("%m-%d-%Y")

    assert valid_comp_date(test_day) == True
    assert valid_comp_date("12-31-2099") == False
    assert valid_comp_date("01-01-2000") == True


def test_round():
    assert round_down_to_two_decimals(2.999) == 2.99
    assert round_down_to_two_decimals(3.325) == 3.32
    assert round_down_to_two_decimals(62.111) == 62.11
