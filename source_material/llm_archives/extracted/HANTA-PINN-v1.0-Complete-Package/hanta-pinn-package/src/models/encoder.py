"""Environmental Encoder: Learns carrying capacity K(t) from climate/NDVI time series."""
import torch
import torch.nn as nn
import torch.nn.functional as F


class EnvironmentalEncoder(nn.Module):
    """
    Encodes environmental time series into carrying capacity K(t).

    Architecture:
        1D-CNN (3 layers, 32/64/128 filters) -> LSTM (64 hidden) -> FC -> Softplus

    Input: [batch, seq_len=24, channels=4] where channels = [NDVI, precip, temp, ENSO]
    Output: [batch, 1] where K(t) > 0
    """

    def __init__(self, input_channels: int = 4, seq_len: int = 24, hidden_dim: int = 64):
        super().__init__()
        self.input_channels = input_channels
        self.seq_len = seq_len
        self.hidden_dim = hidden_dim

        # 1D CNN for local feature extraction
        self.cnn = nn.Sequential(
            nn.Conv1d(input_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Conv1d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )

        # LSTM for temporal dependencies
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=hidden_dim,
            num_layers=1,
            batch_first=True
        )

        # Output: K(t) with biological constraint K > 0
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(32, 1),
            nn.Softplus()  # Enforce positivity
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: [batch, seq_len, input_channels]

        Returns:
            K: [batch, 1] carrying capacity
        """
        # x: [B, T, C] -> [B, C, T] for Conv1d
        x = x.permute(0, 2, 1)
        x = self.cnn(x).squeeze(-1)  # [B, 128]
        x = x.unsqueeze(1)  # [B, 1, 128] for LSTM
        _, (h_n, _) = self.lstm(x)
        K = self.fc(h_n[-1])  # [B, 1]
        return K

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
