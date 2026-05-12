"""Validation rules for the manual international country-level case table."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DEFAULT_CASE_TABLE = Path("data/manual/international_country_cases.csv")

REQUIRED_COLUMNS = {
    "iso3",
    "country",
    "region",
    "syndrome",
    "pathogen_or_virus",
    "case_definition",
    "reporting_system",
    "year",
    "cases",
    "deaths",
    "population",
    "source_url",
    "source_title",
    "accessed_date",
    "source_type",
    "quality_grade",
    "notes",
}

ALLOWED_SYNDROMES = {
    "HFRS",
    "HPS",
    "HCPS",
    "hantavirus_infection",
    "mixed_or_unspecified",
}

ALLOWED_QUALITY_GRADES = {"A", "B", "C", "D"}


@dataclass(frozen=True)
class ValidationResult:
    messages: list[str]
    ok: bool


def _parse_int(value: str, field_name: str, row_number: int, messages: list[str]) -> int | None:
    if value == "":
        messages.append(f"row {row_number}: {field_name} is blank")
        return None
    try:
        parsed = int(value)
    except ValueError:
        messages.append(f"row {row_number}: {field_name} must be an integer")
        return None
    if parsed < 0:
        messages.append(f"row {row_number}: {field_name} must be nonnegative")
        return None
    return parsed


def validate_file(path: Path) -> ValidationResult:
    if not path.exists():
        return ValidationResult([f"MISSING optional manual file: {path}"], ok=True)

    messages: list[str] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        actual_columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - actual_columns)
        if missing:
            return ValidationResult(
                [f"{path}: missing columns: {', '.join(missing)}"],
                ok=False,
            )

        keys: Counter[tuple[str, str, str, str, str]] = Counter()
        for row_number, row in enumerate(reader, start=2):
            iso3 = row["iso3"].strip()
            if len(iso3) != 3 or not iso3.isalpha() or iso3 != iso3.upper():
                messages.append(f"row {row_number}: iso3 must be three uppercase letters")

            syndrome = row["syndrome"].strip()
            if syndrome not in ALLOWED_SYNDROMES:
                allowed = ", ".join(sorted(ALLOWED_SYNDROMES))
                messages.append(f"row {row_number}: syndrome must be one of: {allowed}")

            quality_grade = row["quality_grade"].strip()
            if quality_grade not in ALLOWED_QUALITY_GRADES:
                messages.append(f"row {row_number}: quality_grade must be A, B, C, or D")

            for required_text in (
                "country",
                "region",
                "case_definition",
                "reporting_system",
                "source_url",
                "source_title",
                "accessed_date",
                "source_type",
            ):
                if not row[required_text].strip():
                    messages.append(f"row {row_number}: {required_text} is required")

            year = _parse_int(row["year"].strip(), "year", row_number, messages)
            current_year_plus_one = date.today().year + 1
            if year is not None and not 1900 <= year <= current_year_plus_one:
                messages.append(f"row {row_number}: year is outside expected range")

            cases = _parse_int(row["cases"].strip(), "cases", row_number, messages)
            deaths = _parse_int(row["deaths"].strip(), "deaths", row_number, messages)
            population = _parse_int(row["population"].strip(), "population", row_number, messages)
            if cases is not None and deaths is not None and deaths > cases:
                messages.append(f"row {row_number}: deaths cannot exceed cases")
            if population is not None and population == 0:
                messages.append(f"row {row_number}: population must be greater than zero")

            key = (
                iso3,
                row["year"].strip(),
                syndrome,
                row["pathogen_or_virus"].strip(),
                row["reporting_system"].strip(),
            )
            keys[key] += 1

    duplicates = [key for key, count in keys.items() if count > 1]
    for key in duplicates:
        messages.append(
            "duplicate key iso3/year/syndrome/pathogen_or_virus/reporting_system: "
            + "|".join(key)
        )

    if messages:
        return ValidationResult(messages, ok=False)
    return ValidationResult([f"OK: {path}"], ok=True)
