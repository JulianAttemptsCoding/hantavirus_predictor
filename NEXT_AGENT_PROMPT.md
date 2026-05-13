# Next Agent Prompt

Last updated: 2026-05-12

Use this prompt for the next agent. It is intentionally exact because this
repo is headed toward a journal paper, not a demo.

## Human Inputs Needed

### Needed Now

None for the ECDC-only publication path. Continue without stopping for human
input.

The current local Earthdata credential file was already present and parsed
successfully without printing secrets. Generated data and reports can be
rebuilt from tracked scripts.

### Stop Immediately If Any Of These Become Necessary

Stop and ask the user only if the next task truly cannot continue without the
input.

1. NASA Earthdata credentials fail and MODIS is required.

   Exact user action:

   - Go to https://urs.earthdata.nasa.gov/
   - Confirm the NASA Earthdata account can sign in.
   - At repo root, create or update `nasa earthdata acc info.txt`.
   - Use exactly this format:

     ```text
     username: YOUR_EARTHDATA_USERNAME
     password: YOUR_EARTHDATA_PASSWORD
     ```

   - Do not commit this file.
   - Tell the agent to rerun:

     ```powershell
     python tools/check_earthdata_credentials.py
     ```

2. A true U.S. county-level or subnational human-risk paper is requested.

   Exact user action:

   - Provide a legally shareable restricted partner dataset from CDC, a state
     health department, or an IRB-approved collaborator.
   - Put it under `data/manual/` only if redistribution is allowed locally.
   - Include the data dictionary, case definition, geography, dates, privacy
     restrictions, and permission statement.
   - Until this happens, do not make county-level human claims.

3. Journal submission is ready.

   Exact user action:

   - Pick the target journal: IJHG first, Scientific Data fallback, or BMC
     Public Health fallback.
   - Confirm APC/payment route.
   - Provide author list, affiliations, ORCID IDs if available, corresponding
     author, funding statement, competing interests, acknowledgements, and
     CRediT contribution roles.
   - Confirm whether to post a preprint.
   - Confirm the institutional ethics wording for aggregate public data.

4. DOI deposition is ready.

   Exact user action:

   - Provide the Zenodo/OSF/Figshare destination or confirm GitHub-Zenodo
     integration is enabled.
   - Confirm what name/account should own the DOI.
   - Confirm license for the release package.

### Not Needed For Version 1

- Do not ask the user for PAHO/China data for the ECDC-only paper. Those are
  public-source expansions and are deferred.
- Do not ask the user for CDC county data unless the user changes the paper
  scope to a U.S. subnational human-risk paper.
- Do not ask the user for a new model idea before finishing the benchmark,
  ablation, maps, manuscript, and QA gates below.

## Full Prompt For The Next Agent

You are continuing the `hantavirus_predictor` repository toward a publishable
paper. The current goal is not a live app. The goal is a journal-ready paper
package for an ECDC/EU-EEA country-year public-data benchmark.

Start in:

```powershell
C:\Users\bubga.JULIAN-LAPTOPE2\OneDrive\Desktop\coding\hantavirus_predictor
```

First, read these files in order:

1. `PUBLICATION_MASTER_PLAN.md`
2. `NEXT_AGENT_PROMPT.md`
3. `docs/AGENT_HANDOFF.md`
4. `docs/PROJECT_STATE.md`
5. `docs/data_dictionary.md`
6. `docs/reproducibility_manifest.md`
7. `docs/reviewer_response_playbook.md`

Important current git context:

- The publication-plan baseline before this prompt was commit `7902a63`;
  check `git log -1 --oneline` for the latest handoff commit.
- Pre-existing user-side working-tree dirt may include deleted zip/text files
  and an untracked new zip. Do not stage, revert, delete, or commit those
  unless the user explicitly asks.
- Generated `data/`, `reports/`, and `figures/` outputs are ignored by git.
  Rebuild them locally.

Core scientific rules:

