import pytest
import torch
import numpy as np

from src.models.hantast_pinn_fm import (
    ClimateEncoder, SEIRPhysicsLayer, FoundationPrior,
    SpatiotemporalGAT, HantaSTPINNFM
)


class TestClimateEncoder:
    def test_forward(self):
        model = ClimateEncoder(in_channels=4, hidden_dim=64, num_layers=2, temporal_len=12)
        x = torch.randn(2, 4, 12, 64, 64)

        K_t, beta_t = model(x)

        assert K_t.shape == (2, 12)
        assert beta_t.shape == (2, 12, 2)
        assert torch.all(K_t > 0)
        assert torch.all(beta_t > 0)


class TestSEIRPhysicsLayer:
    def test_forward(self):
        climate_enc = ClimateEncoder(in_channels=4, hidden_dim=64, num_layers=2, temporal_len=12)
        model = SEIRPhysicsLayer(climate_enc)

        climate = torch.randn(2, 4, 12, 64, 64)
        t_span = torch.linspace(0, 100, 101)
        y0 = torch.tensor([[450, 0, 50, 0, 450, 0, 50, 0],
                           [450, 0, 50, 0, 450, 0, 50, 0]], dtype=torch.float32)

        solution = model(climate, t_span, y0)

        assert solution.shape == (101, 2, 8)
        assert torch.all(solution >= 0)

    def test_R0_computation(self):
        climate_enc = ClimateEncoder(in_channels=4, hidden_dim=64, num_layers=2, temporal_len=12)
        model = SEIRPhysicsLayer(climate_enc)

        K_t = torch.tensor([[1000.0], [500.0]])
        beta_t = torch.tensor([[[0.1, 0.03]], [[0.05, 0.015]]])

        R0 = model.compute_R0(K_t, beta_t)

        assert R0.shape == (2, 1)
        assert torch.all(R0 > 0)
        assert R0[0] > R0[1]  # Higher K -> higher R0


class TestSpatiotemporalGAT:
    def test_forward(self):
        from torch_geometric.data import Data

        model = SpatiotemporalGAT(node_dim=64, hidden_dim=64, n_heads=4, forecast_horizon=6)

        x = torch.randn(5, 12, 64)  # 5 nodes, 12 timesteps, 64 features
        edge_index = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 4]], dtype=torch.long)
        edge_attr = torch.ones(4)

        mu, phi, risk_logits = model(x, edge_index, edge_attr)

        assert mu.shape == (5, 6)
        assert phi.shape == (5, 6)
        assert risk_logits.shape == (5, 4)
        assert torch.all(mu > 0)
        assert torch.all(phi > 0)


class TestHantaSTPINNFM:
    def test_end_to_end(self):
        config = {
            "climate_encoder": {"in_channels": 4, "hidden_dim": 32, "num_layers": 2, "temporal_len": 6},
            "pinn": {"depth": 3, "width": 32},
            "foundation": {"model_name": "google/timesfm-2.5-500m", "lora_rank": 4},
            "stgat": {"node_dim": 32, "hidden_dim": 32, "n_heads": 2, "forecast_horizon": 3}
        }

        # Skip if TimesFM not available
        try:
            model = HantaSTPINNFM(config)
        except Exception:
            pytest.skip("TimesFM not available")

        climate = torch.randn(1, 4, 6, 32, 32)
        cases = torch.randn(1, 12)

        from torch_geometric.data import Data
        graph_data = Data(
            x=torch.randn(1, 1, 32),
            edge_index=torch.zeros(2, 0, dtype=torch.long),
            edge_attr=None
        )

        t_span = torch.linspace(0, 50, 51)
        y0 = torch.tensor([[450, 0, 50, 0, 450, 0, 50, 0]], dtype=torch.float32)

        outputs = model(climate, cases, graph_data, t_span, y0)

        assert "forecast_mu" in outputs
        assert "R0" in outputs
        assert outputs["forecast_mu"].shape[1] == 3
