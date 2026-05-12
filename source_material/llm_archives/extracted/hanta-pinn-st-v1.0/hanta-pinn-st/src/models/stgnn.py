"""
Spatiotemporal Graph Neural Network for cross-regional hantavirus spread.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv


class STGNN(nn.Module):
    """
    Spatiotemporal Graph Attention Network.

    Combines GATv2 for spatial diffusion with 1D conv for temporal dynamics.
    """
    def __init__(self, node_dim=256, hidden_dim=64, n_heads=4, n_layers=3):
        super().__init__()

        self.gat_layers = nn.ModuleList()
        for i in range(n_layers):
            in_dim = node_dim if i == 0 else hidden_dim * n_heads
            self.gat_layers.append(
                GATv2Conv(in_dim, hidden_dim, heads=n_heads, 
                         concat=True, dropout=0.2)
            )

        self.temporal_conv = nn.Conv1d(
            hidden_dim * n_heads, hidden_dim,
            kernel_size=3, padding=1, dilation=1
        )

        # Output: negative binomial parameters [mu, log_phi]
        self.output = nn.Linear(hidden_dim, 2)

    def forward(self, x, edge_index, edge_attr=None, temporal_seq=None):
        """
        Args:
            x: [N, node_dim] node features
            edge_index: [2, E] graph edges
            edge_attr: [E, F] optional edge features
            temporal_seq: [N, T, F] temporal sequences per node
        Returns:
            out: [N, 2] [mu, log_phi]
        """
        # Spatial message passing
        for gat in self.gat_layers:
            x = F.elu(gat(x, edge_index, edge_attr))

        # Temporal convolution
        if temporal_seq is not None:
            x_temp = self.temporal_conv(
                temporal_seq.permute(0, 2, 1)
            ).permute(0, 2, 1)
            x = x + x_temp[:, -1, :]  # Residual

        return self.output(x)


class HantaPINNST(nn.Module):
    """
    Full HANTA-PINN-ST model integrating all components.
    """
    def __init__(self, 
                 climate_in_channels=5,
                 temporal_input_dim=4,
                 env_dim=256,
                 node_dim=256,
                 n_compartments=8):
        super().__init__()

        from .climate_encoder import ClimateEncoder
        from .temporal_encoder import TemporalEncoder
        from .pinn_core import PINNCore

        self.climate_encoder = ClimateEncoder(climate_in_channels, 128)
        self.temporal_encoder = TemporalEncoder(temporal_input_dim, 256)
        self.pinn_core = PINNCore(env_dim, 128, n_compartments)
        self.stgnn = STGNN(node_dim, 64, 4, 3)

        # Fusion layer
        self.fusion = nn.Sequential(
            nn.Linear(128 + 256, 256),
            nn.ReLU(),
            nn.Dropout(0.2)
        )

    def forward(self, climate_rasters, temporal_seq, 
                graph_x, edge_index, edge_attr=None, 
                t=None, state_0=None):
        """
        Full forward pass.

        Args:
            climate_rasters: [B, C, T, H, W]
            temporal_seq: [B, T, F]
            graph_x: [N, node_dim]
            edge_index: [2, E]
            t: [T] time points for ODE
            state_0: [B, 8] initial SEIR state
        """
        # Encode modalities
        climate_emb = self.climate_encoder(climate_rasters)
        temporal_emb = self.temporal_encoder(temporal_seq)

        # Fuse
        fused = self.fusion(torch.cat([climate_emb, temporal_emb], dim=-1))

        # PINN physics core
        if t is not None and state_0 is not None:
            trajectory, params = self.pinn_core(t, fused, state_0)
        else:
            trajectory, params = None, None

        # Spatiotemporal graph prediction
        stg_out = self.stgnn(graph_x, edge_index, edge_attr)

        return {
            'climate_emb': climate_emb,
            'temporal_emb': temporal_emb,
            'fused_emb': fused,
            'trajectory': trajectory,
            'params': params,
            'stg_out': stg_out
        }
