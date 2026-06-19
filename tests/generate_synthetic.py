"""Synthetic Petri-dish image generator for offline unit tests.

Draws a circular dish (mid-gray agar) on a dark background with bright colony
blobs covering roughly the requested confluence, plus mild Gaussian noise. Used by
M1's Hough/Otsu parameter tests so CI never depends on private or network images.
"""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def _draw_colonies(
    draw: ImageDraw.ImageDraw,
    rng: np.random.Generator,
    center: int,
    dish_radius: int,
    n_colonies: int,
    colony_radius: int,
) -> None:
    """Draw ``n_colonies`` bright blobs at random positions inside the dish."""
    for _ in range(n_colonies):
        angle = rng.uniform(0.0, 2.0 * math.pi)
        dist = dish_radius * 0.92 * math.sqrt(rng.uniform(0.0, 1.0))
        x = int(center + dist * math.cos(angle))
        y = int(center + dist * math.sin(angle))
        draw.ellipse(
            [x - colony_radius, y - colony_radius, x + colony_radius, y + colony_radius],
            fill=220,
        )


def generate_dish(
    size: int = 512,
    dish_radius: int = 220,
    confluence: float = 0.3,
    colony_radius: int = 10,
    seed: int = 0,
) -> np.ndarray:
    """Generate a synthetic grayscale dish image.

    Args:
        size: Output image side length, in pixels.
        dish_radius: Dish radius, in pixels.
        confluence: Approximate fraction of dish area covered by colonies.
        colony_radius: Radius of each colony blob, in pixels.
        seed: PRNG seed for deterministic output.

    Returns:
        A ``(size, size)`` ``uint8`` grayscale image.
    """
    rng = np.random.default_rng(seed)
    center = size // 2
    image = Image.new("L", (size, size), color=30)
    draw = ImageDraw.Draw(image)
    draw.ellipse(
        [center - dish_radius, center - dish_radius, center + dish_radius, center + dish_radius],
        fill=110,
    )
    dish_area = math.pi * dish_radius**2
    colony_area = math.pi * colony_radius**2
    n_colonies = max(int(confluence * dish_area / colony_area), 0)
    _draw_colonies(draw, rng, center, dish_radius, n_colonies, colony_radius)
    image = image.filter(ImageFilter.GaussianBlur(radius=1.5))
    array = np.asarray(image, dtype=np.float64)
    array += rng.normal(0.0, 4.0, array.shape)
    return np.clip(array, 0, 255).astype(np.uint8)
