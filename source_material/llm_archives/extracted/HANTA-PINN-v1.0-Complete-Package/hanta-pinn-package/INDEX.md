# HANTA-PINN v1.0: Complete Package Index

**Date:** 2026-05-11
**Version:** 1.0-FINAL

---

## Reports

| # | Report | Description |
|---|--------|-------------|
| 00 | [HANTA-PINN_Complete_Framework.md](reports/00_HANTA-PINN_Complete_Framework.md) | Master framework document (37,000+ chars) |
| 01 | [01_Framework_and_QA_Report.md](reports/01_Framework_and_QA_Report.md) | QA audit, verified facts, model spec |
| 02 | [02_Data_Audit_and_Provenance_Report.md](reports/02_Data_Audit_and_Provenance_Report.md) | Data sources, processing pipeline, scarcity mitigation |
| 03 | [03_Validation_and_Statistical_Rigor_Report.md](reports/03_Validation_and_Statistical_Rigor_Report.md) | Metrics, CV strategy, statistical tests, ablations |
| 04 | [04_Reviewer_Response_Playbook.md](reports/04_Reviewer_Response_Playbook.md) | 8 anticipated objections with verbatim responses |

## Source Code

| Module | File | Description |
|--------|------|-------------|
| EnvironmentalEncoder | [src/models/encoder.py](src/models/encoder.py) | 1D-CNN+LSTM for K(t) |
| PINNCore | [src/models/pinn_core.py](src/models/pinn_core.py) | Sex-structured SEIR with physics loss |
| SpilloverDecoder | [src/models/spillover.py](src/models/spillover.py) | Human risk derivation |
| HantaPINN | [src/models/hanta_pinn.py](src/models/hanta_pinn.py) | Complete integrated model |
| SEIR RHS | [src/physics/seir_rhs.py](src/physics/seir_rhs.py) | ODE solver + synthetic generation |
| Trainer | [src/training/trainer.py](src/training/trainer.py) | Training loop with early stopping |
| Metrics | [src/evaluation/metrics.py](src/evaluation/metrics.py) | RMSE, WIS, CRPS, DM test, ECE |
| Seed | [src/utils/seed.py](src/utils/seed.py) | Reproducibility utilities |

## Scripts

| Script | Purpose |
|--------|---------|
| [scripts/train.py](scripts/train.py) | Main training script |
| [scripts/evaluate.py](scripts/evaluate.py) | Evaluation script |
| [scripts/generate_synthetic.py](scripts/generate_synthetic.py) | Synthetic data generation |

## Tests

| Test | Coverage |
|------|----------|
| [tests/test_physics.py](tests/test_physics.py) | SEIR conservation, synthetic generation |
| [tests/test_model.py](tests/test_model.py) | Forward pass, loss, parameter count |

## Configuration

| Config | Purpose |
|--------|---------|
| [config/model.yaml](config/model.yaml) | Architecture hyperparameters |
| [config/data.yaml](config/data.yaml) | Data sources and preprocessing |
| [config/train.yaml](config/train.yaml) | Training hyperparameters |

## Infrastructure

| File | Purpose |
|------|---------|
| [environment.yml](environment.yml) | Conda environment specification |
| [Dockerfile](Dockerfile) | Containerized deployment |
| [setup.py](setup.py) | Python package setup |
| [LICENSE](LICENSE) | MIT License |

---

## Quick Start

```bash
# 1. Setup environment
conda env create -f environment.yml
conda activate hanta-pinn

# 2. Generate synthetic pretraining data
python scripts/generate_synthetic.py --n 10000

# 3. Train model
python scripts/train.py --config config/train.yaml --seed 42

# 4. Run tests
pytest tests/ -v
```

## Publication Checklist

- [x] Mathematical model fully derived
- [x] Data sources documented with exact APIs
- [x] Architecture specified to layer level
- [x] Training protocol with exact hyperparameters
- [x] Validation protocol with metrics and thresholds
- [x] 5 ablation studies designed
- [x] 8 reviewer objections pre-answered
- [x] Code implemented and tested
- [x] Reproducibility plan (Docker, seeds, DVC)
- [x] Limitations honestly disclosed

---

*Package compiled: 2026-05-11*
*Ready for journal submission and code agent handoff*
