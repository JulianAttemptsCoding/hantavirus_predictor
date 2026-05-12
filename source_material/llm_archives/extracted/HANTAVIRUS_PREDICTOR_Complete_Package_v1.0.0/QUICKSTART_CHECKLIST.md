# HANTAVIRUS PREDICTOR: Quick-Start Implementation Checklist
## Day-by-Day Action Plan for Coding Agents

---

## PRE-REQUISITES (Before Day 1)

- [ ] GPU cluster provisioned (4x A100 recommended, 1x A100 minimum)
- [ ] CUDA 12.4 installed and verified
- [ ] Python 3.11 installed
- [ ] Git repository initialized
- [ ] GitHub repo created (public or private)
- [ ] WandB account created + API key
- [ ] Docker installed (optional but recommended)
- [ ] CDC WONDER account (for data access)
- [ ] NASA Earthdata account (for MODIS)
- [ ] Copernicus CDS account (for ERA5)
- [ ] SafeGraph application submitted (if using mobility data)

---

## DAY 1: Environment & Repository Setup

### Morning (4 hours)
- [ ] Clone repository template
- [ ] Create conda environment: `conda env create -f environment.yml`
- [ ] Activate environment: `conda activate hanta-predictor`
- [ ] Install package: `pip install -e .`
- [ ] Verify PyTorch + CUDA: `python -c "import torch; print(torch.cuda.is_available())"`
- [ ] Verify PyTorch Geometric: `python -c "import torch_geometric; print(torch_geometric.__version__)"`
- [ ] Run unit tests: `pytest tests/ -v`
- [ ] Initialize DVC: `dvc init`
- [ ] Configure WandB: `wandb login`

### Afternoon (4 hours)
- [ ] Review `HANTAVIRUS_PREDICTOR_Complete_Framework.md` in full
- [ ] Review `MASTER_INDEX.md` for file map
- [ ] Set up GitHub Actions (copy `.github/workflows/` files)
- [ ] Push initial commit
- [ ] Verify CI passes (may need to adjust for missing data)

### Deliverable: Working development environment

---

## DAY 2: Data Acquisition

### Morning (4 hours)
- [ ] Download CDC hantavirus case data (manual from WONDER or bulk request)
- [ ] Download NEON small mammal data via API
- [ ] Download MODIS NDVI tiles for US Southwest (h09v05, h10v05)
- [ ] Request ERA5 reanalysis via CDS API
- [ ] Download CHIRPS precipitation data

### Afternoon (4 hours)
- [ ] Download CDC SVI shapefile
- [ ] Download Census ACS data
- [ ] Download ESA WorldCover raster
- [ ] Download SRTM elevation
- [ ] (Optional) Request SafeGraph mobility data

### Evening (2 hours)
- [ ] Verify all raw data files exist
- [ ] Run `scripts/download_data.py` to validate
- [ ] Document any missing data in issues tracker
- [ ] Version data with DVC: `dvc add data/raw/`

### Deliverable: All raw data downloaded and versioned

---

## DAY 3: Data Processing & Feature Engineering

### Morning (4 hours)
- [ ] Run `src/data/ingestion.py` to load all raw data
- [ ] Process CDC cases: standardize, geocode, temporal alignment
- [ ] Process NEON rodents: compute seroprevalence by site-month
- [ ] Process MODIS NDVI: cloud mask, resample, monthly aggregation
- [ ] Process ERA5: monthly aggregates, anomaly computation

### Afternoon (4 hours)
- [ ] Spatial alignment: reproject all rasters to EPSG:5070, 1km grid
- [ ] Temporal alignment: ISO week standardization
- [ ] Feature engineering: lag features, rolling features, climate indices
- [ ] Create exposure index from SVI + rurality + housing
- [ ] Create target variables: outbreak labels, log-transforms

### Evening (2 hours)
- [ ] Train/val/test split (temporal, no shuffle)
- [ ] Class imbalance check: verify focal loss config
- [ ] Data quality report: missingness, outliers, leakage check
- [ ] Save processed datasets: `dvc add data/processed/`

