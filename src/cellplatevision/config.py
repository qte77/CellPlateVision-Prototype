"""Runtime configuration loaded from ``config.yaml`` and ``CPV_*`` env variables."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import AnyHttpUrl, BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource

if TYPE_CHECKING:
    from pathlib import Path

    from pydantic_settings import PydanticBaseSettingsSource


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
    """Top-level CellPlateVision configuration.

    Resolution precedence (highest first): constructor args, ``CPV_*`` environment
    variables, then the YAML file set via :func:`load_settings`.
    """

    model_config = SettingsConfigDict(
        env_prefix="CPV_", env_nested_delimiter="__", extra="ignore", yaml_file=None
    )

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
    elabftw_host: AnyHttpUrl = AnyHttpUrl("http://localhost:3148/api/v2")
    elabftw_experiment_id: int = 1
    elabftw_api_key: SecretStr = SecretStr("")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Order sources so env vars override the YAML file."""
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


def load_settings(config_path: Path | None = None) -> Settings:
    """Load settings from a YAML file, overridden by ``CPV_*`` environment variables.

    Args:
        config_path: Path to a YAML config file; if ``None`` or missing, defaults
            (and environment variables) are used.

    Returns:
        A validated :class:`Settings` instance.
    """
    Settings.model_config["yaml_file"] = str(config_path) if config_path is not None else None
    try:
        return Settings()
    finally:
        Settings.model_config["yaml_file"] = None
