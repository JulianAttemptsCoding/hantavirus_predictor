"""Regression checks for EID submission-specific artifacts."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "docs" / "submission_eid"
TABLES = SUBMISSION / "tables"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_eid_model_inputs_table_has_required_reporting_fields() -> None:
    rows = _read_csv(TABLES / "table1_model_inputs.csv")
    assert rows

    required = {
        "category",
        "variable_name",
        "plain_language_definition",
        "unit",
        "source",
        "years_available",
        "lag_used",
        "training_range_min",
        "training_range_max",
        "missingness_rule",
        "included_in_feature_sets",
        "reason_for_inclusion",
        "known_limitation",
    }
    assert required <= set(rows[0])

    variables = {row["variable_name"] for row in rows}
    assert {"cases", "population", "incidence_per_100k"} <= variables
    assert any("MODIS" in row["source"] for row in rows)
    assert not any(row["variable_name"].strip() == "" for row in rows)


def test_surveillance_quality_sensitivity_prespecified_scenarios() -> None:
    rows = _read_csv(TABLES / "appendix_surveillance_quality_sensitivity.csv")
    scenarios = {row["scenario"] for row in rows}

    expected = {
        "primary_all_rows",
        "exclude_belgium_2023",
        "exclude_cyprus_2023",
        "exclude_belgium_2023_and_cyprus_2023",
        "retain_flagged_rows_with_indicator",
        "exclude_2020_training_rows",
        "exclude_2021_training_rows",
        "exclude_2020_2021_training_rows",
    }
    assert expected <= scenarios
    assert all(int(row["coverage_90_denominator"]) > 0 for row in rows)
    assert all("promotion_rule_passed" in row for row in rows)


def test_country_influence_addresses_finland_and_germany() -> None:
    rows = _read_csv(TABLES / "appendix_country_influence.csv")
    by_iso3 = {row["removed_iso3"]: row for row in rows}

    for iso3 in ("FIN", "DEU"):
        assert iso3 in by_iso3
        row = by_iso3[iso3]
        assert row["high_influence_prespecified"] == "True"
        assert row["conclusion_changes"] == "False"
        assert row["loo_best_ablation_feature_set"]


def test_calibration_localization_uses_exact_interval_counts() -> None:
    rows = _read_csv(TABLES / "appendix_calibration_localization.csv")
    assert rows
    assert {
        "covered_90",
        "observed_count",
        "lower_90",
        "predicted_median",
        "upper_90",
    } <= set(rows[0])
    assert {row["year"] for row in rows} == {"2023"}
    assert any(row["covered_90"] == "False" for row in rows)


def test_detectability_screen_keeps_null_false_positive_rate_low() -> None:
    rows = _read_csv(TABLES / "appendix_detectability_screen.csv")
    null_rows = [row for row in rows if row["effect_label"] == "none"]
    assert null_rows

    max_null_selection = max(
        float(row["covariate_selection_probability"]) for row in null_rows
    )
    assert max_null_selection <= 0.10
