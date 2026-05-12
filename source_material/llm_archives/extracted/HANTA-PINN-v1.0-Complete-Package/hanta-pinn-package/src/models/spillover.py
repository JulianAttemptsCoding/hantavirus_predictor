"""Spillover Decoder: Maps rodent reservoir dynamics to human case risk."""
import torch
import torch.nn as nn


class SpilloverDecoder(nn.Module):
    """
    Decodes rodent infectious prevalence into human spillover risk.

    Input: [rodent_states (8), human_features (5)]
    Output: [batch, 1] lambda_H(t) > 0
    """

    def __init__(self, input_dim: int = 8 + 5, hidden_dim: int = 32, dropout: float = 0.2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, rodent_states: torch.Tensor, human_features: torch.Tensor) -> torch.Tensor:
        """
        Args:
            rodent_states: [batch, 8] from PINN core
            human_features: [batch, 5] = [SVI, housing_age, rural_frac, season_sin, season_cos]

        Returns:
            lambda_H: [batch, 1] force of infection
        """
        # Infectious prevalence
        I_total = rodent_states[:, 2:3] + rodent_states[:, 6:7]  # I_m + I_f
        N_total = rodent_states.sum(dim=1, keepdim=True)
        prev = I_total / (N_total + 1e-6)  # [B, 1]

        x = torch.cat([prev, human_features], dim=-1)  # [B, 9]
        log_lambda = self.net(x)
        return torch.exp(log_lambda)  # Ensure lambda > 0

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