### Deliverable: Clean, processed datasets ready for modeling

---

## DAY 4: Baseline Models

### Morning (4 hours)
- [ ] Implement SARIMA baseline (`statsmodels`)
- [ ] Implement XGBoost baseline (`xgboost`)
- [ ] Implement LSTM baseline (`pytorch`)
- [ ] Train all baselines on training set
- [ ] Generate predictions on validation set

### Afternoon (4 hours)
- [ ] Compute baseline metrics: MAE, RMSE, WIS, coverage
- [ ] Save baseline predictions as `.npy` files
- [ ] Document baseline performance in notebook
- [ ] Create baseline comparison figure

### Deliverable: Baseline metrics and predictions for comparison

---

## DAY 5: Synthetic Data Generation

### Morning (4 hours)
- [ ] Implement `SyntheticDataGenerator` class
- [ ] Define parameter priors (beta_m, beta_f, gamma, K, etc.)
- [ ] Generate 10,000 SEIR trajectories
- [ ] Verify trajectories: non-negative, mass conservation, R0 behavior

### Afternoon (4 hours)
- [ ] Add climate scenarios: El Nino, La Nina, Neutral
- [ ] Add initial condition variants: endemic, epidemic, extinction
- [ ] Save synthetic dataset: `data/synthetic/seir_trajectories.parquet`
- [ ] Version with DVC

### Deliverable: 10,000 synthetic trajectories for PINN pretraining

---

## DAY 6: PINN Pretraining (Week 1 Start)

### Morning (4 hours)
- [ ] Implement `ClimateEncoder` (3D CNN + Transformer)
- [ ] Implement `SEIRPhysicsLayer` (differentiable ODE)
- [ ] Implement physics residual computation
- [ ] Implement R0 computation via next-generation matrix

### Afternoon (4 hours)
- [ ] Implement `HantaLoss` with adaptive weighting
- [ ] Set up pretraining config: lambda_ode=10, lambda_data=1
- [ ] Start pretraining on synthetic data
- [ ] Monitor: physics residual should decrease, R0 should be plausible

### Evening (2 hours)
- [ ] Check training logs on WandB
- [ ] Verify no NaN losses
- [ ] Save checkpoint after 500 epochs

### Deliverable: Pretrained PINN weights

---

## DAY 7: PINN Pretraining Continued + Validation

### Morning (4 hours)
- [ ] Continue pretraining (if not converged)
- [ ] Validate on held-out synthetic trajectories
- [ ] Check: compartment trajectories smooth and non-negative
- [ ] Check: R0 responds correctly to K changes
- [ ] Check: disease-free equilibrium stable when R0 < 1

### Afternoon (4 hours)
- [ ] Fine-tune PINN on real NEON seroprevalence data
- [ ] Adjust loss weights: lambda_ode=5, lambda_data=1
- [ ] Monitor rodent prevalence predictions vs observations
- [ ] Save intermediate checkpoint

### Deliverable: PINN fine-tuned on real rodent data

---

## DAY 8: Foundation Model Integration

### Morning (4 hours)
- [ ] Download TimesFM-2.5 weights from HuggingFace
- [ ] Implement `FoundationPrior` with LoRA config
- [ ] Freeze base model, verify LoRA parameters trainable
- [ ] Test zero-shot inference on hantavirus case history

### Afternoon (4 hours)
- [ ] Fine-tune LoRA on rodent seroprevalence + related zoonoses
- [ ] Implement multi-task loss: FM alignment + PINN output
- [ ] Train with frozen PINN backbone
- [ ] Monitor FM embedding quality

### Deliverable: LoRA-adapted foundation model

---

## DAY 9: ST-GAT Training

### Morning (4 hours)
- [ ] Build county adjacency graph
- [ ] Add mobility edges (SafeGraph or gravity model fallback)
- [ ] Add ecological similarity edges (NDVI correlation)
- [ ] Implement `SpatiotemporalGAT` class

