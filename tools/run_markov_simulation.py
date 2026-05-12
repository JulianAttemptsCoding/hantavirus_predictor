"""Run Markov-style incidence-state simulations for scenario stress testing."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.simulations.markov_incidence import simulate_next_year  # noqa: E402


DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "markov_simulation_summary.csv"
DEFAULT_REPORT = ROOT / "reports" / "04_markov_simulation_stress_test.md"


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


def _write_report(result, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    top_risk = result.simulation_summary.sort_values("prob_above_current", ascending=False).head(10)
    lines = [
        "# Markov Simulation Stress Test",
        "",
        "Status: exploratory appendix method, not validation evidence.",
        "",
        "## Purpose",
        "",
        "This stress test estimates zero/low/high reported-incidence state transitions from the ECDC seed panel and simulates next-year reported cases. It can help a paper discuss sparse-surveillance uncertainty and scenario sensitivity without pretending synthetic trajectories are ground truth.",
        "",
        "## Incidence State Thresholds",
        "",
        _markdown_table(pd.DataFrame([result.state_thresholds])),
        "",
        "## Estimated Transition Matrix",
        "",
        _markdown_table(result.transition_matrix.reset_index(names="from_state")),
        "",
        "## Highest Simulated Probability Of Exceeding Current Cases",
        "",
        _markdown_table(
            top_risk[
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
        "## Manuscript Use",
        "",
        "- Use as a robustness/simulation appendix for reported-incidence state persistence.",
        "- Do not use it to inflate sample size or claim prospective outbreak prediction.",
        "- Pair it with the empirical baseline results and clearly label all outputs as simulated.",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--n-simulations", type=int, default=5000)
    parser.add_argument("--reporting-multiplier", type=float, default=1.0)
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    result = simulate_next_year(
        data,
        n_simulations=args.n_simulations,
        reporting_multiplier=args.reporting_multiplier,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.simulation_summary.to_csv(output, index=False)
    _write_report(result, Path(args.report))
    print(f"Wrote {len(result.simulation_summary)} simulation rows to {output}")
    print(f"Wrote simulation report to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
