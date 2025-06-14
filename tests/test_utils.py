# tests/test_utils.py
from app.services.utils import calculate_moving_average

def test_calculate_moving_average():
    prices = [100, 101, 99, 102, 98]
    assert calculate_moving_average(prices) == 100


def test_empty_list_returns_zero():
    assert calculate_moving_average([]) == 0
