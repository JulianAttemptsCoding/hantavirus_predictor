"""Run nested feature-family ablation for the ECDC benchmark."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.models.feature_ablation import (  # noqa: E402
    FEATURE_SET_ORDER,
    run_feature_ablation,
)


DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_PREDICTIONS = ROOT / "data" / "processed" / "feature_ablation_predictions.csv"
DEFAULT_METRICS = ROOT / "data" / "processed" / "feature_ablation_metrics.csv"
DEFAULT_CALIBRATION = ROOT / "data" / "processed" / "feature_ablation_calibration.csv"
DEFAULT_SCREENING = ROOT / "data" / "processed" / "feature_ablation_feature_screening.csv"
DEFAULT_REPORT = ROOT / "reports" / "03_feature_ablation.md"
DEFAULT_FIGURES = ROOT / "figures"


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


def _write_report(
    metrics: pd.DataFrame,
    calibration: pd.DataFrame,
    screening: pd.DataFrame,
    report_path: Path,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    primary = metrics[metrics["split"].isin(["primary_validation_2022", "primary_test_2023"])]
    primary = primary.sort_values(["target_year", "feature_set"])
    best = primary.sort_values(["target_year", "mean_wis"]).groupby("target_year").head(1)
    feature_counts = screening[
        screening["split"].isin(["primary_validation_2022", "primary_test_2023"])
    ][
        [
            "split",
            "feature_set",
            "raw_candidate_features",
            "final_model_features_before_one_hot",
        ]
    ]
    calibration_primary = calibration[
        calibration["split"].isin(["primary_validation_2022", "primary_test_2023"])
    ]
    lines = [
        "# Feature Ablation Report",
        "",
        "Status: nested ECDC-only public-feature ablation.",
        "",
        "## Design",
        "",
        "- Primary training window: 2019-2021.",
        "- Validation target: 2022.",
        "- Test target: 2023.",
        "- Sensitivity: leave-one-year-out splits for 2019-2023.",
        "- Continuous and binary imputation parameters are learned on training rows only.",
        "- Constant, duplicate, high-missingness, and highly correlated predictors are removed before modeling.",
        "- The final feature count is reported before one-hot encoding and separately from the 97-column processed audit table.",
        "",
        "## Nested Feature Sets",
        "",
        "- `surveillance_only`: lagged country and panel surveillance summaries plus target-year indicators.",
        "- `context`: surveillance plus lagged World Bank rurality and GDP context.",
        "- `land_use`: context plus lagged FAOSTAT land-use shares.",
        "- `climate`: land-use set plus lagged TerraClimate climate and water-balance variables.",
        "- `all_public`: climate set plus public source-quality metadata; these metadata must not be interpreted causally.",
        "",
        "## Primary Metrics",
        "",
        _markdown_table(primary),
        "",
        "## Best Primary Feature Set By Year",
        "",
        _markdown_table(best),
        "",
        "## Primary Feature Counts",
        "",
        _markdown_table(feature_counts),
        "",
        "## Calibration",
        "",
        _markdown_table(calibration_primary),
        "",
        "## Interpretation Guardrails",
        "",
        "- A covariate family is not promoted unless WIS or relative WIS improves without unacceptable coverage loss.",
        "- Sparse country-year public surveillance can make negative ablation results publishable when reported honestly.",
        "- Climate, land-use, and source-quality coefficients are not interpreted causally.",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _plot_metric(metrics: pd.DataFrame, column: str, ylabel: str, output: Path) -> None:
    primary = metrics[metrics["split"].isin(["primary_validation_2022", "primary_test_2023"])]
    primary = primary.copy()
    primary["feature_set"] = pd.Categorical(
        primary["feature_set"], categories=FEATURE_SET_ORDER, ordered=True
    )
    pivot = primary.pivot(index="feature_set", columns="target_year", values=column).sort_index()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    pivot.plot(kind="bar", ax=ax, color=["#0072B2", "#D55E00"])
    ax.set_xlabel("Feature set")
    ax.set_ylabel(ylabel)
    ax.set_title(ylabel)
    ax.legend(title="Target year")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300)
    plt.close(fig)


def _plot_calibration(calibration: pd.DataFrame, output: Path) -> None:
    primary = calibration[
        calibration["split"].isin(["primary_validation_2022", "primary_test_2023"])
    ].copy()
    primary["feature_set"] = pd.Categorical(
        primary["feature_set"], categories=FEATURE_SET_ORDER, ordered=True
    )
    fig, ax = plt.subplots(figsize=(5.5, 5))
    for feature_set, group in primary.groupby("feature_set", observed=True):
        group = group.groupby("nominal_coverage", as_index=False)["empirical_coverage"].mean()
        ax.plot(group["nominal_coverage"], group["empirical_coverage"], marker="o", label=feature_set)
    ax.plot([0, 1], [0, 1], color="black", linewidth=1, linestyle="--")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Nominal coverage")
    ax.set_ylabel("Empirical coverage")
    ax.set_title("Calibration")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300)
    plt.close(fig)


def _write_figures(metrics: pd.DataFrame, calibration: pd.DataFrame, figure_dir: Path) -> None:
    _plot_metric(metrics, "mean_wis", "Mean WIS", figure_dir / "03_feature_ablation_wis.png")
    _plot_metric(
        metrics,
        "relative_wis_observed_mean",
        "Relative WIS",
        figure_dir / "03_feature_ablation_relative_wis.png",
    )
    _plot_metric(metrics, "coverage_90", "90 percent coverage", figure_dir / "03_feature_ablation_coverage.png")
    _plot_metric(
        metrics,
        "mean_interval_width_90",
        "Mean 90 percent interval width",
        figure_dir / "03_feature_ablation_interval_width.png",
    )
    _plot_calibration(calibration, figure_dir / "03_feature_ablation_calibration.png")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--calibration", default=str(DEFAULT_CALIBRATION))
    parser.add_argument("--screening", default=str(DEFAULT_SCREENING))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--figures", default=str(DEFAULT_FIGURES))
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    bundle = run_feature_ablation(data)

    predictions_path = Path(args.predictions)
    metrics_path = Path(args.metrics)
    calibration_path = Path(args.calibration)
    screening_path = Path(args.screening)
    for path in [predictions_path, metrics_path, calibration_path, screening_path]:
        path.parent.mkdir(parents=True, exist_ok=True)

    bundle.predictions.to_csv(predictions_path, index=False)
    bundle.metrics.to_csv(metrics_path, index=False)
    bundle.calibration.to_csv(calibration_path, index=False)
    bundle.feature_screening.to_csv(screening_path, index=False)
    _write_report(bundle.metrics, bundle.calibration, bundle.feature_screening, Path(args.report))
    _write_figures(bundle.metrics, bundle.calibration, Path(args.figures))

    print(f"Wrote {len(bundle.predictions)} prediction rows to {predictions_path}")
    print(f"Wrote {len(bundle.metrics)} metric rows to {metrics_path}")
    print(f"Wrote {len(bundle.calibration)} calibration rows to {calibration_path}")
    print(f"Wrote {len(bundle.feature_screening)} screening rows to {screening_path}")
    print(f"Wrote report to {args.report}")
    print(f"Wrote feature ablation figures to {args.figures}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
