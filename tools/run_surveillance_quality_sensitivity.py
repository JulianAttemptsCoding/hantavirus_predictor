"""Run EID surveillance-quality sensitivity scenarios."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.models import feature_ablation as fa  # noqa: E402

DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_METRICS = ROOT / "data" / "processed" / "surveillance_quality_sensitivity_metrics.csv"
DEFAULT_PREDICTIONS = ROOT / "data" / "processed" / "surveillance_quality_sensitivity_predictions.csv"
DEFAULT_TABLE = ROOT / "docs" / "submission_eid" / "tables" / "appendix_surveillance_quality_sensitivity.csv"
DEFAULT_REPORT = ROOT / "docs" / "submission_eid" / "reports" / "surveillance_quality_sensitivity.md"


def _flagged_mask(data: pd.DataFrame) -> pd.Series:
    return data["quality_grade"].astype(str).str.upper().eq("C") | ~data[
        "surveillance_completeness"
    ].astype(str).str.lower().eq("comprehensive")


def _scenarios(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    flagged = _flagged_mask(data)
    return {
        "primary_all_rows": data.copy(),
        "exclude_belgium_2023": data[~(data["iso3"].eq("BEL") & data["year"].eq(2023))].copy(),
        "exclude_cyprus_2023": data[~(data["iso3"].eq("CYP") & data["year"].eq(2023))].copy(),
        "exclude_belgium_2023_and_cyprus_2023": data[
            ~(
                data["year"].eq(2023)
                & data["iso3"].isin(["BEL", "CYP"])
            )
        ].copy(),
        "retain_flagged_rows_with_indicator": data.assign(
            eid_flagged_row_indicator=flagged.astype(int)
        ),
        "exclude_2020_training_rows": data[~data["year"].eq(2020)].copy(),
        "exclude_2021_training_rows": data[~data["year"].eq(2021)].copy(),
        "exclude_2020_2021_training_rows": data[~data["year"].isin([2020, 2021])].copy(),
    }


def _run_one(name: str, data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    original_feature_sets = {key: list(value) for key, value in fa.FEATURE_SETS.items()}
    try:
        if name == "retain_flagged_rows_with_indicator":
            fa.FEATURE_SETS["all_public"] = [
                *fa.FEATURE_SETS["all_public"],
                "eid_flagged_row_indicator",
            ]
        bundle = fa.run_feature_ablation(data.reset_index(drop=True))
    finally:
        fa.FEATURE_SETS.update(original_feature_sets)

    metrics = bundle.metrics.copy()
    predictions = bundle.predictions.copy()
    metrics.insert(0, "scenario", name)
    predictions.insert(0, "scenario", name)
    metrics["coverage_90_numerator"] = (metrics["coverage_90"] * metrics["n"]).round().astype(int)
    metrics["coverage_90_denominator"] = metrics["n"].astype(int)
    metrics["rows_retained"] = len(data)
    metrics["countries_retained"] = data["iso3"].nunique()
    return metrics, predictions


def run_sensitivity(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    metric_frames: list[pd.DataFrame] = []
    prediction_frames: list[pd.DataFrame] = []
    for name, scenario_data in _scenarios(data).items():
        metrics, predictions = _run_one(name, scenario_data)
        metric_frames.append(metrics)
        prediction_frames.append(predictions)
    metrics_all = pd.concat(metric_frames, ignore_index=True)
    predictions_all = pd.concat(prediction_frames, ignore_index=True)
    primary = metrics_all[metrics_all["split"].eq("primary_test_2023")].copy()
    primary = primary.sort_values(["scenario", "mean_wis"]).groupby("scenario", as_index=False).head(1)
    primary["promotion_rule_passed"] = False
    return metrics_all, predictions_all, primary


def _markdown_table(data: pd.DataFrame) -> str:
    columns = list(data.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in data.iterrows():
        lines.append("| " + " | ".join(_fmt(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def _fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def _write_report(summary: pd.DataFrame, report_path: Path) -> None:
    cols = [
        "scenario",
        "feature_set",
        "n",
        "rows_retained",
        "countries_retained",
        "mean_wis",
        "relative_wis_observed_mean",
        "coverage_90_numerator",
        "coverage_90_denominator",
        "coverage_90",
        "mean_interval_width_90",
        "mae",
        "brier_any_case",
        "promotion_rule_passed",
    ]
    lines = [
        "# Surveillance-Quality Sensitivity",
        "",
        "These analyses test whether flagged surveillance rows or COVID-era training years change the main conclusion. They are sensitivity analyses, not causal estimates.",
        "",
        _markdown_table(summary[cols]),
        "",
        "Interpretation: the manuscript may claim model improvement only if the promotion rule holds across the primary and flagged-row scenarios.",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    metrics, predictions, summary = run_sensitivity(pd.read_csv(args.input))
    for path in [Path(args.metrics), Path(args.predictions), Path(args.table), Path(args.report)]:
        path.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(args.metrics, index=False)
    predictions.to_csv(args.predictions, index=False)
    summary.to_csv(args.table, index=False)
    _write_report(summary, Path(args.report))
    print(f"Wrote {len(metrics)} sensitivity metrics to {args.metrics}")
    print(f"Wrote {len(predictions)} sensitivity predictions to {args.predictions}")
    print(f"Wrote summary table to {args.table}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
