# Project State

Last finalized: 2026-05-12

## Goal

Build a publication-ready hantavirus risk modeling project that can survive peer review by keeping claims matched to available data.

Primary publication path:

- international country-year reported human hantavirus incidence
- explicit syndrome strata: HFRS, HPS, HCPS, hantavirus infection, mixed/unspecified
- explicit source-system and region strata
- retrospective one-year-ahead evaluation against strong statistical baselines
- uncertainty, calibration, sharpness, and source-quality flags

Primary journal path:

- International Journal of Health Geographics first
- Scientific Data or BMC Public Health fallback
- PLOS NTD deferred unless a PAHO/LMIC source-system-specific expansion exists

Secondary path:

- U.S./NEON rodent serology and trapping as mechanistic support or a fallback reservoir-risk manuscript

Blocked path:

- public U.S. county-level human prediction, unless restricted partner data are obtained

## Current Repo Status

Ready:

- source archive audit and blocker response
- international publication and marketing plan
- publication-first differentiation plan against HantavirusMap-style live signal trackers
- exact paper implementation plan and blocker register
- data requirements and source registry
- international country-case schema
- international case-source matrix
- international manual-data validator
- reproducible ECDC 2019-2023 country-year seed table builder
- EU/EEA membership and surveillance-completeness metadata flags
- World Bank population, rurality, and GDP context join
- processed international country-year CSV builder
- FAOSTAT land-use download and country-year join
- TerraClimate source manifest, Natural Earth boundary download, and ECDC country-year aggregation
- MOD13C2 source/granule manifest
- Earthdata credential parser for local untracked credential files
- frozen first temporal split config
- historical, persistence, empirical negative-binomial, hierarchical shrinkage, and gradient-boosting baseline runner
- baseline metric outputs with WIS, relative WIS, empirical coverage, interval width, MAE, deviance, and Brier score
- first-pass baseline skill and observed-vs-predicted figure script
- Markov-style incidence-state simulation stress test
- final publication-readiness QA gate
- paper readiness and results report generator
- audited root publication plan
- data dictionary, reproducibility manifest, and reviewer response playbook
- generated local audit and baseline reports
- shared forecast metrics tests
- future-agent handoff

Not ready yet:

- MODIS MOD13C2 quality-masked country-year HDF aggregation
- PAHO Americas and China CDC extension rows
- full Bayesian hierarchical model or dependency-approved negative-binomial GLM
- manuscript text and final journal-specific figure set

## Main Documents

Read in this order:

1. `PUBLICATION_MASTER_PLAN.md`
2. `docs/AGENT_HANDOFF.md`
3. `docs/data_dictionary.md`
4. `docs/reproducibility_manifest.md`
5. `docs/reviewer_response_playbook.md`
6. `docs/PAPER_IMPLEMENTATION_PLAN_AND_BLOCKERS.md`
7. `docs/PUBLICATION_FIRST_DIFFERENTIATION_PLAN.md`
8. `docs/INTERNATIONAL_PUBLICATION_AND_MARKETING_PLAN.md`
9. `docs/DATA_REQUIREMENTS.md`
10. `docs/PUBLICATION_ROADMAP.md`
11. `docs/BLOCKER_RESPONSE_PLAN.md`
12. `configs/data_catalog.yaml`
13. `configs/modeling_plan.yaml`

## QA Commands

Run these from the repository root:

```powershell
python -m pip install -e ".[dev,geo]"
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
python tools/check_publication_readiness.py
python tools/validate_manual_data.py
pytest
python -m ruff check src tests tools
```

Expected today:

- `pytest` passes.
- `ruff` passes for `src`, `tests`, and `tools`.
- `validate_international_cases.py --strict` passes after rebuilding the ECDC seed table.
- `validate_manual_data.py` still reports optional restricted county/state files missing.
- `check_publication_readiness.py` passes for the ECDC-only public-data benchmark path.

## Next Exact Work Package

1. Keep the main manuscript as an ECDC-only public-data benchmark unless PAHO/China extraction is completed with full provenance.
2. Decide whether MODIS quality-masked NDVI/EVI aggregation is worth implementing; otherwise remove vegetation claims from the paper.
3. Add feature ablation tables that compare context only, land use, TerraClimate, and all public covariates.
4. Add MASE, calibration plots, interval-width plots, and IJHG-ready choropleths/data-gap maps.
5. Upgrade empirical count baselines to a penalized or hierarchical count model only after feature ablation.
6. Draft manuscript methods/results from the generated reports and figures.
7. Keep deep learning blocked until simple baselines and covariates are complete.

## Marketing Position

Use this framing:

> Open Hantavirus Risk Benchmark is an open, country-level research benchmark for reported hantavirus risk that is provenance-first, syndrome-aware, and uncertainty-calibrated.

For the manuscript title, prefer:

> An open benchmark for country-level reported hantavirus incidence: retrospective one-year-ahead evaluation under sparse public surveillance

Avoid this framing:

- outbreak oracle
- clinical tool
- individual risk predictor
- prospective forecast unless true prospective labels are withheld
- public county risk dashboard
- global model that ignores syndrome or surveillance differences
