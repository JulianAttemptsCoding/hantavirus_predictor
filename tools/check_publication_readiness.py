"""Run a final QA gate for the ECDC-only public-data benchmark path."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_METRICS = ROOT / "data" / "processed" / "international_baseline_metrics.csv"
DEFAULT_PREDICTIONS = ROOT / "data" / "processed" / "international_baseline_predictions.csv"
DEFAULT_SIMULATION = ROOT / "data" / "processed" / "markov_simulation_summary.csv"
DEFAULT_ABLATION = ROOT / "data" / "processed" / "feature_ablation_metrics.csv"
DEFAULT_ABLATION_SCREENING = ROOT / "data" / "processed" / "feature_ablation_feature_screening.csv"
DEFAULT_SENSITIVITY = ROOT / "data" / "processed" / "sensitivity_metrics.csv"
DEFAULT_POWER = ROOT / "data" / "processed" / "power_detectability.csv"
DEFAULT_COUNT_MODELS = ROOT / "data" / "processed" / "count_model_metrics.csv"
DEFAULT_OUTPUT = ROOT / "reports" / "05_publication_readiness_gate.md"
DEFAULT_FIGURE_1 = ROOT / "docs" / "submission_eid" / "figures" / "Figure_1.tif"
DEFAULT_FIGURE_2 = ROOT / "docs" / "submission_eid" / "figures" / "Figure_2.tif"

ECDC_TOTALS = {
    2019: 4088,
    2020: 1693,
    2021: 4947,
    2022: 2185,
    2023: 1885,
}


def _markdown_table(data: pd.DataFrame) -> str:
    if data.empty:
        return "_No rows._"
    columns = list(data.columns)
    rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in data.iterrows():
        rows.append("| " + " | ".join(_format_cell(row[column]) for column in columns) + " |")
    return "\n".join(rows)


def _format_cell(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def _status(pass_condition: bool, *, warning: bool = False) -> str:
    if pass_condition:
        return "pass"
    return "warn" if warning else "fail"


def _lag_columns(cases: pd.DataFrame) -> list[str]:
    return [
        column
        for column in cases.columns
        if column.startswith("terraclimate_")
        and "_annual_" in column
        and column.endswith("_lag1")
    ]


def _coverage_note(best: pd.DataFrame) -> str:
    if best.empty or "coverage_90" not in best:
        return "No best-model coverage rows available."
    rows = []
    for _, row in best.sort_values("target_year").iterrows():
        coverage = float(row["coverage_90"])
        status = "under-covered" if coverage < 0.8 else "over-wide" if coverage > 0.98 else "near target"
        rows.append(f"{int(row['target_year'])}: {coverage:.3f} ({status})")
    return "; ".join(rows)


def build_gate_report(
    cases: pd.DataFrame,
    metrics: pd.DataFrame,
    predictions: pd.DataFrame,
    simulation: pd.DataFrame,
    ablation: pd.DataFrame | None = None,
    screening: pd.DataFrame | None = None,
    sensitivity: pd.DataFrame | None = None,
    power: pd.DataFrame | None = None,
    count_models: pd.DataFrame | None = None,
    eid_figures_exist: bool = False,
) -> tuple[str, bool]:
    annual = cases.groupby("year", as_index=False)["cases"].sum()
    annual["expected_ecdc_total"] = annual["year"].map(ECDC_TOTALS)
    annual["difference"] = annual["cases"] - annual["expected_ecdc_total"]

    min_year = int(cases["year"].min())
    forecast_rows = cases[cases["year"] > min_year]
    lag_columns = _lag_columns(cases)
    lag_complete = bool(lag_columns) and forecast_rows[lag_columns].notna().all(axis=None)

    best = metrics.sort_values(["target_year", "mean_wis"]).groupby("target_year").head(1)
    required_models = {
        "country_historical_mean_rate",
        "last_observed_country_rate",
        "empirical_negative_binomial_rate",
        "hierarchical_negative_binomial_rate",
        "gradient_boosting_rate",
    }
    ablation = pd.DataFrame() if ablation is None else ablation
    screening = pd.DataFrame() if screening is None else screening
    sensitivity = pd.DataFrame() if sensitivity is None else sensitivity
    power = pd.DataFrame() if power is None else power
    count_models = pd.DataFrame() if count_models is None else count_models
    required_feature_sets = {
        "surveillance_only",
        "context",
        "land_use",
        "climate",
        "all_public",
    }

    checks = pd.DataFrame(
        [
            {
                "area": "ECDC source reconciliation",
                "status": _status(bool((annual["difference"] == 0).all())),
                "evidence": "Annual totals match ECDC Table 1 for 2019-2023.",
            },
            {
                "area": "Processed analysis table",
                "status": _status(len(cases) == 142 and cases["year"].nunique() == 5),
                "evidence": f"{len(cases)} rows across {cases['year'].nunique()} years.",
            },
            {
                "area": "World Bank context",
                "status": _status(
                    cases[["population", "rural_population_pct", "gdp_per_capita_current_usd"]]
                    .notna()
                    .all(axis=None)
                ),
                "evidence": "Population, rurality, and GDP are non-missing for all rows.",
            },
            {
                "area": "FAOSTAT land use",
                "status": _status(bool(cases["faostat_land_use_joined"].all())),
                "evidence": f"{int(cases['faostat_land_use_joined'].sum())} joined rows.",
            },
            {
                "area": "TerraClimate current-year features",
                "status": _status(bool(cases["terraclimate_joined"].all())),
                "evidence": f"{int(cases['terraclimate_joined'].sum())} joined rows.",
            },
            {
                "area": "TerraClimate lag features",
                "status": _status(lag_complete),
                "evidence": (
                    f"{len(lag_columns)} lag-1 climate features complete for "
                    f"{len(forecast_rows)} non-{min_year} rows."
                ),
            },
            {
                "area": "Surveillance metadata flags",
                "status": _status(
                    {"eu_eea_status", "surveillance_completeness"}.issubset(cases.columns)
                ),
                "evidence": (
                    "ECDC source-quality metadata present; Belgium 2023 and Cyprus 2023 "
                    "must be handled in sensitivity analyses."
                ),
            },
            {
                "area": "Forecast benchmark outputs",
                "status": _status(
                    required_models.issubset(set(metrics["model"]))
                    and {2022, 2023}.issubset(set(metrics["target_year"]))
                    and not predictions.empty
                    and {
                        "relative_wis_observed_mean",
                        "mean_interval_width_90",
                    }.issubset(metrics.columns)
                ),
                "evidence": (
                    f"{len(metrics)} metric rows and {len(predictions)} quantile rows, "
                    "including relative WIS and 90 percent interval width."
                ),
            },
            {
                "area": "Calibration caution",
                "status": _status(False, warning=True),
                "evidence": (
                    "Coverage is descriptive at this stage and must be discussed rather "
                    f"than hidden. Best-model coverage: {_coverage_note(best)}."
                ),
            },
            {
                "area": "Feature ablation outputs",
                "status": _status(
                    not ablation.empty
                    and required_feature_sets.issubset(set(ablation["feature_set"]))
                    and {"primary_validation_2022", "primary_test_2023"}.issubset(
                        set(ablation["split"])
                    )
                    and {
                        "mean_wis",
                        "relative_wis_observed_mean",
                        "coverage_90",
                        "mean_interval_width_90",
                        "mae",
                        "brier_any_case",
                        "mase_last_observed_rate",
                    }.issubset(ablation.columns)
                ),
                "evidence": f"{len(ablation)} feature-ablation metric rows.",
            },
            {
                "area": "Model feature dimensions",
                "status": _status(
                    not screening.empty
                    and "final_model_features_before_one_hot" in screening.columns
                    and screening["final_model_features_before_one_hot"].between(1, 25).all()
                ),
                "evidence": (
                    f"{len(screening)} screening rows with raw and final feature counts."
                ),
            },
            {
                "area": "Sensitivity and power analyses",
                "status": _status(not sensitivity.empty and not power.empty),
                "evidence": (
                    f"{len(sensitivity)} sensitivity metric rows and {len(power)} "
                    "detectability rows."
                ),
            },
            {
                "area": "Penalized count-model check",
                "status": _status(
                    not count_models.empty
                    and {"penalized_poisson_glm"}.issubset(set(count_models["model"]))
                    and {
                        "mean_wis",
                        "relative_wis_observed_mean",
                        "coverage_90",
                        "mean_interval_width_90",
                        "poisson_deviance",
                        "brier_any_case",
                    }.issubset(count_models.columns)
                ),
                "evidence": (
                    f"{len(count_models)} penalized count-model metric rows; "
                    "promote only if calibration and WIS beat simple baselines."
                ),
            },
            {
                "area": "EID figure package",
                "status": _status(eid_figures_exist),
                "evidence": (
                    "Draft EID figure files exist separately from manuscript text with "
                    "country-level display only."
                ),
            },
            {
                "area": "Simulation appendix",
                "status": _status(not simulation.empty),
                "evidence": f"{len(simulation)} reported-incidence state simulation rows.",
            },
            {
                "area": "MODIS vegetation claims",
                "status": _status(False, warning=True),
                "evidence": (
                    "MODIS is manifest-only. A paper can proceed as ECDC + World Bank + "
                    "FAOSTAT + TerraClimate, but vegetation claims must be removed unless "
                    "quality-masked MOD13C2 aggregation is implemented."
                ),
            },
            {
                "area": "International generalization claims",
                "status": _status(False, warning=True),
                "evidence": (
                    "PAHO and China CDC rows are not extracted. Frame this as an ECDC/EU-EEA "
                    "public benchmark unless those rows are added with provenance."
                ),
            },
        ]
    )

    failed = bool((checks["status"] == "fail").any())
    verdict = (
        "PASS for an ECDC-only public-data benchmark manuscript path."
        if not failed
        else "FAIL: fix failed criteria before manuscript drafting."
    )
    lines = [
        "# Publication Readiness Gate",
        "",
        f"Verdict: {verdict}",
        "",
        "## Criteria",
        "",
        _markdown_table(checks),
        "",
        "## ECDC Annual Reconciliation",
        "",
        _markdown_table(annual),
        "",
        "## Best Baseline By Target Year",
        "",
        _markdown_table(
            best[
                [
                    "target_year",
                    "model",
                    "n",
                    "mean_wis",
                    "relative_wis_observed_mean",
                    "coverage_90",
                    "mean_interval_width_90",
                    "mae",
                    "brier_any_case",
                ]
            ]
        ),
        "",
        "## Publication Frame That Passes This Gate",
        "",
        "- Main claim: an open, uncertainty-calibrated EU/EEA country-year reported-incidence benchmark using free public surveillance, demographic, land-use, and TerraClimate covariates.",
        "- Simulation claim: reported-incidence state stress testing only; not human-to-human spread prediction and not extra validation data.",
        "- Exclusions: no individual infection prediction, no within-country risk map, no operational alerting, no vegetation claim until MODIS QA aggregation exists, and no global generalization claim until non-ECDC source systems are added.",
    ]
    return "\n".join(lines) + "\n", not failed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--simulation", default=str(DEFAULT_SIMULATION))
    parser.add_argument("--ablation", default=str(DEFAULT_ABLATION))
    parser.add_argument("--ablation-screening", default=str(DEFAULT_ABLATION_SCREENING))
    parser.add_argument("--sensitivity", default=str(DEFAULT_SENSITIVITY))
    parser.add_argument("--power", default=str(DEFAULT_POWER))
    parser.add_argument("--count-models", default=str(DEFAULT_COUNT_MODELS))
    parser.add_argument("--figure-1", default=str(DEFAULT_FIGURE_1))
    parser.add_argument("--figure-2", default=str(DEFAULT_FIGURE_2))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    cases = pd.read_csv(args.cases)
    metrics = pd.read_csv(args.metrics)
    predictions = pd.read_csv(args.predictions)
    simulation = pd.read_csv(args.simulation)
    ablation = pd.read_csv(args.ablation) if Path(args.ablation).exists() else pd.DataFrame()
    screening = (
        pd.read_csv(args.ablation_screening)
        if Path(args.ablation_screening).exists()
        else pd.DataFrame()
    )
    sensitivity = (
        pd.read_csv(args.sensitivity) if Path(args.sensitivity).exists() else pd.DataFrame()
    )
    power = pd.read_csv(args.power) if Path(args.power).exists() else pd.DataFrame()
    count_models = (
        pd.read_csv(args.count_models) if Path(args.count_models).exists() else pd.DataFrame()
    )
    report, passed = build_gate_report(
        cases,
        metrics,
        predictions,
        simulation,
        ablation=ablation,
        screening=screening,
        sensitivity=sensitivity,
        power=power,
        count_models=count_models,
        eid_figures_exist=Path(args.figure_1).exists() and Path(args.figure_2).exists(),
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"Wrote publication readiness gate to {output}")
    print("PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
