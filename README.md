# CellPlateVision

[![Version](https://img.shields.io/badge/version-0.0.0-8A2BE2)](README.md)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Dependabot Updates](https://github.com/qte77/CellPlateVision-Prototype/actions/workflows/dependabot/dependabot-updates/badge.svg?branch=main)](https://github.com/qte77/CellPlateVision-Prototype/actions/workflows/dependabot/dependabot-updates)
[![CodeQL](https://github.com/qte77/CellPlateVision-Prototype/actions/workflows/codeql.yaml/badge.svg?branch=main)](https://github.com/qte77/CellPlateVision-Prototype/actions/workflows/codeql.yaml)
[![CodeFactor](https://www.codefactor.io/repository/github/qte77/CellPlateVision-Prototype/badge/main)](https://www.codefactor.io/repository/github/qte77/CellPlateVision-Prototype)

> **Status: Prototype / Research**

Automated cell culture growth detection on round Petri dishes using
image-based confluence estimation and electronic lab notebook integration.

## Scope

- Detect whether cell cultures grow on round Petri dishes (35/60/100 mm)
- Pipeline: image capture -> dish detection -> segmentation -> confluence -> ELN export
- Growth classification via confluence threshold
- Segmentation backends: [OpenCV][opencv] classical, [Cellpose][cellpose], [Fiji][fiji], VLM, [LandingLens][landinglens] (optional)
- Experiment tracking via [eLabFTW][elabftw] REST API

## Stack

| Layer               | Tool                                     |
| ------------------- | ---------------------------------------- |
| Dish detection      | [OpenCV][opencv] Hough circle transform  |
| Segmentation        | Otsu, [Cellpose][cellpose], [Fiji][fiji] |
| Overlap handling    | Watershed, [Cellpose][cellpose] inst.seg |
| ELN                 | [eLabFTW][elabftw]                       |
| Alt. no-code (opt.) | [LandingLens SDK][landinglens-sdk]       |
| Alt. interactive    | [Fiji][fiji] (manual / macro batch)      |

## Docs

See [docs/outline.md](docs/outline.md) for architecture, analysis, and outlook.

## License

Apache-2.0 — see [LICENSE](LICENSE)

## References

- [Building a Trustworthy Agent Loop for a Physical Lab](https://qte77.github.io/open-self-driving-lab-agent-loop/) — uses this project as the *perceive* step of a self-driving-lab agent loop
- [A $150 Pipetting Robot from a Stock 3D Printer](https://qte77.github.io/pipettebot-sub-150-pipetting-robot/) — companion build; closes the loop on the outcome side (pipette → grow → image → measure)

[cellpose]: https://github.com/MouseLand/cellpose
[elabftw]: https://www.elabftw.net/
[fiji]: https://fiji.sc/
[landinglens]: https://landing.ai/landinglens
[landinglens-sdk]: https://pypi.org/project/landingai/
[opencv]: https://opencv.org/
