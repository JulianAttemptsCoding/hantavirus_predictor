"""Write the first international data audit report."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_OUTPUT = ROOT / "reports" / "01_international_data_audit.md"

ECDC_TOTALS = {
    2019: 4088,
    2020: 1693,
    2021: 4947,
    2022: 2185,
    2023: 1885,
}


def _markdown_table(data: pd.DataFrame) -> str:
    if data.empty:
        return "_No rows._"
    columns = [str(column) for column in data.columns]
    rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in data.iterrows():
        rows.append("| " + " | ".join(_format_cell(row[column]) for column in data.columns) + " |")
    return "\n".join(rows)


def _format_cell(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def _duplicate_report(data: pd.DataFrame) -> pd.DataFrame:
    keys = ["iso3", "year", "syndrome", "pathogen_or_virus", "reporting_system"]
    duplicates = data.groupby(keys).size().reset_index(name="rows")
    return duplicates[duplicates["rows"] > 1]


def _missingness(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for column in columns:
        missing = int(data[column].isna().sum()) if column in data else len(data)
        rows.append(
            {"field": column, "missing_rows": missing, "missing_pct": missing / len(data) * 100}
        )
    return pd.DataFrame(rows)


def build_report(data: pd.DataFrame) -> str:
    counts = (
        data.groupby(["syndrome", "source_system", "quality_grade"])
        .size()
        .reset_index(name="country_year_rows")
    )
    reconciliation = data.groupby("year", as_index=False)["cases"].sum()
    reconciliation["ecdc_reported_total"] = reconciliation["year"].map(ECDC_TOTALS)
    reconciliation["difference"] = reconciliation["cases"] - reconciliation["ecdc_reported_total"]

    population_missing = int(data["population"].isna().sum())
    context_missing = _missingness(
        data,
        [
            "population",
            "rural_population_pct",
            "gdp_per_capita_current_usd",
            "deaths",
        ],
    )
    covariate_status = pd.DataFrame(
        [
            {
                "covariate_family": "World Bank population",
                "joined": True,
                "missing_rows": population_missing,
            },
            {
                "covariate_family": "World Bank rurality/GDP",
                "joined": True,
                "missing_rows": int(
                    data[["rural_population_pct", "gdp_per_capita_current_usd"]]
                    .isna()
                    .any(axis=1)
                    .sum()
                ),
            },
            {
                "covariate_family": "TerraClimate",
                "joined": bool(data["terraclimate_joined"].any()),
                "missing_rows": len(data),
            },
            {
                "covariate_family": "MODIS MOD13C2",
                "joined": bool(data["mod13c2_joined"].any()),
                "missing_rows": len(data),
            },
            {
                "covariate_family": "FAOSTAT land use",
                "joined": bool(data["faostat_land_use_joined"].any()),
                "missing_rows": len(data),
            },
        ]
    )
    duplicates = _duplicate_report(data)

    lines = [
        "# International Data Audit",
        "",
        "Status: reproducible ECDC seed audit for the international country-year track.",
        "",
        "## Source Scope",
        "",
        "- Source: ECDC Hantavirus infection - Annual Epidemiological Report for 2023.",
        "- Case rows: EU/EEA country-year rows from ECDC Table 1, 2019-2023.",
        "- Population denominators: World Bank SP.POP.TOTL joined by ISO3 and year.",
        "- Current source system: ECDC only. PAHO/China rows are intentionally not pooled yet.",
        "",
        "## Row Counts",
        "",
        _markdown_table(counts),
        "",
        "## Source Total Reconciliation",
        "",
        _markdown_table(reconciliation),
        "",
        "## Population Denominator Join",
        "",
        f"- Missing population rows: {population_missing} of {len(data)}.",
        "- Incidence is computed as cases / World Bank population * 100,000.",
        "",
        "## Missingness",
        "",
        _markdown_table(context_missing),
        "",
        "## Covariate Join Status",
        "",
        _markdown_table(covariate_status),
        "",
        "## Duplicate Keys",
        "",
        _markdown_table(duplicates),
        "",
        "## Frozen Split Proposal",
        "",
        "- Train: 2019-2021.",
        "- Validation: 2022.",
        "- Test: 2023.",
        "- Rolling-origin checks: train through 2020 -> test 2021; train through 2021 -> test 2022; train through 2022 -> test 2023.",
        "- Leave-country-out: code path should be exercised now, but publication claims require more years or source systems.",
        "",
        "## Limitations Before Manuscript Use",
        "",
        "- Deaths are only populated for 2023 because the extracted ECDC country-year table does not provide 2019-2022 country death counts.",
        "- TerraClimate, MODIS, and FAOSTAT covariates are represented by explicit unjoined flags in this milestone.",
        "- The current ECDC-only seed table validates the pipeline but is not the final international publication dataset.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_report(data), encoding="utf-8")
    print(f"Wrote audit report to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
