# Project State

Last finalized: 2026-05-12

## Goal

Build a publication-ready hantavirus risk modeling project that can survive peer review by keeping claims matched to available data.

Primary publication path:

- international country-year reported human hantavirus incidence
- explicit syndrome strata: HFRS, HPS, HCPS, hantavirus infection, mixed/unspecified
- explicit source-system and region strata
- uncertainty-calibrated validation against strong statistical baselines

Secondary path:

- U.S./NEON rodent serology and trapping as mechanistic support or a fallback reservoir-risk manuscript

Blocked path:

- public U.S. county-level human prediction, unless restricted partner data are obtained

## Current Repo Status

Ready:

- source archive audit and blocker response
- international publication and marketing plan
- data requirements and source registry
- international country-case schema
- international case-source matrix
- international manual-data validator
- reproducible ECDC 2019-2023 country-year seed table builder
- World Bank population, rurality, and GDP context join
- processed international country-year CSV builder
- frozen first temporal split config
- historical, persistence, empirical negative-binomial, hierarchical shrinkage, and gradient-boosting baseline runner
- generated local audit and baseline reports
- shared forecast metrics tests
- future-agent handoff

Not ready yet:

- TerraClimate country-year feature ingestion
- MODIS MOD13C2 NDVI/EVI ingestion, which needs Earthdata credentials or exported inputs
- FAOSTAT land-use ingestion
- PAHO Americas and China CDC extension rows
- full Bayesian hierarchical model or dependency-approved negative-binomial GLM
- manuscript figures

## Main Documents

Read in this order:

1. `docs/AGENT_HANDOFF.md`
2. `docs/INTERNATIONAL_PUBLICATION_AND_MARKETING_PLAN.md`
3. `docs/DATA_REQUIREMENTS.md`
4. `docs/PUBLICATION_ROADMAP.md`
5. `docs/BLOCKER_RESPONSE_PLAN.md`
6. `configs/data_catalog.yaml`
7. `configs/modeling_plan.yaml`

## QA Commands

Run these from the repository root:

```powershell
python -m pip install -e ".[dev]"
python tools/create_ecdc_case_table.py --accessed-date 2026-05-12
python tools/validate_international_cases.py --strict
python tools/build_international_dataset.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/validate_manual_data.py
pytest
python -m ruff check src tests tools
```

Expected today:

- `pytest` passes.
- `ruff` passes for `src`, `tests`, and `tools`.
- `validate_international_cases.py --strict` passes after rebuilding the ECDC seed table.
- `validate_manual_data.py` still reports optional restricted county/state files missing.

## Next Exact Work Package

1. Add TerraClimate country-year climate features.
2. Add FAOSTAT land-use covariates.
3. Stop for `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` before MODIS MOD13C2 download unless the user provides an exported MOD13C2 country-year table.
4. Add PAHO Americas rows and China CDC rows only with complete source provenance.
5. Add calibration plots and manuscript-ready figures.
6. Upgrade empirical count baselines to a dependency-approved negative-binomial GLM or Bayesian hierarchical model.
7. Keep deep learning blocked until simple baselines and covariates are complete.

## Marketing Position

Use this framing:

> Open Hantavirus Risk Benchmark is an open, country-level research benchmark for reported hantavirus risk that is provenance-first, syndrome-aware, and uncertainty-calibrated.

Avoid this framing:

- outbreak oracle
- clinical tool
- individual risk predictor
- public county risk dashboard
- global model that ignores syndrome or surveillance differences
