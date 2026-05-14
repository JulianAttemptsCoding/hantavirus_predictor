"""Write EID model-input Table 1 for the EU/EEA benchmark."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.models.feature_ablation import (  # noqa: E402
    FEATURE_SETS,
    _make_temporal_features,
    _with_derived_public_features,
)

DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_CSV = ROOT / "docs" / "submission_eid" / "tables" / "table1_model_inputs.csv"
DEFAULT_MD = ROOT / "docs" / "submission_eid" / "tables" / "table1_model_inputs.md"


VARIABLE_META: dict[str, dict[str, str]] = {
    "cases": {
        "category": "outcome",
        "definition": "Annual reported hantavirus infection cases.",
        "unit": "reported cases",
        "source": "ECDC Annual Epidemiological Report/TESSy-derived public tables",
        "reason": "Primary reported-incidence label.",
        "limitation": "Reported cases are not true infections and depend on surveillance systems.",
    },
    "population": {
        "category": "denominator",
        "definition": "Country-year population denominator.",
        "unit": "persons",
        "source": "World Bank/Open Data population series",
        "reason": "Converts reported counts to rates and population-offset predictions.",
        "limitation": "Annual national denominator does not capture subnational exposure.",
    },
    "incidence_per_100k": {
        "category": "derived outcome",
        "definition": "Reported annual cases per 100,000 population.",
        "unit": "reported cases per 100,000 population",
        "source": "Derived from ECDC cases and World Bank population",
        "reason": "Standardized public surveillance outcome.",
        "limitation": "Rate inherits reporting incompleteness from case labels.",
    },
}


SOURCE_RULES = [
    ("country_", "surveillance history", "Derived from prior ECDC country-year labels"),
    ("region_", "surveillance history", "Derived from prior ECDC regional panel labels"),
    ("overall_", "surveillance history", "Derived from prior ECDC panel labels"),
    ("target_year", "time/surveillance", "Derived from target year"),
    ("pandemic_period", "time/surveillance", "Derived from year indicator"),
    ("rural_population", "demographic context", "World Bank/Open Data"),
    ("gdp_per_capita", "demographic context", "World Bank/Open Data"),
    ("faostat_", "land use", "FAOSTAT land-use and land-cover statistics"),
    ("terraclimate_", "climate and water balance", "TerraClimate"),
    ("eu_eea_status", "source quality", "ECDC public surveillance metadata"),
    ("surveillance_completeness", "source quality", "ECDC public surveillance metadata"),
    ("quality_grade", "source quality", "Manual source-quality audit"),
]


def _model_variables() -> list[str]:
    ordered: list[str] = []
    for variables in FEATURE_SETS.values():
        for variable in variables:
            if variable not in ordered:
                ordered.append(variable)
    return ordered


def _category_source(variable: str) -> tuple[str, str]:
    for prefix, category, source in SOURCE_RULES:
        if variable == prefix or variable.startswith(prefix):
            return category, source
    return "model input", "Derived public benchmark table"


def _definition(variable: str) -> str:
    return (
        variable.replace("_lag1", " lagged 1 year")
        .replace("_missing", " missingness indicator")
        .replace("_", " ")
        .strip()
        .capitalize()
        + "."
    )


def _unit(variable: str) -> str:
    if variable.endswith("_missing") or variable.endswith("_joined"):
        return "binary indicator"
    if variable.endswith("_share_lag1"):
        return "share of land area"
    if "population_pct" in variable:
        return "percent"
    if "gdp_per_capita" in variable:
        return "current US dollars"
    if "tmax" in variable or "tmin" in variable:
        return "degrees Celsius"
    if "ppt" in variable or "def" in variable or "soil" in variable:
        return "millimeters"
    if "vpd" in variable:
        return "kilopascals"
    if "rate" in variable:
        return "reported cases per 100,000 population"
    if variable in {"target_year", "country_prior_years"}:
        return "years"
    return "unitless/category"


def _lag(variable: str) -> str:
    if variable.endswith("_lag1") or "_lag1_" in variable:
        return "1 year"
    if variable.startswith(("country_", "region_", "overall_")):
        return "prior years only"
    return "none"


def _feature_sets(variable: str) -> str:
    return ";".join(name for name, variables in FEATURE_SETS.items() if variable in variables)


def _range(values: pd.Series) -> tuple[str, str]:
    numeric = pd.to_numeric(values, errors="coerce")
    if numeric.notna().any():
        return f"{numeric.min():.6g}", f"{numeric.max():.6g}"
    cats = sorted(str(value) for value in values.dropna().unique())
    return "|".join(cats[:8]), "|".join(cats[-8:])


def build_table(data: pd.DataFrame) -> pd.DataFrame:
    data = _with_derived_public_features(data.copy())
    features = _make_temporal_features(data, excluded_year=2023)
    combined = features.copy()
    for column in data.columns:
        if column not in combined.columns:
            combined[column] = data[column]

    rows: list[dict[str, object]] = []
    variables = ["cases", "population", "incidence_per_100k", *_model_variables()]
    variables.append("mod13c2_ndvi_evi_excluded")
    variables.append("natural_earth_country_boundary")

    train = combined[combined["year"].isin([2019, 2020, 2021])]
    validation = combined[combined["year"].eq(2022)]
    test = combined[combined["year"].eq(2023)]
    for variable in variables:
        if variable in VARIABLE_META:
            meta = VARIABLE_META[variable]
            category = meta["category"]
            source = meta["source"]
            definition = meta["definition"]
            reason = meta["reason"]
            limitation = meta["limitation"]
        elif variable == "mod13c2_ndvi_evi_excluded":
            category, source = "excluded candidate covariate", "MODIS MOD13C2/NASA Earthdata"
            definition = "Candidate NDVI/EVI vegetation indices excluded from primary models."
            reason = "Documented exclusion prevents unsupported vegetation claims."
            limitation = "Quality-masked country-year aggregation not implemented for this submission."
        elif variable == "natural_earth_country_boundary":
            category, source = "display boundary", "Natural Earth"
            definition = "Country boundary data used for country-level maps."
            reason = "Supports national-scale figure display only."
            limitation = "Not a predictor and not evidence of within-country risk variation."
        else:
            category, source = _category_source(variable)
            definition = _definition(variable)
            reason = "Pre-specified public-data feature family."
            limitation = "Ecologic country-year covariate; not causal or individual-level."

        if variable in combined.columns:
            train_min, train_max = _range(train[variable])
            missing_train = int(train[variable].isna().sum())
            missing_validation = int(validation[variable].isna().sum())
            missing_test = int(test[variable].isna().sum())
        else:
            train_min = train_max = "not applicable"
            missing_train = missing_validation = missing_test = 0

        rows.append(
            {
                "category": category,
                "variable_name": variable,
                "plain_language_definition": definition,
                "unit": _unit(variable),
                "source": source,
                "source_url_or_citation": "See manuscript references and source manifest.",
                "years_available": "2019-2023" if variable in combined.columns else "not used",
                "lag_used": _lag(variable),
                "training_range_min": train_min,
                "training_range_max": train_max,
                "missing_count_training": missing_train,
                "missing_count_validation": missing_validation,
                "missing_count_test": missing_test,
                "missingness_rule": "Training-only imputation; indicators retained where defined.",
                "included_in_feature_sets": _feature_sets(variable) or "not a model predictor",
                "reason_for_inclusion": reason,
                "known_limitation": limitation,
                "leakage_check": "No target-year case count used as predictor.",
            }
        )
    return pd.DataFrame.from_records(rows)


def _markdown_table(data: pd.DataFrame) -> str:
    columns = list(data.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in data.iterrows():
        lines.append("| " + " | ".join(str(row[column]).replace("|", "/") for column in columns) + " |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--csv", default=str(DEFAULT_CSV))
    parser.add_argument("--md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    table = build_table(pd.read_csv(args.input))
    csv_path = Path(args.csv)
    md_path = Path(args.md)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(csv_path, index=False)
    md_path.write_text(
        "# Table 1. Public data sources and model inputs\n\n"
        + _markdown_table(table)
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(table)} model-input rows to {csv_path}")
    print(f"Wrote Markdown table to {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
