"""Check EID model-input Table 1 completeness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.models.feature_ablation import FEATURE_SETS  # noqa: E402

DEFAULT_TABLE = ROOT / "docs" / "submission_eid" / "tables" / "table1_model_inputs.csv"

REQUIRED_COLUMNS = {
    "category",
    "variable_name",
    "plain_language_definition",
    "unit",
    "source",
    "source_url_or_citation",
    "years_available",
    "lag_used",
    "training_range_min",
    "training_range_max",
    "missing_count_training",
    "missing_count_validation",
    "missing_count_test",
    "missingness_rule",
    "included_in_feature_sets",
    "reason_for_inclusion",
    "known_limitation",
    "leakage_check",
}


def _required_variables() -> set[str]:
    variables: set[str] = {"cases", "population", "incidence_per_100k"}
    for feature_set in FEATURE_SETS.values():
        variables.update(feature_set)
    variables.update({"mod13c2_ndvi_evi_excluded", "natural_earth_country_boundary"})
    return variables


def check_table(table: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    missing_columns = REQUIRED_COLUMNS - set(table.columns)
    if missing_columns:
        errors.append(f"Missing columns: {sorted(missing_columns)}")

    if "variable_name" not in table.columns:
        return errors

    duplicates = table["variable_name"][table["variable_name"].duplicated()].tolist()
    if duplicates:
        errors.append(f"Duplicate variables: {duplicates}")

    missing_variables = sorted(_required_variables() - set(table["variable_name"]))
    if missing_variables:
        errors.append(f"Missing required variables: {missing_variables}")

    required_nonblank = REQUIRED_COLUMNS - {"missing_count_training", "missing_count_validation", "missing_count_test"}
    for column in sorted(required_nonblank & set(table.columns)):
        if table[column].isna().any() or table[column].astype(str).str.strip().eq("").any():
            errors.append(f"Blank values in {column}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    args = parser.parse_args()
    table_path = Path(args.table)
    if not table_path.exists():
        print(f"FAIL: missing table {table_path}")
        return 1
    errors = check_table(pd.read_csv(table_path))
    if errors:
        print("EID model-input Table 1: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("EID model-input Table 1: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
