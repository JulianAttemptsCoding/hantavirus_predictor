import numpy as np
import pandas as pd
import xarray as xr

from hantavirus_predictor.ingest.terraclimate_aggregate import (
    CountryMask,
    add_lag_features,
    annual_reduce,
    complete_country_year_grid,
    weighted_country_values,
)


def test_annual_reduce_keeps_all_nan_sum_cells_missing():
    values = xr.DataArray(
        np.array(
            [
                [[1.0, np.nan], [3.0, 4.0]],
                [[2.0, np.nan], [5.0, 6.0]],
            ]
        ),
        dims=("time", "lat", "lon"),
    )

    reduced = annual_reduce(values, "ppt")

    assert reduced.values[0, 0] == 3.0
    assert np.isnan(reduced.values[0, 1])


def test_weighted_country_values_uses_only_valid_masked_cells():
    mask = np.array([[True, True], [False, False]])
    weights = np.ones((2, 2))
    grid = np.array([[10.0, np.nan], [100.0, 100.0]])
    country_mask = CountryMask("AAA", "A", mask, weights, int(mask.sum()))

    values = weighted_country_values(grid, [country_mask])

    assert values.loc[0, "value"] == 10.0
    assert values.loc[0, "valid_cell_count"] == 1


def test_add_lag_features_shifts_within_country_only():
    data = pd.DataFrame(
        {
            "iso3": ["AAA", "AAA", "BBB", "BBB"],
            "year": [2020, 2021, 2020, 2021],
            "terraclimate_ppt_annual_sum_mm": [10.0, 20.0, 100.0, 200.0],
        }
    )

    lagged = add_lag_features(data, ["terraclimate_ppt_annual_sum_mm"], lags=(1,))

    aaa_2021 = lagged[(lagged["iso3"] == "AAA") & (lagged["year"] == 2021)].iloc[0]
    bbb_2021 = lagged[(lagged["iso3"] == "BBB") & (lagged["year"] == 2021)].iloc[0]
    assert aaa_2021["terraclimate_ppt_annual_sum_mm_lag1"] == 10.0
    assert bbb_2021["terraclimate_ppt_annual_sum_mm_lag1"] == 100.0


def test_complete_country_year_grid_includes_years_without_case_rows():
    countries = pd.DataFrame(
        {
            "iso3": ["AAA", "AAA", "BBB"],
            "country": ["A", "A", "B"],
            "year": [2020, 2021, 2021],
        }
    )

    grid = complete_country_year_grid(countries, [2020, 2021])

    assert len(grid) == 4
    assert {tuple(row) for row in grid[["iso3", "year"]].to_numpy()} == {
        ("AAA", 2020),
        ("AAA", 2021),
        ("BBB", 2020),
        ("BBB", 2021),
    }
