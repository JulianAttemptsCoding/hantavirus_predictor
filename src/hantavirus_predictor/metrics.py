"""Forecast metrics for interval and quantile predictions."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def _as_float_array(values: ArrayLike) -> np.ndarray:
    return np.asarray(values, dtype=float)


def interval_score(y_true: ArrayLike, lower: ArrayLike, upper: ArrayLike, alpha: float) -> np.ndarray:
    """Return interval score for a central ``1 - alpha`` prediction interval."""
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    y = _as_float_array(y_true)
    lo = _as_float_array(lower)
    hi = _as_float_array(upper)
    if np.any(hi < lo):
        raise ValueError("upper interval bound must be greater than or equal to lower bound")

    width = hi - lo
    below = (2.0 / alpha) * (lo - y) * (y < lo)
    above = (2.0 / alpha) * (y - hi) * (y > hi)
    return width + below + above


def interval_coverage(y_true: ArrayLike, lower: ArrayLike, upper: ArrayLike) -> float:
    """Return empirical coverage for interval predictions."""
    y = _as_float_array(y_true)
    lo = _as_float_array(lower)
    hi = _as_float_array(upper)
    return float(np.mean((lo <= y) & (y <= hi)))


def weighted_interval_score(
    y_true: ArrayLike,
    median: ArrayLike,
    lower_bounds: list[ArrayLike],
    upper_bounds: list[ArrayLike],
    alphas: list[float],
) -> np.ndarray:
    """Return WIS per observation.

    Uses the Bracher et al. epidemic-forecast convention: median absolute error
    weight 0.5 and interval weights alpha / 2.
    """
    if not (len(lower_bounds) == len(upper_bounds) == len(alphas)):
        raise ValueError("lower_bounds, upper_bounds, and alphas must have equal length")
    if len(alphas) == 0:
        return np.abs(_as_float_array(y_true) - _as_float_array(median))

    y = _as_float_array(y_true)
    wis = 0.5 * np.abs(y - _as_float_array(median))
    for lo, hi, alpha in zip(lower_bounds, upper_bounds, alphas):
        wis = wis + (alpha / 2.0) * interval_score(y, lo, hi, alpha)
    return wis / (len(alphas) + 0.5)