### Afternoon (4 hours)
- [ ] Combine PINN + FM outputs as node features
- [ ] Train ST-GAT on spatial cross-validation
- [ ] Monitor attention weights for interpretability
- [ ] Save best checkpoint

### Deliverable: Trained ST-GAT with spatial forecasts

---

## DAY 10: Uncertainty Quantification

### Morning (4 hours)
- [ ] Implement conformal prediction wrapper (MAPIE)
- [ ] Calibrate on validation set
- [ ] Verify coverage: target 90% +/- 5%
- [ ] Adjust alpha if needed

### Afternoon (4 hours)
- [ ] Implement SHAP explainability
- [ ] Compute global feature importance
- [ ] Generate local explanations for sample predictions
- [ ] Save SHAP values

### Deliverable: Calibrated prediction intervals + SHAP explanations

---

## DAY 11: Full System Integration

### Morning (4 hours)
- [ ] Integrate all 5 tiers into `HantaSTPINNFM`
- [ ] Implement end-to-end forward pass
- [ ] Verify multi-objective loss computation
- [ ] Test on single batch

### Afternoon (4 hours)
- [ ] Run full training with curriculum learning
- [ ] Monitor all loss components: data, ODE, FM, spatial, calib
- [ ] Verify adaptive loss weighting works
- [ ] Save checkpoints at each curriculum stage

### Deliverable: Fully integrated model, training in progress

---

## DAY 12: Hyperparameter Optimization

### Morning (4 hours)
- [ ] Set up Optuna study
- [ ] Define search space (see framework Section 6.2)
- [ ] Run 100 trials with TPE sampler
- [ ] Prune unpromising trials

### Afternoon (4 hours)
- [ ] Analyze HPO results
- [ ] Identify best hyperparameter set
- [ ] Retrain with best config
- [ ] Save final model

### Deliverable: Optimized hyperparameters + final trained model

---

## DAY 13: Evaluation Suite

### Morning (4 hours)
- [ ] Run temporal CV (5-fold leave-one-year-out)
- [ ] Run spatial CV (leave-one-region-out)
- [ ] Run OOD stress test (El Nino years)
- [ ] Compute all metrics: WIS, CRPS, MAE, coverage, Brier

### Afternoon (4 hours)
- [ ] Run Diebold-Mariano tests vs all baselines
- [ ] Run Clarke tests for pairwise dominance
- [ ] Run Model Confidence Set (Hansen et al.)
- [ ] Generate reliability diagrams and PIT histograms

### Deliverable: Complete evaluation report with statistical tests

---

## DAY 14: Ablation Studies

### Morning (4 hours)
- [ ] Run ablation: remove PINN
- [ ] Run ablation: remove FM
- [ ] Run ablation: remove ST-GAT
- [ ] Run ablation: remove physics constraint

### Afternoon (4 hours)
- [ ] Run ablation: remove sex structure
- [ ] Run ablation: remove conformal UQ
- [ ] Compute WIS delta for each ablation
- [ ] Generate ablation bar chart (Fig 7)

### Deliverable: Ablation results table + figure

---

## DAY 15: Figure Generation

### Morning (4 hours)
- [ ] Generate Fig 1: Architecture diagram
- [ ] Generate Fig 2: SEIR dynamics + phase portrait
- [ ] Generate Fig 3: Spatial risk map
- [ ] Generate Fig 4: Forecast comparison

### Afternoon (4 hours)
- [ ] Generate Fig 5: Calibration plots
- [ ] Generate Fig 6: SHAP importance
- [ ] Generate Fig 7: Ablation chart
- [ ] Generate Fig 8: Attention weights

### Evening (2 hours)
- [ ] Review all figures at 300 DPI
- [ ] Ensure colorblind-friendly palettes
- [ ] Ensure grayscale compatibility
- [ ] Save final versions

### Deliverable: 8 publication-ready figures

---

## DAY 16: Manuscript Writing

