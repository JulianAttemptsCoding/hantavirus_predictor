# Agent Handoff

Start here after opening the repo.

## First Commands

```powershell
git status --short --branch
python -m pip install -e ".[dev]"
python tools/summarize_neon_products.py
python tools/create_ecdc_case_table.py --accessed-date 2026-05-12
python tools/validate_international_cases.py --strict
python tools/build_international_dataset.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/validate_manual_data.py
pytest
python -m ruff check src tests tools
```

## Read Order

1. `instructions.txt`
2. `docs/PROJECT_STATE.md`
3. `docs/SOURCE_ARCHIVE_AUDIT.md`
4. `docs/RESEARCH_CLAIMS_AUDIT.md`
5. `docs/INTERNATIONAL_PUBLICATION_AND_MARKETING_PLAN.md`
6. `docs/DATA_REQUIREMENTS.md`
7. `docs/PUBLICATION_ROADMAP.md`
8. `docs/BLOCKER_RESPONSE_PLAN.md`
9. `configs/data_catalog.yaml`
10. `configs/modeling_plan.yaml`

## Rules For Future Agents

- Do not trust the extracted ZIP package QA reports as real validation.
- Do not copy archive code into `src/` unless tests are ported and passing.
- Do not make human county-level claims without a documented restricted data source.
- Treat international country-year modeling as the primary publication track.
- Do not pool HFRS and HPS/HCPS without explicit syndrome and source-system strata.
- Do not skip simple baselines.
- Do not hide negative results. For this project, a rigorous "complex models do not help with public data" paper may still be publishable.
- Keep raw data out of git. Commit schemas, manifests, checksums, and scripts.

## Immediate Next Tasks

1. Add TerraClimate country-year climate features.
2. Add MODIS MOD13C2 NDVI/EVI features after Earthdata credentials or a credentialed export path exist.
3. Add FAOSTAT land-use covariates.
4. Extend `data/manual/international_country_cases.csv` with PAHO and China CDC rows only when provenance is complete.
5. Add calibration plots from `data/processed/international_baseline_predictions.csv`.
6. Implement a proper negative-binomial GLM or Bayesian hierarchical model if dependencies are approved.
7. Keep U.S./NEON as mechanistic support and fallback manuscript.
8. Only then evaluate PINN, TimesFM, or graph models.

## Expected First Milestone

Delivered locally by tracked scripts:

`reports/01_international_data_audit.md`
`reports/02_international_baselines.md`

Minimum contents:

- Country-year row counts by syndrome, source system, and quality grade.
- Source total reconciliation against ECDC/PAHO/China CDC inputs.
- Population denominator join report.
- Climate, vegetation, and land-use covariate missingness.
- Missingness and duplicate report.
- Exact train/validation/test split proposal.

Generated `data/` and `reports/` files are ignored by git. Rebuild them with the first-command block.
