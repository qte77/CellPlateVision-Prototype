"""Runtime configuration loaded from ``config.yaml`` and ``CPV_*`` env variables."""

from __future__ import annotations

from typing import TYPE_CHECKING

import yaml
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any


class HoughParams(BaseModel):
    """Hough-circle parameters for dish-boundary detection (tuned in M1)."""

    dp: float = 1.2
    min_dist: float = 200.0
    param1: float = 100.0
    param2: float = 30.0
    min_radius_ratio: float = 0.30
    max_radius_ratio: float = 0.95


class OtsuParams(BaseModel):
    """Otsu segmentation parameters."""

    flat_field: bool = False
    flat_field_blur_sigma: float = 25.0
    min_object_size: int = 64
    min_contrast_ratio: float = 0.15


class Settings(BaseSettings):
    """Top-level CellPlateVision configuration."""

    model_config = SettingsConfigDict(env_prefix="CPV_", env_nested_delimiter="__", extra="ignore")

    dish_sizes_mm: list[int] = Field(default_factory=lambda: [35, 60, 100])
    camera_height_mm: int = 250
    confluence_threshold: float = 0.20
    backend: str = "otsu"
    use_gpu: bool = False
    cellpose_model: str = "cyto3"
    cellpose_model_gpu: str = "cpsam_v2"
    escalate_on_low_confidence: bool = True
    hough: HoughParams = Field(default_factory=HoughParams)
    otsu: OtsuParams = Field(default_factory=OtsuParams)
    elabftw_host: str = "http://localhost:3148/api/v2"
    elabftw_experiment_id: int = 1
    elabftw_api_key: SecretStr = SecretStr("")


def load_settings(config_path: Path | None = None) -> Settings:
    """Load settings from a YAML file, overlaid by ``CPV_*`` environment variables.

    Args:
        config_path: Path to a YAML config file; if ``None`` or missing, defaults
            (and environment variables) are used.

    Returns:
        A validated :class:`Settings` instance.
    """
    data: dict[str, Any] = {}
    if config_path is not None and config_path.is_file():
        loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            data = loaded
    return Settings(**data)
