"""Tests for model modules."""
import pytest
import torch
from src.models.hanta_pinn import HantaPINN


def test_model_forward():
    """Test forward pass."""
    model = HantaPINN()
    batch_size = 4

    env = torch.randn(batch_size, 24, 4)
    t = torch.rand(batch_size, 1)
    human = torch.randn(batch_size, 5)

    out = model(env, t, human)

    assert 'K' in out
    assert 'states' in out
    assert 'seroprev' in out
    assert 'R0' in out
    assert out['K'].shape == (batch_size, 1)
    assert out['states'].shape == (batch_size, 8)


def test_model_loss():
    """Test loss computation."""
    model = HantaPINN()
    batch_size = 4

    batch = {
        'env': torch.randn(batch_size, 24, 4),
        't': torch.rand(batch_size, 1),
        'human': torch.randn(batch_size, 5),
        'seroprev': torch.rand(batch_size, 1) * 0.2,
        'cases': torch.poisson(torch.rand(batch_size, 1) * 2)
    }

    loss, metrics = model.compute_loss(batch)
    assert loss.item() > 0
    assert 'L_data' in metrics
    assert 'L_physics' in metrics


def test_parameter_count():
    """Test that parameter count is reasonable."""
    model = HantaPINN()
    n_params = model.count_parameters()
    assert 100000 < n_params < 500000
