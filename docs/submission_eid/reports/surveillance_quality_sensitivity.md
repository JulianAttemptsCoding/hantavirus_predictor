# Surveillance-Quality Sensitivity

These analyses test whether flagged surveillance rows or COVID-era training years change the main conclusion. They are sensitivity analyses, not causal estimates.

| scenario | feature_set | n | rows_retained | countries_retained | mean_wis | relative_wis_observed_mean | coverage_90_numerator | coverage_90_denominator | coverage_90 | mean_interval_width_90 | mae | brier_any_case | promotion_rule_passed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exclude_2020_2021_training_rows | all_public | 28 | 85 | 29 | 75.85 | 1.127 | 25 | 28 | 0.8929 | 764 | 131.3 | 0.285 | False |
| exclude_2020_training_rows | all_public | 28 | 114 | 29 | 138.3 | 2.054 | 25 | 28 | 0.8929 | 593.2 | 173 | 0.2578 | False |
| exclude_2021_training_rows | surveillance_only | 28 | 113 | 29 | 27.93 | 0.4148 | 26 | 28 | 0.9286 | 304.3 | 49.25 | 0.5715 | False |
| exclude_belgium_2023 | land_use | 27 | 141 | 29 | 329.4 | 4.979 | 18 | 27 | 0.6667 | 324.1 | 379.5 | 0.3044 | False |
| exclude_belgium_2023_and_cyprus_2023 | land_use | 26 | 140 | 29 | 341.6 | 4.973 | 17 | 26 | 0.6538 | 327.4 | 393.8 | 0.2777 | False |
| exclude_cyprus_2023 | land_use | 27 | 141 | 29 | 329.9 | 4.726 | 18 | 27 | 0.6667 | 329 | 380.8 | 0.2674 | False |
| primary_all_rows | land_use | 28 | 142 | 29 | 318.5 | 4.732 | 19 | 28 | 0.6786 | 325.9 | 367.4 | 0.2936 | False |
| retain_flagged_rows_with_indicator | land_use | 28 | 142 | 29 | 318.5 | 4.732 | 19 | 28 | 0.6786 | 325.9 | 367.4 | 0.2936 | False |

Interpretation: the manuscript may claim model improvement only if the promotion rule holds across the primary and flagged-row scenarios.
