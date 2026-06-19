# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **M3 end-to-end pipeline**: `run_pipeline` (load -> detect -> segment ->
  confluence -> classify) returning a `PipelineResult`, with optional annotated
  output (dish boundary + cell overlay + confluence text), a wired `cellplatevision
  run` CLI (`--image/--config/--output/--dry-run`), `imaging` load/save/BGR helpers,
  and a `scripts/smoke_test.py` for batch runs over local datasets.

- **M2 eLabFTW integration**: `ElabClient` wrapping the `elabapi-python` SDK
  (`get_experiment` / `patch_experiment` / `upload_file`) with raw-API-key auth,
  a `docker-compose.dev.yml` local instance plus `make elab_up` / `elab_down`, and
  offline wiring tests plus a `network`-marked round-trip test (excluded by default).

- **M1 detection + segmentation (Tier 1)**: `SingleDishFinder` (Hough circle
  transform with a contour fallback) and `OtsuBackend` (Otsu thresholding inside
  the dish, optional flat-field correction, connected-component cleanup, and a
  P20-P80 contrast low-confidence flag), plus a shared `imaging.to_grayscale`
  helper and `circular_mask`. Added opencv/scikit-image/scipy dependencies.

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
