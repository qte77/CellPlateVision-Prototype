"""Tests for growth classification."""

from cellplatevision.classify import classify_growth


def test_growing_above_threshold() -> None:
    assert classify_growth(0.5, 0.2) == "growing"


def test_not_growing_below_threshold() -> None:
    assert classify_growth(0.1, 0.2) == "not_growing"


def test_threshold_boundary_is_growing() -> None:
    assert classify_growth(0.2, 0.2) == "growing"


def test_low_confidence_overrides_threshold() -> None:
    assert classify_growth(0.9, 0.2, low_confidence=True) == "low_confidence"
