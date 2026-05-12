"""PINN Core: Solves sex-structured SEIR ODEs with learned parameters."""
import torch
import torch.nn as nn
import torch.nn.functional as F


class PINNCore(nn.Module):
    """
    Physics-Informed Neural Network core for hantavirus SEIR dynamics.

    Learns time-varying transmission parameters while enforcing ODE constraints.

    Input: [t_normalized, K(t)]
    Output: [S_m, E_m, I_m, R_m, S_f, E_f, I_f, R_f], beta_m, beta_mf, beta_f, gamma
    """

    def __init__(self, hidden_dim: int = 128, n_layers: int = 5, dropout: float = 0.1):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        # MLP backbone
        layers = []
        in_dim = 2  # [t, K]
        for i in range(n_layers):
            layers.extend([
                nn.Linear(in_dim, hidden_dim),
                nn.Tanh(),
                nn.Dropout(dropout)
            ])
            in_dim = hidden_dim
        self.net = nn.Sequential(*layers)

        # Output heads
        self.state_head = nn.Linear(hidden_dim, 8)   # 8 compartments
        self.param_head = nn.Linear(hidden_dim, 4)   # [beta_m, beta_mf, beta_f, gamma]

        # Fixed biological constants
        self.delta = 1.0 / 14.0   # Incubation rate (E->I)
        self.a = 0.001            # Baseline mortality
        self.b = 0.01             # Birth rate

    def forward(self, t: torch.Tensor, K: torch.Tensor):
        """
        Args:
            t: [batch, 1] normalized time
            K: [batch, 1] carrying capacity

        Returns:
            states: [batch, 8] compartment values
            beta_m, beta_mf, beta_f, gamma: [batch, 1] learned parameters
        """
        x = torch.cat([t, K], dim=-1)  # [B, 2]
        h = self.net(x)  # [B, hidden_dim]

        # Predict states with positivity constraint
        states = F.softplus(self.state_head(h)) + 1e-6  # [B, 8]

        # Predict parameters with bounded constraints
        params = self.param_head(h)
        beta_m = torch.sigmoid(params[:, 0:1]) * 0.1     # (0, 0.1)
        beta_mf = torch.sigmoid(params[:, 1:2]) * 0.05   # (0, 0.05)
        beta_f = torch.sigmoid(params[:, 2:3]) * 0.02    # (0, 0.02)
        gamma_eff = torch.sigmoid(params[:, 3:4]) * 0.1  # (0, 0.1)

        return states, beta_m, beta_mf, beta_f, gamma_eff

    def physics_loss(self, t: torch.Tensor, K: torch.Tensor, 
                     states: torch.Tensor, beta_m: torch.Tensor,
                     beta_mf: torch.Tensor, beta_f: torch.Tensor,
                     gamma_eff: torch.Tensor) -> torch.Tensor:
        """
        Compute SEIR ODE residual loss.

        Returns mean squared residual across all compartments.
        """
        # Unpack states
        S_m = states[:, 0:1]
        E_m = states[:, 1:2]
        I_m = states[:, 2:3]
        R_m = states[:, 3:4]
        S_f = states[:, 4:5]
        E_f = states[:, 5:6]
        I_f = states[:, 6:7]
        R_f = states[:, 7:8]

        N_m = S_m + E_m + I_m + R_m
        N_f = S_f + E_f + I_f + R_f
        N_R = N_m + N_f

        # Density-dependent mortality
        c = 1.0 / (K + 1e-6)
        d_N = self.a + c * N_R

        # Harmonic birth function
        B = 2 * self.b * N_m * N_f / (N_m + N_f + 1e-6)

        # Forces of infection
        lambda_m = beta_m * I_m + beta_mf * I_f
        lambda_f = beta_mf * I_m + beta_f * I_f

        # ODE RHS
        dS_m = B / 2 - S_m * d_N - S_m * lambda_m
        dE_m = S_m * lambda_m - E_m * d_N - self.delta * E_m
        dI_m = self.delta * E_m - I_m * d_N - gamma_eff * I_m
        dR_m = gamma_eff * I_m - R_m * d_N

        dS_f = B / 2 - S_f * d_N - S_f * lambda_f
        dE_f = S_f * lambda_f - E_f * d_N - self.delta * E_f
        dI_f = self.delta * E_f - I_f * d_N - gamma_eff * I_f
        dR_f = gamma_eff * I_f - R_f * d_N

        rhs = torch.cat([dS_m, dE_m, dI_m, dR_m, dS_f, dE_f, dI_f, dR_f], dim=1)

        # Compute dy/dt via autograd
        t_req = t.clone().requires_grad_(True)
        y = self.forward(t_req, K)[0]
        dy_dt = torch.autograd.grad(
            y, t_req,
            grad_outputs=torch.ones_like(y),
            create_graph=True
        )[0]

        # Physics residual
        residual = dy_dt - rhs
        return torch.mean(residual ** 2)

    def compute_R0(self, K: torch.Tensor, beta_m: torch.Tensor,
                   beta_mf: torch.Tensor, beta_f: torch.Tensor,
                   gamma_eff: torch.Tensor) -> torch.Tensor:
        """
        Compute basic reproduction number R0.

        R0 = (beta_eff * K) / (gamma_eff + d(K))
        """
        d = self.a + (1.0 / (K + 1e-6)) * K

        # Effective transmission rate
        beta_eff = (beta_m + beta_f) / 2 + torch.sqrt(
            ((beta_m - beta_f) / 2) ** 2 + beta_mf ** 2
        )

        R0 = (beta_eff * K) / (gamma_eff + d)
        return R0

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
