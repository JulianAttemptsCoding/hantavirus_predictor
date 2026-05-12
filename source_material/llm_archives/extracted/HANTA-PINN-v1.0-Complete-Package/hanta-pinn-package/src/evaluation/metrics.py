"""Evaluation metrics for HANTA-PINN."""
import numpy as np
from scipy import stats
from typing import Dict, Tuple


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.sqrt(np.mean((y_pred - y_true) ** 2))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean(np.abs(y_pred - y_true))


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / (ss_tot + 1e-8)


def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean(np.abs((y_pred - y_true) / (y_true + 1e-8))) * 100


def weighted_interval_score(y_true: np.ndarray, y_lower: np.ndarray, 
                            y_upper: np.ndarray, alpha: float = 0.1) -> float:
    """
    Compute WIS for prediction intervals.

    Args:
        y_true: observed values
        y_lower: lower bound of prediction interval
        y_upper: upper bound of prediction interval
        alpha: miscoverage rate (0.1 for 90% PI)
    """
    under = (y_lower > y_true).astype(float)
    over = (y_upper < y_true).astype(float)

    wis = (y_upper - y_lower) +           (2 / alpha) * (y_lower - y_true) * under +           (2 / alpha) * (y_true - y_upper) * over

    return np.mean(wis)


def crps(y_true: np.ndarray, y_pred_samples: np.ndarray) -> float:
    """
    Compute CRPS from samples.

    Args:
        y_true: [n] observed values
        y_pred_samples: [n, m] samples from predictive distribution
    """
    n, m = y_pred_samples.shape
    crps_values = []

    for i in range(n):
        samples = y_pred_samples[i]
        # Empirical CDF
        sorted_samples = np.sort(samples)
        # CRPS integral
        crps_val = np.mean(np.abs(sorted_samples - y_true[i])) -                    0.5 * np.mean(np.abs(sorted_samples[:, None] - sorted_samples[None, :]))
        crps_values.append(crps_val)

    return np.mean(crps_values)


def expected_calibration_error(y_true: np.ndarray, y_pred_mean: np.ndarray,
                                y_pred_std: np.ndarray, n_bins: int = 10) -> float:
    """Compute Expected Calibration Error."""
    z_scores = (y_true - y_pred_mean) / (y_pred_std + 1e-6)

    bin_edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        mask = (np.abs(z_scores) <= bin_edges[i+1]) & (np.abs(z_scores) > bin_edges[i])
        if mask.sum() > 0:
            observed = np.mean(np.abs(z_scores[mask]) <= 1.96)
            predicted = bin_edges[i+1]
            ece += np.abs(observed - predicted) * (mask.sum() / len(z_scores))

    return ece


def diebold_mariano_test(forecasts1: np.ndarray, forecasts2: np.ndarray,
                         actuals: np.ndarray, loss='squared') -> Tuple[float, float]:
    """
    Diebold-Mariano test for forecast comparison.

    Returns:
        dm_stat: DM test statistic
        p_value: p-value
    """
    if loss == 'squared':
        d = (actuals - forecasts1) ** 2 - (actuals - forecasts2) ** 2
    elif loss == 'absolute':
        d = np.abs(actuals - forecasts1) - np.abs(actuals - forecasts2)
    else:
        raise ValueError(f"Unknown loss: {loss}")

    mean_d = np.mean(d)
    var_d = np.var(d, ddof=1) / len(d)
    dm_stat = mean_d / np.sqrt(var_d)
    p_value = 2 * (1 - stats.norm.cdf(np.abs(dm_stat)))

    return dm_stat, p_value


def compute_all_metrics(y_true: np.ndarray, y_pred: np.ndarray,
                        y_lower: np.ndarray = None, y_upper: np.ndarray = None) -> Dict:
    """Compute all evaluation metrics."""
    metrics = {
        'rmse': rmse(y_true, y_pred),
        'mae': mae(y_true, y_pred),
        'r2': r2_score(y_true, y_pred),
        'mape': mape(y_true, y_pred)
    }

    if y_lower is not None and y_upper is not None:
        metrics['wis'] = weighted_interval_score(y_true, y_lower, y_upper)
        metrics['coverage'] = np.mean((y_true >= y_lower) & (y_true <= y_upper))

    return metrics
