# EU/EEA Hantavirus Surveillance Benchmark

Reproducible EU/EEA country-year benchmark for reported hantavirus incidence
and EID-oriented evaluation of public-surveillance forecasting limits.

This repository is not an operational public-health predictor, a live risk
dashboard, a clinical tool, or a within-country risk map. The active target is
an *Emerging Infectious Diseases* Research article about what sparse annual
public surveillance can and cannot support.

## Current Decision

Active target:

1. Journal: *Emerging Infectious Diseases*.
2. Article type: Research.
3. Scope: EU/EEA country-year reported hantavirus incidence, 2019-2023.
4. Evaluation: retrospective one-year-ahead probabilistic benchmark.
5. Data: public surveillance and public covariates only.
6. Claim: public covariates did not provide stable, calibrated improvement over
   surveillance-history baselines; surveillance standardization and uncertainty
   reporting are the practical bottlenecks.

Archived legacy ZIPs, old Overleaf output, pre-EID drafts, and extracted LLM
packages were moved off the active branch. The preserved snapshot is on:

```text
codex/archive-pre-eid-cleanup-20260514
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,geo]"
python tools/create_ecdc_case_table.py --accessed-date 2026-05-14
python tools/validate_international_cases.py --strict
python tools/download_faostat_land_use.py
python tools/create_terraclimate_manifest.py
python tools/download_natural_earth_countries.py
python tools/aggregate_terraclimate_country_year.py
python tools/build_international_dataset.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/run_feature_ablation.py
python tools/run_count_models.py
python tools/run_sensitivity_power.py
python tools/create_eid_figures.py
python tools/build_eid_docx.py
python -m pytest
python -m ruff check src tests tools
```

Generated `data/`, `reports/`, and root-level figure outputs are ignored by git.
Tracked scripts rebuild them.

## Repository Map

- `PUBLICATION_MASTER_PLAN.md` - active EID acceptance plan and QA gates.
- `docs/submission_eid/` - current manuscript, cover letter, author statements,
  figures, supplement, and submission guide.
- `docs/PROJECT_STATE.md` - concise current state and next work package.
- `docs/AGENT_HANDOFF.md` - future-agent start instructions.
- `docs/data_dictionary.md` - EID benchmark data dictionary.
- `docs/reproducibility_manifest.md` - rebuild and archive requirements.
- `docs/reviewer_response_playbook.md` - reviewer-risk response notes.
- `configs/validation_splits.yaml` - frozen temporal split.
- `configs/data_catalog.yaml` - active EID public data sources.
- `configs/modeling_plan.yaml` - active EID model promotion gates.
- `src/hantavirus_predictor/` - tested package code.
- `tools/` - data build, validation, modeling, reporting, and EID artifact scripts.
- `tests/` - regression and QA tests.

## Scientific Guardrails

- Model reported cases/incidence, not true infections.
- Do not call the evaluation prospective.
- Do not claim operational prediction, individual risk, county-level human risk,
  or within-country risk.
- Do not make causal climate or land-use claims.
- Do not promote a model on WIS alone; coverage and interval width are required.
- Keep MODIS/vegetation claims out unless quality-masked aggregation passes a
  documented inclusion gate.
- Keep Andes-virus and cruise-ship context separate from the EU/EEA HFRS
  country-year benchmark.

## Current Data State

The reproducible ECDC seed milestone contains 142 EU/EEA country-year rows.
Annual totals reconcile to ECDC for 2019-2023:

| Year | Reported cases |
| --- | ---: |
| 2019 | 4,088 |
| 2020 | 1,693 |
| 2021 | 4,947 |
| 2022 | 2,185 |
| 2023 | 1,885 |

Belgium 2023 and Cyprus 2023 carry surveillance-quality caveats and must be
tested in sensitivity analyses.

## GitHub

```powershell
origin https://github.com/JulianAttemptsCoding/hantavirus_predictor.git
```
