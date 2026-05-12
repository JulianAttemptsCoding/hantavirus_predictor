# Agent Handoff

Start here after opening the repo.

## First Commands

```powershell
git status --short --branch
python -m pip install -e ".[dev]"
python tools/summarize_neon_products.py
python tools/validate_manual_data.py
pytest
```

## Read Order

1. `instructions.txt`
2. `docs/SOURCE_ARCHIVE_AUDIT.md`
3. `docs/RESEARCH_CLAIMS_AUDIT.md`
4. `docs/DATA_REQUIREMENTS.md`
5. `docs/PUBLICATION_ROADMAP.md`
6. `docs/BLOCKER_RESPONSE_PLAN.md`
7. `configs/data_catalog.yaml`
8. `configs/modeling_plan.yaml`

## Rules For Future Agents

- Do not trust the extracted ZIP package QA reports as real validation.
- Do not copy archive code into `src/` unless tests are ported and passing.
- Do not make human county-level claims without a documented restricted data source.
- Do not skip simple baselines.
- Do not hide negative results. For this project, a rigorous "complex models do not help with public data" paper may still be publishable.
- Keep raw data out of git. Commit schemas, manifests, checksums, and scripts.

## Immediate Next Tasks

1. Use NEON API to download `DP1.10064.001` and matching `DP1.10072.001` tables.
2. Build a site-month fact table with serology counts, trap effort, species counts, and sampling flags.
3. Add Daymet point extraction for NEON sites.
4. Add MODIS/VIIRS AppEEARS request templates for site buffers and quality flags.
5. Implement historical, SARIMAX, GLMM/GAM, and gradient-boosting baselines.
6. Add WIS, CRPS or sample-CRPS, coverage, Brier/PR-AUC for outbreak thresholds, and calibration plots.
7. Write a preregistered validation split file before tuning models.
8. Decide whether restricted human data are available. If not, keep human cases descriptive/state-level.
9. Only then evaluate PINN, TimesFM, or graph models.
10. Start manuscript after results pass the gates in `configs/modeling_plan.yaml`.

## Expected First Milestone

Deliver a reproducible report:

`reports/01_data_audit.md`

Minimum contents:

- NEON row counts by source table.
- Serology positive/negative/indeterminate counts by site, year, species.
- Trap effort denominators by site-month.
- Missingness and duplicate report.
- Exact train/validation/test split proposal.

