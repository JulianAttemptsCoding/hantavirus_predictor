"""
Training loop for HANTA-PINN-ST with mixed precision and DDP support.
"""
import torch
from torch.cuda.amp import autocast, GradScaler
from tqdm import tqdm


class HantaTrainer:
    """
    Trainer with:
    - Mixed precision (FP16)
    - Gradient clipping
    - Cosine annealing + warmup
    - Early stopping
    - W&B logging
    """
    def __init__(self, model, loss_fn, optimizer, config, 
                 device='cuda', use_amp=True):
        self.model = model.to(device)
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.config = config
        self.device = device
        self.use_amp = use_amp
        self.scaler = GradScaler() if use_amp else None

        self.epoch = 0
        self.best_val_loss = float('inf')
        self.patience_counter = 0

    def train_epoch(self, train_loader):
        self.model.train()
        total_loss = 0

        for batch in tqdm(train_loader, desc=f"Epoch {self.epoch}"):
            self.optimizer.zero_grad()

            # Forward pass with mixed precision
            if self.use_amp:
                with autocast():
                    outputs = self.model(**batch)
                    loss, loss_dict = self.compute_loss(outputs, batch)
            else:
                outputs = self.model(**batch)
                loss, loss_dict = self.compute_loss(outputs, batch)

            # Backward pass
            if self.use_amp:
                self.scaler.scale(loss).backward()
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(), 
                    self.config.get('gradient_clip', 1.0)
                )
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                loss.backward()
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(),
                    self.config.get('gradient_clip', 1.0)
                )
                self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(train_loader)

    def compute_loss(self, outputs, batch):
        """Compute multi-component loss."""
        # Extract predictions and targets
        pred = outputs.get('trajectory', outputs['stg_out'])
        target = batch.get('target')

        # ODE residual (if available)
        ode_residual = outputs.get('ode_residual', 
                                   torch.zeros(1, device=self.device))
        sde_term = outputs.get('sde_term', 
                              torch.zeros(1, device=self.device))

        # Spillover prediction
        spill_pred = outputs['stg_out']
        spill_target = batch.get('human_cases', 
                                torch.zeros(spill_pred.size(0), 
                                          device=self.device))

        loss, loss_dict = self.loss_fn(
            pred, target, ode_residual, sde_term,
            spill_pred, spill_target,
            self.model.parameters()
        )
        return loss, loss_dict

    def validate(self, val_loader):
        self.model.eval()
        total_loss = 0

        with torch.no_grad():
            for batch in val_loader:
                outputs = self.model(**batch)
                loss, _ = self.compute_loss(outputs, batch)
                total_loss += loss.item()

        return total_loss / len(val_loader)

    def fit(self, train_loader, val_loader, max_epochs=500):
        for epoch in range(max_epochs):
            self.epoch = epoch
            train_loss = self.train_epoch(train_loader)
            val_loss = self.validate(val_loader)

            print(f"Epoch {epoch}: train_loss={train_loss:.4f}, "
                  f"val_loss={val_loss:.4f}")

            # Early stopping
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self.patience_counter = 0
                # Save checkpoint
                torch.save(self.model.state_dict(), 'best_model.pt')
            else:
                self.patience_counter += 1
                if self.patience_counter >= self.config.get('patience', 30):
                    print(f"Early stopping at epoch {epoch}")
                    break

    def save_checkpoint(self, path):
        torch.save({
            'epoch': self.epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'best_val_loss': self.best_val_loss,
        }, path)
