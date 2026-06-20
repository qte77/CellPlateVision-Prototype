"""Tests for the CLI."""

from pathlib import Path

import numpy as np

from cellplatevision.cli import main
from cellplatevision.imaging import save_image
from tests.generate_synthetic import generate_dish


def test_no_command_prints_help() -> None:
    assert main([]) == 0


def test_run_returns_error_code_when_no_dish(tmp_path: Path) -> None:
    blank = tmp_path / "blank.png"
    save_image(blank, np.zeros((128, 128), dtype=np.uint8))
    assert main(["run", "--image", str(blank)]) == 1


def test_dry_run_returns_zero(tmp_path: Path) -> None:
    image_path = tmp_path / "dish.png"
    save_image(image_path, generate_dish(seed=0))
    assert main(["run", "--image", str(image_path), "--dry-run"]) == 0


def test_run_writes_annotation(tmp_path: Path) -> None:
    image_path = tmp_path / "dish.png"
    save_image(image_path, generate_dish(confluence=0.3, seed=2))
    output_path = tmp_path / "out.png"
    assert main(["run", "--image", str(image_path), "--output", str(output_path)]) == 0
    assert output_path.exists()
