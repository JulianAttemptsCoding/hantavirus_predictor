"""
Transformer-based temporal encoder for time-series features.
"""
import torch
import torch.nn as nn
from .climate_encoder import SinusoidalPositionalEncoding


class TemporalEncoder(nn.Module):
    """
    Transformer encoder for multivariate time series.

    Input: [B, T, input_dim]
    Output: [B, d_model] temporal embedding
    """
    def __init__(self, input_dim=4, d_model=256, nhead=8, 
                 num_layers=4, dropout=0.2):
        super().__init__()

        self.input_proj = nn.Linear(input_dim, d_model)
        self.pos_encoding = SinusoidalPositionalEncoding(d_model, max_len=500)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=1024,
            dropout=dropout,
            batch_first=True,
            activation='gelu'
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, 
                                                 num_layers=num_layers)
        self.output_proj = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        """
        Args:
            x: [B, T, input_dim] time series
            mask: [B, T] optional padding mask
        Returns:
            emb: [B, d_model] temporal embedding
        """
        x = self.input_proj(x)
        x = self.pos_encoding(x)
        x = self.transformer(x, src_key_padding_mask=mask)
        return self.output_proj(x[:, -1, :])  # Last timestep
