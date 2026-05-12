"""
Forecast evaluation metrics for hantavirus prediction.
Implements WIS, CRPS, MAE, RMSE, and classification metrics.
"""
import numpy as np
from scipy import stats


def weighted_interval_score(y_true, y_pred_lower, y_pred_upper, alphas):
    """
    Compute Weighted Interval Score (WIS).

    Args:
        y_true: [N] observed values
        y_pred_lower: [N, n_alphas] lower bounds
        y_pred_upper: [N, n_alphas] upper bounds
        alphas: [n_alphas] significance levels

    Returns:
        wis: scalar WIS
    """
    n = len(y_true)
    scores = []

    for i, alpha in enumerate(alphas):
        lower = y_pred_lower[:, i]
        upper = y_pred_upper[:, i]

        interval_width = upper - lower
        under = 2 / alpha * (lower - y_true) * (y_true < lower)
        over = 2 / alpha * (y_true - upper) * (y_true > upper)

        score = interval_width + under + over
        scores.append(alpha / 2 * score)

    return np.mean(np.sum(scores, axis=0))


def continuous_ranked_probability_score(y_true, y_pred_samples):
    """
    Compute CRPS using empirical CDF from samples.

    Args:
        y_true: [N] observed values
        y_pred_samples: [N, n_samples] predicted samples

    Returns:
        crps: [N] CRPS per observation
    """
    n_samples = y_pred_samples.shape[1]
    y_pred_sorted = np.sort(y_pred_samples, axis=1)

    # Empirical CDF
    cdf = np.arange(1, n_samples + 1) / n_samples

    crps = []
    for i in range(len(y_true)):
        # Integral (F(x) - 1(y >= x))^2 dx
        indicator = (y_pred_sorted[i] >= y_true[i]).astype(float)
        integrand = (cdf - indicator) ** 2
        crps.append(np.trapz(integrand, y_pred_sorted[i]))

    return np.array(crps)


def mean_absolute_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def diebold_mariano_test(forecast1, forecast2, actual, loss='mse'):
    """
    Diebold-Mariano test for forecast comparison.

    H0: Both forecasts have equal accuracy
    H1: forecast1 is more accurate than forecast2

    Returns:
        dm_stat: test statistic
        p_value: one-sided p-value
    """
    if loss == 'mse':
        d = (actual - forecast1)**2 - (actual - forecast2)**2
    elif loss == 'mae':
        d = np.abs(actual - forecast1) - np.abs(actual - forecast2)
    elif loss == 'wis':
        d = forecast1 - forecast2  # assuming WIS already computed
    else:
        raise ValueError(f"Unknown loss: {loss}")

    mean_d = np.mean(d)
    var_d = np.var(d, ddof=1) / len(d)
    dm_stat = mean_d / np.sqrt(var_d + 1e-10)
    p_value = 1 - stats.norm.cdf(dm_stat)

    return dm_stat, p_value


def prediction_interval_coverage(y_true, y_lower, y_upper):
    """Compute empirical coverage of prediction intervals."""
    covered = (y_true >= y_lower) & (y_true <= y_upper)
    return np.mean(covered)


def mean_prediction_interval_width(y_lower, y_upper):
    """Compute mean width of prediction intervals."""
    return np.mean(y_upper - y_lower)


def calibration_slope(y_true, y_prob, n_bins=10):
    """
    Compute calibration slope via binning.

    Args:
        y_true: [N] binary outcomes
        y_prob: [N] predicted probabilities

    Returns:
        slope: calibration slope (ideal = 1.0)
    """
    bin_edges = np.linspace(0, 1, n_bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    observed = []
    predicted = []

    for i in range(n_bins):
        mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i+1])
        if mask.sum() > 0:
            observed.append(y_true[mask].mean())
            predicted.append(y_prob[mask].mean())

    if len(observed) < 2:
        return np.nan

    # Linear regression
    observed = np.array(observed)
    predicted = np.array(predicted)

    # Slope via covariance
    cov = np.cov(predicted, observed)[0, 1]
    var = np.var(predicted)
    slope = cov / (var + 1e-10)

    return slope
