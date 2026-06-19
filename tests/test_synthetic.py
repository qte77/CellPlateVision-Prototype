"""Tests for the synthetic dish image generator."""

import numpy as np

from tests.generate_synthetic import generate_dish


def test_generate_dish_shape_and_dtype() -> None:
    image = generate_dish(size=256, dish_radius=100, confluence=0.3, seed=1)
    assert image.shape == (256, 256)
    assert image.dtype == np.uint8


def test_generate_dish_is_deterministic() -> None:
    first = generate_dish(seed=42)
    second = generate_dish(seed=42)
    assert np.array_equal(first, second)


def test_higher_confluence_has_more_bright_pixels() -> None:
    low = generate_dish(confluence=0.1, seed=3)
    high = generate_dish(confluence=0.6, seed=3)
    assert int((high > 180).sum()) > int((low > 180).sum())
