"""Write country-year calibration localization table for EID."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_ABLATION = ROOT / "data" / "processed" / "feature_ablation_predictions.csv"
DEFAULT_COUNT = ROOT / "data" / "processed" / "count_model_predictions.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "calibration_localization.csv"
DEFAULT_TABLE = ROOT / "docs" / "submission_eid" / "tables" / "appendix_calibration_localization.csv"
DEFAULT_REPORT = ROOT / "docs" / "submission_eid" / "reports" / "calibration_localization.md"


def build_localization(cases: pd.DataFrame, ablation: pd.DataFrame, count: pd.DataFrame) -> pd.DataFrame:
    case_cols = [
        "iso3",
        "year",
        "country",
        "cases",
        "incidence_per_100k",
        "quality_grade",
        "surveillance_completeness",
    ]
    case_lookup = cases[case_cols].copy()
    rows = []

    abl = ablation[ablation["target_year"].eq(2023)].copy()
    for _, row in abl.iterrows():
        rows.append(
            {
                "model_family": "covariate_block",
                "model": row["feature_set"],
                "feature_set": row["feature_set"],
                "iso3": row["iso3"],
                "year": int(row["target_year"]),
                "observed_count": int(row["observed"]),
                "predicted_median": float(row["q50"]),
                "lower_90": float(row["q05"]),
                "upper_90": float(row["q95"]),
                "absolute_error": abs(float(row["observed"]) - float(row["q50"])),
                "interval_width": float(row["q95"]) - float(row["q05"]),
            }
        )

    if not count.empty:
        ct = count[count["target_year"].eq(2023)].copy()
        for _, row in ct.iterrows():
            rows.append(
                {
                    "model_family": "penalized_poisson",
                    "model": row["model"],
                    "feature_set": row["feature_set"],
                    "iso3": row["iso3"],
                    "year": int(row["target_year"]),
                    "observed_count": int(row["observed"]),
                    "predicted_median": float(row["q50"]),
                    "lower_90": float(row["q05"]),
                    "upper_90": float(row["q95"]),
                    "absolute_error": abs(float(row["observed"]) - float(row["q50"])),
                    "interval_width": float(row["q95"]) - float(row["q05"]),
                }
            )

    out = pd.DataFrame.from_records(rows)
    out["covered_90"] = (out["lower_90"] <= out["observed_count"]) & (
        out["observed_count"] <= out["upper_90"]
    )
    out = out.merge(case_lookup, on=["iso3", "year"], how="left")
    out["country"] = out["country"].fillna(out["iso3"])
    out["quality_flag"] = out["quality_grade"].astype(str).str.upper().eq("C")
    return out.sort_values(["model_family", "feature_set", "country"]).reset_index(drop=True)


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


def _write_report(localization: pd.DataFrame, report_path: Path) -> None:
    summary = (
        localization.groupby(["model_family", "feature_set"], as_index=False)
        .agg(
            covered_90_numerator=("covered_90", "sum"),
            covered_90_denominator=("covered_90", "size"),
            mean_interval_width=("interval_width", "mean"),
            mean_absolute_error=("absolute_error", "mean"),
        )
    )
    summary["coverage_90"] = summary["covered_90_numerator"] / summary["covered_90_denominator"]
    lines = [
        "# Calibration Localization",
        "",
        "The table localizes 2023 interval coverage failures by country and model without implying within-country precision.",
        "",
        _markdown_table(summary),
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--ablation", default=str(DEFAULT_ABLATION))
    parser.add_argument("--count", default=str(DEFAULT_COUNT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    count = pd.read_csv(args.count) if Path(args.count).exists() else pd.DataFrame()
    localization = build_localization(
        pd.read_csv(args.cases),
        pd.read_csv(args.ablation),
        count,
    )
    for output in [Path(args.output), Path(args.table), Path(args.report)]:
        output.parent.mkdir(parents=True, exist_ok=True)
    localization.to_csv(args.output, index=False)
    localization.to_csv(args.table, index=False)
    _write_report(localization, Path(args.report))
    print(f"Wrote {len(localization)} calibration-localization rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
