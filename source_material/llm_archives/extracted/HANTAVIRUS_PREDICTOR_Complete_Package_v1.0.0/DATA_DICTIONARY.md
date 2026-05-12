# HANTAVIRUS PREDICTOR: Data Dictionary
## Complete Variable Reference for All Data Sources

---

## 1. HUMAN CASE DATA (CDC NNDSS / WONDER)

| Variable | Type | Description | Units | Range | Missing | Source |
|----------|------|-------------|-------|-------|---------|--------|
| `county_fips` | string | 5-digit FIPS county code | -- | 01001-56045 | 0% | CDC WONDER |
| `date` | datetime | Case report date (monthly) | YYYY-MM-DD | 1993-2023 | 0% | CDC WONDER |
| `year` | int | Case year | -- | 1993-2023 | 0% | CDC WONDER |
| `month` | int | Case month | -- | 1-12 | 0% | CDC WONDER |
| `iso_week` | int | ISO epidemiological week | -- | 1-53 | 0% | Derived |
| `cases` | int | Confirmed hantavirus cases | count | 0-50 | 0% | CDC WONDER |
| `deaths` | int | Hantavirus deaths | count | 0-20 | 0% | CDC WONDER |
| `age_group` | categorical | Patient age group | -- | 0-4, 5-14, ..., 85+ | 5% | CDC WONDER |
| `sex` | categorical | Patient sex | -- | M, F, U | 3% | CDC WONDER |
| `race` | categorical | Patient race | -- | White, Black, ..., Unknown | 8% | CDC WONDER |
| `ethnicity` | categorical | Patient ethnicity | -- | Hispanic, Non-Hispanic, Unknown | 10% | CDC WONDER |
| `outbreak_threshold` | float | 95th percentile of county cases | count | 0-10 | 0% | Derived |
| `is_outbreak` | binary | cases > outbreak_threshold | -- | 0, 1 | 0% | Derived |
| `log_cases` | float | log(1 + cases) | -- | 0-4 | 0% | Derived |

---

## 2. RODENT SURVEILLANCE (NEON DP1.10072.001)

| Variable | Type | Description | Units | Range | Missing | Source |
|----------|------|-------------|-------|-------|---------|--------|
| `site_id` | string | NEON site identifier | -- | e.g., "ABBY", "BARR" | 0% | NEON API |
| `collectDate` | datetime | Trap collection date | YYYY-MM-DD | 2014-2019 | 0% | NEON API |
| `year_month` | period | Collection month | YYYY-MM | 2014-01 to 2019-12 | 0% | Derived |
| `taxonID` | string | Species identifier | -- | e.g., "PEMA", "PELE" | 0% | NEON API |
| `sex` | categorical | Rodent sex | -- | M, F, U | 2% | NEON API |
| `tagID` | string | Individual identifier | -- | unique | 0% | NEON API |
| `testResult` | categorical | Serology result | -- | Positive, Negative, Indeterminate | 0% | NEON API |
| `trap_nights` | int | Total trap-nights per site-month | count | 50-500 | 0% | NEON API |
| `trap_success` | float | Captures per 100 trap-nights | count/100TN | 0-50 | 0% | Derived |
| `positive` | int | Positive serology count | count | 0-20 | 0% | Derived |
| `total_tested` | int | Total tested count | count | 10-200 | 0% | Derived |
| `seroprevalence` | float | positive / total_tested | proportion | 0-0.5 | 0% | Derived |
| `male_seroprev` | float | Male seroprevalence | proportion | 0-0.7 | 5% | Derived |
| `female_seroprev` | float | Female seroprevalence | proportion | 0-0.3 | 5% | Derived |

---

## 3. CLIMATE / REMOTE SENSING

### MODIS NDVI (MOD13Q1)

| Variable | Type | Description | Units | Range | Resolution | Source |
|----------|------|-------------|-------|-------|------------|--------|
| `NDVI` | float | Normalized Difference Vegetation Index | dimensionless | -0.2 to 1.0 | 250m, 16-day | NASA LP DAAC |
| `EVI` | float | Enhanced Vegetation Index | dimensionless | -0.2 to 1.0 | 250m, 16-day | NASA LP DAAC |
| `NDVI_quality` | int | Pixel reliability flag | -- | 0-3 | 250m, 16-day | NASA LP DAAC |
| `NDVI_anom` | float | NDVI anomaly from climatology | dimensionless | -0.5 to 0.5 | 250m, monthly | Derived |
| `NDVI_lag6m` | float | 6-month lagged NDVI | dimensionless | -0.2 to 1.0 | 1km, monthly | Derived |
| `NDVI_lag12m` | float | 12-month lagged NDVI | dimensionless | -0.2 to 1.0 | 1km, monthly | Derived |
| `NDVI_lag18m` | float | 18-month lagged NDVI | dimensionless | -0.2 to 1.0 | 1km, monthly | Derived |
| `NDVI_lag24m` | float | 24-month lagged NDVI | dimensionless | -0.2 to 1.0 | 1km, monthly | Derived |

