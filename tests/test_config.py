"""Tests for configuration loading."""

from pathlib import Path

import pytest
from pydantic import SecretStr, ValidationError

from cellplatevision.config import Settings, load_settings


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


def test_env_overrides_yaml_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text("backend: otsu\n", encoding="utf-8")
    monkeypatch.setenv("CPV_BACKEND", "cellpose")
    assert load_settings(cfg).backend == "cellpose"  # env wins over the file


def test_invalid_host_raises() -> None:
    with pytest.raises(ValidationError):
        Settings.model_validate({"elabftw_host": "not a url"})
