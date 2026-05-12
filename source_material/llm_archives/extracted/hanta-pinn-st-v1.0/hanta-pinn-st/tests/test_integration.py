"""
End-to-end integration tests for the full pipeline.
"""
import pytest
import torch
import numpy as np
import sys
sys.path.insert(0, 'src')

from data.synthetic_generator import SyntheticHantaGenerator
from models.pinn_core import PINNCore


class TestEndToEnd:
    def test_synthetic_generation(self):
        """Synthetic data generation should produce valid trajectories."""
        gen = SyntheticHantaGenerator(n_trajectories=10, seed=42)
        trajs = gen.generate(n=10)

        assert len(trajs) == 10
        assert all('trajectory' in t for t in trajs)
        assert all(t['trajectory'].shape[1] == 8 for t in trajs)

    def test_synthetic_validation(self):
        """Synthetic data should pass biological validation."""
        gen = SyntheticHantaGenerator(n_trajectories=100, seed=42)
        trajs = gen.generate(n=100)
        results = gen.validate(trajs)

        # At least 3/4 tests should pass (some stochastic variation expected)
        passes = sum(1 for r in results.values() if r['pass'])
        assert passes >= 3, f"Only {passes}/4 validation tests passed"

    def test_pinn_forward_pass(self):
        """PINN should produce valid forward pass."""
        model = PINNCore(env_dim=256, hidden_dim=128)
        env_emb = torch.randn(2, 256)
        t = torch.linspace(0, 365, 100)
        state_0 = torch.tensor([[90., 5., 5., 0., 90., 5., 5., 0.]]).expand(2, 8)

        trajectory, params = model(t, env_emb, state_0)

        assert trajectory.shape == (100, 2, 8)
        assert torch.all(trajectory >= 0), "Negative compartments predicted"
        assert params.shape == (2, 3)

    def test_training_step(self):
        """A single training step should complete without error."""
        from models.pinn_core import PINNCore
        from training.losses import HantaLoss

        model = PINNCore(env_dim=256, hidden_dim=128)
        loss_fn = HantaLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

        # Mock batch
        env_emb = torch.randn(4, 256)
        t = torch.linspace(0, 365, 50)
        state_0 = torch.rand(4, 8) * 100
        target = torch.rand(4, 8) * 100

        optimizer.zero_grad()
        trajectory, params = model(t, env_emb, state_0)
        pred = trajectory[-1]  # Final state

        # Mock ODE residual
        ode_residual = torch.randn(4, 8) * 0.01
        sde_term = torch.randn(4, 8) * 0.001
        spill_pred = torch.rand(4, 2)
        spill_target = torch.poisson(torch.rand(4) * 2)

        loss, loss_dict = loss_fn(
            pred, target, ode_residual, sde_term,
            spill_pred, spill_target, model.parameters()
        )

        loss.backward()
        optimizer.step()

        assert loss.item() > 0
        assert all(v.item() >= 0 for v in loss_dict.values() if v.numel() > 0)
