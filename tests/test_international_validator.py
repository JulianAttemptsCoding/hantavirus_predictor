import csv

from hantavirus_predictor.validation.international_cases import REQUIRED_COLUMNS, validate_file


def _write_rows(path, rows):
    columns = list(REQUIRED_COLUMNS)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def _valid_row():
    return {
        "iso3": "ARG",
        "country": "Argentina",
        "region": "Americas",
        "syndrome": "HPS",
        "pathogen_or_virus": "Andes virus or unspecified New World hantavirus",
        "case_definition": "national confirmed HPS case definition",
        "reporting_system": "PAHO/WHO alert citing national source",
        "year": "2025",
        "cases": "66",
        "deaths": "21",
        "population": "45800000",
        "source_url": "https://www.paho.org/",
        "source_title": "PAHO epidemiological alert",
        "accessed_date": "2026-05-12",
        "source_type": "epidemiological_alert",
        "quality_grade": "B",
        "notes": "Example test row.",
    }


def test_validate_international_cases_accepts_complete_rows(tmp_path):
    path = tmp_path / "international_country_cases.csv"
    _write_rows(path, [_valid_row()])

    result = validate_file(path)

    assert result.ok is True


def test_validate_international_cases_rejects_mixed_or_unsourced_rows(tmp_path):
    path = tmp_path / "international_country_cases.csv"
    row = _valid_row()
    row["iso3"] = "arg"
    row["syndrome"] = "unknown"
    row["source_url"] = ""
    row["deaths"] = "99"
    _write_rows(path, [row])

    result = validate_file(path)

    assert result.ok is False
    assert any("iso3" in message for message in result.messages)
    assert any("syndrome" in message for message in result.messages)
    assert any("source_url" in message for message in result.messages)
    assert any("deaths cannot exceed cases" in message for message in result.messages)