### Morning (4 hours)
- [ ] Write Introduction (1,500 words)
- [ ] Write Methods: Mathematical model (1,000 words)
- [ ] Write Methods: Architecture (1,000 words)

### Afternoon (4 hours)
- [ ] Write Methods: Data & Training (1,000 words)
- [ ] Write Methods: Validation (1,000 words)
- [ ] Write Results: Baseline comparison (800 words)

### Deliverable: Draft manuscript (Sections 1-3)

---

## DAY 17: Manuscript Writing Continued

### Morning (4 hours)
- [ ] Write Results: Ablation + Calibration (800 words)
- [ ] Write Results: Spatial risk maps (600 words)
- [ ] Write Results: Sensitivity analysis (600 words)

### Afternoon (4 hours)
- [ ] Write Discussion (2,000 words)
- [ ] Write Conclusion (500 words)
- [ ] Write Abstract (250 words)

### Deliverable: Complete manuscript draft

---

## DAY 18: Manuscript Polish & Submission Prep

### Morning (4 hours)
- [ ] Internal review: read full manuscript aloud
- [ ] Check all figure references
- [ ] Check all table references
- [ ] Verify all citations in references.bib
- [ ] Compile LaTeX: fix errors

### Afternoon (4 hours)
- [ ] Write Data Availability statement
- [ ] Write Code Availability statement
- [ ] Write Competing Interests statement
- [ ] Write Author Contributions
- [ ] Final proofread

### Evening (2 hours)
- [ ] Prepare supplementary materials
- [ ] Check journal submission guidelines
- [ ] Format for target journal

### Deliverable: Submission-ready manuscript

---

## DAY 19: Code Release & Reproducibility

### Morning (4 hours)
- [ ] Final code review: type hints, docstrings, comments
- [ ] Run full test suite: `pytest tests/ -v --cov`
- [ ] Verify coverage > 80%
- [ ] Fix any failing tests

### Afternoon (4 hours)
- [ ] Build Docker image: `docker build -t hantavirus-predictor .`
- [ ] Test Docker image: `docker run --gpus all hantavirus-predictor`
- [ ] Push to Docker Hub
- [ ] Create GitHub release: v1.0.0

### Evening (2 hours)
- [ ] Create Zenodo archive with DOI
- [ ] Update README with final results
- [ ] Update CITATION.cff

### Deliverable: Public code release with DOI

---

## DAY 20: Final QA & Submission

### Morning (4 hours)
- [ ] Run complete pipeline end-to-end on clean environment
- [ ] Verify all outputs reproducible from README instructions
- [ ] Check all links in manuscript
- [ ] Verify figure quality at 300 DPI

### Afternoon (4 hours)
- [ ] Submit to target journal (Nature Communications)
- [ ] Upload manuscript + figures + supplementary
- [ ] Confirm submission receipt
- [ ] Set up submission tracking

### Deliverable: SUBMITTED MANUSCRIPT

---

## POST-SUBMISSION (Ongoing)

- [ ] Monitor peer review status
- [ ] Prepare revision responses
- [ ] Address reviewer comments
- [ ] Update code based on reviewer feedback
- [ ] Publish final version
- [ ] Promote on social media / academic networks
- [ ] Present at conferences

---

## RISK MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Data access denied | Low | High | Use public data only; have backup sources |
| ODE solver unstable | Medium | Medium | Reduce step size; use adaptive methods |
| GPU OOM | Medium | Medium | Gradient checkpointing; reduce batch size |
| Foundation model unavailable | Low | High | Use Chronos as backup; or skip FM tier |
| Poor validation metrics | Medium | High | Extend synthetic data; adjust loss weights |
| Reviewer rejects novelty | Low | High | Emphasize 6-pillar scarcity mitigation |
| Timeline slip | Medium | Medium | Parallelize Days 6-10; use multiple GPUs |

---

*This checklist is designed for a team of 2-3 coding agents working in parallel. Adjust timeline based on team size and GPU availability.*
