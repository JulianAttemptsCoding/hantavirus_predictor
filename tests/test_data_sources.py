from hantavirus_predictor.data_sources import DATA_SOURCES, get_source


def test_core_sources_are_registered():
    ids = {source.source_id for source in DATA_SOURCES}
    assert "neon_hantavirus_serology" in ids
    assert "neon_small_mammal_box_trapping" in ids
    assert "cdc_hantavirus_cases_public" in ids
    assert "cdc_or_state_county_cases_restricted" in ids


def test_county_cases_are_marked_restricted():
    source = get_source("cdc_or_state_county_cases_restricted")
    assert source.manual_required is True
    assert source.spatial_unit == "county or finer"


def test_neon_hantavirus_is_public_but_time_limited():
    source = get_source("neon_hantavirus_serology")
    assert source.manual_required is False
    assert "2019" in source.coverage

