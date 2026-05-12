from hantavirus_predictor.ingest.terraclimate import (
    build_terraclimate_manifest,
    terraclimate_file_url,
)


def test_terraclimate_manifest_uses_expected_file_server_urls():
    url = terraclimate_file_url("ppt", 2023)
    assert url.endswith("TerraClimate_ppt_2023.nc")

    manifest = build_terraclimate_manifest([2023])
    assert set(manifest["status"]) == {"source_discovered_not_aggregated"}