### ERA5 Reanalysis

| Variable | Type | Description | Units | Range | Resolution | Source |
|----------|------|-------------|-------|-------|------------|--------|
| `t2m` | float | 2-meter temperature | K | 250-320 | 0.25deg, hourly | Copernicus CDS |
| `tp` | float | Total precipitation | m | 0-0.5 | 0.25deg, hourly | Copernicus CDS |
| `stl1` | float | Soil temperature level 1 | K | 250-320 | 0.25deg, hourly | Copernicus CDS |
| `rh` | float | Relative humidity | % | 0-100 | 0.25deg, hourly | Copernicus CDS |
| `temp_monthly` | float | Monthly mean temperature | degC | -10 to 40 | 1km, monthly | Derived |
| `precip_monthly` | float | Monthly total precipitation | mm | 0-500 | 1km, monthly | Derived |
| `soil_temp_april` | float | April soil temperature | degC | 0-30 | 1km, annual | Derived |
| `soil_temp_sep` | float | September soil temperature | degC | 10-35 | 1km, annual | Derived |
| `sunshine_sep` | float | September sunshine duration | hours | 100-300 | 1km, annual | Derived |
| `precip_lag12m` | float | 12-month lagged precipitation | mm | 0-500 | 1km, monthly | Derived |
| `precip_lag18m` | float | 18-month lagged precipitation | mm | 0-500 | 1km, monthly | Derived |
| `precip_lag24m` | float | 24-month lagged precipitation | mm | 0-500 | 1km, monthly | Derived |
| `temp_anom` | float | Temperature anomaly | degC | -5 to 5 | 1km, monthly | Derived |
| `precip_anom` | float | Precipitation anomaly | mm | -200 to 200 | 1km, monthly | Derived |

### CHIRPS Precipitation

| Variable | Type | Description | Units | Range | Resolution | Source |
|----------|------|-------------|-------|-------|------------|--------|
| `chirps_precip` | float | Daily precipitation | mm | 0-200 | 0.05deg, daily | USGS |
| `chirps_monthly` | float | Monthly precipitation | mm | 0-1000 | 1km, monthly | Derived |

---

## 4. LAND COVER / GEOGRAPHIC

| Variable | Type | Description | Units | Range | Resolution | Source |
|----------|------|-------------|-------|-------|------------|--------|
| `land_cover` | categorical | ESA WorldCover class | -- | 0-10 | 10m, annual | ESA |
| `elevation` | float | SRTM elevation | m | -50 to 4000 | 30m, static | NASA |
| `slope` | float | Terrain slope | degrees | 0-45 | 30m, static | Derived |
| `aspect` | float | Terrain aspect | degrees | 0-360 | 30m, static | Derived |
| `dist_water` | float | Distance to nearest water body | km | 0-50 | 1km, static | Derived |
| `dist_road` | float | Distance to nearest road | km | 0-20 | 1km, static | OSM |

---

## 5. SOCIOECONOMIC

### CDC SVI (2022)

| Variable | Type | Description | Units | Range | Source |
|----------|------|-------------|-------|-------|--------|
| `SVI_theme1` | float | Socioeconomic status percentile | percentile | 0-1 | CDC |
| `SVI_theme2` | float | Household composition percentile | percentile | 0-1 | CDC |
| `SVI_theme3` | float | Minority status percentile | percentile | 0-1 | CDC |
| `SVI_theme4` | float | Housing type/transportation percentile | percentile | 0-1 | CDC |
| `SVI_overall` | float | Overall SVI percentile | percentile | 0-1 | CDC |
| `poverty_rate` | float | Poverty rate | proportion | 0-1 | Census ACS |
| `unemployment` | float | Unemployment rate | proportion | 0-1 | Census ACS |
| `housing_age` | float | Median housing age | years | 0-100 | Census ACS |
| `rurality_code` | int | Rural-Urban Continuum Code | -- | 1-9 | USDA |
| `population` | int | County population | count | 100-10M | Census |
| `pop_density` | float | Population density | people/km2 | 1-10000 | Derived |

---

## 6. HUMAN MOBILITY (SafeGraph)

