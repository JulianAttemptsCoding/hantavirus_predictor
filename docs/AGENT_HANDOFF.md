# Agent Handoff

Start here after opening the repo.

## First Commands

```powershell
git status --short --branch
python -m pip install -e ".[dev,geo]"
python tools/summarize_neon_products.py
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
python tools/validate_manual_data.py
pytest
python -m ruff check src tests tools
```

## Read Order

1. `docs/PROJECT_STATE.md`
2. `docs/SOURCE_ARCHIVE_AUDIT.md`
3. `docs/RESEARCH_CLAIMS_AUDIT.md`
4. `docs/PAPER_IMPLEMENTATION_PLAN_AND_BLOCKERS.md`
5. `docs/PUBLICATION_FIRST_DIFFERENTIATION_PLAN.md`
6. `docs/INTERNATIONAL_PUBLICATION_AND_MARKETING_PLAN.md`
7. `docs/DATA_REQUIREMENTS.md`
8. `docs/PUBLICATION_ROADMAP.md`
9. `docs/BLOCKER_RESPONSE_PLAN.md`
10. `configs/data_catalog.yaml`
11. `configs/modeling_plan.yaml`

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

1. Treat TerraClimate as implemented for the ECDC country-year path; rerun it with the first-command block when rebuilding local ignored data.
2. Add feature ablation tables that compare context only, FAOSTAT, TerraClimate, and all public covariates.
3. Decide whether MODIS aggregation is feasible locally; if yes, implement QA-masked NDVI/EVI country-year features. If not, remove vegetation claims from the manuscript.
4. Extend `data/manual/international_country_cases.csv` with PAHO and China CDC rows only after covariate QA.
5. Keep simulation as reservoir-spillover/scenario stress testing, not generic human spread.
6. Only then evaluate PINN, TimesFM, or graph models.

## Expected First Milestone

Delivered locally by tracked scripts:

`reports/01_international_data_audit.md`
`reports/02_international_baselines.md`
`reports/05_publication_readiness_gate.md`

Minimum contents:

- Country-year row counts by syndrome, source system, and quality grade.
- Source total reconciliation against ECDC/PAHO/China CDC inputs.
- Population denominator join report.
- Climate and land-use covariate missingness; vegetation only if MODIS is implemented.
- Missingness and duplicate report.
- Exact train/validation/test split proposal.

Generated `data/` and `reports/` files are ignored by git. Rebuild them with the first-command block.

Credential note: `nasa earthdata acc info.txt` is ignored by git. Use `python tools/check_earthdata_credentials.py` to confirm it parses without printing secrets.
