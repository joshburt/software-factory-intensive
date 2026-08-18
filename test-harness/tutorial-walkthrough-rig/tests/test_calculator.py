"""Tests for the calculator module."""

from calculator import add, subtract


def test_add_returns_sum_of_two_numbers() -> None:
    """add returns the sum of two numbers."""
    assert add(2, 3) == 5


def test_subtract_returns_difference() -> None:
    """subtract returns the difference of two numbers."""
    assert subtract(5, 3) == 2