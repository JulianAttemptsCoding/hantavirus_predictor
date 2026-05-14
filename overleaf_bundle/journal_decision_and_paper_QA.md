# Journal Decision And Paper QA Gates

## Recommended Submission Strategy

Primary target: **Eurosurveillance**.

Rationale:

- It is published by ECDC and is explicitly focused on infectious disease surveillance, epidemiology, prevention, and control in Europe.
- DOAJ lists no article processing charges for the journal and describes double anonymous peer review.
- ECDC states the journal is free of charge for both readers and authors and that articles undergo peer review by independent reviewers.
- Eurosurveillance's review-process page says authors' and reviewers' identities are kept confidential.
- The manuscript uses ECDC surveillance data and is framed as surveillance evaluation, not machine learning spectacle.

Timeline caveat:

- DOAJ lists an average of 30 weeks from submission to publication for Eurosurveillance. This is longer than a strict four-month target if "four months" means submission-to-publication.
- If speed becomes more important than fit/prestige, use **Emerging Infectious Diseases** as the fallback. EID has no author fees and its Research article category is 3,500 words with a 150-word abstract; it asks authors to explain findings in public health terms.
- If both high-prestige free targets fail, **Zoonoses** is a respectable safety fallback: it is platinum open access, peer reviewed, indexed in Scopus and DOAJ, and its scope includes zoonotic disease epidemiology and public health. It is less prestigious than Eurosurveillance/EID.

## Verified Source Anchors

- Eurosurveillance DOAJ page: no APC, double anonymous peer review, average 30 weeks submission-to-publication.
- Eurosurveillance review process: screening, at least two independent reviewers for regular articles, author- and reviewer-anonymised peer review.
- ECDC procurement page: Eurosurveillance is devoted to epidemiology, surveillance, prevention and control of communicable diseases relevant to Europe; free for readers and authors; independent peer review.
- EID author pages: Research articles are 3,500 words, 150-word abstract, and should report epidemiologic results in a public health perspective; no author fees.
- Zoonoses scope page: platinum open-access, peer-reviewed, zoonotic disease epidemiology/public-health scope; indexed in Scopus and DOAJ.
- WHO hantavirus fact sheet: rodents are the usual source; Andes virus is the currently known hantavirus with documented limited human-to-human transmission; European/Asian hantaviruses cause HFRS and human-to-human transmission has not been documented in that region.
- ECDC 2023 report: 1,885 EU/EEA cases in 2023, 0.4 per 100,000; Finland and Germany accounted for 60.5%.
- CDC reported cases page: 890 US cases from 1993 through 2023; county-level data cannot be provided for privacy.

## Anti-Hype Communication Gates

The paper must:

- Say "reported incidence", not true infection burden.
- Say "retrospective one-year-ahead evaluation", not prospective forecast.
- Say "country-year benchmark", not local risk map.
- State that hantavirus can be severe while also being uncommon at the public surveillance scale used here.
- Distinguish Andes virus human-to-human transmission from the EU/EEA ECDC target.
- Avoid "COVID-like", "pandemic", "outbreak predictor", "early warning system", and "live risk" language unless discussing unrelated literature.
- State that maps are country-level and do not imply within-country precision.
- State that no clinical, individual, county-level, or operational public health decisions should be made from this benchmark.

The paper must not:

- Claim global generalization.
- Claim county-level U.S. prediction.
- Claim causal climate, land-use, or vegetation effects.
- Claim NDVI/EVI/vegetation results because MODIS QA aggregation did not pass.
- Pool ECDC with PAHO or China CDC labels.
- Hide under-coverage or negative results.

## Data QA Gates

- ECDC annual totals must equal 4,088; 1,693; 4,947; 2,185; 1,885 for 2019--2023.
- Case table must have 142 rows.
- Processed table must have 142 rows.
- Belgium 2023 must be flagged `not_comprehensive`.
- Cyprus 2023 must be flagged `unspecified`.
- No duplicate primary keys.
- No missing required source URLs or access dates.
- TerraClimate lag-1 missingness must be reported per variable.
- Raw table column count must be reported separately from final modelling features.

## Modelling QA Gates

- Baselines must regenerate.
- Feature ablation must regenerate.
- Metrics must include WIS, relative WIS, coverage, interval width, MAE, Brier score, and MASE where valid.
- Imputation must be train-only.
- Target-year leakage must be avoided.
- Complex models cannot be promoted unless they beat simple baselines without unacceptable coverage loss.
- The penalized Poisson model remains exploratory because it has worse WIS than the best simple 2023 baseline and only 0.321 empirical 90% coverage.

## Figure QA Gates

- Natural Earth boundaries must be used.
- Projection must be documented as ETRS89 / LAEA Europe (`EPSG:3035`).
- Palettes must be colorblind-safe.
- Captions must avoid false within-country precision.
- Figures must be 300 dpi or otherwise journal-ready.

## Manuscript QA Gates

- Title must specify EU/EEA, 2019--2023, and reported incidence/benchmark framing.
- Abstract must state row count, data source, metrics, and negative/mixed result.
- Related work must include Zeimes et al., Kallio et al., Reusken/Heyman, Kazasidis/Geduhn/Jacob, Glass et al., Allen et al., and WIS/forecast-benchmark literature.
- Limitations must explicitly mention five years, country-level aggregation, reporting heterogeneity, Belgium 2023, Cyprus 2023, COVID-era sensitivity, and retrospective validation.
- Funding statement must say no external funding.
- Competing interests must say none.
- Ethics statement must say aggregated public data and no individual-level patient data.

## Repo QA Gates

Before submission rerun:

```powershell
python tools/create_ecdc_case_table.py --accessed-date 2026-05-12
python tools/validate_international_cases.py --strict
python tools/build_international_dataset.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/run_feature_ablation.py
python tools/run_count_models.py
python tools/create_ijhg_maps.py
python tools/run_sensitivity_power.py
python tools/check_publication_readiness.py
python -m pytest
python -m ruff check src tests tools
git diff --check
rg -n "password\s*=|token\s*=|secret\s*=|api_key|BEGIN [A-Z ]*PRIVATE KEY" .
```

Expected current status:

- Tests: 26 passed.
- Ruff: passed.
- Publication readiness gate: PASS.
- Secret scan: only expected false positives in docs, dummy tests, Earthdata parser code, and archived source material.
