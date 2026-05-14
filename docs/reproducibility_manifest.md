# Reproducibility Manifest

Last updated: 2026-05-14

This manifest defines the active reproducibility path for the EID benchmark.
The tracked submission snapshot is in `docs/submission_eid/`; generated raw and
processed data remain ignored and rebuildable.

## Environment

Install from the repository root:

```powershell
python -m pip install -e ".[dev,geo]"
```

## Full Rebuild

Run from the repository root:

```powershell
python tools/create_ecdc_case_table.py --accessed-date 2026-05-14
python tools/validate_international_cases.py --strict
python tools/download_faostat_land_use.py
python tools/create_terraclimate_manifest.py
python tools/download_natural_earth_countries.py
python tools/aggregate_terraclimate_country_year.py
python tools/build_international_dataset.py
python tools/create_mod13c2_manifest.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/run_markov_simulation.py
python tools/run_feature_ablation.py
python tools/run_count_models.py
python tools/run_sensitivity_power.py
python tools/write_eid_model_inputs_table.py
python tools/check_eid_model_inputs_table.py
python tools/run_surveillance_quality_sensitivity.py
python tools/run_country_influence.py
python tools/write_calibration_localization.py
python tools/run_detectability_screen.py --iterations 100
python tools/create_eid_figures.py
python tools/build_eid_docx.py
python tools/check_publication_readiness.py
python tools/check_eid_submission_readiness.py --strict
python -m pytest
python -m ruff check src tests tools
git diff --check
```

## Source Data Policy

Tracked:

- Code.
- Tests.
- Schemas.
- Configs.
- Documentation.
- EID manuscript and final submission artifacts.
- EID report/table snapshot under `docs/submission_eid/`.
- Empty `.gitkeep` placeholders for ignored data/report directories.

Ignored:

- Raw downloads.
- Processed data.
- Generated root reports.
- Root-level exploratory figures.
- Model artifacts.
- Credentials.
- Ad hoc ZIP archives.

Credential rule:

- `nasa earthdata acc info.txt` must stay ignored.
- Do not print, stage, or commit credentials.

## Source Attribution

ECDC:

- Cite the ECDC Annual Epidemiological Report for 2023.
- Preserve 2019-2023 total reconciliation.
- Preserve Belgium 2023 and Cyprus 2023 surveillance caveats.

World Bank:

- Attribute World Bank Open Data for population, rural population, and GDP context.

FAOSTAT:

- Attribute FAO/FAOSTAT for land-use data.

TerraClimate:

- Cite Abatzoglou et al. 2018, Scientific Data, doi:10.1038/sdata.2017.191.

Natural Earth:

- Attribute Natural Earth for map boundaries.

MODIS:

- Keep MODIS out of primary manuscript claims unless quality-masked aggregation
  passes the inclusion gate.

## Archive and DOI

Before final EID submission:

1. Confirm the working tree is clean.
2. Generate or verify a final reproducibility manifest with commit hash, OS,
   Python version, command list, row counts, figure DPI, and table paths.
3. Create a clean git tag for the submission version.
4. Deposit the clean archive on Zenodo or update the existing record.
5. Confirm the DOI resolves and points to the final archive version.

Do not upload old ZIP packages or the archive branch contents as the active EID
package.

## Final Local Gate

The package is locally ready for human portal preparation when all commands in
the full rebuild/QA sequence pass and the strict EID checker reports:

```text
EID readiness: PASS
```

Expected warnings are limited to human-only mailing address/phone and final
DOI/archive verification.
