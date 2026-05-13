# Table Shells

## Table 1. Data Sources

| Source | Variables | Time span | License/terms | Role |
| --- | --- | --- | --- | --- |
| ECDC Annual Epidemiological Reports | Country-year cases and metadata | 2019-2023 | ECDC source attribution required | Primary labels |
| World Bank | Population, rurality, GDP | Lagged public context | CC BY 4.0 default unless otherwise labeled | Context covariates |
| FAOSTAT | Land-use areas and shares | Lagged country-year summaries | FAO open data attribution | Land-use covariates |
| TerraClimate | Climate and water-balance summaries | Lagged country-year summaries | Cite Abatzoglou et al. | Climate context |
| Natural Earth | Country boundaries | Static | Public domain | Maps |

## Table 2. ECDC Country-Year Audit

| Item | Result |
| --- | --- |
| Years | 2019-2023 |
| Rows | 142 |
| Annual totals | 4088, 1693, 4947, 2185, 1885 |
| Belgium 2023 | `not_comprehensive`, quality grade C |
| Cyprus 2023 | `unspecified`, quality grade C |
| UK handling | Excluded from primary balanced panel |

## Table 3. Feature Families

| Feature set | Additions | Primary final features before one-hot encoding |
| --- | --- | ---: |
| `surveillance_only` | Lagged surveillance summaries | 7 |
| `context` | World Bank rurality and GDP | 9 |
| `land_use` | FAOSTAT land-use shares | 14 |
| `climate` | TerraClimate variables | 19 |
| `all_public` | Public source-quality metadata | 20 |

## Table 4. Primary Feature Ablation Metrics

| Target year | Best ablation set | Mean WIS | Relative WIS | Coverage 90 | Interval width | MAE |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 2022 | `all_public` | 74.46 | 0.99 | 0.76 | 264.92 | 109.89 |
| 2023 | `land_use` | 318.55 | 4.73 | 0.68 | 325.87 | 367.44 |

## Table 5. Sensitivity Analyses

| Scenario | Purpose | Expected interpretation |
| --- | --- | --- |
| Exclude non-comprehensive/unspecified rows | Belgium and Cyprus caveats | Check whether conclusions depend on flagged source metadata |
| Pandemic-period indicator | 2020-2021 reporting disruption | Included in all nested feature sets |
| Exclude 2020-2021 training rows | COVID-era sensitivity | Sparse-sample stress test only |

## Table 6. Detectability Simulation

| Effect size | Quantity |
| --- | --- |
| Log-rate effect per SD of lagged precipitation | Simulated covariate signal |
| Detectability rate | Share of simulations with at least 5 percent WIS improvement |

## Table 7. Penalized Count Model

| Model | Offset | Tuning | Promotion status |
| --- | --- | --- | --- |
| Penalized Poisson GLM | `log(population / 100000)` | 2022 validation WIS | Exploratory unless WIS and coverage beat simple baselines |
