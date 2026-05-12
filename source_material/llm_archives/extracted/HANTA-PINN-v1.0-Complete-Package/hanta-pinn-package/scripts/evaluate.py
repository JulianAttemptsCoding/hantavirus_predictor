#!/usr/bin/env python
"""Evaluation script for HANTA-PINN."""
import argparse
import torch
import numpy as np

from src.models.hanta_pinn import HantaPINN
from src.evaluation.metrics import compute_all_metrics, diebold_mariano_test


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', required=True)
    parser.add_argument('--test_data', required=True)
    args = parser.parse_args()

    # Load model
    model = HantaPINN()
    model.load_state_dict(torch.load(args.model_path))
    model.eval()

    # Load test data (implement real loader)
    # For now, dummy
    print("Evaluation complete. Implement real data loading.")


if __name__ == '__main__':
    main()
