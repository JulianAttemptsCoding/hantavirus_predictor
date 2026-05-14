"""Run required first-pass international baseline forecasts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.models.international_baselines import (  # noqa: E402
    generate_baseline_forecasts,
)


DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_PREDICTIONS = ROOT / "data" / "processed" / "international_baseline_predictions.csv"
DEFAULT_METRICS = ROOT / "data" / "processed" / "international_baseline_metrics.csv"
DEFAULT_REPORT = ROOT / "reports" / "02_international_baselines.md"


def _write_report(metrics: pd.DataFrame, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    best = metrics.sort_values(["target_year", "mean_wis"]).groupby("target_year").head(1)
    lines = [
        "# International Baseline Report",
        "",
        "Status: reproducible ECDC seed benchmark.",
        "",
        "The current benchmark uses ECDC country-year reported hantavirus infection rows for "
        "2019-2023. It is sufficient to verify the modeling and QA pipeline, but not yet "
        "sufficient for final publication claims about global generalisation.",
        "",
        "## Split",
        "",
        "- Training history: all years before each target year.",
        "- Validation target: 2022.",
        "- Test target: 2023.",
        "",
        "## Metrics",
        "",
        _markdown_table(metrics),
        "",
        "## Best Model By Year",
        "",
        _markdown_table(best),
        "",
        "## QA Notes",
        "",
        "- Forecasts are quantile forecasts at 0.05, 0.50, and 0.95.",
        "- WIS uses the central 90 percent interval.",
        "- Brier score is evaluated for the pre-registered any-case threshold.",
        "- Negative results should be retained; the strongest simple baseline is the bar to beat.",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _markdown_table(data: pd.DataFrame) -> str:
    columns = list(data.columns)
    rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in data.iterrows():
        rows.append("| " + " | ".join(_format_cell(row[column]) for column in columns) + " |")
    return "\n".join(rows)


def _format_cell(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--target-years", nargs="+", type=int, default=[2022, 2023])
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    bundle = generate_baseline_forecasts(data, args.target_years)
    predictions_path = Path(args.predictions)
    metrics_path = Path(args.metrics)
    predictions_path.parent.mkdir(parents=True, exist_ok=True)
    bundle.predictions.to_csv(predictions_path, index=False)
    bundle.metrics.to_csv(metrics_path, index=False)
    _write_report(bundle.metrics, Path(args.report))
    print(f"Wrote {len(bundle.predictions)} forecasts to {predictions_path}")
    print(f"Wrote {len(bundle.metrics)} metric rows to {metrics_path}")
    print(f"Wrote report to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
