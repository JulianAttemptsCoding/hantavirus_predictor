"""Create first-pass baseline skill and calibration figures."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METRICS = ROOT / "data" / "processed" / "international_baseline_metrics.csv"
DEFAULT_PREDICTIONS = ROOT / "data" / "processed" / "international_baseline_predictions.csv"
DEFAULT_CASES = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_OUTPUT = ROOT / "figures"


def _load_wide_predictions(predictions_path: Path, cases_path: Path) -> pd.DataFrame:
    predictions = pd.read_csv(predictions_path)
    predictions["target_year"] = predictions["forecast_date"].str.slice(0, 4).astype(int) + 1
    wide = (
        predictions.pivot_table(
            index=["target_year", "iso3", "location", "syndrome", "source_system", "model"],
            columns="quantile",
            values="value",
            aggfunc="first",
        )
        .reset_index()
        .rename(columns={0.05: "q05", 0.5: "q50", 0.95: "q95"})
    )
    cases = pd.read_csv(cases_path)[["iso3", "year", "cases"]].rename(
        columns={"year": "target_year", "cases": "observed"}
    )
    return wide.merge(cases, on=["iso3", "target_year"], how="left", validate="many_to_one")


def _plot_skill(metrics: pd.DataFrame, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    for year, group in metrics.groupby("target_year"):
        group = group.sort_values("mean_wis")
        ax.plot(group["model"], group["mean_wis"], marker="o", label=str(year))
    ax.set_ylabel("Mean WIS")
    ax.set_xlabel("Model")
    ax.set_title("International baseline forecast skill")
    ax.tick_params(axis="x", rotation=35, labelsize=8)
    ax.legend(title="Target year")
    fig.tight_layout()
    fig.savefig(output / "international_baseline_mean_wis.png", dpi=300)
    plt.close(fig)


def _plot_observed_vs_predicted(wide: pd.DataFrame, output: Path) -> None:
    test_year = int(wide["target_year"].max())
    candidates = wide[wide["target_year"] == test_year]
    model_scores = (
        (candidates["observed"] - candidates["q50"])
        .abs()
        .groupby(candidates["model"])
        .mean()
        .sort_values()
    )
    model = str(model_scores.index[0])
    plot_data = candidates[candidates["model"] == model]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(plot_data["q50"], plot_data["observed"], alpha=0.8)
    max_value = max(float(plot_data["q50"].max()), float(plot_data["observed"].max()))
    ax.plot([0, max_value], [0, max_value], color="black", linewidth=1)
    ax.set_xlabel("Predicted median cases")
    ax.set_ylabel("Observed cases")
    ax.set_title(f"{test_year} observed vs predicted: {model}")
    fig.tight_layout()
    fig.savefig(output / "international_baseline_observed_vs_predicted.png", dpi=300)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    metrics = pd.read_csv(args.metrics)
    wide = _load_wide_predictions(Path(args.predictions), Path(args.cases))
    _plot_skill(metrics, output)
    _plot_observed_vs_predicted(wide, output)
    print(f"Wrote baseline figures to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
