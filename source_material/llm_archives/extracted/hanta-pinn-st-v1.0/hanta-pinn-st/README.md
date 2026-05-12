# HANTA-PINN-ST: Physics-Informed Spatiotemporal Predictor for Hantavirus Risk

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.3+](https://img.shields.io/badge/pytorch-2.3+-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A publication-grade framework for predicting hantavirus risk using Physics-Informed Neural Networks (PINNs) with spatiotemporal Graph Neural Networks (ST-GNNs).

## Overview

Hantavirus is a data-scarce zoonotic disease (~890 US cases over 30 years). This framework addresses the data scarcity challenge through:

- **Synthetic SEIR augmentation**: 50,000 biologically plausible trajectories
- **Transfer learning**: Pre-training on dengue/leptospirosis (10,000+ city-years)
- **Rodent proxy targets**: NEON seroprevalence as primary training signal
- **Physics-informed constraints**: SEIR-SDE embedded as differentiable loss terms

## Architecture

```
Input Modality Stack
|-- Satellite/Climate: [NDVI, LST, Precip] x 24 months
|-- Tabular: [SVI, Elevation, LandCover]
|-- Time Series: [Cases, Dengue, Lepto] x 24 months
|-- Graph: [County adjacency, Mobility, Habitat]

HANTA-PINN-ST
|-- Climate Encoder (3D CNN) -> 128-dim
|-- Temporal Encoder (Transformer) -> 256-dim
|-- PINN Core (Neural ODE) -> SEIR trajectories
|-- ST-GNN (GATv2 + TCN) -> County-level forecasts
|-- Output: Negative Binomial [mu, phi] + 5 quantiles
```

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/hanta-pinn-st.git
cd hanta-pinn-st

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Or use Docker
docker build -t hanta-pinn-st .
docker run --gpus all hanta-pinn-st
```

### Generate Synthetic Data

```python
from src.data.synthetic_generator import SyntheticHantaGenerator

gen = SyntheticHantaGenerator(n_trajectories=50000, seed=42)
trajectories = gen.generate()
validation = gen.validate(trajectories)
print(validation)
```

### Train Model

```python
from src.models.pinn_core import PINNCore
from src.training.trainer import HantaTrainer
from src.training.losses import HantaLoss

model = PINNCore(env_dim=256, hidden_dim=128)
loss_fn = HantaLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

trainer = HantaTrainer(model, loss_fn, optimizer, config={})
trainer.fit(train_loader, val_loader, max_epochs=500)
```

### Run Tests

```bash
pytest tests/ --cov=src --cov-report=html
```

## Data Sources

| Source | Type | Access |
|--------|------|--------|
| CDC NNDSS | Human cases | [wonder.cdc.gov](https://wonder.cdc.gov) |
| NEON | Rodent surveillance | [data.neonscience.org](https://data.neonscience.org) |
| MODIS | NDVI/LST | [LP DAAC](https://lpdaac.usgs.gov) |
| ERA5 | Climate reanalysis | [CDS](https://cds.climate.copernicus.eu) |
| CHIRPS | Precipitation | [CHC UCSB](https://data.chc.ucsb.edu) |
| CDC SVI | Socioeconomic | [ATSDR](https://www.atsdr.cdc.gov) |

## Repository Structure

```
hanta-pinn-st/
|-- src/
|   |-- data/           # Ingestion & synthetic generation
|   |-- features/       # Feature engineering
|   |-- models/         # PINN, GNN, encoders
|   |-- training/       # Losses, trainer
|   |-- evaluation/     # Metrics, CV, calibration
|   |-- visualization/  # Maps & plots
|-- configs/            # Hydra YAML configs
|-- tests/              # pytest suite
|-- reports/            # Analysis reports
|-- notebooks/          # Jupyter notebooks
|-- docker/             # Container configs
```

## Citation

```bibtex
@article{hanta_pinn_st_2026,
  title={Physics-Informed Neural Networks for Spatiotemporal Forecasting of Hantavirus Risk Under Data Scarcity},
  journal={Nature Communications},
  year={2026}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.
