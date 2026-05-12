"""Aggregate TerraClimate monthly grids to country-year features."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from hantavirus_predictor.ingest.terraclimate import (
    ANNUAL_FEATURES,
    annual_feature_column,
    annual_feature_stat,
)


EUROPE_CLIP_BOUNDS = (-31.5, 34.0, 45.5, 72.5)
NATURAL_EARTH_50M_URL = (
    "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
)
ISO_COLUMN_CANDIDATES = ("ISO_A3_EH", "ISO_A3", "ADM0_A3", "SOV_A3")


@dataclass(frozen=True)
class CountryMask:
    iso3: str
    country: str
    mask: np.ndarray
    weights: np.ndarray
    cell_count: int


def add_lag_features(
    data: pd.DataFrame,
    feature_columns: Iterable[str],
    lags: Iterable[int] = (1,),
    group_column: str = "iso3",
) -> pd.DataFrame:
    """Add non-leaky lagged country covariates sorted by country and year."""
    result = data.sort_values([group_column, "year"]).copy()
    for feature in feature_columns:
        for lag in lags:
            result[f"{feature}_lag{lag}"] = result.groupby(group_column)[feature].shift(lag)
    return result.sort_values(["iso3", "year"]).reset_index(drop=True)


def complete_country_year_grid(
    countries: pd.DataFrame,
    years: Iterable[int],
) -> pd.DataFrame:
    """Return every country-year combination needed for covariate lag construction."""
    country_rows = countries[["iso3", "country"]].drop_duplicates().sort_values(["iso3"])
    year_rows = pd.DataFrame({"year": sorted(int(year) for year in years)})
    return country_rows.merge(year_rows, how="cross")


def annual_reduce(data_array: object, variable: str) -> object:
    """Reduce a monthly TerraClimate xarray DataArray to an annual grid."""
    stat = annual_feature_stat(variable)
    if stat == "sum":
        return data_array.sum(dim="time", skipna=True, min_count=1)
    if stat == "mean":
        return data_array.mean(dim="time", skipna=True)
    raise ValueError(f"Unsupported annual statistic: {stat}")


def read_country_boundaries(
    boundaries_path: Path,
    countries: pd.DataFrame,
    clip_bounds: tuple[float, float, float, float] | None = EUROPE_CLIP_BOUNDS,
):
    """Read Natural Earth boundaries and return clipped country geometries."""
    try:
        import geopandas as gpd
        from shapely.geometry import box
    except ImportError as exc:  # pragma: no cover - exercised only without optional deps
        raise ImportError(
            "TerraClimate aggregation requires the geo optional dependencies: "
            "pip install -e .[geo]"
        ) from exc

    path = Path(boundaries_path)
    source = f"zip://{path.resolve().as_posix()}" if path.suffix == ".zip" else str(path)
    world = gpd.read_file(source)
    iso_column = next((column for column in ISO_COLUMN_CANDIDATES if column in world.columns), None)
    if iso_column is None:
        raise ValueError(
            "Could not find an ISO3 column in the boundary file. "
            f"Tried: {', '.join(ISO_COLUMN_CANDIDATES)}"
        )

    wanted = countries[["iso3", "country"]].drop_duplicates()
    selected = world[world[iso_column].isin(set(wanted["iso3"]))].copy()
    selected = selected.rename(columns={iso_column: "iso3"})
    if selected.crs is None:
        selected = selected.set_crs("EPSG:4326")
    selected = selected.to_crs("EPSG:4326")

    if clip_bounds is not None:
        selected["geometry"] = selected.geometry.intersection(box(*clip_bounds))
        selected = selected[~selected.geometry.is_empty & selected.geometry.notna()].copy()

    selected = selected.merge(wanted, on="iso3", how="left", validate="many_to_one")
    dissolved = selected[["iso3", "country", "geometry"]].dissolve(
        by=["iso3", "country"], as_index=False
    )
    return dissolved


def combined_bounds(
    boundaries,
    clip_bounds: tuple[float, float, float, float] | None = EUROPE_CLIP_BOUNDS,
    padding_degrees: float = 0.25,
) -> tuple[float, float, float, float]:
    min_lon, min_lat, max_lon, max_lat = boundaries.total_bounds
    bounds = (
        float(min_lon - padding_degrees),
        float(min_lat - padding_degrees),
        float(max_lon + padding_degrees),
        float(max_lat + padding_degrees),
    )
    if clip_bounds is None:
        return bounds
    return (
        max(bounds[0], clip_bounds[0]),
        max(bounds[1], clip_bounds[1]),
        min(bounds[2], clip_bounds[2]),
        min(bounds[3], clip_bounds[3]),
    )


def slice_dataset_to_bounds(dataset: object, bounds: tuple[float, float, float, float]) -> object:
    """Slice an xarray Dataset/DataArray to lon/lat bounds, handling descending latitude."""
    min_lon, min_lat, max_lon, max_lat = bounds
    lat_values = dataset["lat"].values
    lat_slice = slice(max_lat, min_lat) if lat_values[0] > lat_values[-1] else slice(min_lat, max_lat)
    return dataset.sel(lat=lat_slice, lon=slice(min_lon, max_lon))


def build_country_masks(
    boundaries,
    lat_values: np.ndarray,
    lon_values: np.ndarray,
    *,
    all_touched: bool = True,
) -> list[CountryMask]:
    """Rasterize country geometries onto a TerraClimate lon/lat grid."""
    try:
        from rasterio.features import geometry_mask
        from rasterio.transform import from_origin
        from shapely.geometry import mapping
    except ImportError as exc:  # pragma: no cover - exercised only without optional deps
        raise ImportError(
            "TerraClimate aggregation requires rasterio and shapely: pip install -e .[geo]"
        ) from exc

    lat = np.asarray(lat_values, dtype=float)
    lon = np.asarray(lon_values, dtype=float)
    if lat[0] < lat[-1]:
        raise ValueError("Latitude values must be descending before mask construction.")
    lon_res = float(abs(np.median(np.diff(lon))))
    lat_res = float(abs(np.median(np.diff(lat))))
    transform = from_origin(
        west=float(lon.min() - lon_res / 2),
        north=float(lat.max() + lat_res / 2),
        xsize=lon_res,
        ysize=lat_res,
    )
    lat_weights = np.cos(np.deg2rad(lat))[:, None]
    masks: list[CountryMask] = []
    for row in boundaries.itertuples(index=False):
        mask = geometry_mask(
            [mapping(row.geometry)],
            out_shape=(len(lat), len(lon)),
            transform=transform,
            invert=True,
            all_touched=all_touched,
        )
        weights = np.broadcast_to(lat_weights, mask.shape).copy()
        weights[~mask] = 0.0
        masks.append(
            CountryMask(
                iso3=row.iso3,
                country=row.country,
                mask=mask,
                weights=weights,
                cell_count=int(mask.sum()),
            )
        )
    return masks


def weighted_country_values(grid_values: np.ndarray, masks: list[CountryMask]) -> pd.DataFrame:
    rows = []
    values = np.asarray(grid_values, dtype=float)
    for country_mask in masks:
        valid = country_mask.mask & np.isfinite(values)
        weight_sum = float(country_mask.weights[valid].sum())
        value = (
            float(np.sum(values[valid] * country_mask.weights[valid]) / weight_sum)
            if weight_sum > 0
            else np.nan
        )
        rows.append(
            {
                "iso3": country_mask.iso3,
                "country": country_mask.country,
                "value": value,
                "valid_cell_count": int(valid.sum()),
                "raster_cell_count": country_mask.cell_count,
            }
        )
    return pd.DataFrame.from_records(rows)


def aggregate_terraclimate_country_year(
    cases: pd.DataFrame,
    manifest: pd.DataFrame,
    boundaries,
    *,
    variables: Iterable[str] | None = None,
    years: Iterable[int] | None = None,
    lags: Iterable[int] = (1,),
    bounds: tuple[float, float, float, float] | None = None,
    use_opendap: bool = True,
    all_touched: bool = True,
) -> pd.DataFrame:
    """Aggregate TerraClimate source rows into wide country-year features."""
    try:
        import xarray as xr
    except ImportError as exc:  # pragma: no cover - exercised only without optional deps
        raise ImportError("TerraClimate aggregation requires xarray: pip install -e .[geo]") from exc

    selected_variables = set(variables or ANNUAL_FEATURES.keys())
    selected_years = set(int(year) for year in (years or sorted(cases["year"].unique())))
    source_rows = manifest[
        manifest["variable"].isin(selected_variables) & manifest["year"].isin(selected_years)
    ].copy()
    if source_rows.empty:
        raise ValueError("No TerraClimate manifest rows match the requested years and variables.")

    base = complete_country_year_grid(cases[["iso3", "country"]], selected_years)
    feature_frames: list[pd.DataFrame] = []
    masks: list[CountryMask] | None = None

    for source in source_rows.sort_values(["year", "variable"]).itertuples(index=False):
        variable = source.variable
        url = getattr(source, "opendap_url", None) if use_opendap else None
        if not url or pd.isna(url):
            url = str(source.url).replace("/fileServer/", "/dodsC/") if use_opendap else source.url

        with xr.open_dataset(url) as dataset:
            dataset = slice_dataset_to_bounds(dataset, bounds or combined_bounds(boundaries))
            if float(dataset["lat"].values[0]) < float(dataset["lat"].values[-1]):
                dataset = dataset.sortby("lat", ascending=False)
            annual_grid = annual_reduce(dataset[variable], variable).load()
            if masks is None:
                masks = build_country_masks(
                    boundaries,
                    annual_grid["lat"].values,
                    annual_grid["lon"].values,
                    all_touched=all_touched,
                )
            values = weighted_country_values(annual_grid.values, masks)

        feature_column = annual_feature_column(variable)
        values = values.rename(
            columns={
                "value": feature_column,
                "valid_cell_count": f"{feature_column}_valid_cell_count",
                "raster_cell_count": f"{feature_column}_raster_cell_count",
            }
        )
        values["year"] = int(source.year)
        feature_frames.append(values)

    wide_features = (
        pd.concat(feature_frames, ignore_index=True)
        .groupby(["iso3", "country", "year"], as_index=False)
        .first()
    )
    features = base.merge(wide_features, on=["iso3", "country", "year"], how="left")

    annual_columns = [annual_feature_column(variable) for variable in sorted(selected_variables)]
    for column in annual_columns:
        features[f"{column}_missing"] = features[column].isna()
    features["terraclimate_joined"] = features[annual_columns].notna().any(axis=1)
    features = add_lag_features(features, annual_columns, lags=lags)
    for column in annual_columns:
        for lag in lags:
            lag_column = f"{column}_lag{lag}"
            features[f"{lag_column}_missing"] = features[lag_column].isna()
    return features.sort_values(["iso3", "year"]).reset_index(drop=True)
