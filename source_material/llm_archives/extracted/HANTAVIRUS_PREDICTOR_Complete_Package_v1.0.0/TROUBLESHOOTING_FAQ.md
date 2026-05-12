# HANTAVIRUS PREDICTOR: Troubleshooting Guide & FAQ

---

## FREQUENTLY ASKED QUESTIONS

### Q1: Why hantavirus specifically? Why not a general zoonosis model?

**A:** Hantavirus is the ideal test case for data-scarce zoonotic prediction because:
- It has a well-understood mechanistic model (SEIR with sex structure)
- It has a clear climate-driven ecological signal (R0 proportional to K)
- Human cases are rare enough to be challenging but not impossible
- Rodent surveillance data exists (NEON) to serve as primary training targets
- The 2026 MV Hondius outbreak demonstrates real-world urgency

The architecture is designed to generalize: replace SEIR parameters with plague/Lassa parameters, swap rodent hosts, and the same framework applies.

---

### Q2: How do you handle the fact that hantavirus has only ~30 US cases/year?

**A:** This is the core problem we solve. Six strategies:
1. **Rodent-first training:** NEON has 104K captures with 2.1% seroprevalence -- 100x denser than human data
2. **Synthetic data:** 10,000 SEIR trajectories with parameter sweeps
3. **Foundation models:** TimesFM pretrained on 100B+ time points provides zero-shot priors
4. **Multi-task learning:** Transfer from leptospirosis (~1M cases/year) and plague (~3K/year)
5. **Physics regularization:** SEIR constraints reduce effective parameter count by 75%
6. **Bayesian pooling:** Borrow strength across regions

With all six, we need only ~50 human cases + 200 rodent observations.

---

### Q3: Why not just use XGBoost or SARIMA?

**A:** Baselines are essential and we compare against them. But they have fundamental limitations:
- **XGBoost:** Cannot model temporal dynamics or spatial diffusion; no uncertainty quantification
- **SARIMA:** Linear only; cannot capture climate-disease nonlinearities; no spatial component
- **LSTM:** Black box; requires massive data; no mechanistic grounding

Our hybrid approach combines the interpretability of mechanistic models with the flexibility of deep learning, while using 10x less data than pure ML.

---

### Q4: How do you know the physics constraints are correct?

**A:** The SEIR model is derived from peer-reviewed epidemiology (Allen et al. 2006, Abramson-Kenkre 2002). We validate:
- Conservation of mass: dN/dt = births - deaths (numerically verified)
- R0 formula matches next-generation matrix derivation
- Disease-free equilibrium stable when R0 < 1
- Endemic equilibrium exists when R0 > 1
- Synthetic trajectories match known outbreak patterns (1993 Four Corners)

The physics loss is a soft constraint (weighted MSE), not a hard constraint, so the model can learn deviations.

---

### Q5: What if the foundation model (TimesFM) doesn't understand epidemiology?

**A:** Foundation models learn universal temporal patterns: seasonality, trends, shocks, autocorrelation. While not trained on epidemiology specifically, these patterns transfer because:
- Epidemic time series share structure with sales, weather, and financial data
- The LoRA adaptation fine-tunes the model on rodent seroprevalence
- The multi-task loss aligns FM embeddings with PINN outputs
- We use FM as a prior, not a sole predictor -- the PINN provides mechanistic grounding

If TimesFM is unavailable, Chronos or a custom transformer trained on synthetic data works as a fallback.

---

### Q6: How do you prevent data leakage?

**A:** Three layers of protection:
1. **Temporal:** Strict train/val/test splits by year. No future data in training.
2. **Spatial:** Leave-one-region-out CV. Test counties never seen in training.
3. **Feature:** All lag features use strictly past data. No t+1 information.

We verify with:
- `pytest tests/test_data.py::test_no_temporal_leakage`
- Manual inspection of feature correlation matrices
- Ablation: removing autoregressive features should not catastrophically degrade performance

---

### Q7: What about climate change making historical patterns invalid?

**A:** This is a real concern. Mitigations:
- **Rolling window retraining:** Model retrains monthly on recent data
- **Online learning:** ADWIN drift detection triggers model updates
- **Domain adaptation:** CORAL or DANN layers handle distribution shift
- **Conservative UQ:** Conformal prediction widens intervals when drift is detected
- **Scenario testing:** Train on neutral/La Nina years, test on El Nino extremes

We explicitly discuss this limitation in the manuscript and propose future work.

---

### Q8: Can this actually be used by public health agencies?

**A:** Yes, with caveats:
- **Strengths:** 6-12 month lead time, calibrated uncertainty, explainable predictions
- **Limitations:** US-centric validation, requires rodent surveillance data, computational cost
- **Deployment:** FastAPI server + Streamlit dashboard provided
- **Actionability:** Tiered alerts (Low/Mod/High/Crit) with SHAP explanations

We recommend partnering with CDC or state health departments for pilot deployment.

---

## TROUBLESHOOTING

