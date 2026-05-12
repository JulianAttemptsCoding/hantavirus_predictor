# Reproducibility Manifest

Last updated: 2026-05-12

This manifest defines the minimum reproducibility package required before
journal submission.

## Environment

Install from repo root:

```powershell
python -m pip install -e ".[dev,geo]"
```

Minimum QA:

```powershell
python -m pytest
python -m ruff check src tests tools
```

## Rebuild Commands

Run from repo root:

```powershell
python tools/create_ecdc_case_table.py --accessed-date 2026-05-12
python tools/validate_international_cases.py --strict
python tools/download_faostat_land_use.py
python tools/create_terraclimate_manifest.py
python tools/download_natural_earth_countries.py
python tools/aggregate_terraclimate_country_year.py
python tools/build_international_dataset.py
python tools/create_mod13c2_manifest.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/plot_international_baselines.py
python tools/run_markov_simulation.py
python tools/write_paper_readiness_report.py
python tools/check_publication_readiness.py
```

## Source Data Policy

Tracked:

- Code.
- Tests.
- Schemas.
- Configs.
- Documentation.
- Empty `.gitkeep` placeholders.

Ignored:

- Raw downloads.
- Processed data.
- Reports.
- Figures.
- Model artifacts.
- Credentials.

Credential rule:

- `nasa earthdata acc info.txt` must stay ignored.
- Do not print, stage, or commit credentials.

## Source Attribution Requirements

ECDC:

- Cite the ECDC Annual Epidemiological Report for 2023.
- Acknowledge ECDC as the surveillance source.

World Bank:

- Dataset terms default to CC BY 4.0 unless specifically labeled otherwise.
- Attribute World Bank data in data availability and relevant tables.

FAOSTAT:

- Attribute FAO/FAOSTAT for land-use data.

TerraClimate:

- Cite Abatzoglou et al. 2018, Scientific Data, doi:10.1038/sdata.2017.191.

Natural Earth:

- Public domain. Recommended attribution: "Made with Natural Earth. Free
  vector and raster map data at naturalearthdata.com."

MODIS:

- Use only MOD13C2 Version 6.1 unless the plan is updated.
- Record product version, access date, granule list, QA mask, and checksums.

## Checksums And Archive

Before submission:

1. Generate SHA-256 checksums for final processed tables and reports.
2. Create a GitHub release tag matching the manuscript version.
3. Deposit final processed tables, documentation, and code snapshot on Zenodo
   or OSF if source licenses allow redistribution.
4. Add DOI to the manuscript data availability statement.

Large-file handling:

- Do not commit raw downloads above normal git size limits.
- Document exact source URLs, access dates, and checksums.
- Use Zenodo/OSF for publication snapshots, not ad hoc zip packages.

## Final Reproducibility Gate

The publication package is not ready until:

- ECDC annual totals reconcile.
- Strict schema validation passes.
- Baseline metrics include WIS, relative WIS, coverage, interval width, MAE,
  deviance, and Brier score.
- TerraClimate per-variable missingness is reported.
- Non-comprehensive surveillance rows are flagged.
- No credentials are tracked.
- `pytest`, `ruff`, and `git diff --check` pass.
