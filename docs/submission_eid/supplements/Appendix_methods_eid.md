# Appendix: Statistical Methods

## Incidence and Count Scale

For country i and year t, reported incidence per 100,000 population was computed as:

```text
incidence_per_100k_it = cases_it / population_it * 100,000
```

For rate-based forecasts, the predicted count mean was:

```text
mu_it = predicted_rate_per_100k_it / 100,000 * population_it
```

All weighted interval score, coverage, interval-width, mean absolute error, and
Brier-score calculations were performed on reported annual case counts, not on
incidence rates.

## Forecast Baselines

Last-observed country-rate baseline:

```text
r_hat_it = incidence_i,t-1
mu_hat_it = r_hat_it / 100,000 * population_it
Y_it ~ Poisson(mu_hat_it)
```

Country historical mean-rate baseline:

```text
r_hat_it = mean(incidence_i,s for all s < t)
mu_hat_it = r_hat_it / 100,000 * population_it
Y_it ~ Poisson(mu_hat_it)
```

Empirical negative-binomial baseline:

```text
alpha_nb = max((var(y_train) - mean(y_train)) / mean(y_train)^2, 1e-6)
size = 1 / alpha_nb
prob = size / (size + mu_hat_it)
Y_it ~ NegBin(size, prob)
```

Hierarchical negative-binomial baseline:

```text
r_country = country historical mean rate
r_region = region historical mean rate
n_i = number of prior country observations
lambda_i = n_i / (n_i + k)
r_hat_it = lambda_i * r_country + (1 - lambda_i) * r_region
mu_hat_it = r_hat_it / 100,000 * population_it
```

The shrinkage constant k was selected on 2022 validation-year weighted interval
score. Negative-binomial baselines were treated as conservative uncertainty
references, not as biological transmission models.

## Penalized Poisson Count Model

The exploratory count model used a log population offset:

```text
log(mu_it) = log(population_it / 100,000) + beta_0 + X_it beta
```

The ridge objective, up to constants, was:

```text
min_beta sum_i [mu_i - y_i * eta_i] + 0.5 * alpha * sum_j beta_j^2
```

where:

```text
eta_i = offset_i + beta_0 + X_i beta
mu_i = exp(eta_i)
```

The penalty applied to non-intercept coefficients only. The penalty parameter
alpha was selected on 2022 validation WIS from {0.01, 0.1, 1, 10}. Coefficients
were not interpreted causally.

## Weighted Interval Score

For observed count y, lower interval bound l, upper interval bound u, median m,
and miscoverage alpha = 0.10:

```text
IS_alpha = (u - l)
         + (2 / alpha) * (l - y) * 1(y < l)
         + (2 / alpha) * (y - u) * 1(y > u)

WIS = [0.5 * abs(y - m) + (alpha / 2) * IS_alpha] / 1.5
```

Coverage and sharpness metrics were:

```text
coverage_90 = mean(q05 <= observed <= q95)
interval_width = mean(q95 - q05)
MAE = mean(abs(observed - q50))
Brier = mean((P(Y > 0) - 1(observed > 0))^2)
```

Models were not ranked by WIS alone; WIS, coverage, and interval width were read
together.

## Promotion Rule

A covariate-augmented model was promoted only if all conditions held:

```text
1. WIS_2023 <= 0.95 * WIS_best_simple_baseline_2023
   OR WIS was comparable and coverage was closer to 0.90.
2. coverage_90_2023 was not lower than the best simple baseline by >0.05.
3. Interval width was interpretable and not merely inflated.
4. Tuning used no 2023 outcome information.
5. No causal coefficient interpretation was made.
```

No covariate-rich model passed this promotion rule.
