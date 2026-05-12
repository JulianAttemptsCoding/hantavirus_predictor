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


def terraclimate_file_url(variable: str, year: int) -> str:
    if variable not in VARIABLES:
        raise ValueError(f"Unsupported TerraClimate variable: {variable}")
    return (
        "http://thredds.northwestknowledge.net:8080/thredds/fileServer/"
        f"TERRACLIMATE_ALL/data/TerraClimate_{variable}_{year}.nc"
    )


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
                    "status": "source_discovered_not_aggregated",
                }
            )
    return pd.DataFrame.from_records(rows)
