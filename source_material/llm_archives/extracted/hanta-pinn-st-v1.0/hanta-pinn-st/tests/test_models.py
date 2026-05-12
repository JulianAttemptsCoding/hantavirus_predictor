"""
Architecture and shape tests for HANTA-PINN-ST components.
"""
import pytest
import torch
import sys
sys.path.insert(0, 'src')

from models.climate_encoder import ClimateEncoder
from models.temporal_encoder import TemporalEncoder
from models.stgnn import STGNN


class TestClimateEncoder:
    def test_output_shape(self):
        encoder = ClimateEncoder(in_channels=5, output_dim=128)
        x = torch.randn(4, 5, 24, 64, 64)
        out = encoder(x)
        assert out.shape == (4, 128), f"Expected (4, 128), got {out.shape}"

    def test_batch_independence(self):
        encoder = ClimateEncoder(in_channels=5, output_dim=128)
        x1 = torch.randn(1, 5, 24, 64, 64)
        x2 = torch.randn(1, 5, 24, 64, 64)

        out1 = encoder(x1)
        out2 = encoder(x2)

        # Different inputs should give different outputs
        assert not torch.allclose(out1, out2)

    def test_dropout_active_in_train(self):
        encoder = ClimateEncoder(in_channels=5, output_dim=128)
        encoder.train()
        x = torch.randn(2, 5, 24, 64, 64)

        out1 = encoder(x)
        out2 = encoder(x)

        # With dropout, same input should give different outputs in train mode
        assert not torch.allclose(out1, out2, atol=1e-5)


class TestTemporalEncoder:
    def test_output_shape(self):
        encoder = TemporalEncoder(input_dim=4, d_model=256)
        x = torch.randn(4, 52, 4)  # [B, T, F]
        out = encoder(x)
        assert out.shape == (4, 256), f"Expected (4, 256), got {out.shape}"

    def test_masking(self):
        encoder = TemporalEncoder(input_dim=4, d_model=256)
        x = torch.randn(2, 52, 4)
        mask = torch.ones(2, 52, dtype=torch.bool)
        mask[:, 40:] = False  # Mask last 12 timesteps

        out = encoder(x, mask=mask)
        assert out.shape == (2, 256)


class TestSTGNN:
    def test_output_shape(self):
        model = STGNN(node_dim=256, hidden_dim=64, n_heads=4, n_layers=3)
        x = torch.randn(10, 256)
        edge_index = torch.randint(0, 10, (2, 20))
        temporal_seq = torch.randn(10, 12, 4)

        out = model(x, edge_index, temporal_seq=temporal_seq)
        assert out.shape == (10, 2), f"Expected (10, 2), got {out.shape}"

    def test_positive_nb_parameters(self):
        model = STGNN(node_dim=256, hidden_dim=64)
        x = torch.randn(10, 256)
        edge_index = torch.randint(0, 10, (2, 20))
        temporal_seq = torch.randn(10, 12, 4)

        out = model(x, edge_index, temporal_seq=temporal_seq)
        mu, log_phi = out[:, 0], out[:, 1]

        assert torch.all(mu > 0), "Negative mu predicted"
        assert torch.all(torch.exp(log_phi) > 0), "Negative phi predicted"

    def test_gradient_flow(self):
        model = STGNN(node_dim=256, hidden_dim=64)
        x = torch.randn(10, 256, requires_grad=True)
        edge_index = torch.randint(0, 10, (2, 20))
        temporal_seq = torch.randn(10, 12, 4)

        out = model(x, edge_index, temporal_seq=temporal_seq)
        loss = out.sum()
        loss.backward()

        assert x.grad is not None, "No gradient flow to input"
        assert not torch.all(x.grad == 0), "Zero gradients"
