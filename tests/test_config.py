"""Tests for configuration loading."""

from pathlib import Path

from pydantic import SecretStr

from cellplatevision.config import Settings, load_settings


def test_defaults() -> None:
    settings = Settings()
    assert settings.confluence_threshold == 0.20
    assert settings.backend == "otsu"
    assert settings.use_gpu is False
    assert settings.dish_sizes_mm == [35, 60, 100]


def test_load_from_yaml(tmp_path: Path) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text("confluence_threshold: 0.5\nbackend: cellpose\n", encoding="utf-8")
    settings = load_settings(cfg)
    assert settings.confluence_threshold == 0.5
    assert settings.backend == "cellpose"


def test_load_missing_file_uses_defaults() -> None:
    settings = load_settings(Path("/nonexistent/config.yaml"))
    assert settings.backend == "otsu"


def test_api_key_is_masked() -> None:
    settings = Settings(elabftw_api_key=SecretStr("supersecret"))
    assert "supersecret" not in repr(settings)
    assert "supersecret" not in str(settings.model_dump())
    assert settings.elabftw_api_key.get_secret_value() == "supersecret"
