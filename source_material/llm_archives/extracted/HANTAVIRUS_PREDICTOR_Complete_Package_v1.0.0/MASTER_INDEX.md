# HANTAVIRUS PREDICTOR: Master File Index
## Complete Implementation Package for Publication-Ready Hantavirus Forecasting

**Version:** 1.0 | **Date:** May 2026 | **Total Files:** 28 | **Total Size:** ~350 KB

---

## DOCUMENT HIERARCHY

```
HANTAVIRUS PREDICTOR PACKAGE
|
|-- FRAMEWORK & PLANNING
|   |-- HANTAVIRUS_PREDICTOR_Complete_Framework.md  [MAIN DOCUMENT]
|   |-- README.md
|   |-- CITATION.cff
|   |-- LICENSE (create separately)
|
|-- MATHEMATICAL & THEORETICAL
|   |-- manuscript.tex              [LaTeX manuscript template]
|   |-- references.bib              [Bibliography for LaTeX]
|
|-- SOURCE CODE
|   |-- src_models_hantast_pinn_fm.py      [Core model: ClimateEncoder, PINN, FM, ST-GAT]
|   |-- src_data_pipeline.py               [Data ingestion, features, augmentation]
|   |-- src_training_trainer.py            [PyTorch Lightning training module]
|   |-- src_evaluation.py                  [Metrics, calibration, significance tests]
|   |-- src_visualization.py               [Publication-ready figure generation]
|
|-- SCRIPTS (Entry Points)
|   |-- scripts_train.py          [Training pipeline]
|   |-- scripts_evaluate.py       [Evaluation suite]
|   |-- scripts_deploy.py         [FastAPI inference server]
|
|-- CONFIGURATION
|   |-- config_train_config.yaml  [Training hyperparameters]
|   |-- config_model_config.yaml  [Architecture configuration]
|   |-- config_data_config.yaml   [Data source & processing config]
|   |-- requirements.txt          [Python dependencies]
|   |-- setup.py                  [Package setup]
|   |-- environment.yml           [Conda environment]
|
|-- INFRASTRUCTURE
|   |-- Dockerfile                [Production container]
|   |-- docker-compose.yml        [Multi-service orchestration]
|   |-- Makefile                  [Build automation]
|   |-- .gitignore                [Git exclusions]
|   |-- .github_workflows_tests.yml      [CI: tests + linting]
|   |-- .github_workflows_docker.yml     [CI: Docker build + push]
|
|-- TESTS
|   |-- tests_test_data.py        [Data pipeline tests]
|   |-- tests_test_models.py      [Model architecture tests]
```

---

## FILE DESCRIPTIONS

### 1. HANTAVIRUS_PREDICTOR_Complete_Framework.md [MAIN]
**Size:** ~42 KB | **Words:** ~5,700
**Contents:** The complete theoretical framework covering:
- Executive Summary & Novelty Statement
- Mathematical Model (SEIR-SDE, carrying capacity, spillover)
- Data Architecture (14 sources, ingestion pipeline)
- Algorithm Architecture (5-tier HantaST-PINN-FM system)
- Implementation Specifications (repo structure, Docker, compute)
- Training Protocol (3-stage curriculum learning)
- Validation & Statistical Rigor (WIS, CRPS, DM tests, coverage)
- Data Scarcity Mitigation (6-pillar strategy)
- Publication Strategy (target journals, manuscript structure)
- QA Checklist & Known Limitations

**Usage:** Primary reference document. Read first before any implementation.

---

### 2. manuscript.tex
**Size:** ~12 KB
**Contents:** Complete LaTeX manuscript template for journal submission.
- Abstract (250 words)
- Introduction (data scarcity problem, contributions)
- Methods (SEIR math, architecture, data, training, validation)
- Results (baseline comparison, ablation, calibration, risk maps)
- Discussion (public health utility, limitations, transferability)
- Data/Code Availability statements

**Target Journals:** Nature Communications, PLOS Computational Biology, Lancet Planetary Health
**Usage:** Fill in actual results after training. Compile with `pdflatex` + `bibtex`.

---

