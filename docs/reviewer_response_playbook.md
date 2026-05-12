# Reviewer Response Playbook

Last updated: 2026-05-12

This file is a compact defense guide for the publication-track manuscript.

## What Does This Add Beyond ECDC Tables?

ECDC provides authoritative surveillance totals. This project adds a frozen,
open, reproducible benchmark that links those labels to public demographic,
land-use, and climate covariates, evaluates probabilistic one-year-ahead
retrospective predictions, and quantifies whether covariates improve over
simple surveillance baselines.

## How Is This Different From HantavirusMap?

HantavirusMap is a live public signal tracker. This project is a benchmark:
frozen labels, documented source provenance, reproducible covariate joins,
calibration metrics, ablation tests, and negative results retained.

## How Is This Different From Zeimes Et Al. 2015?

Zeimes et al. studied spatial distribution and environmental risk of human
hantavirus cases in Europe. This project studies country-year reported
incidence as a temporal benchmark with probabilistic evaluation and
source-audited public covariates.

## Why Country-Year Rather Than County Or District?

The paper is limited to free public harmonized surveillance. Country-year ECDC
reports are the available cross-national public labels. More granular human
data are often privacy-limited; CDC explicitly states that U.S. county-level
hantavirus data cannot be provided to protect identities.

## Why Not PAHO Or China In Version 1?

PAHO alerts are event-based Hantavirus Pulmonary Syndrome signals in the
Americas. China CDC Weekly reports HFRS with PLAD/county structure and HTNV/
SEOV diversity. These are different source systems, syndromes, viruses, and
spatial scales. Pooling them with ECDC would create false comparability.

## Why Not A Human-To-Human Spread Simulation?

Most hantavirus transmission is reservoir-to-human. Andes virus can transmit
person-to-person, but that is not the ECDC country-year target. The current
simulation is only a sparse reported-incidence state stress test and is not
used as validation evidence.

## What If Climate Adds No Predictive Value?

That is still a useful result. It would show that, at the public EU/EEA
country-year scale, simple surveillance baselines are hard to beat and that
improved surveillance completeness/timeliness may matter more than adding
coarse covariates.

## What If 90 Percent Coverage Is Poor?

Report it directly. Calibration failure is a result, not something to hide.
Discuss WIS together with empirical coverage and interval width so reviewers
can see the tradeoff between accuracy and sharpness.

## Why Use WIS?

Weighted interval score is a proper score widely used for probabilistic
epidemic forecast evaluation. It rewards accurate medians while penalizing
miscalibrated and overly wide intervals.

## Why Avoid PLOS NTD For ECDC-Only?

PLOS NTD focuses on neglected diseases affecting under-resourced and often
LMIC populations, and its scope restricts high-income-country work unless it
has LMIC consequences. The ECDC-only paper is a better fit for IJHG, Scientific
Data, or BMC Public Health.
