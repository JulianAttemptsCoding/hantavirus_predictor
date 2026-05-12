# Hantavirus Predictor

Research-grade setup for an international hantavirus surveillance, reservoir, and
spillover-risk forecasting project.

This repository is not an operational public-health predictor yet. It is a rigor-first handoff for future agents to build one without inheriting unsupported claims from the LLM-generated archive packages in `source_material/`.

## Current Decision

The live project should target:

1. An international country-year reported-incidence paper as the primary publication path.
2. Explicit syndrome and surveillance strata: HFRS, HPS/HCPS, region, and source system.
3. U.S./NEON rodent serology as mechanistic support and a fallback reservoir-risk paper.
4. County-level U.S. human prediction only after a state health department, CDC, or IRB-approved partner provides data.

The supplied ZIP packages are preserved and audited, but their code is not copied into production because their tests either fail or depend on uninstalled heavy packages, and their reports overclaim readiness.

## Quick Start

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -e ".[dev]"
python tools/summarize_neon_products.py
python tools/validate_international_cases.py
pytest
```

## Repository Map

- `docs/SOURCE_ARCHIVE_AUDIT.md` - what is inside the three ZIP packages and what is reusable.
- `docs/RESEARCH_CLAIMS_AUDIT.md` - checked claims, citations, and project decisions.
- `docs/PROJECT_STATE.md` - current checkpoint, QA status, and next work package.
- `docs/DATA_REQUIREMENTS.md` - exact data inventory and what must be provided manually.
- `docs/PUBLICATION_ROADMAP.md` - spec-by-spec plan from this repo to journal submission.
- `docs/INTERNATIONAL_PUBLICATION_AND_MARKETING_PLAN.md` - international pivot, QA,
  implementation specs, and audience positioning.
- `docs/BLOCKER_RESPONSE_PLAN.md` - response to the blockers in the root text files.
- `docs/AGENT_HANDOFF.md` - next-agent instructions.
- `src/hantavirus_predictor/` - small, tested utilities for shared metadata and metrics.
- `tools/` - setup and validation scripts.
- `source_material/llm_archives/extracted/` - extracted LLM packages for reference only.

## Non-Negotiable Scientific Guardrails

- Do not claim county-level human case prediction from public CDC data; CDC's current hantavirus page says public case data are state-level only for privacy.
- Do not pool HFRS and HPS/HCPS as one disease process without explicit syndrome, region, and source-system strata.
- Do not claim the model predicts human infections unless validated against human case data at the matching spatial and temporal resolution.
- Do not train primarily on synthetic trajectories unless the manuscript frames them as priors or regularizers, not evidence.
- Do not advance a PINN, graph neural network, or time-series foundation model unless it beats SARIMAX, GAM/GLMM, and gradient-boosted baselines under strict temporal and spatial validation.

## Current Data State

The publication track is ready for data extraction, but the primary manual table
is intentionally not filled yet:

- `data/manual/international_country_cases.csv` is ignored by git until sourced data are extracted.
- `python tools/validate_international_cases.py` is allowed to report it missing during setup.
- `python tools/validate_international_cases.py --strict` should pass only after the country-year source table is created.

## GitHub

Remote:

```powershell
origin https://github.com/JulianAttemptsCoding/hantavirus_predictor.git
```