### 3. references.bib
**Size:** ~8 KB | **Entries:** 28
**Contents:** BibTeX bibliography covering:
- SEIR modeling (Allen et al. 2006, Abramson-Kenkre 2002)
- Hantavirus epidemiology (CDC, WHO, PAHO, LANL)
- ML methods (PINN, TimesFM, Chronos, GAT, SHAP, conformal prediction)
- Statistical tests (Diebold-Mariano, Clarke, Hansen MCS)
- Remote sensing (MODIS, ERA5, CHIRPS)

**Usage:** Linked by `manuscript.tex`. Compile with `bibtex` or `biber`.

---

### 4. src_models_hantast_pinn_fm.py
**Size:** ~15 KB
**Contents:** Complete PyTorch implementation of all model components:
- `ClimateEncoder`: 3D CNN + Temporal Transformer -> K(t), beta(t)
- `SEIRPhysicsLayer`: Differentiable ODE solver with autograd
- `FoundationPrior`: TimesFM with LoRA adaptation
- `SpatiotemporalGAT`: Graph Attention + GRU forecaster
- `HantaSTPINNFM`: Full system integration with multi-objective loss

**Key Features:**
- Automatic differentiation for physics residuals
- Sex-structured SEIR with next-generation matrix R0
- Negative binomial output for count data
- Modular design: each tier can be trained independently

**Dependencies:** torch, torchdiffeq, torch-geometric, transformers, peft

---

### 5. src_data_pipeline.py
**Size:** ~12 KB
**Contents:** Three modules:
- `ingestion.py`: CDC, NEON, MODIS, ERA5, CHIRPS data fetchers
- `features.py`: Lag engineering, rolling features, climate indices, exposure index
- `augmentation.py`: Synthetic SEIR trajectory generation (10,000 samples)

**Key Features:**
- Dask/xarray for GPU-accelerated raster processing
- Temporal stratified sampling by ENSO phase
- Focal loss configuration for class imbalance
- Parameter sweep: beta_m in [0.01, 0.5], K in [100, 10000]

---

### 6. src_training_trainer.py
**Size:** ~8 KB
**Contents:**
- `HantavirusDataset`: PyTorch Dataset with rodent + human targets
- `HantaSTPINNFMModule`: PyTorch Lightning module
- `CurriculumScheduler`: 4-stage curriculum (rodent-only -> full multi-task)

**Key Features:**
- Mixed precision (FP16) training
- Cosine annealing with warm restarts
- Gradient clipping + early stopping on val_wis
- WandB logging with model checkpointing
- Multi-GPU DDP support

---

### 7. src_evaluation.py
**Size:** ~10 KB
**Contents:**
- `ForecastMetrics`: WIS, CRPS, MAE, MAPE, coverage, Brier, Moran's I
- `StatisticalTests`: Diebold-Mariano, Clarke, Wilcoxon, Model Confidence Set
- `CalibrationDiagnostics`: Reliability diagrams, PIT histograms, slope/intercept
- `AblationStudy`: 6 configurations with component removal

**Key Features:**
- WIS implementation per Bracher et al. 2021 (11 quantile levels)
- HAC standard errors for DM test
- Block bootstrap for conformal prediction
- Morris method for sensitivity analysis

---

### 8. src_visualization.py
**Size:** ~12 KB
**Contents:** `PublicationFigures` class generating all 8 required figures:
- Fig 1: Architecture diagram (5 tiers)
- Fig 2: SEIR dynamics + phase portrait + R0 vs K
- Fig 3: Spatial risk map (Cartopy, 1km resolution)
- Fig 4: Forecast comparison (time series + cumulative error)
- Fig 5: Reliability diagram + PIT histogram
- Fig 6: SHAP global + local importance
- Fig 7: Ablation bar chart
- Fig 8: ST-GAT attention weights (transmission corridors)

**Style:** 300 DPI, Times New Roman, publication-ready

---

### 9-11. scripts_*.py
**train.py:** Full training pipeline with argparse, config loading, DDP
**evaluate.py:** Evaluation suite with ablation, baseline comparison, DM tests
**deploy.py:** FastAPI inference server with /predict and /risk_map endpoints

---

### 12-14. config_*.yaml
**train_config.yaml:** 500-line config with curriculum stages, loss weights, HPO
**model_config.yaml:** Architecture specs + biological parameter priors
**data_config.yaml:** 14 data sources with access URLs, variables, licenses