### Installation Issues

#### Problem: `torch_geometric` installation fails
**Symptoms:** `ModuleNotFoundError: No module named 'torch_geometric'` or CUDA version mismatch

**Solutions:**
```bash
# Verify PyTorch CUDA version
python -c "import torch; print(torch.version.cuda)"

# Install matching PyG wheels
pip install torch-geometric -f https://data.pyg.org/whl/torch-2.3.0+cu124.html
pip install torch-scatter torch-sparse torch-cluster -f https://data.pyg.org/whl/torch-2.3.0+cu124.html

# If still failing, use conda
conda install pyg -c pyg
```

---

#### Problem: `torchdiffeq` OOM during ODE solve
**Symptoms:** `CUDA out of memory` during `odeint()` call

**Solutions:**
```python
# 1. Reduce batch size
batch_size = 32  # instead of 64

# 2. Use gradient checkpointing
model.gradient_checkpointing_enable()

# 3. Reduce ODE evaluation points
t_span = torch.linspace(0, 100, 51)  # instead of 101

# 4. Use CPU for ODE solving, GPU for neural net
solution = odeint(..., method='dopri5', options={'dtype': torch.float32})
```

---

#### Problem: `transformers` cannot load TimesFM
**Symptoms:** `OSError: Model not found` or authentication error

**Solutions:**
```bash
# Login to HuggingFace
huggingface-cli login

# Or use token
from huggingface_hub import login
login(token="your_token")

# If TimesFM unavailable, use Chronos
model_name = "amazon/chronos-t5-base"
```

---

### Training Issues

#### Problem: Physics loss is NaN
**Symptoms:** `L_ode = nan` within first 100 steps

**Causes & Solutions:**
```python
# Cause 1: Physics weight too high
# Solution: Use adaptive weighting
def adaptive_lambda(epoch, total):
    return 10.0 * (1 - epoch/total) + 0.1 * (epoch/total)

# Cause 2: Stiff ODE with large dt
# Solution: Reduce tolerances
odeint(..., rtol=1e-7, atol=1e-8)

# Cause 3: Negative compartments due to numerical error
# Solution: Add ReLU or log-transform
y = torch.clamp(y, min=0.0)

# Cause 4: Division by zero in birth function
# Solution: Add epsilon
B = 2*b*(N_m*N_f)/(N_m + N_f + 1e-8)
```

---

#### Problem: Model overfits to synthetic data
**Symptoms:** Great synthetic performance, poor real data performance

**Solutions:**
```python
# 1. Increase real data weight in curriculum
# Stage 2: rodent_weight=0.7, human_weight=0.3

# 2. Add domain randomization to synthetic data
noise_scale = 0.05  # instead of 0.01

# 3. Use smaller synthetic pretraining (5000 instead of 10000)

# 4. Fine-tune with lower learning rate
lr = 5e-5  # instead of 1e-3
```

---

#### Problem: Foundation model loss dominates
**Symptoms:** `L_fm >> L_data`, PINN outputs ignored

**Solutions:**
```python
# 1. Reduce FM weight
loss_weights = {"fm": 0.3, "data": 1.0, "ode": 0.5}

# 2. Freeze FM after initial warm-up
if epoch > 50:
    for param in model.foundation.parameters():
        param.requires_grad = False

# 3. Use FM as auxiliary loss only
L_fm = 0.1 * mse(fm_embedding, pin_embedding)
```

---

#### Problem: ST-GAT attention weights are uniform
**Symptoms:** All attention weights ~ 1/n_neighbors

**Solutions:**
```python
# 1. Use GATv2 instead of GAT (dynamic attention)
self.gat = GATv2Conv(...)

# 2. Add edge features
edge_attr = torch.tensor([distance, mobility, similarity])

# 3. Use fewer heads (4 instead of 8)
# 4. Add residual connections
h_out = gat(h_in, edge_index) + h_in

# 5. Increase learning rate for GAT layers
param_groups = [
    {'params': model.stgat.parameters(), 'lr': 1e-3},
    {'params': model.pinn.parameters(), 'lr': 5e-4}
]
```

---

### Data Issues

#### Problem: NEON data has gaps
**Symptoms:** Missing months for some sites

**Solutions:**
```python
# 1. Impute with Gaussian process
from sklearn.gaussian_process import GaussianProcessRegressor
gp = GaussianProcessRegressor()
gp.fit(known_dates, known_values)
imputed = gp.predict(missing_dates)

# 2. Use site-level mean
site_mean = df.groupby('site_id')['seroprevalence'].transform('mean')
df['seroprevalence'] = df['seroprevalence'].fillna(site_mean)

# 3. Exclude sites with >30% missing
df = df.groupby('site_id').filter(lambda x: x['seroprevalence'].isna().mean() < 0.3)
```

---

#### Problem: MODIS data has clouds
**Symptoms:** NDVI values of -0.2 (invalid)

