from __future__ import annotations

import pandas as pd

from hantavirus_predictor.models.feature_ablation import FEATURE_SET_ORDER, run_feature_ablation


def _example_panel() -> pd.DataFrame:
    rows = []
    countries = [
        ("AAA", "Country A", 1_000_000),
        ("BBB", "Country B", 2_000_000),
        ("CCC", "Country C", 500_000),
    ]
    for year in range(2019, 2024):
        for country_index, (iso3, country, population) in enumerate(countries):
            cases = (year - 2018) * (country_index + 1)
            rows.append(
                {
                    "iso3": iso3,
                    "country": country,
                    "region": "Europe",
                    "syndrome": "hantavirus_infection",
                    "source_system": "ECDC",
                    "eu_eea_status": "eu_member",
                    "surveillance_completeness": "comprehensive",
                    "quality_grade": "B",
                    "year": year,
                    "cases": cases,
                    "population": population,
                    "rural_population_pct_lag1": 20 + country_index,
                    "gdp_per_capita_current_usd_lag1": 30_000 + 1000 * country_index,
                    "rural_population_pct_lag1_missing": 0,
                    "gdp_per_capita_current_usd_lag1_missing": 0,
                    "faostat_land_area_1000ha_lag1": 1000 + 100 * country_index,
                    "faostat_agricultural_land_1000ha_lag1": 300 + 10 * year,
                    "faostat_cropland_1000ha_lag1": 150 + 5 * country_index,
                    "faostat_forest_land_1000ha_lag1": 400 - 10 * country_index,
                    "faostat_perm_meadows_pastures_1000ha_lag1": 100 + country_index,
                    "faostat_other_land_1000ha_lag1": 50 + country_index,
                    "faostat_land_use_joined": True,
                    "terraclimate_def_annual_sum_mm_lag1": 10 + country_index,
                    "terraclimate_ppt_annual_sum_mm_lag1": 700 + 20 * country_index,
                    "terraclimate_soil_annual_mean_mm_lag1": 50 + country_index,
                    "terraclimate_tmax_annual_mean_c_lag1": 18 + country_index,
                    "terraclimate_tmin_annual_mean_c_lag1": 7 + country_index,
                    "terraclimate_vpd_annual_mean_kpa_lag1": 1 + country_index / 10,
                    "terraclimate_def_annual_sum_mm_lag1_missing": 0,
                    "terraclimate_ppt_annual_sum_mm_lag1_missing": 0,
                    "terraclimate_soil_annual_mean_mm_lag1_missing": 0,
                    "terraclimate_tmax_annual_mean_c_lag1_missing": 0,
                    "terraclimate_tmin_annual_mean_c_lag1_missing": 0,
                    "terraclimate_vpd_annual_mean_kpa_lag1_missing": 0,
                }
            )
    return pd.DataFrame(rows)


def test_feature_ablation_emits_required_metrics_and_splits() -> None:
    bundle = run_feature_ablation(_example_panel())
    primary = bundle.metrics[bundle.metrics["split"].eq("primary_test_2023")]

    assert set(FEATURE_SET_ORDER).issubset(set(primary["feature_set"]))
    assert {
        "mean_wis",
        "relative_wis_observed_mean",
        "coverage_90",
        "mean_interval_width_90",
        "mae",
        "brier_any_case",
        "mase_last_observed_rate",
    }.issubset(bundle.metrics.columns)
    assert "leave_one_year_out_2022" in set(bundle.metrics["split"])
    assert not bundle.calibration.empty


def test_feature_screening_reports_model_counts_separately() -> None:
    bundle = run_feature_ablation(_example_panel())
    screening = bundle.feature_screening

    assert "raw_candidate_features" in screening.columns
    assert "final_model_features_before_one_hot" in screening.columns
    assert screening["final_model_features_before_one_hot"].between(1, 25).all()
