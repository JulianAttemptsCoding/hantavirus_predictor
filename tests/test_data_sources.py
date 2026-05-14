from hantavirus_predictor.data_sources import DATA_SOURCES, get_source


def test_core_sources_are_registered():
    ids = {source.source_id for source in DATA_SOURCES}
    assert "ecdc_hantavirus_surveillance" in ids
    assert "world_bank_indicators" in ids
    assert "faostat_land_use" in ids
    assert "terraclimate_global" in ids
    assert "mod13c2_global_vegetation" in ids
    assert "natural_earth_countries" in ids


def test_active_registry_is_eid_scoped():
    source_ids = {source.source_id for source in DATA_SOURCES}
    assert not any(source_id.startswith("neon_") for source_id in source_ids)
    assert "cdc_or_state_county_cases_restricted" not in source_ids


def test_ecdc_labels_require_manual_source_audit():
    source = get_source("ecdc_hantavirus_surveillance")
    assert source.manual_required is True
    assert source.spatial_unit == "EU/EEA country"


def test_modis_is_optional_and_quality_gated():
    source = get_source("mod13c2_global_vegetation")
    assert source.manual_required is True
    assert "quality-masked" in source.notes
