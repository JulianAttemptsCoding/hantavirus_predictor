"""HANTA-PINN: Complete model integrating all modules."""
import torch
import torch.nn as nn
import torch.nn.functional as F

from .encoder import EnvironmentalEncoder
from .pinn_core import PINNCore
from .spillover import SpilloverDecoder


class HantaPINN(nn.Module):
    """
    Complete HANTA-PINN model for hantavirus reservoir dynamics and spillover prediction.

    Architecture:
        EnvironmentalEncoder -> PINNCore -> SpilloverDecoder
    """

    def __init__(self, encoder_config: dict = None, pinn_config: dict = None, 
                 spillover_config: dict = None):
        super().__init__()

        encoder_config = encoder_config or {}
        pinn_config = pinn_config or {}
        spillover_config = spillover_config or {}

        self.env_encoder = EnvironmentalEncoder(**encoder_config)
        self.pinn_core = PINNCore(**pinn_config)
        self.spillover_decoder = SpilloverDecoder(**spillover_config)

    def forward(self, env_history: torch.Tensor, t: torch.Tensor, 
                human_features: torch.Tensor) -> dict:
        """
        Forward pass through complete model.

        Args:
            env_history: [batch, seq_len, n_env_features]
            t: [batch, 1] normalized time
            human_features: [batch, n_human_features]

        Returns:
            dict with keys: K, states, beta_m, params, lambda_H, seroprev, R0
        """
        # Environmental encoder -> K(t)
        K = self.env_encoder(env_history)

        # PINN core -> SEIR states + parameters
        states, beta_m, beta_mf, beta_f, gamma = self.pinn_core(t, K)

        # Spillover decoder -> human risk
        lambda_H = self.spillover_decoder(states, human_features)

        # Derived quantities
        I_total = states[:, 2] + states[:, 6]
        N_total = states.sum(dim=1)
        seroprev = I_total / (N_total + 1e-6)

        R0 = self.pinn_core.compute_R0(K, beta_m, beta_mf, beta_f, gamma)

        return {
            'K': K,
            'states': states,
            'beta_m': beta_m,
            'beta_mf': beta_mf,
            'beta_f': beta_f,
            'gamma': gamma,
            'params': (beta_m, beta_mf, beta_f, gamma),
            'lambda_H': lambda_H,
            'seroprev': seroprev,
            'R0': R0
        }

    def compute_loss(self, batch: dict, alpha_data: float = 0.6,
                     alpha_physics: float = 0.3, alpha_reg: float = 0.1) -> tuple:
        """
        Compute combined loss: data + physics + spillover + regularization.

        Returns:
            loss: total loss
            metrics: dict of individual loss components
        """
        env_history = batch['env']
        t = batch['t']
        human_features = batch['human']

        out = self.forward(env_history, t, human_features)

        # 1. Data loss (rodent seroprevalence)
        pred_seroprev = out['seroprev']
        true_seroprev = batch['seroprev']
        L_data = F.mse_loss(pred_seroprev, true_seroprev)

        # 2. Physics loss (SEIR residual)
        K = out['K']
        states = out['states']
        beta_m, beta_mf, beta_f, gamma = out['params']
        L_physics = self.pinn_core.physics_loss(t, K, states, beta_m, beta_mf, beta_f, gamma)

        # 3. Spillover loss (human cases, downweighted)
        pred_lambda = out['lambda_H']
        true_cases = batch['cases']
        L_spillover = F.poisson_nll_loss(pred_lambda, true_cases, log_input=False, full=False)

        # 4. Regularization
        L_reg = sum(p.pow(2).sum() for p in self.parameters()) * 1e-5

        # Combined
        loss = (alpha_data * L_data + alpha_physics * L_physics + 
                0.1 * alpha_data * L_spillover + alpha_reg * L_reg)

        metrics = {
            'L_data': L_data.item(),
            'L_physics': L_physics.item(),
            'L_spillover': L_spillover.item(),
            'L_reg': L_reg.item(),
            'L_total': loss.item()
        }

        return loss, metrics

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
