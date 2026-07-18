from econlab.metrics import gini


def test_gini_equality() -> None:
    assert gini([10, 10, 10, 10]) == 0.0


def test_gini_maximal_inequality_is_high() -> None:
    assert gini([0, 0, 0, 100]) > 0.70
