"""TerraClimate source manifest helpers."""

from __future__ import annotations

import pandas as pd


VARIABLES = {
    "ppt": "precipitation_mm",
    "tmin": "minimum_temperature_c",
    "tmax": "maximum_temperature_c",
    "vpd": "vapor_pressure_deficit_kpa",
    "soil": "soil_moisture_mm",
    "def": "climate_water_deficit_mm",
}

ANNUAL_FEATURES = {
    "ppt": ("terraclimate_ppt_annual_sum_mm", "sum"),
    "tmin": ("terraclimate_tmin_annual_mean_c", "mean"),
    "tmax": ("terraclimate_tmax_annual_mean_c", "mean"),
    "vpd": ("terraclimate_vpd_annual_mean_kpa", "mean"),
    "soil": ("terraclimate_soil_annual_mean_mm", "mean"),
    "def": ("terraclimate_def_annual_sum_mm", "sum"),
}


def terraclimate_file_url(variable: str, year: int) -> str:
    if variable not in VARIABLES:
        raise ValueError(f"Unsupported TerraClimate variable: {variable}")
    return (
        "http://thredds.northwestknowledge.net:8080/thredds/fileServer/"
        f"TERRACLIMATE_ALL/data/TerraClimate_{variable}_{year}.nc"
    )


def terraclimate_opendap_url(variable: str, year: int) -> str:
    return terraclimate_file_url(variable, year).replace("/fileServer/", "/dodsC/")


def annual_feature_column(variable: str) -> str:
    if variable not in ANNUAL_FEATURES:
        raise ValueError(f"Unsupported TerraClimate variable: {variable}")
    return ANNUAL_FEATURES[variable][0]


def annual_feature_stat(variable: str) -> str:
    if variable not in ANNUAL_FEATURES:
        raise ValueError(f"Unsupported TerraClimate variable: {variable}")
    return ANNUAL_FEATURES[variable][1]


def build_terraclimate_manifest(years: list[int]) -> pd.DataFrame:
    rows = []
    for year in years:
        for variable, feature_family in VARIABLES.items():
            rows.append(
                {
                    "year": year,
                    "variable": variable,
                    "feature_family": feature_family,
                    "url": terraclimate_file_url(variable, year),
                    "opendap_url": terraclimate_opendap_url(variable, year),
                    "annual_feature": annual_feature_column(variable),
                    "annual_stat": annual_feature_stat(variable),
                    "status": "source_discovered_not_aggregated",
                }
            )
    return pd.DataFrame.from_records(rows)
