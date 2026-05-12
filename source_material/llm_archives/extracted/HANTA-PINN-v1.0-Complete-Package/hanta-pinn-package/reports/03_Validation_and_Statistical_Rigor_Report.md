# REPORT 3: Validation Protocol & Statistical Rigor
**Version:** 1.0-FINAL  
**Date:** 2026-05-11  

---

## 1. EVALUATION METRICS

### 1.1 Primary Metrics: Rodent Reservoir Dynamics

| Metric | Formula | Target | Interpretation |
|--------|---------|--------|----------------|
| RMSE | sqrt(mean((y_pred - y_true)^2)) | < 0.05 | Absolute error in seroprevalence |
| MAE | mean(|y_pred - y_true|) | < 0.04 | Robust absolute error |
| R^2 | 1 - SS_res/SS_tot | > 0.60 | Variance explained |
| MAPE | mean(|(y_pred - y_true)/y_true|) | < 25% | Percentage error |

### 1.2 Secondary Metrics: Human Spillover

| Metric | Formula | Target | Interpretation |
|--------|---------|--------|----------------|
| WIS | Weighted Interval Score | < baseline by 15% | Probabilistic forecast quality |
| CRPS | Continuous Ranked Probability Score | < baseline by 10% | Probabilistic accuracy |
| RMSE (cases) | sqrt(mean((cases_pred - cases_true)^2)) | < 2.0 | Point forecast accuracy |

### 1.3 Classification Metrics: Outbreak Detection

| Metric | Target | Notes |
|--------|--------|-------|
| ROC-AUC | > 0.85 | Binary: outbreak (>=2 cases) vs. no outbreak |
| PR-AUC | > 0.70 | Precision-recall for imbalanced data |
| Sensitivity | > 0.80 | Catch true outbreaks |
| Specificity | > 0.85 | Avoid false alarms |
| F1-score | > 0.75 | Balanced performance |

### 1.4 Calibration Metrics

| Metric | Target | Interpretation |
|--------|--------|----------------|
| Coverage Probability | 90% +/- 5% | Empirical coverage of 90% PIs |
| MPIW | As narrow as possible | Mean Prediction Interval Width |
| ECE | < 0.05 | Expected Calibration Error |
| MCE | < 0.10 | Maximum Calibration Error |

---

## 2. CROSS-VALIDATION STRATEGY

### 2.1 Temporal Cross-Validation (Primary)

    Fold 1: Train [2014, 2015, 2016] | Val [2017] | Test [2018]
    Fold 2: Train [2014, 2015, 2016, 2017] | Val [2018] | Test [2019]
    Fold 3: Train [2015, 2016, 2017] | Val [2018] | Test [2019]

**Rules:**
1. NO random shuffling of time points
2. All lag features must satisfy: feature_time <= prediction_time
3. Hyperparameter tuning uses validation set only
4. Test set is used exactly once per fold
5. Final metrics averaged across folds

### 2.2 Spatial Cross-Validation (Secondary)

    Leave-One-NEON-Domain-Out:
    - 18 domains total
    - For each domain D:
      - Train on all sites NOT in D
      - Test on all sites IN D
      - Repeat for all 18 domains

**Purpose:** Tests generalization to unseen ecosystems.

### 2.3 Nested Cross-Validation

For hyperparameter tuning:
- Outer loop: 3-fold temporal CV
- Inner loop: 2-fold temporal CV on training set
- Prevents overfitting in hyperparameter selection

---

## 3. STATISTICAL TESTS

### 3.1 Forecast Comparison Tests

**Diebold-Mariano Test**
- Null hypothesis: Two models have equal forecast accuracy
- Alternative: HANTA-PINN is more accurate than baseline
- Significance: alpha = 0.05
- Loss function: Squared error for point forecasts, WIS for probabilistic

**Clarke Test**
- Null hypothesis: No model dominates
- Alternative: HANTA-PINN dominates baseline
- Significance: alpha = 0.05

### 3.2 Distribution Tests

**Kolmogorov-Smirnov Test**
- Purpose: Detect concept drift in feature distributions
- Null: Training and test distributions are identical
- Threshold: p > 0.05 for stability

**Shapiro-Wilk Test**
- Purpose: Test residual normality
- Null: Residuals are normally distributed
- Threshold: p > 0.05

**Ljung-Box Test**
- Purpose: Test residual autocorrelation
- Null: No autocorrelation in residuals
- Threshold: p > 0.05

### 3.3 Spatial Autocorrelation

**Moran's I**
- Purpose: Test if model captures spatial patterns
- Expected: I > 0.3 for meaningful spatial structure
- Test: Permutation test with 999 permutations

---

## 4. ABLATION STUDIES

### 4.1 Required Ablations

| Study | Modification | Expected Result | Interpretation |
|-------|-------------|-----------------|----------------|
| A1: No physics loss | alpha_physics = 0 | RMSE increases 20-40% | Physics constraints prevent overfitting |
| A2: No sex structure | Single-sex SEIR | Seroprevalence underestimated by 15% | Male-biased transmission is critical |
| A3: Fixed K(t) | K(t) = K0 constant | R^2 drops to < 0.3 | Climate-driven K(t) is essential |
| A4: No spillover decoder | Predict rodents only | Cannot evaluate human risk | Spillover bridge is necessary |
| A5: Pure LSTM baseline | Replace PINN with LSTM | WIS worse by 15-25% | PINN > black-box for sparse data |
| A6: No climate encoder | Use raw climate features | R^2 drops by 30% | Learned K(t) encoder is critical |
| A7: No synthetic pretraining | Train from random init | Convergence 2x slower | Synthetic data accelerates learning |

### 4.2 Ablation Protocol

See implementation in src/evaluation/ablation.py.

---

## 5. UNCERTAINTY QUANTIFICATION

### 5.1 Method 1: Monte Carlo Dropout

- Dropout rate: p = 0.2
- Forward passes: T = 100
- Prediction: mu = (1/T) sum_t y_hat_t, sigma^2 = (1/T) sum_t (y_hat_t - mu)^2

### 5.2 Method 2: Deep Ensembles

- Train 5 models with different random seeds: [42, 123, 456, 789, 999]
- Aggregate predictions: mixture of Gaussians

### 5.3 Method 3: Conformal Prediction (MAPIE)

- Split conformal on validation set
- Guarantee: 90% coverage regardless of model correctness

---

## 6. CALIBRATION VALIDATION

### 6.1 Reliability Diagram

Generate reliability diagram for probabilistic forecasts.

### 6.2 Expected Calibration Error

**Target:** ECE < 0.05

---

## 7. BASELINE COMPARISONS

### 7.1 Required Baselines

| Baseline | Description | Why Required |
|----------|-------------|--------------|
| SARIMAX | Seasonal ARIMA with exogenous climate variables | Standard epidemiological forecasting |
| XGBoost | Gradient boosting on lagged features | Strong tabular baseline |
| Pure LSTM | LSTM without physics constraints | Tests value of PINN approach |
| MaxEnt | Ecological niche model | Standard for spatial risk mapping |
| Null model | Historical mean prediction | Minimum performance threshold |

---

*End of Report 3*
