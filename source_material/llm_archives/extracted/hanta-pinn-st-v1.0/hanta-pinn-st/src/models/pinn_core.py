"""
Physics-Informed Neural Network Core for Hantavirus SEIR-SDE
Implements gender-structured rodent reservoir dynamics with climate forcing.
"""
import torch
import torch.nn as nn
from torchdiffeq import odeint


class PINNCore(nn.Module):
    """
    Neural ODE-based PINN that embeds 8-compartment SEIR dynamics.

    Learns time-varying parameters beta_m(t), beta_f(t), K(t) from climate embeddings.
    Enforces ODE residuals via automatic differentiation.
    """
    def __init__(self, env_dim=256, hidden_dim=128, n_compartments=8):
        super().__init__()
        self.env_dim = env_dim
        self.hidden_dim = hidden_dim
        self.n_compartments = n_compartments

        # Parameter network: maps [env_emb, time] -> [beta_m, beta_f, K]
        self.param_net = nn.Sequential(
            nn.Linear(env_dim + 1, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 3),
            nn.Softplus()  # Ensure positive parameters
        )

        # State network: maps [env_emb, state, time] -> state derivatives
        self.state_net = nn.Sequential(
            nn.Linear(env_dim + n_compartments + 1, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, n_compartments)
        )

        # Fixed biological parameters (from literature)
        self.register_buffer('delta', torch.tensor(0.135))  # incubation rate (1/7.4 days)
        self.register_buffer('a', torch.tensor(0.002))      # baseline mortality
        self.register_buffer('c', torch.tensor(0.0003))     # density dependence
        self.register_buffer('b', torch.tensor(0.1))        # birth rate

    def seir_rhs(self, state, params):
        """
        Compute the right-hand side of the 8-compartment SEIR ODE.

        Args:
            state: [B, 8] tensor [S_m, E_m, I_m, R_m, S_f, E_f, I_f, R_f]
            params: [B, 3] tensor [beta_m, beta_f, K]

        Returns:
            rhs: [B, 8] tensor of derivatives
        """
        S_m, E_m, I_m, R_m, S_f, E_f, I_f, R_f = state.T
        beta_m, beta_f, K = params.T

        # Population totals
        N_m = S_m + E_m + I_m + R_m
        N_f = S_f + E_f + I_f + R_f
        N = N_m + N_f

        # Density-dependent mortality
        d_N = self.a + self.c * N

        # Birth function (harmonic mean, scaled to carrying capacity)
        B = torch.where(N > 0, 
                        2 * self.b * N_m * N_f / (N_m + N_f),
                        torch.zeros_like(N))
        B = B * torch.clamp(K / (N + 1e-6), 0.5, 2.0)  # density feedback

        # Male-male and male-female transmission
        beta_mf = 0.74 * beta_m  # intermediate rate (literature: beta_mf ~ 0.74*beta_m)

        # Force of infection
        lambda_m = beta_m * I_m + beta_mf * I_f
        lambda_f = beta_mf * I_m + beta_f * I_f

        # ODE system
        dS_m = B / 2 - S_m * d_N - S_m * lambda_m
        dE_m = S_m * lambda_m - E_m * d_N - self.delta * E_m
        dI_m = self.delta * E_m - I_m * d_N - 0.033 * I_m  # gamma_m = 1/30
        dR_m = 0.033 * I_m - R_m * d_N

        dS_f = B / 2 - S_f * d_N - S_f * lambda_f
        dE_f = S_f * lambda_f - E_f * d_N - self.delta * E_f
        dI_f = self.delta * E_f - I_f * d_N - 0.05 * I_f   # gamma_f = 1/20
        dR_f = 0.05 * I_f - R_f * d_N

        return torch.stack([dS_m, dE_m, dI_m, dR_m, 
                           dS_f, dE_f, dI_f, dR_f], dim=1)

    def forward(self, t, env_emb, state_0):
        """
        Integrate the SEIR ODE from t=0 to t=T using learned parameters.

        Args:
            t: [T] tensor of time points
            env_emb: [B, env_dim] climate/environment embedding
            state_0: [B, 8] initial compartment states

        Returns:
            trajectory: [T, B, 8] compartment trajectories
            params_t: [B, 3] learned parameters at final time
        """
        # Learn parameters at query time
        params_t = self.param_net(torch.cat([env_emb, t[-1:].unsqueeze(-1).expand(env_emb.size(0), 1)], dim=-1))

        # Neural ODE integration
        def ode_func(t_scalar, state):
            # Expand env_emb for batch
            t_expanded = t_scalar.unsqueeze(0).expand(env_emb.size(0), 1)
            params = self.param_net(torch.cat([env_emb, t_expanded], dim=-1))
            return self.seir_rhs(state, params)

        trajectory = odeint(ode_func, state_0, t, 
                           method='dopri5', rtol=1e-5, atol=1e-6)
        return trajectory, params_t

    def compute_ode_residual(self, t, env_emb, state):
        """
        Compute ODE residual for physics loss.

        Args:
            t: [B, 1] time points (requires grad)
            env_emb: [B, env_dim] embeddings
            state: [B, 8] predicted states

        Returns:
            residual: [B, 8] ||du/dt - f(u)||
        """
        t = t.requires_grad_(True)

        # Compute du/dt via autograd
        state_flat = state.view(-1)
        du_dt = torch.autograd.grad(
            state_flat.sum(), t,
            create_graph=True, retain_graph=True
        )[0]

        # Compute analytical RHS
        params = self.param_net(torch.cat([env_emb, t], dim=-1))
        rhs = self.seir_rhs(state, params)

        return du_dt - rhs

    def compute_r0(self, params):
        """
        Compute basic reproduction number from learned parameters.

        Args:
            params: [B, 3] [beta_m, beta_f, K]

        Returns:
            r0: [B] basic reproduction numbers
        """
        beta_m, beta_f, K = params.T
        beta_eff = (beta_m + beta_f) / 2  # effective transmission
        gamma_eff = 0.04  # average recovery
        d_K = self.a + self.c * K

        r0 = beta_eff * K / (gamma_eff + d_K)
        return r0
