"""Training loop for HANTA-PINN."""
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from typing import Dict, Optional
import wandb


class Trainer:
    """Trainer for HANTA-PINN with physics-informed loss."""

    def __init__(self, model, config: Dict, device: str = 'cuda'):
        self.model = model.to(device)
        self.config = config
        self.device = device

        # Optimizer
        self.optimizer = AdamW(
            model.parameters(),
            lr=config.get('lr', 1e-3),
            weight_decay=config.get('weight_decay', 1e-4)
        )

        # Scheduler
        self.scheduler = CosineAnnealingLR(
            self.optimizer,
            T_max=config.get('T_max', 200)
        )

        # Loss weights
        self.alpha_data = config.get('alpha_data', 0.6)
        self.alpha_physics = config.get('alpha_physics', 0.3)
        self.alpha_reg = config.get('alpha_reg', 0.1)

        # Training state
        self.epoch = 0
        self.best_val_loss = float('inf')
        self.patience_counter = 0

    def train_epoch(self, train_loader) -> Dict[str, float]:
        self.model.train()
        total_loss = 0.0
        metrics_accum = {}

        for batch in train_loader:
            batch = {k: v.to(self.device) for k, v in batch.items()}

            self.optimizer.zero_grad()
            loss, metrics = self.model.compute_loss(
                batch,
                alpha_data=self.alpha_data,
                alpha_physics=self.alpha_physics,
                alpha_reg=self.alpha_reg
            )
            loss.backward()

            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)

            self.optimizer.step()

            total_loss += loss.item()
            for k, v in metrics.items():
                metrics_accum[k] = metrics_accum.get(k, 0.0) + v

        n = len(train_loader)
        return {k: v / n for k, v in metrics_accum.items()}

    def validate(self, val_loader) -> Dict[str, float]:
        self.model.eval()
        total_loss = 0.0
        metrics_accum = {}

        with torch.no_grad():
            for batch in val_loader:
                batch = {k: v.to(self.device) for k, v in batch.items()}
                loss, metrics = self.model.compute_loss(
                    batch,
                    alpha_data=self.alpha_data,
                    alpha_physics=self.alpha_physics,
                    alpha_reg=self.alpha_reg
                )
                total_loss += loss.item()
                for k, v in metrics.items():
                    metrics_accum[k] = metrics_accum.get(k, 0.0) + v

        n = len(val_loader)
        return {k: v / n for k, v in metrics_accum.items()}

    def fit(self, train_loader, val_loader, epochs: int = 500, 
            patience: int = 50, use_wandb: bool = True):
        """Full training loop with early stopping."""
        for epoch in range(epochs):
            self.epoch = epoch

            train_metrics = self.train_epoch(train_loader)
            val_metrics = self.validate(val_loader)

            self.scheduler.step()

            # Logging
            log_dict = {
                'epoch': epoch,
                'train_loss': train_metrics['L_total'],
                'val_loss': val_metrics['L_total'],
                **{f'train_{k}': v for k, v in train_metrics.items()},
                **{f'val_{k}': v for k, v in val_metrics.items()}
            }

            if use_wandb:
                wandb.log(log_dict)

            # Early stopping
            val_loss = val_metrics['L_total']
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self.patience_counter = 0
                # Save best model
                torch.save(self.model.state_dict(), 'best_model.pt')
            else:
                self.patience_counter += 1

            if self.patience_counter >= patience:
                print(f"Early stopping at epoch {epoch}")
                break

            if epoch % 10 == 0:
                print(f"Epoch {epoch}: train_loss={train_metrics['L_total']:.4f}, "
                      f"val_loss={val_metrics['L_total']:.4f}")

        # Load best model
        self.model.load_state_dict(torch.load('best_model.pt'))
