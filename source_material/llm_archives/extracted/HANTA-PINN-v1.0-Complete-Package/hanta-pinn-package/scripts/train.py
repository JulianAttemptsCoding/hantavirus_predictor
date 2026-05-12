#!/usr/bin/env python
"""Training script for HANTA-PINN."""
import argparse
import yaml
import torch
from torch.utils.data import DataLoader, TensorDataset

from src.models.hanta_pinn import HantaPINN
from src.training.trainer import Trainer
from src.utils.seed import set_seed


def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_dummy_loaders(batch_size=64):
    """Create dummy loaders for testing. Replace with real data loaders."""
    # Dummy data shapes
    env = torch.randn(1000, 24, 4)
    t = torch.rand(1000, 1)
    human = torch.randn(1000, 5)
    seroprev = torch.rand(1000, 1) * 0.2
    cases = torch.poisson(torch.rand(1000, 1) * 2)

    dataset = TensorDataset(env, t, human, seroprev, cases)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_ds, val_ds = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    return train_loader, val_loader


def collate_fn(batch):
    """Custom collate for dict-style batches."""
    env, t, human, seroprev, cases = zip(*batch)
    return {
        'env': torch.stack(env),
        't': torch.stack(t),
        'human': torch.stack(human),
        'seroprev': torch.stack(seroprev),
        'cases': torch.stack(cases)
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config/train.yaml')
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    # Set seed
    set_seed(args.seed)

    # Load configs
    train_cfg = load_config(args.config)
    model_cfg = load_config('config/model.yaml')

    # Create model
    model = HantaPINN(
        encoder_config=model_cfg['encoder'],
        pinn_config=model_cfg['pinn_core'],
        spillover_config=model_cfg['spillover']
    )

    print(f"Model parameters: {model.count_parameters():,}")

    # Create data loaders (replace with real ones)
    train_loader, val_loader = create_dummy_loaders(
        batch_size=train_cfg['training']['batch_size']
    )

    # Train
    trainer = Trainer(model, train_cfg['training'])
    trainer.fit(
        train_loader, val_loader,
        epochs=train_cfg['training']['epochs'],
        patience=train_cfg['training']['patience']
    )

    # Save
    torch.save(model.state_dict(), 'hanta_pinn_final.pt')
    print("Training complete. Model saved.")


if __name__ == '__main__':
    main()
