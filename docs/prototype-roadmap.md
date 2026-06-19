---
title: CellPlateVision — Prototype Roadmap
description: Research-backed recommendations and the M0–M5 implementation roadmap for the prototype
created: 2026-06-19
status: roadmap
---

## Purpose

This complements [outline.md](outline.md) (architecture) and
[feasibility-assessment.md](feasibility-assessment.md) (the GO-WITH-CAVEATS gate
decision). It records the **research-backed recommendations** for the open
questions and the **milestone roadmap** used to scaffold the prototype.

All facts below were web-verified as of **mid-2026**.

## Recommendations for the open feasibility questions

None of the five open questions block engineering — each has a config-driven default
with a substitute that lets development proceed before the lab provides resources.

| # | Question | Default adopted |
|---|---|---|
| 1 | Imaging rig vs ad-hoc | Fixed rig: start with the ~$33 cardboard diffusion box (Frontiers Microbiology 2021); fixed camera distance + manual exposure recorded in `config.yaml`. PiRamid (~$135, 95 mm fixed height) is the upgrade path. |
| 2 | eLabFTW version/access | Develop against a **local Docker** eLabFTW (`get.elabftw.net/?config`); use the official **`elabapi-python`** SDK. v5.5.14 confirms API **v2** and all three endpoints are stable. Production creds via `CPV_*` env. |
| 3 | Multi-well plates | **Defer.** Keep the door open with the `DishFinder` ABC; `SingleDishFinder` (Hough) now, `MultiWellFinder` (ANSI/SBS grid) later. |
| 4 | LandingLens | **Demote** to a documented, lowest-priority optional plugin (cloud-only, US-East default, 1k-credit/mo cap, SDK stale since Oct 2024). Open default path is Otsu → Cellpose. |
| 5 | Sample images + GPU | Use public CC datasets (AGAR, Scientific Data 2023) for tuning; default **CPU** (`use_gpu: false`, Cellpose `cyto3`). GPU (`cpsam_v2`) is a one-line config flag. |

## Segmentation backend tiering

1. **Otsu + morphological cleanup** (default; instant, offline).
2. **Cellpose `cyto3`** (CPU-feasible) — auto-escalated when Otsu flags `low_confidence`
   (unimodal histogram at near-empty/near-confluent).
3. **Cellpose `cpsam_v2`** (GPU, ~1.23 GB weights, ~16 GB VRAM) — opt-in via `use_gpu`.
4. **VLM QA layer** (optional) — coarse "growing / contaminated / unclear" check only.

Cellpose is at **4.2.1.1**; eLabFTW auth is a **raw API key** header (not `Bearer`).

## Public datasets (for parameter tuning, not CI)

- **AGAR** (CC-BY-NC 2.0) — 18k top-down Petri dish photos; ideal for Hough/Otsu tuning.
- **Scientific Data 2023** (CC-BY 4.0) — 369 dish images, 56,865 annotated colonies.
- **LIVECell** (CC-BY 4.0) — phase-contrast cells for segmentation benchmarking.

CI uses only **synthetic fixtures** (no license or network dependency).

## Milestone roadmap

| Milestone | Scope | Depends on |
|---|---|---|
| **M0** | Dev env + package skeleton + synthetic test harness + dataset script + CI + this doc | — |
| **M1** | Hough `SingleDishFinder` + `OtsuBackend` (Tier 1) + confluence/classify wiring | M0 |
| **M2** | `ElabClient` (`elabapi-python`) + local Docker eLabFTW + integration tests | M0 |
| **M3** | End-to-end pipeline + CLI `run` + smoke test on AGAR + annotated PNG output | M1 + M2 |
| **M4** | Cellpose `cyto3` backend (Tier 2) + plugin interface + LandingLens stub | M3 |
| **M5** | Real-lab validation (out of scope here) | prod creds + real images + GPU decision |

## Open decisions deferred to M5 (need the user/lab)

1. Production eLabFTW credentials + staging experiment id.
2. 5–100 real dish images for final parameter validation.
3. GPU availability — determines `cyto3` (CPU) vs `cpsam_v2` (GPU) as the M5 default.
