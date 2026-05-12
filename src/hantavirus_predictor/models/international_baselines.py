"""International country-year baseline forecasts."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import nbinom, poisson
from sklearn.ensemble import HistGradientBoostingRegressor

from hantavirus_predictor.metrics import (
    brier_score,
    interval_coverage,
    poisson_deviance,
    weighted_interval_score,
)


QUANTILES = (0.05, 0.5, 0.95)


@dataclass(frozen=True)
class ForecastBundle:
    predictions: pd.DataFrame
    metrics: pd.DataFrame


def _rate(cases: pd.Series, population: pd.Series) -> pd.Series:
    return cases / population * 100_000


def _fallback_rate(train: pd.DataFrame) -> float:
    total_population = train["population"].sum()
    if total_population <= 0:
        return 0.0
    return float(train["cases"].sum() / total_population * 100_000)


def _group_rate(
    train: pd.DataFrame,
    row: pd.Series,
    columns: list[str],
    fallback: float,
) -> float:
    mask = pd.Series(True, index=train.index)
    for column in columns:
        mask &= train[column] == row[column]
    group = train.loc[mask]
    if group.empty:
        return fallback
    return float(group["cases"].sum() / group["population"].sum() * 100_000)


def _last_observed_rate(train: pd.DataFrame, row: pd.Series, fallback: float) -> float:
    mask = (
        (train["iso3"] == row["iso3"])
        & (train["syndrome"] == row["syndrome"])
        & (train["source_system"] == row["source_system"])
    )
    history = train.loc[mask].sort_values("year")
    if history.empty:
        return fallback
    last = history.iloc[-1]
    return float(last["cases"] / last["population"] * 100_000)


def _hierarchical_rate(train: pd.DataFrame, row: pd.Series, fallback: float) -> float:
    country_mask = (
        (train["iso3"] == row["iso3"])
        & (train["syndrome"] == row["syndrome"])
        & (train["source_system"] == row["source_system"])
    )
    country_history = train.loc[country_mask]
    country_rate = _group_rate(train, row, ["iso3", "syndrome", "source_system"], fallback)
    region_rate = _group_rate(train, row, ["region", "syndrome", "source_system"], fallback)
    shrinkage_weight = len(country_history) / (len(country_history) + 2.0)
    return float(shrinkage_weight * country_rate + (1.0 - shrinkage_weight) * region_rate)


def _poisson_summary(mean: float) -> tuple[dict[float, float], float]:
    mean = max(float(mean), 1e-9)
    values = {quantile: float(poisson.ppf(quantile, mean)) for quantile in QUANTILES}
    probability_positive = 1.0 - float(poisson.pmf(0, mean))
    return values, probability_positive


def _negative_binomial_summary(mean: float, alpha: float) -> tuple[dict[float, float], float]:
    mean = max(float(mean), 1e-9)
    alpha = max(float(alpha), 1e-6)
    size = 1.0 / alpha
    probability = size / (size + mean)
    values = {quantile: float(nbinom.ppf(quantile, size, probability)) for quantile in QUANTILES}
    probability_positive = 1.0 - float(nbinom.pmf(0, size, probability))
    return values, probability_positive


def _estimate_nb_alpha(train: pd.DataFrame) -> float:
    counts = train["cases"].astype(float)
    mean = float(counts.mean())
    variance = float(counts.var(ddof=1))
    if mean <= 0 or variance <= mean:
        return 1e-6
    return (variance - mean) / (mean**2)


def _model_feature_matrix(data: pd.DataFrame) -> pd.DataFrame:
    categorical_columns = ["iso3", "region", "syndrome", "source_system"]
    numeric_columns = ["year", "population"]
    lagged_covariates = [
        column
        for column in data.columns
        if column.endswith("_lag1")
        and not column.endswith("_missing")
        and (
            column.startswith("terraclimate_")
            or column.startswith("faostat_")
            or column in {"rural_population_pct_lag1", "gdp_per_capita_current_usd_lag1"}
        )
    ]
    if lagged_covariates:
        numeric_columns.extend(sorted(lagged_covariates))
    else:
        numeric_columns.extend(["rural_population_pct", "gdp_per_capita_current_usd"])

    features = data[categorical_columns + numeric_columns].copy()
    for column in numeric_columns:
        features[column] = pd.to_numeric(features[column], errors="coerce")
        median = features[column].median()
        features[column] = features[column].fillna(0.0 if pd.isna(median) else median)
    features["log_population"] = np.log(features["population"].astype(float))
    features = features.drop(columns=["population"])
    return pd.get_dummies(features, columns=categorical_columns)


def _gradient_boosting_predictions(train: pd.DataFrame, target: pd.DataFrame) -> pd.Series:
    combined = pd.concat([train, target], axis=0, ignore_index=True)
    features = _model_feature_matrix(combined)
    x_train = features.iloc[: len(train)]
    x_target = features.iloc[len(train) :]
    y_train = np.log1p(_rate(train["cases"], train["population"]))
    model = HistGradientBoostingRegressor(max_iter=100, learning_rate=0.05, random_state=20260512)
    model.fit(x_train, y_train)
    return pd.Series(np.expm1(model.predict(x_target)), index=target.index).clip(lower=0)


def generate_baseline_forecasts(data: pd.DataFrame, target_years: list[int]) -> ForecastBundle:
    """Generate long-format quantile forecasts and evaluation metrics."""
    data = data.sort_values(["year", "iso3"]).reset_index(drop=True)
    prediction_rows: list[dict[str, object]] = []
    metric_rows: list[dict[str, object]] = []

    for target_year in target_years:
        train = data[data["year"] < target_year].copy()
        target = data[data["year"] == target_year].copy()
        if train.empty or target.empty:
            continue

        fallback = _fallback_rate(train)
        nb_alpha = _estimate_nb_alpha(train)
        gb_rates = _gradient_boosting_predictions(train, target) if len(train) >= 20 else None
        train_rates = _rate(train["cases"], train["population"])
        train_expected_counts = train_rates / 100_000 * train["population"]
        gb_residual_q = float(np.quantile(np.abs(train["cases"] - train_expected_counts), 0.9))

        wide_rows = []
        for row_index, row in target.iterrows():
            model_rates = {
                "country_historical_mean_rate": _group_rate(
                    train, row, ["iso3", "syndrome", "source_system"], fallback
                ),
                "last_observed_country_rate": _last_observed_rate(train, row, fallback),
                "region_syndrome_mean_rate": _group_rate(
                    train, row, ["region", "syndrome", "source_system"], fallback
                ),
                "empirical_negative_binomial_rate": _group_rate(
                    train, row, ["iso3", "syndrome", "source_system"], fallback
                ),
                "hierarchical_negative_binomial_rate": _hierarchical_rate(train, row, fallback),
            }
            if gb_rates is not None:
                model_rates["gradient_boosting_rate"] = float(gb_rates.loc[row_index])

            for model_name, rate in model_rates.items():
                mean = max(float(rate) / 100_000 * float(row["population"]), 1e-9)
                if model_name in {
                    "empirical_negative_binomial_rate",
                    "hierarchical_negative_binomial_rate",
                }:
                    quantile_values, probability_positive = _negative_binomial_summary(
                        mean, nb_alpha
                    )
                elif model_name == "gradient_boosting_rate":
                    quantile_values = {
                        0.05: max(0.0, mean - gb_residual_q),
                        0.5: mean,
                        0.95: mean + gb_residual_q,
                    }
                    probability_positive = 1.0 - float(np.exp(-mean))
                else:
                    quantile_values, probability_positive = _poisson_summary(mean)

                wide_rows.append(
                    {
                        "target_year": target_year,
                        "iso3": row["iso3"],
                        "country": row["country"],
                        "syndrome": row["syndrome"],
                        "source_system": row["source_system"],
                        "model": model_name,
                        "observed": int(row["cases"]),
                        "mean": mean,
                        "q05": quantile_values[0.05],
                        "q50": quantile_values[0.5],
                        "q95": quantile_values[0.95],
                        "probability_positive": probability_positive,
                    }
                )

                for quantile, value in quantile_values.items():
                    prediction_rows.append(
                        {
                            "forecast_date": f"{target_year - 1}-12-31",
                            "target": "annual reported hantavirus cases",
                            "horizon": "1 year",
                            "location": row["country"],
                            "iso3": row["iso3"],
                            "syndrome": row["syndrome"],
                            "source_system": row["source_system"],
                            "model": model_name,
                            "quantile": quantile,
                            "value": value,
                        }
                    )

        wide = pd.DataFrame.from_records(wide_rows)
        for model_name, group in wide.groupby("model"):
            wis = weighted_interval_score(
                group["observed"],
                group["q50"],
                [group["q05"]],
                [group["q95"]],
                [0.1],
            )
            metric_rows.append(
                {
                    "target_year": target_year,
                    "model": model_name,
                    "n": len(group),
                    "mean_wis": float(np.mean(wis)),
                    "coverage_90": interval_coverage(group["observed"], group["q05"], group["q95"]),
                    "mae": float(np.mean(np.abs(group["observed"] - group["q50"]))),
                    "poisson_deviance": float(
                        np.mean(poisson_deviance(group["observed"], group["mean"]))
                    ),
                    "brier_any_case": brier_score(
                        (group["observed"] > 0).astype(int),
                        group["probability_positive"],
                    ),
                }
            )

    return ForecastBundle(
        predictions=pd.DataFrame.from_records(prediction_rows),
        metrics=pd.DataFrame.from_records(metric_rows),
    )
