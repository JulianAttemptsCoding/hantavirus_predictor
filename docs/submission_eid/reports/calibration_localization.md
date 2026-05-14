# Calibration Localization

The table localizes 2023 interval coverage failures by country and model without implying within-country precision.

| model_family | feature_set | covered_90_numerator | covered_90_denominator | mean_interval_width | mean_absolute_error | coverage_90 |
| --- | --- | --- | --- | --- | --- | --- |
| covariate_block | all_public | 42 | 56 | 283.2 | 239.4 | 0.75 |
| covariate_block | climate | 43 | 56 | 292 | 255.2 | 0.7679 |
| covariate_block | context | 43 | 56 | 310.5 | 248.9 | 0.7679 |
| covariate_block | land_use | 43 | 56 | 317.5 | 238 | 0.7679 |
| covariate_block | surveillance_only | 42 | 56 | 309.1 | 240.6 | 0.75 |
| penalized_poisson | all_public | 6 | 28 | 35.14 | 273 | 0.2143 |
| penalized_poisson | climate | 7 | 28 | 35.5 | 285 | 0.25 |
| penalized_poisson | context | 9 | 28 | 37.11 | 286.5 | 0.3214 |
| penalized_poisson | land_use | 9 | 28 | 28.82 | 167.6 | 0.3214 |
| penalized_poisson | surveillance_only | 9 | 28 | 35.32 | 260.7 | 0.3214 |
