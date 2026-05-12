"""
HantaST-PINN-FM: PyTorch Lightning Training Module
File: src/training/trainer.py
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping, LearningRateMonitor
from pytorch_lightning.loggers import WandbLogger
import numpy as np
from typing import Dict, Optional, Tuple
import wandb


class HantavirusDataset(Dataset):
    """Dataset for hantavirus prediction."""

    def __init__(self, 
                 climate_data: np.ndarray,      # [N, C, T, H, W]
                 case_history: np.ndarray,      # [N, T_cases]
                 seroprevalence: np.ndarray,    # [N]
                 human_cases: np.ndarray,       # [N]
                 graph_edges: np.ndarray,       # [2, E]
                 graph_weights: np.ndarray,     # [E]
                 t_span: np.ndarray,            # [T_ode]
                 y0: np.ndarray):               # [N, 8]
        self.climate = torch.FloatTensor(climate_data)
        self.cases = torch.FloatTensor(case_history)
        self.sero = torch.FloatTensor(seroprevalence)
        self.human = torch.FloatTensor(human_cases)
        self.edges = torch.LongTensor(graph_edges)
        self.weights = torch.FloatTensor(graph_weights)
        self.t_span = torch.FloatTensor(t_span)
        self.y0 = torch.FloatTensor(y0)

    def __len__(self):
        return len(self.climate)

    def __getitem__(self, idx):
        return {
            "climate": self.climate[idx],
            "cases": self.cases[idx],
            "seroprevalence": self.sero[idx],
            "human_cases": self.human[idx],
            "t_span": self.t_span,
            "y0": self.y0[idx]
        }


class HantaSTPINNFMModule(pl.LightningModule):
    """PyTorch Lightning module for HantaST-PINN-FM."""

    def __init__(self, model_config: Dict, train_config: Dict):
        super().__init__()
        self.save_hyperparameters()

        from src.models.hantast_pinn_fm import HantaSTPINNFM
        self.model = HantaSTPINNFM(model_config)

        self.train_config = train_config
        self.loss_weights = train_config["loss_weights"]

        # Metrics
        self.train_mae = []
        self.val_mae = []
        self.val_wis = []

    def forward(self, batch):
        """Forward pass."""
        from torch_geometric.data import Data

        # Create graph data
        graph_data = Data(
            x=batch["climate"].mean(dim=[2, 3, 4]).unsqueeze(1),  # Simplified
            edge_index=batch.get("edge_index", torch.zeros(2, 0, dtype=torch.long)),
            edge_attr=batch.get("edge_attr", None)
        )

        return self.model(
            climate_input=batch["climate"],
            case_history=batch["cases"],
            graph_data=graph_data,
            t_span=batch["t_span"][0],  # Same for all in batch
            y0=batch["y0"]
        )

    def training_step(self, batch, batch_idx):
        """Training step with multi-objective loss."""
        outputs = self.forward(batch)

        # Prepare targets
        targets = {
            "rodent_prevalence": batch["seroprevalence"],
            "human_cases": batch["human_cases"]
        }

        # Compute physics residual
        physics_residual = self._compute_physics_residual(batch, outputs)
        outputs["physics_residual"] = physics_residual

        # Compute loss
        loss, loss_dict = self.model.compute_loss(outputs, targets, self.train_config)

        # Log
        self.log("train_loss", loss, prog_bar=True)
        for k, v in loss_dict.items():
            self.log(f"train_{k}", v, prog_bar=False)

        # Log R0
        self.log("train_R0_mean", outputs["R0"].mean(), prog_bar=False)

        return loss

    def validation_step(self, batch, batch_idx):
        """Validation step."""
        outputs = self.forward(batch)

        targets = {
            "rodent_prevalence": batch["seroprevalence"],
            "human_cases": batch["human_cases"]
        }

        physics_residual = self._compute_physics_residual(batch, outputs)
        outputs["physics_residual"] = physics_residual

        loss, loss_dict = self.model.compute_loss(outputs, targets, self.train_config)

        # Compute metrics
        mae = F.l1_loss(outputs["forecast_mu"].squeeze(), batch["human_cases"])

        self.log("val_loss", loss, prog_bar=True)
        self.log("val_mae", mae, prog_bar=True)
        for k, v in loss_dict.items():
            self.log(f"val_{k}", v, prog_bar=False)

        return {"val_loss": loss, "val_mae": mae}

    def test_step(self, batch, batch_idx):
        """Test step with full metric computation."""
        outputs = self.forward(batch)

        # Point forecast metrics
        mae = F.l1_loss(outputs["forecast_mu"].squeeze(), batch["human_cases"])
        mse = F.mse_loss(outputs["forecast_mu"].squeeze(), batch["human_cases"])

        # Coverage (simplified - would need full quantile predictions)
        coverage = self._compute_coverage(outputs, batch)

        self.log("test_mae", mae)
        self.log("test_rmse", torch.sqrt(mse))
        self.log("test_coverage", coverage)

        return {
            "test_mae": mae,
            "test_rmse": torch.sqrt(mse),
            "test_coverage": coverage,
            "predictions": outputs["forecast_mu"].detach(),
            "targets": batch["human_cases"].detach()
        }

    def _compute_physics_residual(self, batch, outputs):
        """Compute ODE physics residual."""
        # Simplified: compute MSE between numerical derivative and analytical RHS
        seir = outputs["seir_solution"]  # [T, B, 8]

        if seir.size(0) < 3:
            return torch.tensor(0.0, device=seir.device)

        # Numerical derivative (central difference)
        dy_dt = (seir[2:] - seir[:-2]) / 2.0

        # For a proper physics residual, we'd need the analytical RHS
        # Here we use a proxy: conservation of total population
        total_pop = seir.sum(dim=-1)  # [T, B]
        pop_drift = torch.abs(total_pop[1:] - total_pop[:-1]).mean()

        return pop_drift

    def _compute_coverage(self, outputs, batch):
        """Compute empirical coverage of prediction intervals."""
        mu = outputs["forecast_mu"].squeeze()
        phi = outputs["forecast_phi"].squeeze()
        y_true = batch["human_cases"]

        # Negative binomial 90% PI
        # Approximate: mu +/- 1.645 * sqrt(mu + mu^2/phi)
        std = torch.sqrt(mu + mu**2 / (phi + 1e-8))
        lower = mu - 1.645 * std
        upper = mu + 1.645 * std

        covered = ((y_true >= lower) & (y_true <= upper)).float().mean()
        return covered

    def configure_optimizers(self):
        """Configure optimizer and scheduler."""
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.train_config["lr"],
            weight_decay=self.train_config.get("weight_decay", 1e-4),
            betas=(0.9, 0.999)
        )

        scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer,
            T_0=self.train_config.get("warmup_steps", 1000),
            T_mult=2,
            eta_min=self.train_config["lr"] * 0.01
        )

        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "interval": "step"
            }
        }


class CurriculumScheduler:
    """Curriculum learning scheduler for multi-task training."""

    def __init__(self, total_epochs: int, stages: list):
        """
        Args:
            stages: List of dicts with keys:
                - start_epoch: int
                - end_epoch: int
                - rodent_weight: float
                - human_weight: float
                - loss_weights: dict
        """
        self.total_epochs = total_epochs
        self.stages = sorted(stages, key=lambda x: x["start_epoch"])

    def get_weights(self, epoch: int) -> Dict:
        """Get loss weights for current epoch."""
        for stage in self.stages:
            if stage["start_epoch"] <= epoch < stage["end_epoch"]:
                return stage["loss_weights"]

        # Default to last stage
        return self.stages[-1]["loss_weights"]


# Example curriculum configuration
CURRICULUM_STAGES = [
    {
        "start_epoch": 0,
        "end_epoch": 50,
        "description": "Rodent-only pretraining",
        "loss_weights": {
            "data": 1.0, "ode": 10.0, "fm": 0.0,
            "spatial": 0.0, "calib": 0.0
        }
    },
    {
        "start_epoch": 50,
        "end_epoch": 100,
        "description": "Introduce human cases",
        "loss_weights": {
            "data": 1.0, "ode": 5.0, "fm": 0.1,
            "spatial": 0.05, "calib": 0.05
        }
    },
    {
        "start_epoch": 100,
        "end_epoch": 200,
        "description": "Full multi-task",
        "loss_weights": {
            "data": 1.0, "ode": 0.5, "fm": 0.3,
            "spatial": 0.1, "calib": 0.1
        }
    },
    {
        "start_epoch": 200,
        "end_epoch": 500,
        "description": "Fine-tuning with foundation model",
        "loss_weights": {
            "data": 0.5, "ode": 0.1, "fm": 1.0,
            "spatial": 0.3, "calib": 0.2
        }
    }
]
