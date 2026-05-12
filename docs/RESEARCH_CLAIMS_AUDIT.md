# Research Claims Audit

Audit date: 2026-05-12

This file records claims from the ZIP packages and blocker notes against current authoritative sources. It is intentionally cautious: unsupported claims stay out of the publication plan.

## Source Links Used

- CDC About Hantavirus: https://www.cdc.gov/hantavirus/about/index.html
- CDC Reported Cases: https://www.cdc.gov/hantavirus/data-research/cases/index.html
- CDC Case Definition and Reporting: https://www.cdc.gov/hantavirus/php/surveillance/index.html
- CDC NNDSS Annual Tables: https://www.cdc.gov/nndss/notifiable-infectious-disease-tables/about-tables.html
- CDC NNDSS Data Locations: https://www.cdc.gov/nndss/infectious-disease/weekly-and-annual-disease-data-tables.html
- NEON Rodent Pathogen API: https://data.neonscience.org/api/v0/products/DP1.10064.001
- NEON Small Mammal API: https://data.neonscience.org/api/v0/products/DP1.10072.001
- NASA AppEEARS: https://www.earthdata.nasa.gov/data/tools/appeears
- Daymet: https://daymet.ornl.gov/
- USGS Annual NLCD: https://www.usgs.gov/centers/eros/science/annual-nlcd-data-access
- CDC/ATSDR SVI: https://www.atsdr.cdc.gov/place-health/php/svi/index.html
- Census ACS API: https://www.census.gov/programs-surveys/acs/data/data-via-api.html
- NOAA ONI: https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php
- WHO MV Hondius DON599: https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON599
- WHO MV Hondius DON600: https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600
- Google TimesFM: https://github.com/google-research/timesfm
- Bracher et al. WIS: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008618

## Verdict Table

| Claim | Verdict | Evidence | Project decision |
|---|---:|---|---|
| Hantavirus is mainly rodent-borne. | Verified | CDC says hantaviruses are spread mainly by rodents and exposure to urine, droppings, and saliva. | Model reservoir and exposure risk first. |
| Andes virus is the only hantavirus known for person-to-person spread. | Verified | CDC states Andes virus is the only type known to spread person-to-person. WHO confirms limited person-to-person transmission has been reported for Andes virus. | Keep Andes H2H as separate module, not part of U.S. Sin Nombre baseline. |
| U.S. public hantavirus cases are sparse. | Verified | CDC reports 890 U.S. cases from 1993 through 2023. | Human case modeling must be low-dimensional and uncertainty-heavy. |
| Public CDC county-level hantavirus data can be used. | False for public data | CDC reported-cases page says data are state-only and county-level data cannot be provided publicly to protect identities. | County model blocked until restricted partner data exist. |
| NNDSS annual data are exact incidence truth. | False | CDC says finalized NNDSS data are likely underestimates because of under-recognition and under-reporting. | Treat as reported-case surveillance, not true incidence. |
| NEON hantavirus serology ends after 2019. | Verified | NEON API says samples were tested for hantaviruses from 2014-2019 and testing changed in 2020. | Serology ground truth ends in 2019; later reservoir dynamics require proxy validation. |
| NEON small mammal trapping continues beyond 2019. | Verified | NEON API summary shows DP1.10072.001 active with current availability through 2026-03 at time of audit. | Use as abundance/trap-success proxy, not infection label. |
| TimesFM 2.5 is not public. | Outdated/false as of audit | Google Research repository says TimesFM 2.5 is out and loads from public Hugging Face checkpoints. | TimesFM may be an optional baseline/prior, not a blocker. |
| MV Hondius 2026 Andes virus outbreak is real. | Verified | WHO DON599/DON600 describe the cluster, confirmed hantavirus, and Andes sequencing. | Include as motivation for scope clarity and optional Andes appendix only. |
| WIS is appropriate for epidemic interval forecasts. | Verified | Bracher et al. describe WIS as a proper score approximating CRPS for interval/quantile forecasts. | Use WIS, coverage, and calibration as primary probabilistic metrics. |
| SafeGraph/Meta mobility is required. | Unsupported and risky | Supplied packages propose it, but no authoritative source makes it necessary for reservoir risk. | Exclude unless ethics/license are already approved. |
| Synthetic SEIR trajectories prove model validity. | False | Synthetic data can encode assumptions but cannot validate real-world predictive skill. | Use synthetic trajectories only for unit tests, priors, or pretraining experiments with ablation. |
| "35 percent WIS improvement" is expected. | Unsupported | No real training results in archives. | Treat any performance target as a preregistered gate, not a claim. |
| "R2 around 0.15" for rodent proxies is established here. | Unverified from supplied files | Blocker note gives no citation. Literature supports weak and context-dependent links but not this exact value from the repo. | Do not quote this value without source-specific evidence. |

## NEON API Snapshot

Generated by querying NEON product APIs during setup:

- `DP1.10064.001`: 45 sites, first month `2014-04`, last month `2019-11`, 56 unique available months.
- `DP1.10072.001`: 46 sites, first month `2013-06`, last month `2026-03`, 130 unique available months.

Run this to refresh the snapshot:

```powershell
python tools/summarize_neon_products.py
```

## Core Scientific Reframe

The project should not be pitched as "the best algorithmic human hantavirus predictor" yet. The publishable claim is:

> A rigorously validated, uncertainty-calibrated reservoir and spillover-risk forecasting framework that quantifies when public data are sufficient, when they are not, and how much added value complex models provide over strong baselines.

That claim is less flashy and much harder for reviewers to knock down.

