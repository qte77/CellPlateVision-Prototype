# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **M0 scaffold**: uv/hatchling `src/` package, runtime config via
  `pydantic-settings` (`config.yaml` + `CPV_*` env), and the pipeline skeleton
  (`dish_finder`, `segmentation`, `confluence`, `classify`, `pipeline`,
  `elab_client`, `cli`).
- Implemented and unit-tested `compute_confluence` and `classify_growth`.
- Synthetic dish-image generator (`tests/generate_synthetic.py`) for offline tests.
- Public-dataset download helper (`scripts/download_datasets.py`).
- Dev tooling: ruff, pyright, complexipy, pytest config; `Makefile`; `validate`
  CI workflow; CodeQL restored to baseline; Dependabot switched to the uv variant.
- Project docs: `AGENTS.md`, `CONTRIBUTING.md`, `docs/prototype-roadmap.md`.
