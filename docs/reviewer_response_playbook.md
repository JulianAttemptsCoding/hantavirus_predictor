# Reviewer Response Playbook

Last updated: 2026-05-14

This is a compact defense guide for the EID manuscript.

## What Does This Add Beyond ECDC Tables?

ECDC provides authoritative surveillance totals. This project adds a reproducible
benchmark that links those labels to public covariates, compares forecasts with
strong surveillance-history baselines, and quantifies calibration and sharpness
with held-out country-year observations.

## Why Is A Negative Result Publishable?

Because the result identifies a practical public-health bottleneck. Sparse annual
public surveillance and heterogeneous completeness metadata limit what calibrated
country-level forecasting can support. The paper should not say "we built a
predictor"; it should say "we tested the public-data forecasting ceiling."

## Why Country-Year Rather Than District Or Monthly Data?

Country-year ECDC reports are the public cross-national labels that can be
audited and reproduced across EU/EEA countries. District-level or monthly
modeling would answer a different question and often requires country-specific
or nonpublic data systems.

## Does This Contradict German Puumala Forecasting Work?

No. Kazasidis and Jacob 2023 and Kazasidis, Geduhn, and Jacob 2024 use richer
German district-level PUUV data and biologically specific predictors. This
project tests a harder and coarser public EU/EEA country-year setting.

## Why Reported Cases Instead Of True Infections?

The public outcome is reported annual cases. Reported incidence reflects true
incidence, ascertainment, case definitions, reporting completeness, and health
system behavior. The manuscript must not claim unbiased infection burden.

## Why Include 2020-2021?

Those years are part of the available 2019-2023 public panel. The manuscript must
include COVID-era sensitivity analyses rather than silently removing or ignoring
them.

## Could Belgium Or Cyprus Drive The Result?

This must be tested directly. The EID-ready package needs separate Belgium 2023,
Cyprus 2023, combined exclusion, and flagged-row indicator scenarios.

## Could Finland Or Germany Drive The Result?

This must be tested directly because ECDC reports Finland and Germany accounted
for 60.5% of 2023 cases. The EID-ready package needs leave-one-country-out
influence analysis.

## Why Use WIS?

Weighted interval score is a proper interval-format forecast score used in
epidemic forecast evaluation. It rewards forecasts that are sharp and calibrated,
but it must be reported with empirical coverage and interval width.

## Why Not Promote The Penalized Poisson Model?

The current best penalized Poisson model is sharp but poorly calibrated. In 2023,
the land-use penalized Poisson model covered 9/28 observations, about 32%, far
below the nominal 90% interval target.

## Why No MODIS Vegetation Claim?

The MODIS source manifest exists, but quality-masked country-year aggregation did
not pass the inclusion gate. Excluding it is a strength: the paper avoids claims
it cannot audit.

## What Is The Public-Health Takeaway?

Before public covariates can support credible pan-European hantavirus forecasts,
surveillance systems need standardized completeness flags, longer comparable
panels, harmonized metadata, and explicit uncertainty reporting.
