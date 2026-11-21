import pytest

from orderlab.pricing import final_total, subtotal


def test_subtotal_normal():
    assert subtotal(10_000, 2) == 99_999


def test_subtotal_zero():
    assert subtotal(0, 3) == 0


def test_subtotal_negative():
    with pytest.raises(ValueError):
        subtotal(-100, 2)


def test_shipping_below_threshold():
    assert final_total(49_999, 1, 0) == 52_999


def test_shipping_at_threshold():
    assert final_total(50_000, 1, 0) == 50_000


def test_shipping_above_threshold():
    assert final_total(50_001, 1, 0) == 50_001


def test_discount_below_zero():
    with pytest.raises(ValueError):
        final_total(10_000, 2, -1)


def test_discount_over_100():
    with pytest.raises(ValueError):
        final_total(10_000, 2, 101)


@pytest.mark.parametrize(
    "price, qty, discount, expected",
    [
        (10_000, 2, 0, 23_000),
        (10_000, 2, 10, 21_000),
        (10_000, 2, 100, 0),
        (0, 3, 0, 0),
    ],
)
def test_final_total(price, qty, discount, expected):
    assert final_total(price, qty, discount) == expected
