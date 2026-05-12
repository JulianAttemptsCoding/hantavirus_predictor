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
- shared forecast metrics tests
- future-agent handoff

Not ready yet:

- `data/manual/international_country_cases.csv`
- extracted ECDC country-year case table
- World Bank/TerraClimate/MODIS/FAOSTAT ingestion code
- international baseline models
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
python tools/validate_international_cases.py
python tools/validate_manual_data.py
pytest
python -m ruff check src tests tools
```

Expected today:

- `pytest` passes.
- `ruff` passes for `src`, `tests`, and `tools`.
- non-strict `validate_international_cases.py` may report the manual country-case table missing.
- strict `validate_international_cases.py --strict` should fail until real source rows are extracted.

## Next Exact Work Package

1. Create `data/manual/international_country_cases.csv` from ECDC country-year rows.
2. Run `python tools/validate_international_cases.py --strict`.
3. Reconcile extracted totals to the ECDC annual report.
4. Write `reports/01_international_data_audit.md`.
5. Add World Bank population and rurality ingestion.
6. Add TerraClimate country-year climate features.
7. Add MODIS MOD13C2 NDVI/EVI features.
8. Add FAOSTAT land-use covariates.
9. Implement international baselines before any deep learning.

## Marketing Position

Use this framing:

> Open Hantavirus Risk Benchmark is an open, country-level research benchmark for reported hantavirus risk that is provenance-first, syndrome-aware, and uncertainty-calibrated.

Avoid this framing:

- outbreak oracle
- clinical tool
- individual risk predictor
- public county risk dashboard
- global model that ignores syndrome or surveillance differences
