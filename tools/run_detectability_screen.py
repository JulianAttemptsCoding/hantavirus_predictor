"""Run null-calibrated detectability screen for the country-year panel."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import nbinom, poisson
from sklearn.linear_model import Ridge

from hantavirus_predictor.metrics import interval_coverage, weighted_interval_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "detectability_screen.csv"
DEFAULT_TABLE = ROOT / "docs" / "submission_eid" / "tables" / "appendix_detectability_screen.csv"
DEFAULT_REPORT = ROOT / "docs" / "submission_eid" / "reports" / "detectability_screen.md"


def _zscore(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    numeric = numeric.fillna(numeric.median())
    std = numeric.std(ddof=0)
    if std == 0 or pd.isna(std):
        return pd.Series(0.0, index=values.index)
    return (numeric - numeric.mean()) / std


def _simulate_counts(
    data: pd.DataFrame,
    effect: float,
    overdispersion: str,
    observed_like_missingness: bool,
    rng: np.random.Generator,
) -> pd.DataFrame:
    out = data.copy()
    base_rate = (
        out.groupby("iso3")["cases"].transform("mean")
        / out.groupby("iso3")["population"].transform("mean")
        * 100_000
    )
    base_rate = base_rate.fillna(out["cases"].sum() / out["population"].sum() * 100_000)
    x = _zscore(out["terraclimate_ppt_annual_sum_mm_lag1"])
    mean = np.maximum(base_rate.to_numpy(dtype=float) * np.exp(effect * x), 1e-9)
    mean_counts = mean / 100_000 * out["population"].to_numpy(dtype=float)
    alpha_map = {"low": 0.05, "observed_like": 0.75, "high": 1.5}
    alpha = alpha_map[overdispersion]
    if alpha <= 0:
        out["cases"] = rng.poisson(mean_counts)
    else:
        size = 1.0 / alpha
        prob = size / (size + np.maximum(mean_counts, 1e-9))
        out["cases"] = rng.negative_binomial(size, prob)
    if observed_like_missingness:
        flagged = out["quality_grade"].astype(str).str.upper().eq("C")
        out.loc[flagged, "cases"] = rng.poisson(np.maximum(mean_counts[flagged.to_numpy()] * 0.6, 1e-9))
    return out


def _history_features(data: pd.DataFrame) -> pd.DataFrame:
    ordered = data.sort_values(["iso3", "year"]).copy()
    rate = ordered["cases"] / ordered["population"] * 100_000
    prior_cases = ordered.groupby("iso3")["cases"].cumsum() - ordered["cases"]
    prior_pop = ordered.groupby("iso3")["population"].cumsum() - ordered["population"]
    mean_rate = prior_cases / prior_pop.replace(0, np.nan) * 100_000
    last_rate = rate.groupby(ordered["iso3"]).shift(1)

    annual = ordered.groupby("year", as_index=True)[["cases", "population"]].sum().sort_index()
    annual["cum_cases"] = annual["cases"].cumsum() - annual["cases"]
    annual["cum_population"] = annual["population"].cumsum() - annual["population"]
    annual["fallback_rate"] = annual["cum_cases"] / annual["cum_population"].replace(0, np.nan) * 100_000
    fallback = ordered["year"].map(annual["fallback_rate"]).fillna(0.0)

    features = pd.DataFrame(
        {
            "last_rate": last_rate.fillna(fallback).to_numpy(dtype=float),
            "mean_rate": mean_rate.fillna(fallback).to_numpy(dtype=float),
            "target_year": ordered["year"].to_numpy(dtype=float),
            "ppt_z": _zscore(ordered["terraclimate_ppt_annual_sum_mm_lag1"]).to_numpy(dtype=float),
        },
        index=ordered.index,
    )
    return features.loc[data.index]


def _fit_predict(train: pd.DataFrame, target: pd.DataFrame, features: pd.DataFrame, columns: list[str]) -> np.ndarray:
    x_train = features.loc[train.index, columns].to_numpy(dtype=float)
    x_target = features.loc[target.index, columns].to_numpy(dtype=float)
    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0)
    std[std == 0] = 1.0
    model = Ridge(alpha=10.0)
    y = np.log1p(train["cases"].to_numpy(dtype=float) / train["population"].to_numpy(dtype=float) * 100_000)
    model.fit((x_train - mean) / std, y)
    rate = np.expm1(model.predict((x_target - mean) / std)).clip(min=0.0)
    return rate / 100_000 * target["population"].to_numpy(dtype=float)


def _score(observed: np.ndarray, mean: np.ndarray, overdispersion: str) -> tuple[float, float]:
    mean = np.maximum(mean, 1e-9)
    if overdispersion == "poisson":
        q05 = poisson.ppf(0.05, mean)
        q50 = poisson.ppf(0.50, mean)
        q95 = poisson.ppf(0.95, mean)
    else:
        alpha = 0.75
        size = 1.0 / alpha
        prob = size / (size + mean)
        q05 = nbinom.ppf(0.05, size, prob)
        q50 = nbinom.ppf(0.50, size, prob)
        q95 = nbinom.ppf(0.95, size, prob)
    wis = weighted_interval_score(observed, q50, [q05], [q95], [0.1])
    return float(np.mean(wis)), interval_coverage(observed, q05, q95)


def run_screen(data: pd.DataFrame, iterations: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    effect_sizes = [0.0, 0.15, 0.35, 0.70]
    overdispersions = ["low", "observed_like", "high"]
    missingness_patterns = [False, True]

    for effect in effect_sizes:
        for overdispersion in overdispersions:
            for observed_like_missingness in missingness_patterns:
                improvements: list[float] = []
                selections: list[bool] = []
                coverages: list[float] = []
                for _ in range(iterations):
                    simulated = _simulate_counts(
                        data,
                        effect,
                        overdispersion,
                        observed_like_missingness,
                        rng,
                    )
                    features = _history_features(simulated)
                    train = simulated[simulated["year"].isin([2019, 2020, 2021])]
                    test = simulated[simulated["year"].eq(2023)]
                    baseline_mean = _fit_predict(train, test, features, ["target_year", "last_rate", "mean_rate"])
                    covariate_mean = _fit_predict(
                        train,
                        test,
                        features,
                        ["target_year", "last_rate", "mean_rate", "ppt_z"],
                    )
                    observed = test["cases"].to_numpy(dtype=float)
                    baseline_wis, _ = _score(observed, baseline_mean, "negative_binomial")
                    covariate_wis, coverage = _score(observed, covariate_mean, "negative_binomial")
                    improvement = (baseline_wis - covariate_wis) / baseline_wis if baseline_wis > 0 else 0.0
                    improvements.append(improvement)
                    coverages.append(coverage)
                    selections.append((improvement >= 0.10) and (coverage >= 0.80))
                rows.append(
                    {
                        "effect_label": {0.0: "none", 0.15: "small", 0.35: "moderate", 0.70: "large"}[effect],
                        "log_rate_effect_per_sd": effect,
                        "overdispersion": overdispersion,
                        "missingness_pattern": "observed_like" if observed_like_missingness else "none",
                        "iterations": iterations,
                        "mean_relative_wis_improvement": float(np.mean(improvements)),
                        "median_relative_wis_improvement": float(np.median(improvements)),
                        "covariate_selection_probability": float(np.mean(selections)),
                        "mean_coverage_90": float(np.mean(coverages)),
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


def _write_report(results: pd.DataFrame, report_path: Path) -> None:
    null = results[results["effect_label"].eq("none")]
    max_false_positive = float(null["covariate_selection_probability"].max())
    lines = [
        "# Null-Calibrated Detectability Screen",
        "",
        "Simulation results do not validate model skill; they indicate whether this sample structure can detect covariate effects under tested assumptions.",
        "",
        f"Maximum null covariate-selection probability: {max_false_positive:.3f}.",
        "",
        _markdown_table(results),
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260514)
    args = parser.parse_args()
    results = run_screen(pd.read_csv(args.input), args.iterations, args.seed)
    for output in [Path(args.output), Path(args.table), Path(args.report)]:
        output.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(args.output, index=False)
    results.to_csv(args.table, index=False)
    _write_report(results, Path(args.report))
    print(f"Wrote {len(results)} detectability rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