- Version 1 is ECDC/EU-EEA, 2019-2023, country-year reported incidence.
- Call the task retrospective one-year-ahead evaluation, not prospective
  forecasting.
- Target International Journal of Health Geographics first.
- Use Scientific Data or BMC Public Health as fallbacks.
- Do not target PLOS NTD for the ECDC-only paper.
- Do not claim global generalization.
- Do not claim county-level U.S. human prediction.
- Do not claim causal climate effects.
- Do not claim vegetation/NDVI/EVI effects unless MODIS QA aggregation passes.
- Do not pool ECDC, PAHO, and China CDC without source-system and syndrome
  strata.
- Keep negative results. If simple baselines beat complex models, that is a
  publishable finding when documented rigorously.

## Required Work Plan

### Phase 1: Rebuild And Verify Current Baseline

Run:

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
python tools/run_markov_simulation.py
python tools/write_paper_readiness_report.py
python tools/check_publication_readiness.py
```

Required results:

- ECDC totals exactly equal 4088, 1693, 4947, 2185, 1885.
- Case table has 142 rows.
- Processed table has 142 rows.
- Belgium 2023 is flagged `not_comprehensive`.
- Cyprus 2023 is flagged `unspecified`.
- TerraClimate lag-1 missingness is reported per variable.
- Publication readiness gate passes for ECDC-only manuscript path.

### Phase 2: Implement Feature Ablation

Build a tracked tool, likely:

- `tools/run_feature_ablation.py`

Add tested source code under `src/hantavirus_predictor/` as needed.

Required feature sets:

- `surveillance_only`
- `context`
- `land_use`
- `climate`
- `all_public`
- `modis_optional` only if MODIS passes its gate

Requirements:

- Feature sets are nested.
- Train 2019-2021, validate 2022, test 2023.
- Add leave-one-year-out sensitivity.
- Use train-only median/mode imputation.
- Save/report final modeling feature count separately from raw processed
  table columns.
- Drop constant/duplicate features.
- Screen correlated features using VIF or pairwise correlation.
- Keep final model features normally between 15 and 25 before one-hot encoding.

Metrics required:

- WIS.
- Relative WIS.
- 90 percent empirical coverage.
- Mean 90 percent interval width.
- MAE.
- Brier any-case.
- MASE where denominator is valid.
- Calibration table/plot.

Required reports:

- `reports/03_feature_ablation.md`
- Figures for WIS/relative WIS, coverage, and interval width.

### Phase 3: Decide MODIS

Use the gate in `PUBLICATION_MASTER_PLAN.md`.

Include MODIS only if all are true:

- MOD13C2 Version 6.1 QA-masked aggregation is implemented.
- Valid-pixel coverage is at least 95 percent for at least 90 percent of
  country-years.
- MODIS improves WIS or relative WIS by at least 5 percent against
  `all_public`.
- MODIS does not materially worsen 90 percent coverage.
- The pipeline is reproducible from documented inputs.

If this fails:

- Remove vegetation claims from manuscript.
- Keep MODIS as future work.
- Use TerraClimate water-balance variables only as climate/water-balance
  context, not vegetation.

### Phase 4: Add Maps For IJHG

Implement IJHG-ready geospatial figures:

- EU/EEA incidence choropleth.
- Surveillance completeness/data-gap map.
- Predicted versus observed incidence map for the best model.
- Uncertainty map or hatching layer for interval width.

Requirements:

- Use Natural Earth.
- Document projection.
- Avoid false within-country precision.
- Use colorblind-safe palettes.
- Save publication-quality static figures.

### Phase 5: Count Model Upgrade

Only after ablation is working:

- Add penalized Poisson or negative-binomial GLM with population offset.
- Avoid unregularized country fixed effects.
- Use validation 2022 or leave-one-year-out CV for hyperparameters.
- Do not interpret coefficients causally.
- If unstable, report instability and keep empirical baselines as the main
  result.

### Phase 6: Sensitivity And Power

Required:

- Sensitivity excluding Belgium 2023 and other non-comprehensive rows.
- Sensitivity with pandemic-period indicator for 2020-2021.
- Sensitivity excluding 2020-2021 where sample size permits.
- Simulation-based power/detectability analysis for covariate effects.

### Phase 7: Manuscript Package

Create tracked manuscript docs under `manuscript/` or `docs/manuscript/`:

- Main manuscript draft.
- Figure captions.
- Table shells.
- Cover letter for IJHG.
- Data availability statement.
- Code availability statement.
- Ethics statement.
- CRediT contribution template.
- Reviewer response draft.

Required manuscript framing:

- Exact time span: 2019-2023.
- Exact row count after final freeze.
- ECDC-only primary scope.
- Novelty against HantavirusMap and Zeimes et al.
- Negative-result framing if complex models fail.
- No overclaims.

### Phase 8: Archive Package

Prepare but do not fake DOI deposition:

- `CITATION.cff` updated if needed.
- `LICENSE` present.
- Data dictionary complete.
- Reproducibility manifest complete.
- Checksums for final processed outputs.
- Zenodo/OSF deposition instructions.

Stop for user input before final DOI deposition if account ownership or
license choice is unclear.

## Final QA Gates

Do not declare the project done until every applicable gate passes.

### Data QA

```powershell
python tools/create_ecdc_case_table.py --accessed-date 2026-05-12
python tools/validate_international_cases.py --strict
python tools/build_international_dataset.py
python tools/write_international_data_audit.py
python tools/check_publication_readiness.py
```

Must pass:

- ECDC totals reconcile exactly.
- No duplicate primary keys.
- No missing required source URLs/access dates.
- Surveillance flags are present.
- Raw table dimensions and model feature dimensions are separately reported.

### Modeling QA

Must pass:

- Baselines regenerate.
- Feature ablation regenerates.
- Metrics include WIS, relative WIS, coverage, interval width, MAE, Brier,
  and MASE where valid.
- No target-year leakage.
- Imputation is train-only.
- Complex models are not promoted unless they beat simple baselines without
  unacceptable calibration loss.

### Figure QA

Must pass:

- Required IJHG maps exist.
- Figure scripts are tracked.
- Projection documented.
- Color palettes are colorblind-safe.
- Captions avoid false precision.

### Manuscript QA

Must pass:

- Title uses retrospective one-year-ahead language.
- Abstract states 2019-2023 and final row count.
- Related work includes Zeimes et al., Kallio et al., Reusken/Heyman,
  Kazasidis/Geduhn/Jacob, Glass et al., Allen et al., and forecast-benchmark
  literature.
- Limitations explicitly mention sparse years, country-level aggregation,
  reporting heterogeneity, Belgium 2023, COVID-era sensitivity, and
  non-prospective validation.
- Ethics/data/code/author contribution statements are present.

### Repo QA

```powershell
python -m pytest
python -m ruff check src tests tools
git diff --check
rg -n "password\s*=|token\s*=|secret\s*=|api_key|BEGIN [A-Z ]*PRIVATE KEY" .
```

Must pass:

- Tests pass.
- Ruff passes.
- No whitespace errors.
- No secrets committed. Expected regex false positives in code/tests/archive
  must be reviewed, not blindly accepted.
- `nasa earthdata acc info.txt` remains ignored.

### Git QA

Must pass:

- Commit only intended tracked changes.
- Do not commit generated data/reports/figures unless the publication plan
  deliberately changes this.
- Do not commit user-side zip deletions or the untracked new zip without
  explicit user instruction.
- Push to `origin main` after a clean commit.

## Done Definition

The project is "done" for this stage only when:

- Feature ablation, maps, sensitivity analysis, and manuscript package exist.
- All QA gates above pass.
- The root plan and handoff docs are current.
- The final answer reports exact outputs, metrics, tests, commit hash, and any
  remaining human-only publication tasks.
