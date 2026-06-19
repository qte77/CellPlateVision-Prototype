"""Tests for the end-to-end pipeline."""

from pathlib import Path

import numpy as np
import pytest

from cellplatevision.config import Settings
from cellplatevision.imaging import save_image
from cellplatevision.pipeline import DishNotFoundError, PipelineResult, run_pipeline
from tests.generate_synthetic import generate_dish


def test_run_pipeline_produces_result_and_annotation(tmp_path: Path) -> None:
    image_path = tmp_path / "dish.png"
    save_image(image_path, generate_dish(confluence=0.3, seed=1))
    output_path = tmp_path / "annotated.png"
    result = run_pipeline(image_path, Settings(), output_path=output_path)
    assert isinstance(result, PipelineResult)
    assert result.label in {"growing", "not_growing", "low_confidence"}
    assert 0.0 <= result.confluence <= 1.0
    assert output_path.exists()


def test_run_pipeline_raises_when_no_dish(tmp_path: Path) -> None:
    blank_path = tmp_path / "blank.png"
    save_image(blank_path, np.zeros((256, 256), dtype=np.uint8))
    with pytest.raises(DishNotFoundError):
        run_pipeline(blank_path, Settings())
