"""Penalized count models for the ECDC country-year benchmark."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import poisson

from hantavirus_predictor.metrics import (
    brier_score,
    interval_coverage,
    poisson_deviance,
    weighted_interval_score,
)
from hantavirus_predictor.models.feature_ablation import (
    FEATURE_SET_ORDER,
    FEATURE_SETS,
    _make_temporal_features,
    _prepare_features,
    _with_derived_public_features,
)


ALPHA_GRID = [0.01, 0.1, 1.0, 10.0]


@dataclass(frozen=True)
class CountModelBundle:
    predictions: pd.DataFrame
    metrics: pd.DataFrame
    tuning: pd.DataFrame


@dataclass(frozen=True)
class _FitResult:
    coef: np.ndarray
    mean: np.ndarray
    scale_mean: np.ndarray
    scale_std: np.ndarray


def run_penalized_poisson_models(data: pd.DataFrame) -> CountModelBundle:
    """Run validation-tuned penalized Poisson GLMs with population offsets."""
    data = _with_derived_public_features(data.copy())
    features = _make_temporal_features(data, excluded_year=2023)
    train_rows = data[data["year"].isin([2019, 2020, 2021])].copy()
    validation_rows = data[data["year"].eq(2022)].copy()
    test_rows = data[data["year"].eq(2023)].copy()
    train_features = features.loc[train_rows.index]
    validation_features = features.loc[validation_rows.index]
    test_features = features.loc[test_rows.index]

    prediction_rows: list[dict[str, object]] = []
    metric_rows: list[dict[str, object]] = []
    tuning_rows: list[dict[str, object]] = []

    for feature_set in FEATURE_SET_ORDER:
        prepared_validation = _prepare_features(
            train_features,
            validation_features,
            FEATURE_SETS[feature_set],
        )
        if not prepared_validation.model_columns:
            continue
        alpha_scores = []
        for alpha in ALPHA_GRID:
            fit = _fit_penalized_poisson(
                prepared_validation.train[prepared_validation.model_columns],
                train_rows,
                alpha,
            )
            validation_mean = _predict_mean(
                fit,
                prepared_validation.target[prepared_validation.model_columns],
                validation_rows,
            )
            score = _mean_wis(validation_rows["cases"].to_numpy(dtype=float), validation_mean)
            alpha_scores.append((alpha, score))
            tuning_rows.append(
                {
                    "feature_set": feature_set,
                    "alpha": alpha,
                    "validation_mean_wis": score,
                }
            )
        best_alpha = min(alpha_scores, key=lambda item: item[1])[0]

        train_plus_validation = pd.concat([train_rows, validation_rows], axis=0)
        train_plus_validation_features = features.loc[train_plus_validation.index]
        prepared_test = _prepare_features(
            train_plus_validation_features,
            test_features,
            FEATURE_SETS[feature_set],
        )
        fit = _fit_penalized_poisson(
            prepared_test.train[prepared_test.model_columns],
            train_plus_validation,
            best_alpha,
        )
        test_mean = _predict_mean(
            fit,
            prepared_test.target[prepared_test.model_columns],
            test_rows,
        )
        prediction_rows.extend(
            _prediction_records(feature_set, best_alpha, test_rows, test_mean)
        )
        metric_rows.append(
            _metric_record(
                feature_set,
                best_alpha,
                test_rows,
                test_mean,
                len(prepared_test.feature_names),
            )
        )

    return CountModelBundle(
        predictions=pd.DataFrame.from_records(prediction_rows),
        metrics=pd.DataFrame.from_records(metric_rows),
        tuning=pd.DataFrame.from_records(tuning_rows),
    )


def _fit_penalized_poisson(features: pd.DataFrame, rows: pd.DataFrame, alpha: float) -> _FitResult:
    x = features.to_numpy(dtype=float)
    scale_mean = x.mean(axis=0)
    scale_std = x.std(axis=0)
    scale_std[scale_std == 0] = 1.0
    x_scaled = (x - scale_mean) / scale_std
    y = rows["cases"].to_numpy(dtype=float)
    offset = np.log(rows["population"].to_numpy(dtype=float) / 100_000)

    def objective(coef: np.ndarray) -> tuple[float, np.ndarray]:
        intercept = coef[0]
        beta = coef[1:]
        eta = np.clip(offset + intercept + x_scaled @ beta, -20.0, 20.0)
        mu = np.exp(eta)
        value = float(np.sum(mu - y * eta) + 0.5 * alpha * np.sum(beta**2))
        residual = mu - y
        grad_intercept = np.sum(residual)
        grad_beta = x_scaled.T @ residual + alpha * beta
        return value, np.concatenate([[grad_intercept], grad_beta])

    initial_rate = max(float(rows["cases"].sum() / rows["population"].sum() * 100_000), 1e-9)
    initial = np.zeros(x_scaled.shape[1] + 1)
    initial[0] = np.log(initial_rate)
    result = minimize(
        lambda coef: objective(coef),
        initial,
        method="L-BFGS-B",
        jac=True,
        options={"maxiter": 1000},
    )
    coef = result.x if result.success else initial
    mean = _predict_from_scaled(x_scaled, offset, coef)
    return _FitResult(coef=coef, mean=mean, scale_mean=scale_mean, scale_std=scale_std)


def _predict_mean(fit: _FitResult, features: pd.DataFrame, rows: pd.DataFrame) -> np.ndarray:
    x = features.to_numpy(dtype=float)
    x_scaled = (x - fit.scale_mean) / fit.scale_std
    offset = np.log(rows["population"].to_numpy(dtype=float) / 100_000)
    return _predict_from_scaled(x_scaled, offset, fit.coef)


def _predict_from_scaled(x_scaled: np.ndarray, offset: np.ndarray, coef: np.ndarray) -> np.ndarray:
    eta = np.clip(offset + coef[0] + x_scaled @ coef[1:], -20.0, 20.0)
    return np.exp(eta)


def _mean_wis(observed: np.ndarray, mean: np.ndarray) -> float:
    q05 = poisson.ppf(0.05, np.maximum(mean, 1e-9))
    q50 = poisson.ppf(0.50, np.maximum(mean, 1e-9))
    q95 = poisson.ppf(0.95, np.maximum(mean, 1e-9))
    return float(np.mean(weighted_interval_score(observed, q50, [q05], [q95], [0.1])))


def _prediction_records(
    feature_set: str,
    alpha: float,
    rows: pd.DataFrame,
    mean: np.ndarray,
) -> list[dict[str, object]]:
    mean = np.maximum(mean, 1e-9)
    q05 = poisson.ppf(0.05, mean)
    q50 = poisson.ppf(0.50, mean)
    q95 = poisson.ppf(0.95, mean)
    records = []
    for position, (_, row) in enumerate(rows.iterrows()):
        records.append(
            {
                "target_year": 2023,
                "feature_set": feature_set,
                "model": "penalized_poisson_glm",
                "alpha": alpha,
                "iso3": row["iso3"],
                "country": row["country"],
                "observed": int(row["cases"]),
                "mean": float(mean[position]),
                "q05": float(q05[position]),
                "q50": float(q50[position]),
                "q95": float(q95[position]),
                "probability_positive": float(1.0 - poisson.pmf(0, mean[position])),
            }
        )
    return records


def _metric_record(
    feature_set: str,
    alpha: float,
    rows: pd.DataFrame,
    mean: np.ndarray,
    feature_count: int,
) -> dict[str, object]:
    observed = rows["cases"].to_numpy(dtype=float)
    mean = np.maximum(mean, 1e-9)
    q05 = poisson.ppf(0.05, mean)
    q50 = poisson.ppf(0.50, mean)
    q95 = poisson.ppf(0.95, mean)
    wis = weighted_interval_score(observed, q50, [q05], [q95], [0.1])
    return {
        "target_year": 2023,
        "feature_set": feature_set,
        "model": "penalized_poisson_glm",
        "alpha": alpha,
        "n": len(rows),
        "mean_observed": float(np.mean(observed)),
        "mean_wis": float(np.mean(wis)),
        "relative_wis_observed_mean": (
            float(np.mean(wis) / np.mean(observed)) if np.mean(observed) > 0 else np.nan
        ),
        "coverage_90": interval_coverage(observed, q05, q95),
        "mean_interval_width_90": float(np.mean(q95 - q05)),
        "mae": float(np.mean(np.abs(observed - q50))),
        "poisson_deviance": float(np.mean(poisson_deviance(observed, mean))),
        "brier_any_case": brier_score(
            (observed > 0).astype(int),
            1.0 - poisson.pmf(0, mean),
        ),
        "final_model_features_before_one_hot": feature_count,
    }
