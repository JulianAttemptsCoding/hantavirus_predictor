#!/usr/bin/env python3
"""Training script for HantaST-PINN-FM."""

import argparse
import yaml
import torch
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping, LearningRateMonitor
from pytorch_lightning.loggers import WandbLogger

from src.training.trainer import HantaSTPINNFMModule
from src.data.pipeline import load_data


def parse_args():
    parser = argparse.ArgumentParser(description="Train HantaST-PINN-FM")
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--gpus", type=int, default=1)
    parser.add_argument("--precision", type=int, default=16, choices=[16, 32, 64])
    parser.add_argument("--resume", type=str, default=None)
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    pl.seed_everything(42, workers=True)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    print("Loading data...")
    train_loader, val_loader, test_loader = load_data(config["data"])

    if args.debug:
        train_loader = [next(iter(train_loader))]
        val_loader = [next(iter(val_loader))]

    print("Initializing model...")
    model = HantaSTPINNFMModule(config["model"], config["training"])

    checkpoint_cb = ModelCheckpoint(
        dirpath="outputs/checkpoints",
        filename="hanta-{epoch:02d}-{val_wis:.4f}",
        monitor="val_wis", mode="min", save_top_k=3, save_last=True
    )
    early_stop_cb = EarlyStopping(
        monitor="val_wis", patience=config["training"].get("patience", 30), mode="min"
    )

    wandb_logger = WandbLogger(
        project="hantavirus-predictor",
        name=config.get("experiment_name", "hanta-default"),
        log_model=True
    )

    trainer = pl.Trainer(
        max_epochs=config["training"]["max_epochs"],
        accelerator="gpu", devices=args.gpus,
        strategy="ddp" if args.gpus > 1 else "auto",
        precision=args.precision,
        gradient_clip_val=config["training"].get("gradient_clipping", 1.0),
        callbacks=[checkpoint_cb, early_stop_cb, LearningRateMonitor()],
        logger=wandb_logger
    )

    print("Starting training...")
    trainer.fit(model, train_dataloaders=train_loader, val_dataloaders=val_loader, ckpt_path=args.resume)

    print("Running test...")
    trainer.test(model, dataloaders=test_loader, ckpt_path="best")

    trainer.save_checkpoint("outputs/checkpoints/hantast_pinn_fm_final.ckpt")
    wandb_logger.experiment.finish()


if __name__ == "__main__":
    main()
