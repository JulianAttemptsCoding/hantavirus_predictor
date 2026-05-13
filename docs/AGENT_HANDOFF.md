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
python tools/run_feature_ablation.py
python tools/run_count_models.py
python tools/create_ijhg_maps.py
python tools/run_sensitivity_power.py
python tools/run_markov_simulation.py
python tools/write_paper_readiness_report.py
python tools/check_publication_readiness.py
python tools/validate_manual_data.py
pytest
python -m ruff check src tests tools
```

## Read Order

1. `PUBLICATION_MASTER_PLAN.md`
2. `NEXT_AGENT_PROMPT.md`
3. `docs/PROJECT_STATE.md`
4. `docs/data_dictionary.md`
5. `docs/reproducibility_manifest.md`
6. `docs/reviewer_response_playbook.md`
7. `docs/SOURCE_ARCHIVE_AUDIT.md`
8. `docs/RESEARCH_CLAIMS_AUDIT.md`
9. `docs/PAPER_IMPLEMENTATION_PLAN_AND_BLOCKERS.md`
10. `docs/PUBLICATION_FIRST_DIFFERENTIATION_PLAN.md`
11. `docs/INTERNATIONAL_PUBLICATION_AND_MARKETING_PLAN.md`
12. `docs/DATA_REQUIREMENTS.md`
13. `docs/PUBLICATION_ROADMAP.md`
14. `docs/BLOCKER_RESPONSE_PLAN.md`
15. `configs/data_catalog.yaml`
16. `configs/modeling_plan.yaml`

## Rules For Future Agents

- Do not trust the extracted ZIP package QA reports as real validation.
- Do not copy archive code into `src/` unless tests are ported and passing.
- Do not make human county-level claims without a documented restricted data source.
- Treat international country-year modeling as the primary publication track.
- Do not pool HFRS and HPS/HCPS without explicit syndrome and source-system strata.
- Do not skip simple baselines.
- Do not call the current ECDC-only work prospective forecasting; it is retrospective one-year-ahead evaluation.
- Do not target PLOS NTD for the ECDC-only paper. Use IJHG first, then Scientific Data or BMC Public Health.
- Do not describe the raw processed table column count as the modeling feature count.
- Do not hide negative results. For this project, a rigorous "complex models do not help with public data" paper may still be publishable.
- Keep raw data out of git. Commit schemas, manifests, checksums, and scripts.
- Use `NEXT_AGENT_PROMPT.md` as the exact active work order and QA gate list.

## Immediate Next Tasks

1. Review regenerated feature ablation, IJHG map, sensitivity, and detectability outputs.
2. Keep the penalized Poisson GLM exploratory unless it beats simple baselines without unacceptable coverage loss.
3. Keep MODIS out of manuscript claims unless quality-masked aggregation passes the hard gate in `PUBLICATION_MASTER_PLAN.md`.
4. Keep PAHO and China CDC deferred unless a source-system-stratified expansion is explicitly requested.
5. Expand the tracked manuscript draft after authorship, funding, ethics wording, and target-journal details are confirmed.
6. Only then evaluate PINN, TimesFM, graph models, or other complex methods.

## Expected First Milestone

Delivered locally by tracked scripts:

`reports/01_international_data_audit.md`
`reports/02_international_baselines.md`
`reports/03_feature_ablation.md`
`reports/05_publication_readiness_gate.md`
`reports/06_ijhg_maps.md`
`reports/07_sensitivity_power.md`

Minimum contents:

- Country-year row counts by syndrome, source system, and quality grade.
- Source total reconciliation against ECDC/PAHO/China CDC inputs.
- Population denominator join report.
- Climate and land-use covariate missingness; vegetation only if MODIS is implemented.
- Missingness and duplicate report.
- Exact train/validation/test split proposal.

Generated `data/` and `reports/` files are ignored by git. Rebuild them with the first-command block.

Credential note: `nasa earthdata acc info.txt` is ignored by git. Use `python tools/check_earthdata_credentials.py` to confirm it parses without printing secrets.
