"""Feature-family ablation for the ECDC country-year benchmark."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from hantavirus_predictor.metrics import (
    brier_score,
    interval_coverage,
    poisson_deviance,
    weighted_interval_score,
)


FEATURE_SET_ORDER = [
    "surveillance_only",
    "context",
    "land_use",
    "climate",
    "all_public",
]

MAX_MODEL_FEATURES = 25
CORRELATION_THRESHOLD = 0.95
MISSINGNESS_THRESHOLD = 0.40

SURVEILLANCE_FEATURES = [
    "target_year",
    "pandemic_period",
    "country_historical_rate",
    "country_last_rate",
    "country_prior_years",
    "country_zero_share",
    "region_historical_rate",
    "overall_historical_rate",
]

CONTEXT_FEATURES = [
    "rural_population_pct_lag1",
    "gdp_per_capita_current_usd_lag1",
    "rural_population_pct_lag1_missing",
    "gdp_per_capita_current_usd_lag1_missing",
]

LAND_USE_FEATURES = [
    "faostat_agricultural_share_lag1",
    "faostat_cropland_share_lag1",
    "faostat_forest_share_lag1",
    "faostat_pasture_share_lag1",
    "faostat_other_land_share_lag1",
    "faostat_land_use_joined",
]

CLIMATE_FEATURES = [
    "terraclimate_def_annual_sum_mm_lag1",
    "terraclimate_ppt_annual_sum_mm_lag1",
    "terraclimate_soil_annual_mean_mm_lag1",
    "terraclimate_tmax_annual_mean_c_lag1",
    "terraclimate_tmin_annual_mean_c_lag1",
    "terraclimate_vpd_annual_mean_kpa_lag1",
    "terraclimate_def_annual_sum_mm_lag1_missing",
    "terraclimate_ppt_annual_sum_mm_lag1_missing",
    "terraclimate_soil_annual_mean_mm_lag1_missing",
    "terraclimate_tmax_annual_mean_c_lag1_missing",
    "terraclimate_tmin_annual_mean_c_lag1_missing",
    "terraclimate_vpd_annual_mean_kpa_lag1_missing",
]

ALL_PUBLIC_FEATURES = [
    "eu_eea_status",
    "surveillance_completeness",
    "quality_grade",
]

FEATURE_SETS = {
    "surveillance_only": SURVEILLANCE_FEATURES,
    "context": SURVEILLANCE_FEATURES + CONTEXT_FEATURES,
    "land_use": SURVEILLANCE_FEATURES + CONTEXT_FEATURES + LAND_USE_FEATURES,
    "climate": SURVEILLANCE_FEATURES
    + CONTEXT_FEATURES
    + LAND_USE_FEATURES
    + CLIMATE_FEATURES,
    "all_public": SURVEILLANCE_FEATURES
    + CONTEXT_FEATURES
    + LAND_USE_FEATURES
    + CLIMATE_FEATURES
    + ALL_PUBLIC_FEATURES,
}


@dataclass(frozen=True)
class AblationBundle:
    """Feature ablation outputs ready for CSV/report writing."""

    predictions: pd.DataFrame
    metrics: pd.DataFrame
    calibration: pd.DataFrame
    feature_screening: pd.DataFrame


@dataclass(frozen=True)
class _PreparedFeatures:
    train: pd.DataFrame
    target: pd.DataFrame
    feature_names: list[str]
    model_columns: list[str]
    raw_feature_count: int
    dropped_missing: list[str]
    dropped_constant: list[str]
    dropped_duplicate: list[str]
    dropped_correlated: list[str]
    dropped_cap: list[str]


def run_feature_ablation(data: pd.DataFrame) -> AblationBundle:
    """Run primary split and leave-one-year-out feature ablations."""
    data = _with_derived_public_features(data.copy())
    prediction_rows: list[dict[str, object]] = []
    metric_rows: list[dict[str, object]] = []
    calibration_rows: list[dict[str, object]] = []
    screening_rows: list[dict[str, object]] = []

    split_specs = [
        ("primary_validation_2022", [2019, 2020, 2021], 2022),
        ("primary_test_2023", [2019, 2020, 2021], 2023),
    ]
    split_specs.extend(
        (
            f"leave_one_year_out_{year}",
            [other for other in sorted(data["year"].unique()) if other != year],
            year,
        )
        for year in sorted(data["year"].unique())
    )

    for split_name, train_years, target_year in split_specs:
        train_rows = data[data["year"].isin(train_years)].copy()
        target_rows = data[data["year"] == target_year].copy()
        if train_rows.empty or target_rows.empty:
            continue

        feature_frame = _make_temporal_features(data, excluded_year=target_year)
        train_feature_rows = feature_frame.loc[train_rows.index]
        target_feature_rows = feature_frame.loc[target_rows.index]

        for feature_set in FEATURE_SET_ORDER:
            prepared = _prepare_features(
                train_feature_rows,
                target_feature_rows,
                FEATURE_SETS[feature_set],
            )
            if not prepared.model_columns:
                continue

            model = Ridge(alpha=1.0)
            y_train = np.log1p(_rate(train_rows["cases"], train_rows["population"]))
            model.fit(prepared.train[prepared.model_columns], y_train)

            train_rate = np.expm1(model.predict(prepared.train[prepared.model_columns])).clip(min=0.0)
            train_mean = train_rate / 100_000 * train_rows["population"].to_numpy(dtype=float)
            train_residual = train_rows["cases"].to_numpy(dtype=float) - train_mean
            residual_q05 = float(np.quantile(train_residual, 0.05))
            residual_q25 = float(np.quantile(train_residual, 0.25))
            residual_q75 = float(np.quantile(train_residual, 0.75))
            residual_q95 = float(np.quantile(train_residual, 0.95))

            target_rate = np.expm1(model.predict(prepared.target[prepared.model_columns])).clip(
                min=0.0
            )
            target_mean = target_rate / 100_000 * target_rows["population"].to_numpy(dtype=float)
            q05 = np.maximum(0.0, target_mean + residual_q05)
            q25 = np.maximum(0.0, target_mean + residual_q25)
            q50 = target_mean
            q75 = np.maximum(q25, target_mean + residual_q75)
            q95 = np.maximum(q75, target_mean + residual_q95)
            probability_positive = 1.0 - np.exp(-np.maximum(target_mean, 1e-9))

            target_records = _prediction_records(
                split_name,
                target_year,
                feature_set,
                target_rows,
                target_mean,
                q05,
                q25,
                q50,
                q75,
                q95,
                probability_positive,
            )
            prediction_rows.extend(target_records)

            metrics = _metric_record(
                split_name,
                target_year,
                feature_set,
                target_rows,
                target_feature_rows,
                target_mean,
                q05,
                q50,
                q95,
                probability_positive,
                prepared,
            )
            metric_rows.append(metrics)
            calibration_rows.extend(
                _calibration_records(
                    split_name,
                    target_year,
                    feature_set,
                    target_rows["cases"].to_numpy(dtype=float),
                    q25,
                    q75,
                    q05,
                    q95,
                )
            )
            screening_rows.append(
                {
                    "split": split_name,
                    "target_year": target_year,
                    "feature_set": feature_set,
                    "raw_candidate_features": prepared.raw_feature_count,
                    "final_model_features_before_one_hot": len(prepared.feature_names),
                    "dropped_missingness": ";".join(prepared.dropped_missing),
                    "dropped_constant": ";".join(prepared.dropped_constant),
                    "dropped_duplicate": ";".join(prepared.dropped_duplicate),
                    "dropped_correlated": ";".join(prepared.dropped_correlated),
                    "dropped_feature_cap": ";".join(prepared.dropped_cap),
                    "final_features": ";".join(prepared.feature_names),
                }
            )

    return AblationBundle(
        predictions=pd.DataFrame.from_records(prediction_rows),
        metrics=pd.DataFrame.from_records(metric_rows),
        calibration=pd.DataFrame.from_records(calibration_rows),
        feature_screening=pd.DataFrame.from_records(screening_rows),
    )


def _with_derived_public_features(data: pd.DataFrame) -> pd.DataFrame:
    denominator = data["faostat_land_area_1000ha_lag1"].replace(0, np.nan)
    share_specs = {
        "faostat_agricultural_share_lag1": "faostat_agricultural_land_1000ha_lag1",
        "faostat_cropland_share_lag1": "faostat_cropland_1000ha_lag1",
        "faostat_forest_share_lag1": "faostat_forest_land_1000ha_lag1",
        "faostat_pasture_share_lag1": "faostat_perm_meadows_pastures_1000ha_lag1",
        "faostat_other_land_share_lag1": "faostat_other_land_1000ha_lag1",
    }
    for output, source in share_specs.items():
        data[output] = pd.to_numeric(data[source], errors="coerce") / denominator
    return data


def _make_temporal_features(data: pd.DataFrame, excluded_year: int) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    safe_history = data[data["year"] != excluded_year].copy()
    for index, row in data.iterrows():
        history = safe_history[safe_history["year"] < row["year"]]
        fallback = _fallback_rate(history)
        country_history = history[history["iso3"] == row["iso3"]]
        region_history = history[history["region"] == row["region"]]
        last_rate = fallback
        if not country_history.empty:
            last_row = country_history.sort_values("year").iloc[-1]
            last_rate = float(last_row["cases"] / last_row["population"] * 100_000)

        values = row.to_dict()
        values.update(
            {
                "target_year": int(row["year"]),
                "pandemic_period": int(row["year"] in {2020, 2021}),
                "overall_historical_rate": fallback,
                "country_historical_rate": _aggregate_rate(country_history, fallback),
                "country_last_rate": last_rate,
                "country_prior_years": int(country_history["year"].nunique()),
                "country_zero_share": (
                    float((country_history["cases"] == 0).mean()) if not country_history.empty else 0.0
                ),
                "region_historical_rate": _aggregate_rate(region_history, fallback),
            }
        )
        rows.append(values)
    return pd.DataFrame.from_records(rows, index=data.index)


def _fallback_rate(history: pd.DataFrame) -> float:
    if history.empty or history["population"].sum() <= 0:
        return 0.0
    return float(history["cases"].sum() / history["population"].sum() * 100_000)


def _aggregate_rate(history: pd.DataFrame, fallback: float) -> float:
    if history.empty or history["population"].sum() <= 0:
        return fallback
    return float(history["cases"].sum() / history["population"].sum() * 100_000)


def _prepare_features(
    train: pd.DataFrame,
    target: pd.DataFrame,
    candidate_features: list[str],
) -> _PreparedFeatures:
    existing = [column for column in candidate_features if column in train.columns]
    train_raw = train[existing].copy()
    target_raw = target[existing].copy()
    raw_feature_count = len(existing)

    dropped_missing = [
        column
        for column in existing
        if train_raw[column].isna().mean() > MISSINGNESS_THRESHOLD
        and column not in SURVEILLANCE_FEATURES
    ]
    train_raw = train_raw.drop(columns=dropped_missing)
    target_raw = target_raw.drop(columns=dropped_missing)

    numeric_columns = [
        column
        for column in train_raw.columns
        if pd.api.types.is_numeric_dtype(train_raw[column])
        or train_raw[column].dropna().isin([0, 1, True, False]).all()
    ]
    categorical_columns = [column for column in train_raw.columns if column not in numeric_columns]

    train_imputed = pd.DataFrame(index=train_raw.index)
    target_imputed = pd.DataFrame(index=target_raw.index)
    for column in numeric_columns:
        train_values = pd.to_numeric(train_raw[column], errors="coerce")
        target_values = pd.to_numeric(target_raw[column], errors="coerce")
        fill_value = train_values.mode(dropna=True).iloc[0] if _is_binary(train_values) else train_values.median()
        if pd.isna(fill_value):
            fill_value = 0.0
        train_imputed[column] = train_values.fillna(fill_value).astype(float)
        target_imputed[column] = target_values.fillna(fill_value).astype(float)

    for column in categorical_columns:
        train_imputed[column] = train_raw[column].fillna("missing").astype(str)
        target_imputed[column] = target_raw[column].fillna("missing").astype(str)

    dropped_constant = [
        column for column in train_imputed.columns if train_imputed[column].nunique(dropna=False) <= 1
    ]
    train_imputed = train_imputed.drop(columns=dropped_constant)
    target_imputed = target_imputed.drop(columns=dropped_constant)

    dropped_duplicate = _duplicate_columns(train_imputed)
    train_imputed = train_imputed.drop(columns=dropped_duplicate)
    target_imputed = target_imputed.drop(columns=dropped_duplicate)

    dropped_correlated = _correlated_columns(train_imputed)
    train_imputed = train_imputed.drop(columns=dropped_correlated)
    target_imputed = target_imputed.drop(columns=dropped_correlated)

    feature_names = list(train_imputed.columns)
    dropped_cap: list[str] = []
    if len(feature_names) > MAX_MODEL_FEATURES:
        keep = [column for column in _priority_order(candidate_features) if column in feature_names][
            :MAX_MODEL_FEATURES
        ]
        dropped_cap = [column for column in feature_names if column not in keep]
        train_imputed = train_imputed[keep]
        target_imputed = target_imputed[keep]
        feature_names = keep

    if not feature_names:
        return _PreparedFeatures(
            train=pd.DataFrame(index=train.index),
            target=pd.DataFrame(index=target.index),
            feature_names=[],
            model_columns=[],
            raw_feature_count=raw_feature_count,
            dropped_missing=dropped_missing,
            dropped_constant=dropped_constant,
            dropped_duplicate=dropped_duplicate,
            dropped_correlated=dropped_correlated,
            dropped_cap=dropped_cap,
        )

    final_feature_names = list(train_imputed.columns)
    train_model, target_model = _encode_categoricals(train_imputed, target_imputed)
    return _PreparedFeatures(
        train=train_model,
        target=target_model,
        feature_names=final_feature_names,
        model_columns=list(train_model.columns),
        raw_feature_count=raw_feature_count,
        dropped_missing=dropped_missing,
        dropped_constant=dropped_constant,
        dropped_duplicate=dropped_duplicate,
        dropped_correlated=dropped_correlated,
        dropped_cap=dropped_cap,
    )


def _is_binary(values: pd.Series) -> bool:
    unique = set(values.dropna().unique())
    return bool(unique) and unique.issubset({0, 1, 0.0, 1.0, True, False})


def _duplicate_columns(data: pd.DataFrame) -> list[str]:
    dropped: list[str] = []
    seen: dict[tuple[object, ...], str] = {}
    for column in data.columns:
        values = tuple(data[column].tolist())
        if values in seen:
            dropped.append(column)
        else:
            seen[values] = column
    return dropped


def _correlated_columns(data: pd.DataFrame) -> list[str]:
    numeric = data.select_dtypes(include=[np.number])
    if numeric.shape[1] < 2:
        return []
    corr = numeric.corr().abs()
    dropped: list[str] = []
    for column in corr.columns:
        if column in dropped:
            continue
        correlated = corr.index[(corr[column] > CORRELATION_THRESHOLD) & (corr.index != column)]
        for candidate in correlated:
            if candidate not in dropped and candidate not in SURVEILLANCE_FEATURES:
                dropped.append(candidate)
    return dropped


def _priority_order(candidate_features: Iterable[str]) -> list[str]:
    ordered = []
    for group in [
        SURVEILLANCE_FEATURES,
        CONTEXT_FEATURES,
        LAND_USE_FEATURES,
        CLIMATE_FEATURES,
        ALL_PUBLIC_FEATURES,
    ]:
        ordered.extend([column for column in group if column in candidate_features])
    return ordered


def _encode_categoricals(
    train: pd.DataFrame,
    target: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    combined = pd.concat([train, target], axis=0)
    categorical_columns = [
        column for column in combined.columns if not pd.api.types.is_numeric_dtype(combined[column])
    ]
    encoded = pd.get_dummies(combined, columns=categorical_columns, drop_first=False, dtype=float)
    train_encoded = encoded.iloc[: len(train)].copy()
    target_encoded = encoded.iloc[len(train) :].copy()
    return train_encoded, target_encoded


def _prediction_records(
    split_name: str,
    target_year: int,
    feature_set: str,
    target_rows: pd.DataFrame,
    mean: np.ndarray,
    q05: np.ndarray,
    q25: np.ndarray,
    q50: np.ndarray,
    q75: np.ndarray,
    q95: np.ndarray,
    probability_positive: np.ndarray,
) -> list[dict[str, object]]:
    rows = []
    arrays = {"mean": mean, "q05": q05, "q25": q25, "q50": q50, "q75": q75, "q95": q95}
    for position, (_, row) in enumerate(target_rows.iterrows()):
        record = {
            "split": split_name,
            "target_year": target_year,
            "feature_set": feature_set,
            "iso3": row["iso3"],
            "country": row["country"],
            "observed": int(row["cases"]),
            "probability_positive": float(probability_positive[position]),
        }
        for name, values in arrays.items():
            record[name] = float(values[position])
        rows.append(record)
    return rows


def _metric_record(
    split_name: str,
    target_year: int,
    feature_set: str,
    target_rows: pd.DataFrame,
    target_features: pd.DataFrame,
    mean: np.ndarray,
    q05: np.ndarray,
    q50: np.ndarray,
    q95: np.ndarray,
    probability_positive: np.ndarray,
    prepared: _PreparedFeatures,
) -> dict[str, object]:
    observed = target_rows["cases"].to_numpy(dtype=float)
    wis = weighted_interval_score(observed, q50, [q05], [q95], [0.1])
    naive = target_features["country_last_rate"].to_numpy(dtype=float) / 100_000
    naive = naive * target_rows["population"].to_numpy(dtype=float)
    denominator = float(np.mean(np.abs(observed - naive)))
    return {
        "split": split_name,
        "target_year": target_year,
        "feature_set": feature_set,
        "n": len(target_rows),
        "mean_observed": float(np.mean(observed)),
        "mean_wis": float(np.mean(wis)),
        "relative_wis_observed_mean": (
            float(np.mean(wis) / np.mean(observed)) if np.mean(observed) > 0 else np.nan
        ),
        "coverage_90": interval_coverage(observed, q05, q95),
        "mean_interval_width_90": float(np.mean(q95 - q05)),
        "mae": float(np.mean(np.abs(observed - q50))),
        "mase_last_observed_rate": (
            float(np.mean(np.abs(observed - q50)) / denominator) if denominator > 0 else np.nan
        ),
        "poisson_deviance": float(np.mean(poisson_deviance(observed, np.maximum(mean, 1e-9)))),
        "brier_any_case": brier_score((observed > 0).astype(int), probability_positive),
        "raw_candidate_features": prepared.raw_feature_count,
        "final_model_features_before_one_hot": len(prepared.feature_names),
    }


def _calibration_records(
    split_name: str,
    target_year: int,
    feature_set: str,
    observed: np.ndarray,
    q25: np.ndarray,
    q75: np.ndarray,
    q05: np.ndarray,
    q95: np.ndarray,
) -> list[dict[str, object]]:
    return [
        {
            "split": split_name,
            "target_year": target_year,
            "feature_set": feature_set,
            "nominal_coverage": 0.5,
            "empirical_coverage": interval_coverage(observed, q25, q75),
        },
        {
            "split": split_name,
            "target_year": target_year,
            "feature_set": feature_set,
            "nominal_coverage": 0.9,
            "empirical_coverage": interval_coverage(observed, q05, q95),
        },
    ]


def _rate(cases: pd.Series, population: pd.Series) -> pd.Series:
    return cases / population * 100_000
