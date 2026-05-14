"""Run leave-one-country-out influence checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.models.feature_ablation import run_feature_ablation  # noqa: E402
from hantavirus_predictor.models.international_baselines import generate_baseline_forecasts  # noqa: E402

DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_METRICS = ROOT / "data" / "processed" / "country_influence_metrics.csv"
DEFAULT_TABLE = ROOT / "docs" / "submission_eid" / "tables" / "appendix_country_influence.csv"
DEFAULT_REPORT = ROOT / "docs" / "submission_eid" / "reports" / "country_influence.md"


def _primary_feature_metrics(data: pd.DataFrame) -> pd.DataFrame:
    return run_feature_ablation(data.reset_index(drop=True)).metrics.query(
        "split == 'primary_test_2023'"
    ).copy()


def _primary_baseline_metrics(data: pd.DataFrame) -> pd.DataFrame:
    return generate_baseline_forecasts(data.reset_index(drop=True), [2023]).metrics.copy()


def run_influence(data: pd.DataFrame) -> pd.DataFrame:
    full_ablation = _primary_feature_metrics(data)
    full_baseline = _primary_baseline_metrics(data)
    full_best_ablation = full_ablation.sort_values("mean_wis").iloc[0]
    full_best_baseline = full_baseline.sort_values("mean_wis").iloc[0]

    rows: list[dict[str, object]] = []
    for iso3, country in data[["iso3", "country"]].drop_duplicates().sort_values("country").itertuples(index=False):
        subset = data[~data["iso3"].eq(iso3)].copy()
        ablation = _primary_feature_metrics(subset)
        baseline = _primary_baseline_metrics(subset)
        best_ablation = ablation.sort_values("mean_wis").iloc[0]
        best_baseline = baseline.sort_values("mean_wis").iloc[0]
        rows.append(
            {
                "removed_iso3": iso3,
                "removed_country": country,
                "removed_2023_cases": int(data[(data["iso3"].eq(iso3)) & data["year"].eq(2023)]["cases"].sum()),
                "high_influence_prespecified": iso3 in {"FIN", "DEU"},
                "full_best_ablation_feature_set": full_best_ablation["feature_set"],
                "loo_best_ablation_feature_set": best_ablation["feature_set"],
                "full_best_ablation_wis": float(full_best_ablation["mean_wis"]),
                "loo_best_ablation_wis": float(best_ablation["mean_wis"]),
                "delta_best_ablation_wis": float(best_ablation["mean_wis"] - full_best_ablation["mean_wis"]),
                "full_best_ablation_coverage": float(full_best_ablation["coverage_90"]),
                "loo_best_ablation_coverage": float(best_ablation["coverage_90"]),
                "delta_best_ablation_coverage": float(best_ablation["coverage_90"] - full_best_ablation["coverage_90"]),
                "full_best_baseline_model": full_best_baseline["model"],
                "loo_best_baseline_model": best_baseline["model"],
                "full_best_baseline_wis": float(full_best_baseline["mean_wis"]),
                "loo_best_baseline_wis": float(best_baseline["mean_wis"]),
                "delta_best_baseline_wis": float(best_baseline["mean_wis"] - full_best_baseline["mean_wis"]),
                "conclusion_changes": bool(best_ablation["mean_wis"] < best_baseline["mean_wis"]),
            }
        )
    return pd.DataFrame.from_records(rows)


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


def _write_report(metrics: pd.DataFrame, report_path: Path) -> None:
    summary_cols = [
        "removed_country",
        "removed_2023_cases",
        "high_influence_prespecified",
        "loo_best_ablation_feature_set",
        "delta_best_ablation_wis",
        "delta_best_ablation_coverage",
        "loo_best_baseline_model",
        "delta_best_baseline_wis",
        "conclusion_changes",
    ]
    lines = [
        "# Leave-One-Country-Out Influence",
        "",
        "This analysis reruns the primary 2023 ablation and surveillance baselines after removing each country. Finland and Germany are pre-specified because ECDC reported that they accounted for 60.5% of 2023 cases.",
        "",
        _markdown_table(metrics[summary_cols]),
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    metrics = run_influence(pd.read_csv(args.input))
    for output in [Path(args.metrics), Path(args.table), Path(args.report)]:
        output.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(args.metrics, index=False)
    metrics.to_csv(args.table, index=False)
    _write_report(metrics, Path(args.report))
    print(f"Wrote {len(metrics)} country-influence rows to {args.metrics}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
