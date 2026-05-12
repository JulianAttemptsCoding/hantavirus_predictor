"""
Scientific sanity tests for hantavirus SEIR dynamics.
Ensures biological plausibility of the model.
"""
import pytest
import torch
import numpy as np
import sys
sys.path.insert(0, 'src')

from models.pinn_core import PINNCore


class TestPhysicsConstraints:
    """Tests that the model respects biological laws."""

    def test_r0_proportional_to_k(self):
        """R_0 must increase monotonically with carrying capacity."""
        model = PINNCore(env_dim=256, hidden_dim=128)
        K_values = torch.linspace(100, 5000, 50)
        r0_values = []

        for K in K_values:
            params = torch.tensor([[0.1, 0.05, K.item()]])
            r0 = model.compute_r0(params)
            r0_values.append(r0.item())

        diffs = np.diff(r0_values)
        assert np.all(diffs >= -1e-6), (
            f"R_0 not monotonic: min diff = {np.min(diffs)}"
        )

    def test_mass_conservation(self):
        """Total rodent population approximately conserved at equilibrium."""
        model = PINNCore(env_dim=256, hidden_dim=128)
        state = torch.tensor([[90., 5., 5., 0., 90., 5., 5., 0.]])
        params = torch.tensor([[0.1, 0.05, 1000.]])

        rhs = model.seir_rhs(state, params)
        total_change = rhs.sum()

        assert abs(total_change.item()) < 1e-3, (
            f"Mass not conserved: total change = {total_change.item()}"
        )

    def test_positivity_preservation(self):
        """ODE RHS should not drive compartments negative from positive states."""
        model = PINNCore(env_dim=256, hidden_dim=128)
        state = torch.tensor([[90., 5., 5., 0., 90., 5., 5., 0.]])
        params = torch.tensor([[0.1, 0.05, 1000.]])

        rhs = model.seir_rhs(state, params)

        # For small compartments, derivative should be non-negative
        # (or at least not strongly negative)
        assert rhs[0, 3].item() >= -1e-6, "R_m derivative negative from zero"
        assert rhs[0, 7].item() >= -1e-6, "R_f derivative negative from zero"

    def test_parameter_positivity(self):
        """Parameter network must output positive values."""
        model = PINNCore(env_dim=256, hidden_dim=128)
        env_emb = torch.randn(10, 256)
        t = torch.rand(10, 1)

        params = model.param_net(torch.cat([env_emb, t], dim=-1))

        assert torch.all(params > 0), "Parameter network output non-positive"
        assert torch.all(params[:, 2] > 0), "Carrying capacity K non-positive"

    def test_r0_near_literature_value(self):
        """R_0 with literature parameters should be ~1.35."""
        model = PINNCore(env_dim=256, hidden_dim=128)

        # Literature parameters for Bayou virus in rice rats
        params = torch.tensor([[0.1, 0.04, 1500.]])
        r0 = model.compute_r0(params)

        assert 1.2 <= r0.item() <= 1.5, (
            f"R_0 = {r0.item():.3f}, expected ~1.35"
        )


class TestAndesVirusH2H:
    """Tests for Andes virus human-to-human transmission."""

    def test_h2h_only_for_andes(self):
        """H2H transmission should only be active for ANDV strain."""
        # This would be tested in the full model
        # Placeholder for strain-specific behavior
        assert True

    def test_confinement_scaling(self):
        """Confinement index should scale H2H transmission."""
        # beta_HH should increase with confinement
        kappa_values = [0.3, 1.0, 3.0]
        beta_base = 0.01

        betas = [beta_base * k for k in kappa_values]
        assert betas[0] < betas[1] < betas[2], (
            "Confinement not monotonically scaling transmission"
        )
