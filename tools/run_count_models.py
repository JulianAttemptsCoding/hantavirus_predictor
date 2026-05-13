"""Run penalized count-model upgrade for the ECDC benchmark."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.models.count_models import run_penalized_poisson_models  # noqa: E402


DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_PREDICTIONS = ROOT / "data" / "processed" / "count_model_predictions.csv"
DEFAULT_METRICS = ROOT / "data" / "processed" / "count_model_metrics.csv"
DEFAULT_TUNING = ROOT / "data" / "processed" / "count_model_tuning.csv"
DEFAULT_REPORT = ROOT / "reports" / "08_count_models.md"


def _format_cell(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def _markdown_table(data: pd.DataFrame) -> str:
    columns = list(data.columns)
    rows = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in data.iterrows():
        rows.append("| " + " | ".join(_format_cell(row[column]) for column in columns) + " |")
    return "\n".join(rows)


def _write_report(metrics: pd.DataFrame, tuning: pd.DataFrame, report_path: Path) -> None:
    best = metrics.sort_values("mean_wis").head(1)
    lines = [
        "# Penalized Count Model Report",
        "",
        "Status: exploratory penalized Poisson GLM with population offset.",
        "",
        "## Model",
        "",
        "- Offset: `log(population / 100000)`.",
        "- Penalty: ridge penalty on non-intercept coefficients.",
        "- Hyperparameter selection: 2022 validation WIS.",
        "- Test target: 2023.",
        "- Coefficients are not interpreted causally.",
        "",
        "## 2023 Metrics",
        "",
        _markdown_table(metrics),
        "",
        "## Best Count Model By WIS",
        "",
        _markdown_table(best),
        "",
        "## Validation Tuning",
        "",
        _markdown_table(tuning),
        "",
        "## Promotion Rule",
        "",
        "Do not promote this model unless it improves WIS or relative WIS over simple "
        "baselines without unacceptable coverage loss.",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--tuning", default=str(DEFAULT_TUNING))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    bundle = run_penalized_poisson_models(pd.read_csv(args.input))
    predictions_path = Path(args.predictions)
    metrics_path = Path(args.metrics)
    tuning_path = Path(args.tuning)
    for path in [predictions_path, metrics_path, tuning_path]:
        path.parent.mkdir(parents=True, exist_ok=True)
    bundle.predictions.to_csv(predictions_path, index=False)
    bundle.metrics.to_csv(metrics_path, index=False)
    bundle.tuning.to_csv(tuning_path, index=False)
    _write_report(bundle.metrics, bundle.tuning, Path(args.report))

    print(f"Wrote {len(bundle.predictions)} count-model prediction rows to {predictions_path}")
    print(f"Wrote {len(bundle.metrics)} count-model metric rows to {metrics_path}")
    print(f"Wrote {len(bundle.tuning)} tuning rows to {tuning_path}")
    print(f"Wrote report to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
