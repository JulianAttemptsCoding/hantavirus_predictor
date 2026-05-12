# HANTA-PINN: Physics-Informed Neural Network for Hantavirus Prediction

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.2+](https://img.shields.io/badge/pytorch-2.2+-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Physics-Informed Neural Network (PINN) for predicting hantavirus reservoir dynamics and deriving human spillover risk.

## Overview

HANTA-PINN addresses the fundamental challenge of hantavirus modeling -- extreme data scarcity on the human side (~30 cases/year) -- by pivoting to the reservoir side, where 14,000+ seroprevalence samples from NEON provide abundant training data.

**Key Innovation:** Embedding a sex-structured SEIR compartmental model as differentiable constraints within a neural network.

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/hanta-pinn.git
cd hanta-pinn

# Create environment
conda env create -f environment.yml
conda activate hanta-pinn

# Generate synthetic pretraining data
python scripts/generate_synthetic.py --n 10000

# Train model
python scripts/train.py --config config/train.yaml --seed 42

# Evaluate
python scripts/evaluate.py --model_path best_model.pt --test_data data/processed/test.pt
```

## Architecture

```
[NDVI, Precip, Temp, ENSO] (24-month history)
           |
           v
   EnvironmentalEncoder (1D-CNN + LSTM)
           |
           v
        K(t) > 0
           |
    +------+------+
    |             |
    v             v
 PINN Core    [t_normalized]
 (5-layer     |
  MLP, 128    v
  hidden)   PINN Core
    |       (continued)
    v         |
 [S_m,E_m,   v
  I_m,R_m,  [beta_m, beta_mf,
  S_f,E_f,   beta_f, gamma]
  I_f,R_f]
    |             |
    +------+------+
           |
           v
    SpilloverDecoder
           |
           v
    lambda_H(t) -> E[Cases]
```

## Repository Structure

```
hanta-pinn/
|-- config/           # Model, data, and training configs
|-- src/              # Source code
|   |-- models/       # Neural network modules
|   |-- physics/      # SEIR ODE and synthetic generation
|   |-- training/     # Training loop
|   |-- evaluation/   # Metrics and validation
|   |-- utils/        # Reproducibility utilities
|-- scripts/          # Training and evaluation scripts
|-- tests/            # Unit tests
|-- reports/          # Comprehensive QA and validation reports
|-- notebooks/        # Jupyter notebooks for exploration
```

## Data Sources

| Dataset | Source | Use |
|---------|--------|-----|
| NEON Rodent Pathogen | DP1.10064.001 | Primary training target (seroprevalence) |
| NEON Small Mammal | DP1.10072.001 | Trap success proxy |
| MODIS NDVI | NASA LP DAAC | Vegetation / carrying capacity proxy |
| ERA5-Land | Copernicus CDS | Climate variables |
| CHIRPS | USGS/UCSB | Precipitation |
| CDC NNDSS | CDC WONDER | Human case validation |
| CDC SVI | CDC ATSDR | Socioeconomic risk factors |

## Validation

- **Temporal CV:** Train 2014-2017, Val 2018, Test 2019
- **Spatial CV:** Leave-one-NEON-domain-out (18 folds)
- **Metrics:** RMSE, MAE, R2, WIS, CRPS, ROC-AUC, ECE
- **Statistical Tests:** Diebold-Mariano, Clarke, KS, Shapiro-Wilk, Ljung-Box
- **Uncertainty:** MC Dropout, Deep Ensembles, Conformal Prediction (MAPIE)

## Citation

```bibtex
@article{hanta_pinn_2026,
  title={HANTA-PINN: A Physics-Informed Neural Network for Climate-Driven Hantavirus Reservoir Dynamics},
  author={[Authors]},
  journal={PLOS Computational Biology},
  year={2026}
}
```

## License

MIT License. See LICENSE file.

## Contact

For questions or collaboration inquiries, please open an issue.
