# HANTA-PINN-ST Implementation Guide
**For Coding Agents & Developers**

---

## Phase 1: Environment Setup (Week 1)

### 1.1 Hardware Requirements
- **Minimum:** 1x NVIDIA A100 (40GB), 64GB RAM
- **Recommended:** 4x NVIDIA A100 (80GB), 256GB RAM
- **Storage:** 2TB SSD (MODIS rasters are large)

### 1.2 Software Stack
```bash
# Ubuntu 22.04
# CUDA 12.4
# Python 3.10

pip install torch==2.3.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

### 1.3 Data Access Setup
```bash
# NASA Earthdata (for MODIS)
# Create account at: https://urs.earthdata.nasa.gov/
# Save credentials to ~/.netrc

# Copernicus CDS (for ERA5)
# Create account at: https://cds.climate.copernicus.eu/
# Save API key to ~/.cdsapirc

# NEON (free, no key needed)
# SafeGraph (academic application required)
```

## Phase 2: Data Pipeline (Weeks 1-2)

### 2.1 Priority Order
1. **Synthetic data** (no external dependencies)
2. **NEON rodent data** (public, immediate)
3. **CDC case data** (public, manual download)
4. **MODIS/ERA5** (requires API keys)
5. **Transfer data** (dengue/lepto from SINAN)

### 2.2 Synthetic Data First
```python
# Start here - zero external dependencies
from src.data.synthetic_generator import SyntheticHantaGenerator

gen = SyntheticHantaGenerator(n_trajectories=50000, seed=42)
trajs = gen.generate()
val = gen.validate(trajs)

# Save for pre-training
torch.save(trajs, 'data/processed/synthetic_trajectories.pt')
```

### 2.3 Feature Engineering Pipeline
```python
from src.features.build_features import FeatureEngineer

fe = FeatureEngineer(lag_windows=[6, 12, 18, 24])

# Climate anomalies
ndvi_anom = fe.climate_anomalies(df, 'ndvi')
precip_anom = fe.climate_anomalies(df, 'precip')

# Carrying capacity proxy
K_proxy = fe.carrying_capacity_proxy(ndvi_anom, precip_anom, temp_anom)

# Human exposure
exposure = fe.human_exposure_index(svi, rural_pct, housing_age, road_density)
```

## Phase 3: Model Development (Weeks 3-8)

### 3.1 Development Order
1. **PINN Core** (most critical, most complex)
2. **Climate Encoder** (standard 3D CNN)
3. **Temporal Encoder** (standard Transformer)
4. **ST-GNN** (PyG integration)
5. **Fusion & Output Heads**

### 3.2 PINN Core Debugging Tips
```python
# Common issues and solutions:

# 1. ODE residual not converging
# -> Reduce lr to 1e-4
# -> Increase lambda_ode weight
# -> Check for NaN in state derivatives

# 2. Negative compartments
# -> Add ReLU boundary loss
# -> Clip states in forward pass
# -> Check birth/death rate balance

# 3. R0 not monotonic in K
# -> Verify density-dependent mortality
# -> Check parameter positivity (Softplus)
```

### 3.3 Multi-GPU Training
```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# Launch: torchrun --nproc_per_node=4 train.py
model = HantaPINNST(...)
model = DDP(model, device_ids=[local_rank])

# Use torch.compile for speedup
model = torch.compile(model)
```

## Phase 4: Validation (Weeks 9-12)

### 4.1 Critical Tests
```bash
# Run in this order:
pytest tests/test_physics.py -v      # Must pass first
pytest tests/test_models.py -v       # Architecture validation
pytest tests/test_integration.py -v  # End-to-end
```

### 4.2 Benchmark Comparison
```python
from src.evaluation.metrics import diebold_mariano_test

# Your model vs SARIMA
wis_pinn = compute_wis(y_true, pinn_forecasts)
wis_sarima = compute_wis(y_true, sarima_forecasts)

dm_stat, p_value = diebold_mariano_test(
    pinn_forecasts, sarima_forecasts, y_true, loss='mse'
)

assert p_value < 0.05, "Model not significantly better than baseline"
```

### 4.3 Calibration Check
```python
from src.evaluation.metrics import calibration_slope, prediction_interval_coverage

slope = calibration_slope(y_true, y_prob)
picp = prediction_interval_coverage(y_true, y_lower, y_upper)

assert 0.9 <= slope <= 1.1, f"Poor calibration: slope={slope}"
assert 0.85 <= picp <= 0.95, f"Poor coverage: PICP={picp}"
```

## Phase 5: Publication (Weeks 13-18)

### 5.1 Manuscript Checklist
- [ ] LaTeX template from target journal
- [ ] All figures at 300 DPI
- [ ] Equations numbered and referenced
- [ ] Data availability statement
- [ ] Code availability statement (GitHub + Zenodo)
- [ ] EPIFORGE checklist completed
- [ ] Supplementary info prepared

### 5.2 Code Release Checklist
- [ ] Repository public
- [ ] Docker image built and tested
- [ ] README with quickstart
- [ ] requirements.txt pinned
- [ ] DVC remote configured
- [ ] W&B project public
- [ ] License file (MIT)

## Common Pitfalls

1. **Temporal leakage:** Never use future features. Always lag by at least 6 months.
2. **Spatial leakage:** Don't mix train/test counties in same biome.
3. **Class imbalance:** Use focal loss or weighted sampling for outbreak prediction.
4. **ODE stiffness:** Use adaptive solvers (dopri5, not Euler).
5. **Memory:** Gradient checkpointing for long trajectories.

## Support

For issues:
1. Check `docs/` directory
2. Review `reports/QA_REPORT.md`
3. Open GitHub issue with minimal reproducible example