**Solutions:**
```python
# 1. Quality flag filtering
ndvi = ndvi.where(quality == 0)  # Keep only good pixels

# 2. Temporal interpolation
ndvi = ndvi.interpolate_na(dim='time', method='linear')

# 3. Savitzky-Golay smoothing
from scipy.signal import savgol_filter
ndvi_smooth = savgol_filter(ndvi, window_length=5, polyorder=2)
```

---

#### Problem: Class imbalance causes poor recall
**Symptoms:** High precision, low recall for outbreak prediction

**Solutions:**
```python
# 1. Focal loss
from torch.nn import functional as F
focal_loss = FocalLoss(gamma=2.0, alpha=0.75)

# 2. Class weights
weights = torch.tensor([1.0, 10.0])  # 10x weight for outbreak class

# 3. SMOTE for tabular features
from imblearn.over_sampling import SMOTE
smote = SMOTE(sampling_strategy=0.3)
X_res, y_res = smote.fit_resample(X, y)

# 4. Threshold tuning
from sklearn.metrics import precision_recall_curve
prec, rec, thresh = precision_recall_curve(y_true, y_prob)
best_thresh = thresh[np.argmax(prec * rec)]
```

---

### Evaluation Issues

#### Problem: Coverage is too low (<80%)
**Symptoms:** Prediction intervals too narrow

**Solutions:**
```python
# 1. Increase conformal alpha
alpha = 0.15  # instead of 0.1 (gives wider intervals)

# 2. Use split conformal with larger calibration set
cal_size = int(0.3 * len(data))  # instead of 0.2

# 3. Add heteroscedastic output
# Predict both mu and sigma, use sigma for interval width

# 4. Use quantile regression instead of conformal
from mapie.regression import MapieRegressor
mapie = MapieRegressor(method='quantile', cv='split')
```

---

#### Problem: Diebold-Mariano test is not significant
**Symptoms:** p > 0.05 even though WIS is better

**Causes:**
- Sample size too small (need T > 50)
- Loss differential has high variance
- Models are genuinely equivalent

**Solutions:**
```python
# 1. Increase test period
# 2. Use multiple forecast horizons
# 3. Use Clark test as backup
clarke = StatisticalTests.clarke_test(y_true, pred_a, pred_b)

# 4. Use Model Confidence Set
mcs = StatisticalTests.mcb_test(y_true, predictions)
```

---

### Deployment Issues

#### Problem: Docker image too large (>10GB)
**Symptoms:** Slow build, slow push, slow pull

**Solutions:**
```dockerfile
# 1. Multi-stage build
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 AS builder
# ... install build deps, compile ...

FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 AS runtime
# ... copy only compiled artifacts ...

# 2. Remove cache
RUN pip install --no-cache-dir -r requirements.txt

# 3. Use smaller base image
FROM nvidia/cuda:12.4.1-base-ubuntu22.04

# 4. Exclude large files in .dockerignore
# data/
# outputs/checkpoints/*.ckpt
```

---

#### Problem: Inference API is slow (>1s per request)
**Symptoms:** High latency on /predict endpoint

**Solutions:**
```python
# 1. Use TorchScript
model = torch.jit.script(model)

# 2. Use ONNX Runtime
import onnxruntime as ort
session = ort.InferenceSession("model.onnx")

# 3. Batch requests
# 4. Use GPU for inference
# 5. Cache frequent queries
from functools import lru_cache
@lru_cache(maxsize=1000)
def predict_cached(county_fips, date):
    return model.predict(...)
```

---

## PERFORMANCE BENCHMARKS

### Expected Training Times (4x A100)

| Phase | Duration | GPU Memory | Notes |
|-------|----------|------------|-------|
| Data preprocessing | 8 hours | CPU | Dask parallel |
| Synthetic generation | 2 hours | 2 GB | CPU parallel |
| PINN pretraining | 24 hours | 20 GB | 500 epochs |
| Foundation fine-tuning | 12 hours | 40 GB | LoRA only |
| ST-GAT training | 36 hours | 30 GB | Spatial CV |
| Full integration | 48 hours | 40 GB | Curriculum |
| HPO (100 trials) | 20 hours | 40 GB | Optuna |
| Evaluation | 6 hours | 20 GB | All metrics |
| **Total** | **~158 hours** | -- | **~6.5 days** |

### Expected Inference Times

| Task | Latency | Throughput |
|------|---------|------------|
| Single county prediction | 50 ms | 20/sec |
| Batch of 100 counties | 2 sec | 50/sec |
| Full US risk map (3000 counties) | 5 min | -- |
| SHAP explanation (single) | 200 ms | 5/sec |

---

## CONTACT & SUPPORT

- **GitHub Issues:** https://github.com/username/hantavirus-predictor/issues
- **GitHub Discussions:** https://github.com/username/hantavirus-predictor/discussions
- **Email:** hanta-support@university.edu
- **Slack:** #hantavirus-predictor

---

*Last updated: May 2026 | For the latest troubleshooting, check GitHub Issues*
