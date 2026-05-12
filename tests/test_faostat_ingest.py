from zipfile import ZipFile

import pandas as pd

from hantavirus_predictor.ingest.faostat import LAND_USE_MEMBER, build_land_use_features


def test_build_land_use_features_maps_country_year_items(tmp_path):
    zip_path = tmp_path / "land.zip"
    rows = pd.DataFrame(
        {
            "Area": ["Austria", "Austria"],
            "Item": ["Cropland", "Forest land"],
            "Year": [2023, 2023],
            "Unit": ["1000 ha", "1000 ha"],
            "Value": [1320.0, 3890.0],
            "Flag": ["A", "A"],
        }
    )
    with ZipFile(zip_path, "w") as archive:
        archive.writestr(LAND_USE_MEMBER, rows.to_csv(index=False))

    countries = pd.DataFrame({"iso3": ["AUT"], "country": ["Austria"]})
    features = build_land_use_features(zip_path, countries, [2023])

    assert features.loc[0, "faostat_cropland_1000ha"] == 1320.0
    assert features.loc[0, "faostat_forest_land_1000ha"] == 3890.0
