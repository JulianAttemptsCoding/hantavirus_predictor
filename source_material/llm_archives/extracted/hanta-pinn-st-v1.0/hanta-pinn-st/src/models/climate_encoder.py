"""
3D CNN Climate Encoder for satellite/raster data.
Processes MODIS NDVI/LST + ERA5 climate stacks.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class ClimateEncoder(nn.Module):
    """
    3D CNN encoder for spatiotemporal climate rasters.

    Input: [B, C=5, T=24, H=64, W=64]
    Output: [B, 128] embedding
    """
    def __init__(self, in_channels=5, output_dim=128):
        super().__init__()

        self.conv1 = nn.Conv3d(in_channels, 32, kernel_size=(3, 3, 3), padding=1)
        self.bn1 = nn.BatchNorm3d(32)
        self.pool1 = nn.MaxPool3d((2, 2, 2))

        self.conv2 = nn.Conv3d(32, 64, kernel_size=(3, 3, 3), padding=1)
        self.bn2 = nn.BatchNorm3d(64)
        self.pool2 = nn.MaxPool3d((2, 2, 2))

        self.conv3 = nn.Conv3d(64, 128, kernel_size=(3, 3, 3), padding=1)
        self.bn3 = nn.BatchNorm3d(128)
        self.adaptive_pool = nn.AdaptiveAvgPool3d((1, 1, 1))

        self.fc = nn.Linear(128, output_dim)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        """
        Args:
            x: [B, C, T, H, W] climate raster stack
        Returns:
            emb: [B, output_dim] climate embedding
        """
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = self.adaptive_pool(F.relu(self.bn3(self.conv3(x))))
        x = x.view(x.size(0), -1)
        return self.dropout(self.fc(x))


class SinusoidalPositionalEncoding(nn.Module):
    """Sinusoidal positional encoding for temporal sequences."""
    def __init__(self, d_model, max_len=500):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                            (-torch.log(torch.tensor(10000.0)) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:x.size(1), :]
