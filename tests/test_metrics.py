import numpy as np
import pytest

from hantavirus_predictor.metrics import (
    brier_score,
    interval_coverage,
    interval_score,
    poisson_deviance,
    weighted_interval_score,
)


def test_interval_score_inside_interval_is_width():
    score = interval_score([5], [3], [7], alpha=0.2)
    assert score.tolist() == [4.0]


def test_interval_score_penalizes_misses():
    score = interval_score([10], [3], [7], alpha=0.2)
    assert score.tolist() == [34.0]


def test_interval_score_rejects_bad_alpha():
    with pytest.raises(ValueError):
        interval_score([1], [0], [2], alpha=1.0)


def test_weighted_interval_score_reduces_to_absolute_error_without_intervals():
    wis = weighted_interval_score([1, 4], [2, 2], [], [], [])
    np.testing.assert_allclose(wis, [1, 2])


def test_interval_coverage():
    coverage = interval_coverage([1, 2, 5], [0, 2, 6], [2, 3, 8])
    assert coverage == pytest.approx(2 / 3)


def test_brier_score():
    score = brier_score([0, 1], [0.25, 0.75])
    assert score == pytest.approx(0.0625)


def test_poisson_deviance_is_zero_for_perfect_mean():
    deviance = poisson_deviance([0, 3], [1e-9, 3])
    np.testing.assert_allclose(deviance, [2e-9, 0], rtol=1e-5, atol=1e-12)
