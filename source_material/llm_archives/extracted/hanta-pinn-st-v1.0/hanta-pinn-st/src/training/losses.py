"""
Multi-component loss function for HANTA-PINN-ST.
Combines data fidelity, physics constraints, and regularization.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class HantaLoss(nn.Module):
    """
    Combined loss for physics-informed hantavirus prediction.

    Components:
    - L_data: MSE against observed seroprevalence/cases
    - L_ode: SEIR ODE residual
    - L_sde: Stochastic noise penalty
    - L_spill: Negative binomial negative log-likelihood for human cases
    - L_bound: Positivity and boundedness constraints
    - L_reg: L2 weight regularization
    """
    def __init__(self, 
                 lambda_data=1.0, 
                 lambda_ode=0.1, 
                 lambda_sde=0.01,
                 lambda_spill=1.0, 
                 lambda_bound=0.1, 
                 lambda_reg=1e-4):
        super().__init__()
        self.lambdas = {
            'data': lambda_data,
            'ode': lambda_ode,
            'sde': lambda_sde,
            'spill': lambda_spill,
            'bound': lambda_bound,
            'reg': lambda_reg
        }

    def forward(self, pred, target, ode_residual, sde_term,
                spill_pred, spill_target, model_params):
        """
        Compute total loss.

        Args:
            pred: [B, ...] predicted states
            target: [B, ...] observed states
            ode_residual: [B, 8] ODE residual
            sde_term: [B, ...] SDE noise term
            spill_pred: [B, 2] [mu, log_phi] for negative binomial
            spill_target: [B] observed human case counts
            model_params: iterable of model parameters
        """
        losses = {}

        # Data fidelity
        losses['data'] = F.mse_loss(pred, target)

        # Physics (ODE residual)
        losses['ode'] = torch.mean(ode_residual ** 2)

        # Stochasticity
        losses['sde'] = torch.mean(sde_term ** 2)

        # Spillover (Negative Binomial)
        mu, log_phi = spill_pred[:, 0], spill_pred[:, 1]
        phi = F.softplus(log_phi) + 1e-6
        losses['spill'] = self.nb_nll(spill_target, mu, phi)

        # Boundary (positivity + conservation)
        losses['bound'] = (torch.mean(F.relu(-pred)) + 
                          torch.mean(F.relu(pred - 1e6)))

        # Regularization
        losses['reg'] = sum(p.pow(2).sum() for p in model_params)

        # Total
        total = sum(self.lambdas[k] * losses[k] for k in losses)
        return total, losses

    def nb_nll(self, y, mu, phi):
        """
        Negative Binomial negative log-likelihood.

        Parameterization: mean = mu, dispersion = phi
        p = phi / (phi + mu)
        """
        p = phi / (phi + mu + 1e-8)
        nll = (-torch.lgamma(y + phi) + torch.lgamma(phi) + 
               torch.lgamma(y + 1) - phi * torch.log(p + 1e-8) - 
               y * torch.log(1 - p + 1e-8))
        return nll.mean()

    def adaptive_weight_update(self, losses_dict, model_params):
        """
        Update loss weights using NTK-based balancing.
        Re-normalize every 100 epochs.
        """
        grads = {}
        for key, loss in losses_dict.items():
            grad = torch.autograd.grad(loss, model_params, 
                                      retain_graph=True, 
                                      allow_unused=True)
            grad_norm = sum(g.pow(2).sum() for g in grad if g is not None)
            grads[key] = grad_norm.sqrt()

        total_grad = sum(grads.values()) + 1e-8
        for key in grads:
            self.lambdas[key] = (grads[key] / total_grad).item()


class QuantileLoss(nn.Module):
    """Pinball loss for probabilistic forecasting."""
    def __init__(self, quantiles=[0.05, 0.25, 0.5, 0.75, 0.95]):
        super().__init__()
        self.quantiles = quantiles

    def forward(self, preds, target):
        """
        Args:
            preds: [B, n_quantiles] predicted quantiles
            target: [B] observed values
        """
        losses = []
        for i, q in enumerate(self.quantiles):
            errors = target - preds[:, i]
            losses.append(torch.max((q - 1) * errors, q * errors).unsqueeze(1))
        return torch.mean(torch.sum(torch.cat(losses, dim=1), dim=1))
