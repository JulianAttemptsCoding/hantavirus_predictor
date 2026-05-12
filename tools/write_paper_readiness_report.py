"""Summarize current paper readiness, outputs, and remaining blockers."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_METRICS = ROOT / "data" / "processed" / "international_baseline_metrics.csv"
DEFAULT_SIM = ROOT / "data" / "processed" / "markov_simulation_summary.csv"
DEFAULT_OUTPUT = ROOT / "reports" / "00_paper_readiness_and_results.md"


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


def build_report(cases: pd.DataFrame, metrics: pd.DataFrame, simulation: pd.DataFrame) -> str:
    annual = cases.groupby("year", as_index=False)["cases"].sum()
    annual["countries_reporting_or_zero"] = cases.groupby("year")["iso3"].nunique().to_numpy()
    terraclimate_rows = int(cases["terraclimate_joined"].sum())
    terraclimate_status = "ready" if terraclimate_rows else "not joined"
    joined = pd.DataFrame(
        [
            {"asset": "ECDC country-year case rows", "status": "ready", "value": len(cases)},
            {
                "asset": "World Bank population/rurality/GDP",
                "status": "ready",
                "value": int(
                    cases[["population", "rural_population_pct", "gdp_per_capita_current_usd"]]
                    .notna()
                    .all(axis=1)
                    .sum()
                ),
            },
            {
                "asset": "FAOSTAT land use",
                "status": "ready",
                "value": int(cases["faostat_land_use_joined"].sum()),
            },
            {
                "asset": "TerraClimate country-year covariates",
                "status": terraclimate_status,
                "value": terraclimate_rows,
            },
            {
                "asset": "MOD13C2 country-year covariates",
                "status": "manifest only",
                "value": int(cases["mod13c2_joined"].sum()),
            },
        ]
    )
    best = metrics.sort_values(["target_year", "mean_wis"]).groupby("target_year").head(1)
    best_sim = simulation.sort_values("prob_above_current", ascending=False).head(5)

    go_no_go = pd.DataFrame(
        [
            {
                "criterion": "Reproducible ECDC data audit",
                "status": "pass",
                "note": "Source totals reconcile exactly for 2019-2023.",
            },
            {
                "criterion": "Baseline benchmark",
                "status": "pass for seed study",
                "note": "Simple baselines run and expose negative/weak ML results.",
            },
            {
                "criterion": "Climate and vegetation covariates",
                "status": "partial pass" if terraclimate_rows else "not yet",
                "note": "TerraClimate is joined when available; MODIS still requires QA-masked aggregation.",
            },
            {
                "criterion": "International generalization",
                "status": "not yet",
                "note": "PAHO and China CDC source-system rows are not yet extracted.",
            },
            {
                "criterion": "Submission-ready manuscript",
                "status": "not yet",
                "note": "Current state supports a methods/data note or pre-analysis scaffold, not final claims.",
            },
        ]
    )

    lines = [
        "# Paper Readiness And Current Results",
        "",
        "## Verdict",
        "",
        "Not fully journal-submission-ready yet. The project is now a reproducible ECDC seed benchmark with audited data, first-pass baselines, FAOSTAT land-use covariates, optional TerraClimate country-year aggregation, source manifests for MOD13C2, figures, and an exploratory Markov simulation stress test. It is not ready for final journal submission until MODIS is either implemented or removed from claims, and the manuscript chooses an ECDC-only methods/data frame or adds PAHO/China source systems.",
        "",
        "## Current Data Assets",
        "",
        _markdown_table(joined),
        "",
        "## Annual ECDC Reported Cases",
        "",
        _markdown_table(annual),
        "",
        "## Best Baseline By Evaluation Year",
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
        "## Markov Simulation Signal",
        "",
        _markdown_table(
            best_sim[
                [
                    "iso3",
                    "country",
                    "current_state",
                    "median_cases",
                    "q05_cases",
                    "q95_cases",
                    "prob_any_case",
                    "prob_above_current",
                ]
            ]
        ),
        "",
        "## Go/No-Go For Paper",
        "",
        _markdown_table(go_no_go),
        "",
        "## How To Make The Paper Useful",
        "",
        "1. Keep the main empirical claim narrow: an open, audited ECDC/EU-EEA country-year reported-incidence benchmark.",
        "2. Use TerraClimate lagged features for climate claims; add MODIS country-year lags only before making vegetation claims.",
        "3. Use the Markov simulation as a scenario stress-test appendix for sparse surveillance dynamics, not as extra validation data.",
        "4. Add PAHO/China CDC only with full provenance and explicit syndrome/source-system strata.",
        "5. Promote complex models only if they beat the best simple baseline under WIS, relative WIS, interval width, and coverage.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--simulation", default=str(DEFAULT_SIM))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    cases = pd.read_csv(args.cases)
    metrics = pd.read_csv(args.metrics)
    simulation = pd.read_csv(args.simulation)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_report(cases, metrics, simulation), encoding="utf-8")
    print(f"Wrote paper readiness report to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
