"""Tests for physics module."""
import pytest
import numpy as np
from src.physics.seir_rhs import hantavirus_seir, generate_synthetic_trajectory


def test_seir_conservation():
    """Test that total population is conserved (births = deaths at equilibrium)."""
    params = {
        'beta_m': 0.02, 'beta_mf': 0.01, 'beta_f': 0.005,
        'gamma_m': 1/30, 'gamma_f': 1/25,
        'delta': 1/14, 'a': 0.001, 'c': 1e-4,
        'b': 0.01, 'K': 1000
    }
    y0 = [450, 0, 50, 0, 450, 0, 50, 0]
    dy = hantavirus_seir(0, y0, params)

    # At equilibrium-ish, total change should be small
    total_change = sum(dy)
    assert abs(total_change) < 10  # Loose bound for initial transient


def test_synthetic_generation():
    """Test synthetic trajectory generation."""
    traj = generate_synthetic_trajectory(K=1000, t_max=365)
    assert traj['states'].shape[1] == 8
    assert len(traj['t']) == len(traj['states'])
    assert np.all(traj['states'] >= 0)


def test_seroprev_range():
    """Test that seroprevalence is in [0, 1]."""
    traj = generate_synthetic_trajectory(K=1000, t_max=365)
    assert np.all(traj['seroprev'] >= 0)
    assert np.all(traj['seroprev'] <= 1)
