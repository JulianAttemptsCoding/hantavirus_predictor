# Leave-One-Country-Out Influence

This analysis reruns the primary 2023 ablation and surveillance baselines after removing each country. Finland and Germany are pre-specified because ECDC reported that they accounted for 60.5% of 2023 cases.

| removed_country | removed_2023_cases | high_influence_prespecified | loo_best_ablation_feature_set | delta_best_ablation_wis | delta_best_ablation_coverage | loo_best_baseline_model | delta_best_baseline_wis | conclusion_changes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Austria | 97 | False | land_use | -10.15 | 0.02513 | last_observed_country_rate | -0.9152 | False |
| Belgium | 99 | False | land_use | 9.152 | -0.0119 | empirical_negative_binomial_rate | 0.8539 | False |
| Bulgaria | 6 | False | land_use | 9.103 | -0.0119 | last_observed_country_rate | 1.448 | False |
| Croatia | 2 | False | land_use | 174.1 | -0.04894 | gradient_boosting_rate | 1.183 | False |
| Cyprus | 0 | False | land_use | 17.53 | -0.0119 | last_observed_country_rate | 1.587 | False |
| Czechia | 11 | False | land_use | 10.98 | -0.0119 | last_observed_country_rate | 1.527 | False |
| Estonia | 19 | False | land_use | 34.33 | -0.0119 | last_observed_country_rate | 1.5 | False |
| Finland | 806 | True | land_use | -38.01 | 0.02513 | gradient_boosting_rate | -23.36 | False |
| France | 50 | False | land_use | -34.7 | 0.02513 | gradient_boosting_rate | -0.761 | False |
| Germany | 335 | True | land_use | -12.19 | -0.0119 | country_historical_mean_rate | -8.834 | False |
| Greece | 1 | False | land_use | 9.881 | -0.0119 | gradient_boosting_rate | 0.1021 | False |
| Hungary | 11 | False | land_use | 14.19 | -0.0119 | last_observed_country_rate | 1.263 | False |
| Iceland | 0 | False | land_use | 4.028 | 0 | last_observed_country_rate | 0 | False |
| Ireland | 0 | False | land_use | 18.11 | -0.0119 | last_observed_country_rate | 1.587 | False |
| Italy | 0 | False | land_use | -17.49 | 0.02513 | last_observed_country_rate | 1.587 | False |
| Latvia | 4 | False | land_use | 17.23 | -0.0119 | last_observed_country_rate | 1.569 | False |
| Liechtenstein | 0 | False | land_use | 1.53 | -0.0119 | last_observed_country_rate | 1.587 | False |
| Lithuania | 0 | False | land_use | 17.28 | -0.0119 | last_observed_country_rate | 1.587 | False |
| Luxembourg | 5 | False | land_use | -66.71 | 0.09921 | last_observed_country_rate | 1.544 | False |
| Malta | 0 | False | land_use | 16.96 | -0.0119 | last_observed_country_rate | 1.587 | False |
| Netherlands | 0 | False | land_use | 5.558 | 0.02513 | last_observed_country_rate | 1.571 | False |
| Norway | 15 | False | land_use | -5.588 | -0.0119 | last_observed_country_rate | 1.507 | False |
| Poland | 43 | False | land_use | -1.537 | 0.02513 | last_observed_country_rate | 0.27 | False |
| Portugal | 0 | False | land_use | 13.77 | -0.0119 | gradient_boosting_rate | 1.392 | False |
| Romania | 6 | False | land_use | 6.283 | -0.0119 | last_observed_country_rate | 1.564 | False |
| Slovakia | 154 | False | land_use | -2.605 | 0.02513 | last_observed_country_rate | -0.672 | False |
| Slovenia | 64 | False | all_public | -132.6 | 0.02513 | last_observed_country_rate | -0.4115 | False |
| Spain | 0 | False | land_use | -9.065 | 0.02513 | last_observed_country_rate | 1.587 | False |
| Sweden | 157 | False | land_use | -8.42 | -0.0119 | last_observed_country_rate | -8.895 | False |