---

### 15-17. Infrastructure Files
**Dockerfile:** CUDA 12.4, PyTorch 2.3, PyG, multi-stage build
**docker-compose.yml:** Training + inference + dashboard services
**Makefile:** install, test, lint, format, docker, train, eval, deploy, clean

---

### 18-21. CI/CD
**.github/workflows/tests.yml:** pytest, black, flake8, mypy, codecov
**.github/workflows/docker.yml:** Buildx, Docker Hub push, caching

---

### 22-23. Tests
**test_data.py:** Lag features, outbreak labels, synthetic trajectory generation
**test_models.py:** ClimateEncoder, PINN-SEIR, ST-GAT, end-to-end integration

---

### 24-28. Meta Files
**README.md:** Quick start, installation, usage, citation
**CITATION.cff:** Software citation metadata (CFF v1.2.0)
**.gitignore:** Python, data, outputs, LaTeX exclusions
**requirements.txt:** 60+ dependencies with version pins
**setup.py:** Package metadata, entry points, extras_require

---

## IMPLEMENTATION ROADMAP

### Phase 0: Environment Setup (Day 1)
```bash
# 1. Provision GPU instance (4x A100 recommended)
# 2. Install CUDA 12.4, Python 3.11
# 3. Clone repo, create conda env, install dependencies
make install

# 4. Verify installation
python -c "import torch; print(torch.cuda.is_available())"
pytest tests/ -v
```

### Phase 1: Data Acquisition (Days 2-3)
```bash
# Download all data sources
python scripts/download_data.py --config config/data_config.yaml

# Verify data integrity
python -c "from src.data.ingestion import *; print('OK')"
```

### Phase 2: Baseline Models (Days 4-5)
```bash
# Train XGBoost and SARIMA baselines
# Save predictions for comparison
python notebooks/02_baseline_models.ipynb
```

### Phase 3: Core Model Training (Days 6-14)
```bash
# Week 1: PINN pretraining on synthetic data
python scripts/train.py --config config/train_config.yaml --gpus 4

# Week 2: Multi-task fine-tuning
# (continues automatically via curriculum)
```

### Phase 4: Evaluation & Publication (Days 15-21)
```bash
# Run full evaluation
python scripts/evaluate.py --run_ablation --compare_baselines ...

# Generate figures
python -c "from src.visualization import *; PublicationFigures().generate_all(...)"

# Compile manuscript
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

### Phase 5: Deployment (Day 22+)
```bash
# Build and deploy
docker-compose up -d

# Or submit to journal
# Nature Communications: https://www.nature.com/ncomms/
```

---

## CRITICAL SUCCESS FACTORS

1. **Data first:** Verify NEON + CDC data access before any model work
2. **Synthetic pretraining:** Do NOT skip Week 1 synthetic SEIR pretraining
3. **Physics weight tuning:** Use adaptive lambda (NTK-based) for stable PINN training
4. **Temporal causality:** Strict train/val/test splits by time; never shuffle
5. **Coverage calibration:** Target 90% +/- 5%; adjust conformal alpha if needed
6. **Reproducibility:** Fix all seeds, log hardware, version data with DVC

---

## TROUBLESHOOTING QUICK REFERENCE

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| ODE solver diverges | Stiff system + large dt | Reduce rtol/atol to 1e-7 |
| PINN loss NaN | Physics weight too high | Reduce lambda_ode, use adaptive |
| FM OOM | TimesFM too large for GPU | Use gradient checkpointing, reduce batch |
| ST-GAT over-smoothing | Too many GAT layers | Add residual connections, use GATv2 |
| Poor coverage | Underdispersed predictions | Increase phi (dispersion) head capacity |
| Low WIS improvement | Data leakage | Check temporal split integrity |
| Slow data loading | Unoptimized raster I/O | Use Zarr + Dask, enable pin_memory |

---

## CONTACT & SUPPORT

- **Issues:** GitHub Issues tab
- **Discussions:** GitHub Discussions tab
- **Email:** corresponding.author@university.edu
- **Slack:** #hantavirus-predictor channel

---

*This package represents a complete, publication-ready implementation framework. All files are designed to work together as an integrated system. Start with the main framework document, then proceed through the implementation roadmap.*
