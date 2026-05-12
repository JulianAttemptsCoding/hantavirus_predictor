# Agent Handoff

Start here after opening the repo.

## First Commands

```powershell
git status --short --branch
python -m pip install -e ".[dev]"
python tools/summarize_neon_products.py
python tools/validate_international_cases.py
python tools/validate_manual_data.py
pytest
```

## Read Order

1. `instructions.txt`
2. `docs/SOURCE_ARCHIVE_AUDIT.md`
3. `docs/RESEARCH_CLAIMS_AUDIT.md`
4. `docs/INTERNATIONAL_PUBLICATION_AND_MARKETING_PLAN.md`
5. `docs/DATA_REQUIREMENTS.md`
6. `docs/PUBLICATION_ROADMAP.md`
7. `docs/BLOCKER_RESPONSE_PLAN.md`
8. `configs/data_catalog.yaml`
9. `configs/modeling_plan.yaml`

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

1. Fill `data/manual/international_country_cases.csv` with ECDC country-year rows.
2. Run `python tools/validate_international_cases.py --strict`.
3. Reconcile extracted totals to official source totals and write `reports/01_international_data_audit.md`.
4. Join World Bank population denominators and reporting-context covariates.
5. Add TerraClimate, MODIS MOD13C2, and FAOSTAT country-year covariates.
6. Implement historical, persistence, negative-binomial, hierarchical, and gradient-boosting baselines.
7. Add WIS, log score/deviance, coverage, Brier score for pre-registered thresholds, and calibration plots.
8. Write a preregistered temporal and leave-country validation split file before tuning models.
9. Keep U.S./NEON as mechanistic support and fallback manuscript.
10. Only then evaluate PINN, TimesFM, or graph models.

## Expected First Milestone

Deliver a reproducible report:

`reports/01_international_data_audit.md`

Minimum contents:

- Country-year row counts by syndrome, source system, and quality grade.
- Source total reconciliation against ECDC/PAHO/China CDC inputs.
- Population denominator join report.
- Climate, vegetation, and land-use covariate missingness.
- Missingness and duplicate report.
- Exact train/validation/test split proposal.
