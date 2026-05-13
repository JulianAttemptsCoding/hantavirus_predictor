"""Run sensitivity and detectability analyses for the ECDC benchmark."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.metrics import weighted_interval_score  # noqa: E402
from hantavirus_predictor.models.feature_ablation import run_feature_ablation  # noqa: E402


DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_METRICS = ROOT / "data" / "processed" / "sensitivity_metrics.csv"
DEFAULT_POWER = ROOT / "data" / "processed" / "power_detectability.csv"
DEFAULT_REPORT = ROOT / "reports" / "07_sensitivity_power.md"


def _rate(cases: pd.Series, population: pd.Series) -> pd.Series:
    return cases / population * 100_000


def _fallback_rate(history: pd.DataFrame) -> float:
    if history.empty or history["population"].sum() <= 0:
        return 0.0
    return float(history["cases"].sum() / history["population"].sum() * 100_000)


def _last_rate(data: pd.DataFrame) -> pd.Series:
    values = []
    for _, row in data.iterrows():
        history = data[(data["iso3"].eq(row["iso3"])) & (data["year"] < row["year"])]
        fallback = _fallback_rate(data[data["year"] < row["year"]])
        if history.empty:
            values.append(fallback)
        else:
            last = history.sort_values("year").iloc[-1]
            values.append(float(last["cases"] / last["population"] * 100_000))
    return pd.Series(values, index=data.index)


def _make_power_features(data: pd.DataFrame) -> pd.DataFrame:
    out = data.copy()
    out["last_rate"] = _last_rate(out)
    out["target_year"] = out["year"].astype(float)
    climate = pd.to_numeric(out["terraclimate_ppt_annual_sum_mm_lag1"], errors="coerce")
    climate = climate.fillna(climate.median())
    std = climate.std(ddof=0)
    out["ppt_z"] = 0.0 if std == 0 or pd.isna(std) else (climate - climate.mean()) / std
    return out


def _fit_rate_model(train: pd.DataFrame, target: pd.DataFrame, columns: list[str]) -> np.ndarray:
    model = Ridge(alpha=1.0)
    x_train = train[columns].to_numpy(dtype=float)
    x_target = target[columns].to_numpy(dtype=float)
    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0)
    std[std == 0] = 1.0
    x_train = (x_train - mean) / std
    x_target = (x_target - mean) / std
    y_train = np.log1p(_rate(train["cases"], train["population"]).to_numpy(dtype=float))
    model.fit(x_train, y_train)
    return np.expm1(model.predict(x_target)).clip(min=0.0)


def _poisson_wis(observed: np.ndarray, mean: np.ndarray) -> float:
    from scipy.stats import poisson

    mean = np.maximum(mean, 1e-9)
    q05 = poisson.ppf(0.05, mean)
    q50 = poisson.ppf(0.50, mean)
    q95 = poisson.ppf(0.95, mean)
    wis = weighted_interval_score(observed, q50, [q05], [q95], [0.1])
    return float(np.mean(wis))


def _run_power(data: pd.DataFrame, iterations: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    base = _make_power_features(data)
    base_train = base[base["year"].isin([2019, 2020, 2021])].copy()
    base_test = base[base["year"].eq(2023)].copy()
    baseline_columns = ["target_year", "last_rate"]
    climate_columns = baseline_columns + ["ppt_z"]
    effect_sizes = [0.0, 0.25, 0.50, 0.75, 1.00]
    rows = []

    historical_rate = max(_fallback_rate(base_train), 1e-6)
    for effect in effect_sizes:
        improvements = []
        for _ in range(iterations):
            simulated = base.copy()
            rate = historical_rate * np.exp(effect * simulated["ppt_z"].to_numpy(dtype=float))
            mean_cases = rate / 100_000 * simulated["population"].to_numpy(dtype=float)
            simulated["cases"] = rng.poisson(np.maximum(mean_cases, 1e-9))
            train = simulated.loc[base_train.index]
            test = simulated.loc[base_test.index]
            baseline_rate = _fit_rate_model(train, test, baseline_columns)
            climate_rate = _fit_rate_model(train, test, climate_columns)
            observed = test["cases"].to_numpy(dtype=float)
            baseline_wis = _poisson_wis(
                observed, baseline_rate / 100_000 * test["population"].to_numpy(dtype=float)
            )
            climate_wis = _poisson_wis(
                observed, climate_rate / 100_000 * test["population"].to_numpy(dtype=float)
            )
            improvement = (
                (baseline_wis - climate_wis) / baseline_wis if baseline_wis > 0 else np.nan
            )
            improvements.append(improvement)
        valid = np.asarray([value for value in improvements if not pd.isna(value)])
        rows.append(
            {
                "log_rate_effect_per_sd": effect,
                "iterations": iterations,
                "mean_relative_wis_improvement": float(np.mean(valid)),
                "median_relative_wis_improvement": float(np.median(valid)),
                "detectability_rate_5pct_wis": float(np.mean(valid >= 0.05)),
            }
        )
    return pd.DataFrame.from_records(rows)


def _scenario_metrics(data: pd.DataFrame) -> pd.DataFrame:
    scenarios = {
        "primary_all_rows": data,
        "exclude_non_comprehensive_or_unspecified": data[
            data["surveillance_completeness"].eq("comprehensive")
        ],
        "exclude_2020_2021_training_years": data[~data["year"].isin([2020, 2021])],
    }
    frames = []
    for scenario, scenario_data in scenarios.items():
        metrics = run_feature_ablation(scenario_data.reset_index(drop=True)).metrics
        metrics.insert(0, "scenario", scenario)
        frames.append(metrics)
    return pd.concat(frames, ignore_index=True)


def _markdown_table(data: pd.DataFrame) -> str:
    columns = list(data.columns)
    rows = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in data.iterrows():
        rows.append("| " + " | ".join(_format_cell(row[column]) for column in columns) + " |")
    return "\n".join(rows)


def _format_cell(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def _write_report(metrics: pd.DataFrame, power: pd.DataFrame, report_path: Path) -> None:
    primary = metrics[
        metrics["split"].isin(["primary_validation_2022", "primary_test_2023"])
    ][
        [
            "scenario",
            "split",
            "feature_set",
            "n",
            "mean_wis",
            "relative_wis_observed_mean",
            "coverage_90",
            "mean_interval_width_90",
            "mae",
            "mase_last_observed_rate",
        ]
    ]
    lines = [
        "# Sensitivity And Detectability Report",
        "",
        "Status: ECDC-only sensitivity checks and simulation-based detectability screen.",
        "",
        "## Sensitivity Scenarios",
        "",
        "- `primary_all_rows`: original ECDC country-year panel.",
        "- `exclude_non_comprehensive_or_unspecified`: removes Belgium 2023, Cyprus 2023, and any future non-comprehensive rows.",
        "- `exclude_2020_2021_training_years`: excludes COVID-era rows where sample size permits.",
        "- The feature-ablation design already includes a 2020-2021 pandemic-period indicator in `surveillance_only` and all nested sets.",
        "",
        "## Primary Sensitivity Metrics",
        "",
        _markdown_table(primary),
        "",
        "## Simulation-Based Detectability",
        "",
        "The simulation preserves the observed country-year structure and population offsets, "
        "then injects a standardized precipitation effect into simulated count rates. "
        "Detectability is the proportion of simulations where a climate-augmented Poisson rate "
        "model improves 2023 WIS by at least 5 percent over a simple surveillance-rate model.",
        "",
        _markdown_table(power),
        "",
        "## Interpretation",
        "",
        "These simulations are a power screen, not validation evidence. Low detectability supports "
        "cautious negative-result language: covariate effects may be undetectable at public "
        "country-year scale rather than absent biologically.",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--power", default=str(DEFAULT_POWER))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20260512)
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    metrics = _scenario_metrics(data)
    power = _run_power(data, iterations=args.iterations, seed=args.seed)

    metrics_path = Path(args.metrics)
    power_path = Path(args.power)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    power_path.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(metrics_path, index=False)
    power.to_csv(power_path, index=False)
    _write_report(metrics, power, Path(args.report))

    print(f"Wrote {len(metrics)} sensitivity metric rows to {metrics_path}")
    print(f"Wrote {len(power)} power rows to {power_path}")
    print(f"Wrote report to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
