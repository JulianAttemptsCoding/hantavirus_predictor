# EU/EEA Hantavirus Surveillance Benchmark

Research-grade setup for an EU/EEA hantavirus reported-incidence surveillance
benchmark and EID submission package.

This repository is not an operational public-health predictor. It is a
rigor-first handoff for future agents to build a publishable paper without
inheriting unsupported claims from the LLM-generated archive packages in
`source_material/`.

## Current Decision

The live project should target:

1. An ECDC/EU-EEA country-year reported-incidence benchmark as the primary publication path.
2. Retrospective one-year-ahead evaluation, not true prospective forecasting.
3. Emerging Infectious Diseases (EID, CDC) as the first journal target, with Scientific Data or BMC Public Health as fallbacks.
4. Explicit syndrome and surveillance strata before any non-ECDC expansion.
5. U.S./NEON rodent serology as mechanistic support and a fallback reservoir-risk paper.
6. County-level U.S. human prediction only after a state health department, CDC, or IRB-approved partner provides data.

The supplied ZIP packages are preserved and audited, but their code is not copied into production because their tests either fail or depend on uninstalled heavy packages, and their reports overclaim readiness.

## Quick Start

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
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
pytest
```

## Repository Map

- `PUBLICATION_MASTER_PLAN.md` - authoritative audited plan from repo state to publication.
- `docs/SOURCE_ARCHIVE_AUDIT.md` - what is inside the three ZIP packages and what is reusable.
- `docs/RESEARCH_CLAIMS_AUDIT.md` - checked claims, citations, and project decisions.
- `docs/PROJECT_STATE.md` - current checkpoint, QA status, and next work package.
- `docs/data_dictionary.md` - publication-track data dictionary.
- `docs/reproducibility_manifest.md` - rebuild, attribution, and archive manifest.
- `docs/reviewer_response_playbook.md` - reviewer defense notes.
- `docs/DATA_REQUIREMENTS.md` - exact data inventory and what must be provided manually.
- `docs/PUBLICATION_ROADMAP.md` - spec-by-spec plan from this repo to journal submission.
- `docs/PUBLICATION_FIRST_DIFFERENTIATION_PLAN.md` - how to publish something distinct from HantavirusMap.
- `docs/PAPER_IMPLEMENTATION_PLAN_AND_BLOCKERS.md` - exact implementation plan and blocker responses.
- `docs/INTERNATIONAL_PUBLICATION_AND_MARKETING_PLAN.md` - international pivot, QA,
  implementation specs, and audience positioning.
- `docs/BLOCKER_RESPONSE_PLAN.md` - response to the blockers in the root text files.
- `docs/AGENT_HANDOFF.md` - next-agent instructions.
- `src/hantavirus_predictor/` - tested utilities for source metadata, ingestion, features,
  metrics, and first-pass baselines.
- `tools/` - setup, validation, data-build, audit, and benchmark scripts.
- `source_material/llm_archives/extracted/` - extracted LLM packages for reference only.

## Non-Negotiable Scientific Guardrails

- Do not claim county-level human case prediction from public CDC data; CDC's current hantavirus page says public case data are state-level only for privacy.
- Do not pool HFRS and HPS/HCPS as one disease process without explicit syndrome, region, and source-system strata.
- Do not claim the model predicts human infections unless validated against human case data at the matching spatial and temporal resolution.
- Do not train primarily on synthetic trajectories unless the manuscript frames them as priors or regularizers, not evidence.
- Do not advance a PINN, graph neural network, or time-series foundation model unless it beats SARIMAX, GAM/GLMM, and gradient-boosted baselines under strict temporal and spatial validation.

## Current Data State

The first ECDC seed milestone is reproducible:

- `tools/create_ecdc_case_table.py` creates the ignored manual ECDC country-year table.
- The ECDC table carries EU/EEA status and surveillance-completeness flags, including
  Belgium 2023 and Cyprus 2023 caveats.
- `tools/build_international_dataset.py` joins World Bank population, rurality, and GDP context.
- `tools/download_faostat_land_use.py` adds FAOSTAT land-use features to the processed table.
- `tools/create_terraclimate_manifest.py`, `tools/download_natural_earth_countries.py`, and
  `tools/aggregate_terraclimate_country_year.py` add country-year TerraClimate climate and
  water-balance covariates.
- `tools/create_mod13c2_manifest.py` creates the MODIS source manifest; quality-masked
  vegetation aggregation is optional future work until it is implemented and audited.
- `tools/write_international_data_audit.py` writes `reports/01_international_data_audit.md`.
- `tools/run_international_baselines.py` writes quantile forecasts, WIS, relative WIS,
  empirical coverage, interval width, MAE, deviance, Brier metrics, and
  `reports/02_international_baselines.md`.

Generated `data/` and `reports/` outputs are ignored by git; tracked scripts rebuild them.

## GitHub

Remote:

```powershell
origin https://github.com/JulianAttemptsCoding/hantavirus_predictor.git
```
