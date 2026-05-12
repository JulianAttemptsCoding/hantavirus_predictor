#!/usr/bin/env python3
"""Evaluation script for HantaST-PINN-FM."""

import argparse
import yaml
import json
from pathlib import Path
import numpy as np

from src.evaluation.metrics import ForecastMetrics, CalibrationDiagnostics
from src.evaluation.significance import StatisticalTests


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate HantaST-PINN-FM")
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="outputs/evaluation")
    parser.add_argument("--compare_baselines", type=str, nargs="+", default=[])
    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # Load predictions (placeholder - actual implementation would load from model)
    y_true = np.load("outputs/predictions/y_true.npy")
    y_pred = np.load("outputs/predictions/y_pred.npy")
    y_lower = y_pred - 1.645 * np.std(y_pred)
    y_upper = y_pred + 1.645 * np.std(y_pred)

    print("Computing metrics...")
    metrics = ForecastMetrics.compute_all(y_true, y_pred, y_lower, y_upper)

    print("\n=== EVALUATION RESULTS ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    if args.compare_baselines:
        print("\nRunning statistical tests...")
        for baseline_path in args.compare_baselines:
            baseline_pred = np.load(baseline_path)
            dm = StatisticalTests.diebold_mariano(y_true, y_pred, baseline_pred)
            print(f"vs {baseline_path}: DM p={dm['p_value']:.4f}, significant={dm['significant']}")

    print(f"\nResults saved to {output_dir}")


if __name__ == "__main__":
    main()
