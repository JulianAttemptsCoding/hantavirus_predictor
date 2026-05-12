import numpy as np
import pytest

from hantavirus_predictor.metrics import (
    interval_coverage,
    interval_score,
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