| Variable | Type | Description | Units | Range | Source |
|----------|------|-------------|-------|-------|--------|
| `origin_cbg` | string | Origin Census Block Group | -- | 12-digit | SafeGraph |
| `destination_cbg` | string | Destination Census Block Group | -- | 12-digit | SafeGraph |
| `visitor_count` | int | Number of visitors | count | 0-10000 | SafeGraph |
| `mobility_index` | float | Normalized mobility flow | dimensionless | 0-1 | Derived |

---

## 7. CLIMATE INDICES

| Variable | Type | Description | Units | Range | Source |
|----------|------|-------------|-------|-------|--------|
| `enso_oni` | float | ENSO Oceanic Nino Index | degC | -3 to 3 | NOAA |
| `enso_phase` | categorical | ENSO phase | -- | El_Nino, La_Nina, Neutral | Derived |
| `pdo_index` | float | Pacific Decadal Oscillation | dimensionless | -3 to 3 | JISAO |
| `nao_index` | float | North Atlantic Oscillation | dimensionless | -3 to 3 | NCAR |
| `season` | categorical | Meteorological season | -- | Winter, Spring, Summer, Fall | Derived |

---

## 8. MODEL FEATURES (Engineered)

| Variable | Type | Description | Formula | Range |
|----------|------|-------------|---------|-------|
| `exposure_index` | float | Human-rodent contact proxy | sigmoid(w1*SVI + w2*rurality + w3*housing + w4*occupation) | 0-1 |
| `carrying_capacity_proxy` | float | K(t) environmental proxy | NDVI_anom * precip_anom * exp(-temp_stress) | 0-10 |
| `cases_lag1m` | float | Cases 1 month ago | lag(cases, 1) | 0-50 |
| `cases_lag6m` | float | Cases 6 months ago | lag(cases, 6) | 0-50 |
| `cases_lag12m` | float | Cases 12 months ago | lag(cases, 12) | 0-50 |
| `sero_lag3m` | float | Seroprevalence 3 months ago | lag(seroprevalence, 3) | 0-0.5 |
| `sero_lag6m` | float | Seroprevalence 6 months ago | lag(seroprevalence, 6) | 0-0.5 |
| `ndvi_roll_mean_3m` | float | 3-month rolling mean NDVI | rolling_mean(NDVI, 3) | -0.2-1.0 |
| `ndvi_roll_std_6m` | float | 6-month rolling std NDVI | rolling_std(NDVI, 6) | 0-0.3 |
| `precip_roll_sum_12m` | float | 12-month rolling sum precipitation | rolling_sum(precip, 12) | 0-5000 |

---

## 9. MODEL OUTPUTS

| Variable | Type | Description | Units | Range |
|----------|------|-------------|-------|-------|
| `forecast_mu` | float | Predicted mean case count | count | 0-50 |
| `forecast_phi` | float | Predicted dispersion parameter | -- | 0.001-10 |
| `forecast_lower` | float | Lower 90% prediction bound | count | 0-50 |
| `forecast_upper` | float | Upper 90% prediction bound | count | 0-100 |
| `risk_tier` | categorical | Risk classification | -- | Low, Moderate, High, Critical |
| `R0` | float | Basic reproduction number | -- | 0-10 |
| `rodent_prevalence` | float | Predicted rodent infectious prevalence | proportion | 0-0.5 |
| `spillover_probability` | float | Probability of human spillover | proportion | 0-1 |
| `shap_value_i` | float | SHAP attribution for feature i | -- | -inf to +inf |

---

## DATA QUALITY FLAGS

| Flag | Description | Action |
|------|-------------|--------|
| `missing_core` | Missing >10% of core features | Exclude from training |
| `temporal_gap` | >3 consecutive months missing | Interpolate or exclude |
| `spatial_outlier` | Value >5 SD from regional mean | Investigate, possibly cap |
| `negative_count` | Negative case count after processing | Set to 0, flag |
| `future_leakage` | Feature uses data from t+1 or later | Reject, fix pipeline |
| `low_population` | County population < 1000 | Exclude or aggregate |

---

## DATA LICENSES

| Source | License | Attribution Required | Commercial Use |
|--------|---------|---------------------|----------------|
| CDC NNDSS | Public Domain | No | Yes |
| NEON | CC0 | No | Yes |
| MODIS | Free | Yes (NASA) | Yes |
| ERA5 | Copernicus T&C | Yes | Yes |
| CHIRPS | Free | Yes (USGS) | Yes |
| ESA WorldCover | Free | Yes | Yes |
| SRTM | Free | Yes (NASA) | Yes |
| CDC SVI | Public Domain | No | Yes |
| Census ACS | Public Domain | No | Yes |
| SafeGraph | Application Required | Yes | Yes |

---

*Last updated: May 2026 | For questions, contact data-team@university.edu*
