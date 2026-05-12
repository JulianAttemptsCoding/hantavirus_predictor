"""
HantaST-PINN-FM: Complete PyTorch Implementation
File: src/models/hantast_pinn_fm.py
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv
from torchdiffeq import odeint
from transformers import TimesFMForForecasting
from peft import LoraConfig, get_peft_model
import numpy as np


class ClimateEncoder(nn.Module):
    """3D CNN + Temporal Transformer for K(t) and beta(t) estimation."""

    def __init__(self, in_channels=4, hidden_dim=128, num_layers=4, 
                 spatial_size=(64, 64), temporal_len=24):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.temporal_len = temporal_len

        # 3D CNN backbone
        self.cnn3d = nn.Sequential(
            nn.Conv3d(in_channels, 32, kernel_size=(3, 3, 3), padding=(1, 1, 1)),
            nn.BatchNorm3d(32), nn.ReLU(), nn.MaxPool3d((1, 2, 2)),
            nn.Conv3d(32, 64, kernel_size=(3, 3, 3), padding=(1, 1, 1)),
            nn.BatchNorm3d(64), nn.ReLU(), nn.MaxPool3d((1, 2, 2)),
            nn.Conv3d(64, 128, kernel_size=(3, 3, 3), padding=(1, 1, 1)),
            nn.BatchNorm3d(128), nn.ReLU(),
            nn.AdaptiveAvgPool3d((temporal_len, 1, 1))
        )

        # Temporal positional encoding
        self.pos_encoding = nn.Parameter(
            torch.randn(1, temporal_len, hidden_dim) * 0.02
        )

        # Temporal Transformer
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim, nhead=8, dim_feedforward=512,
            dropout=0.1, batch_first=True, activation='gelu'
        )
        self.temporal_transformer = nn.TransformerEncoder(
            encoder_layer, num_layers=num_layers
        )

        # Output heads with biological constraints
        self.k_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2), nn.GELU(),
            nn.Linear(hidden_dim // 2, 1)
        )
        self.beta_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2), nn.GELU(),
            nn.Linear(hidden_dim // 2, 2)  # [beta_m, beta_f]
        )

        # Initialize
        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x):
        """
        Args:
            x: [B, C, T, H, W] where C=4 (NDVI, precip, temp, ENSO_broadcast)
        Returns:
            K_t: [B, T] carrying capacity trajectory
            beta_t: [B, T, 2] transmission rate trajectories
        """
        B = x.size(0)

        # 3D CNN
        cnn_out = self.cnn3d(x)  # [B, 128, T, 1, 1]
        cnn_out = cnn_out.squeeze(-1).squeeze(-1).permute(0, 2, 1)  # [B, T, 128]

        # Add positional encoding
        cnn_out = cnn_out + self.pos_encoding[:, :self.temporal_len, :]

        # Temporal Transformer
        temporal = self.temporal_transformer(cnn_out)  # [B, T, 128]

        # Output heads with biological constraints
        K_t = F.softplus(self.k_head(temporal)).squeeze(-1) + 10.0  # K > 10
        beta_t = F.softplus(self.beta_head(temporal)) + 0.001  # beta > 0.001

        return K_t, beta_t


class SEIRPhysicsLayer(nn.Module):
    """Differentiable SEIR ODE layer with climate-driven parameters."""

    def __init__(self, climate_encoder):
        super().__init__()
        self.climate_encoder = climate_encoder

        # Learnable biological parameters with informative priors
        self.log_gamma_m = nn.Parameter(torch.log(torch.tensor(1/30.0)))
        self.log_gamma_f = nn.Parameter(torch.log(torch.tensor(1/21.0)))
        self.log_delta = nn.Parameter(torch.log(torch.tensor(1/14.0)))
        self.log_a = nn.Parameter(torch.log(torch.tensor(0.01)))
        self.log_c = nn.Parameter(torch.log(torch.tensor(1e-4)))
        self.log_b = nn.Parameter(torch.log(torch.tensor(0.1)))

        # Spillover efficiency
        self.log_alpha = nn.Parameter(torch.log(torch.tensor(1e-4)))

    @property
    def gamma_m(self):
        return torch.exp(self.log_gamma_m)

    @property
    def gamma_f(self):
        return torch.exp(self.log_gamma_f)

    @property
    def delta(self):
        return torch.exp(self.log_delta)

    @property
    def a(self):
        return torch.exp(self.log_a)

    @property
    def c(self):
        return torch.exp(self.log_c)

    @property
    def b(self):
        return torch.exp(self.log_b)

    @property
    def alpha(self):
        return torch.exp(self.log_alpha)

    def seir_rhs(self, t, y, K_t_interp, beta_t_interp):
        """Compute RHS of sex-structured SEIR system."""
        S_m, E_m, I_m, R_m, S_f, E_f, I_f, R_f = y.unbind(-1)

        N_m = S_m + E_m + I_m + R_m
        N_f = S_f + E_f + I_f + R_f
        N = N_m + N_f

        # Interpolate climate-driven parameters at time t
        t_idx = torch.clamp(t.long(), 0, K_t_interp.size(1) - 1)
        K_t = K_t_interp[:, t_idx]
        beta_m = beta_t_interp[:, t_idx, 0]
        beta_f = beta_t_interp[:, t_idx, 1]
        beta_mf = (beta_m + beta_f) / 2.0

        # Density-dependent death
        d_N = self.a + self.c * N

        # Harmonic birth function
        B = 2.0 * self.b * (N_m * N_f) / (N_m + N_f + 1e-8)

        # Male equations
        dS_m = B/2.0 - S_m * d_N - S_m * (beta_m * I_m + beta_mf * I_f)
        dE_m = S_m * (beta_m * I_m + beta_mf * I_f) - self.delta * E_m - E_m * d_N
        dI_m = self.delta * E_m - self.gamma_m * I_m - I_m * d_N
        dR_m = self.gamma_m * I_m - R_m * d_N

        # Female equations
        dS_f = B/2.0 - S_f * d_N - S_f * (beta_mf * I_m + beta_f * I_f)
        dE_f = S_f * (beta_mf * I_m + beta_f * I_f) - self.delta * E_f - E_f * d_N
        dI_f = self.delta * E_f - self.gamma_f * I_f - I_f * d_N
        dR_f = self.gamma_f * I_f - R_f * d_N

        return torch.stack([
            dS_m, dE_m, dI_m, dR_m,
            dS_f, dE_f, dI_f, dR_f
        ], dim=-1)

    def forward(self, climate_input, t_span, y0):
        """
        Args:
            climate_input: [B, C, T, H, W]
            t_span: [T_ode] time points for ODE integration
            y0: [B, 8] initial conditions
        Returns:
            solution: [T_ode, B, 8] compartment trajectories
        """
        K_t, beta_t = self.climate_encoder(climate_input)

        # Solve ODE
        solution = odeint(
            lambda t, y: self.seir_rhs(t, y, K_t, beta_t),
            y0, t_span,
            method='dopri5',
            rtol=1e-5,
            atol=1e-6
        )

        return solution

    def compute_physics_residual(self, climate_input, t_coll, y_coll):
        """Compute ODE residual at collocation points for PINN loss."""
        K_t, beta_t = self.climate_encoder(climate_input)

        # Compute dy/dt via autograd
        t_coll.requires_grad_(True)

        # Forward pass at collocation points
        y_pred = []
        for t in t_coll:
            t_idx = torch.clamp(t.long(), 0, K_t.size(1) - 1)
            rhs = self.seir_rhs(t, y_coll, K_t, beta_t)
            y_pred.append(rhs)

        y_pred = torch.stack(y_pred, dim=0)  # [T_coll, B, 8]

        # Compute numerical derivative
        dy_dt = torch.autograd.grad(
            y_coll.sum(), t_coll,
            create_graph=True, retain_graph=True
        )[0]

        # Physics residual
        residual = dy_dt.unsqueeze(-1) - y_pred
        return residual.pow(2).mean()

    def compute_R0(self, K_t, beta_t):
        """Compute basic reproduction number from next-generation matrix."""
        beta_m = beta_t[..., 0]
        beta_f = beta_t[..., 1]
        beta_mf = (beta_m + beta_f) / 2.0

        gamma_m = self.gamma_m
        gamma_f = self.gamma_f
        delta = self.delta
        d_K = self.a + self.c * K_t

        # Next-generation matrix F * V^{-1}
        # F = [[beta_m * K, beta_mf * K], [beta_mf * K, beta_f * K]]
        # V = diag(gamma_m + d_K, gamma_f + d_K)

        F11 = beta_m * K_t
        F12 = beta_mf * K_t
        F21 = beta_mf * K_t
        F22 = beta_f * K_t

        V11 = gamma_m + d_K
        V22 = gamma_f + d_K

        # det(F * V^{-1} - lambda * I) = 0
        trace = F11 / V11 + F22 / V22
        det = (F11 * F22 - F12 * F21) / (V11 * V22)

        R0 = (trace + torch.sqrt(trace**2 - 4 * det)) / 2.0
        return R0


class FoundationPrior(nn.Module):
    """TimesFM/Chronos foundation model with LoRA adaptation."""

    def __init__(self, model_name="google/timesfm-2.5-500m", lora_rank=8, 
                 lora_alpha=16, dropout=0.1):
        super().__init__()

        self.base_model = TimesFMForForecasting.from_pretrained(model_name)

        # Freeze base
        for param in self.base_model.parameters():
            param.requires_grad = False

        # LoRA
        lora_config = LoraConfig(
            r=lora_rank,
            lora_alpha=lora_alpha,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
            lora_dropout=dropout,
            bias="none",
            task_type="FEATURE_EXTRACTION"
        )
        self.model = get_peft_model(self.base_model, lora_config)

        # Projection to common embedding space
        hidden_size = self.model.config.hidden_size
        self.proj = nn.Sequential(
            nn.Linear(hidden_size, 256),
            nn.LayerNorm(256),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128)
        )

    def forward(self, case_history, covariates=None):
        """
        Args:
            case_history: [B, T] normalized case counts
            covariates: [B, T, C] optional climate features
        Returns:
            embedding: [B, 128] temporal prior embedding
        """
        B, T = case_history.shape

        # Prepare input for TimesFM
        inputs = case_history.unsqueeze(-1)  # [B, T, 1]

        # Forward through foundation model
        outputs = self.model(
            input_ids=inputs,
            freq=torch.ones(B, dtype=torch.long, device=inputs.device) * 12
        )

        # Extract hidden states
        hidden = outputs.hidden_states[-1]  # [B, T, hidden]

        # Mean pooling over time
        pooled = hidden.mean(dim=1)  # [B, hidden]

        return self.proj(pooled)


class SpatiotemporalGAT(nn.Module):
    """Graph Attention Network for cross-regional diffusion."""

    def __init__(self, node_dim=128, hidden_dim=128, n_heads=8, 
                 n_gat_layers=2, n_gru_layers=2, forecast_horizon=12,
                 dropout=0.2):
        super().__init__()

        self.forecast_horizon = forecast_horizon

        # Temporal encoder
        self.temporal_gru = nn.GRU(
            input_size=node_dim,
            hidden_size=hidden_dim,
            num_layers=n_gru_layers,
            dropout=dropout if n_gru_layers > 1 else 0,
            batch_first=True
        )

        # Spatial encoder (GATv2)
        self.gat_layers = nn.ModuleList()
        in_dim = hidden_dim
        for i in range(n_gat_layers):
            out_dim = hidden_dim * n_heads if i < n_gat_layers - 1 else hidden_dim
            concat = i < n_gat_layers - 1
            self.gat_layers.append(
                GATv2Conv(
                    in_channels=in_dim,
                    out_channels=hidden_dim,
                    heads=n_heads,
                    concat=concat,
                    dropout=dropout,
                    add_self_loops=True
                )
            )
            in_dim = out_dim

        # Fusion
        self.fusion = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # Output heads
        self.mu_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2), nn.ReLU(),
            nn.Linear(hidden_dim // 2, forecast_horizon)
        )
        self.phi_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2), nn.ReLU(),
            nn.Linear(hidden_dim // 2, forecast_horizon)
        )
        self.risk_head = nn.Linear(hidden_dim, 4)

    def forward(self, x, edge_index, edge_attr=None):
        """
        Args:
            x: [N, T, node_dim] node features over time
            edge_index: [2, E] graph connectivity
            edge_attr: [E] optional edge weights
        Returns:
            mu: [N, horizon] predicted mean counts
            phi: [N, horizon] predicted dispersion
            risk_logits: [N, 4] risk tier logits
        """
        # Temporal encoding
        h_temp, _ = self.temporal_gru(x)  # [N, T, hidden]
        h_temp = h_temp[:, -1, :]  # [N, hidden] last timestep

        # Spatial encoding
        h_spat = h_temp
        for gat in self.gat_layers:
            h_spat = gat(h_spat, edge_index, edge_attr)
            h_spat = F.elu(h_spat)

        # Fusion
        h_fused = self.fusion(torch.cat([h_temp, h_spat], dim=-1))

        # Outputs
        mu = F.softplus(self.mu_head(h_fused))  # [N, horizon]
        phi = F.softplus(self.phi_head(h_fused)) + 1e-3  # [N, horizon]
        risk_logits = self.risk_head(h_fused)  # [N, 4]

        return mu, phi, risk_logits


class HantaSTPINNFM(nn.Module):
    """Complete HantaST-PINN-FM model integrating all tiers."""

    def __init__(self, config):
        super().__init__()

        ce_cfg = config["climate_encoder"]
        pinn_cfg = config["pinn"]
        fm_cfg = config["foundation"]
        stgat_cfg = config["stgat"]

        # Tier 1: Climate Encoder
        self.climate_encoder = ClimateEncoder(
            in_channels=ce_cfg.get("in_channels", 4),
            hidden_dim=ce_cfg.get("hidden_dim", 128),
            num_layers=ce_cfg.get("num_layers", 4),
            temporal_len=ce_cfg.get("temporal_len", 24)
        )

        # Tier 2: PINN-SEIR
        self.pinn = SEIRPhysicsLayer(self.climate_encoder)

        # Tier 3: Foundation Model
        self.foundation = FoundationPrior(
            model_name=fm_cfg.get("model_name", "google/timesfm-2.5-500m"),
            lora_rank=fm_cfg.get("lora_rank", 8),
            lora_alpha=fm_cfg.get("lora_alpha", 16)
        )

        # Tier 4: ST-GAT
        self.stgat = SpatiotemporalGAT(
            node_dim=stgat_cfg.get("node_dim", 128),
            hidden_dim=stgat_cfg.get("hidden_dim", 128),
            n_heads=stgat_cfg.get("n_heads", 8),
            n_gat_layers=stgat_cfg.get("n_gat_layers", 2),
            n_gru_layers=stgat_cfg.get("n_gru_layers", 2),
            forecast_horizon=stgat_cfg.get("forecast_horizon", 12)
        )

        # Feature combiner for ST-GAT input
        self.feature_combiner = nn.Sequential(
            nn.Linear(128 + 128 + 8, 128),  # FM + PINN state + env
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(0.2)
        )

    def forward(self, climate_input, case_history, graph_data, t_span, y0):
        """
        Args:
            climate_input: [B, C, T, H, W] climate raster stack
            case_history: [B, T_cases] historical case counts
            graph_data: PyG Data object with x, edge_index, edge_attr
            t_span: [T_ode] ODE integration times
            y0: [B, 8] initial SEIR conditions
        Returns:
            dict with all model outputs
        """
        # Tier 2: PINN forward
        seir_solution = self.pinn(climate_input, t_span, y0)

        # Extract final state
        final_state = seir_solution[-1]  # [B, 8]
        rodent_prev = (final_state[:, 2] + final_state[:, 6]) / (
            final_state.sum(dim=-1) + 1e-8
        )  # (I_m + I_f) / N

        # Tier 3: Foundation model
        fm_embedding = self.foundation(case_history)

        # Tier 4: ST-GAT
        # Combine features
        node_features = self.feature_combiner(
            torch.cat([fm_embedding, final_state], dim=-1)
        )

        # Reshape for ST-GAT [N, T, node_dim]
        node_features = node_features.unsqueeze(1)  # [N, 1, node_dim]

        mu, phi, risk_logits = self.stgat(
            node_features,
            graph_data.edge_index,
            graph_data.edge_attr
        )

        return {
            "seir_solution": seir_solution,
            "rodent_prevalence": rodent_prev,
            "fm_embedding": fm_embedding,
            "forecast_mu": mu,
            "forecast_phi": phi,
            "risk_logits": risk_logits,
            "R0": self.pinn.compute_R0(
                self.climate_encoder(climate_input)[0][:, -1],
                self.climate_encoder(climate_input)[1][:, -1]
            )
        }

    def compute_loss(self, outputs, targets, config):
        """Compute multi-objective loss."""
        lambdas = config["loss_weights"]

        # Data loss
        L_data = F.mse_loss(
            outputs["rodent_prevalence"], 
            targets["rodent_prevalence"]
        )

        if "human_cases" in targets:
            L_data += 0.1 * F.poisson_nll_loss(
                outputs["forecast_mu"],
                targets["human_cases"],
                log_input=False
            )

        # Physics loss (computed separately during training loop)
        L_ode = outputs.get("physics_residual", torch.tensor(0.0))

        # Foundation alignment loss
        L_fm = F.mse_loss(
            outputs["fm_embedding"],
            outputs.get("fm_target", outputs["fm_embedding"])
        ) if "fm_target" in outputs else torch.tensor(0.0)

        # Spatial smoothness
        L_spat = outputs.get("spatial_smoothness", torch.tensor(0.0))

        # Calibration loss
        L_calib = outputs.get("calibration_error", torch.tensor(0.0))

        total = (
            lambdas["data"] * L_data +
            lambdas["ode"] * L_ode +
            lambdas["fm"] * L_fm +
            lambdas["spatial"] * L_spat +
            lambdas["calib"] * L_calib
        )

        return total, {
            "L_data": L_data.item(),
            "L_ode": L_ode.item() if isinstance(L_ode, torch.Tensor) else 0.0,
            "L_fm": L_fm.item() if isinstance(L_fm, torch.Tensor) else 0.0,
            "L_spat": L_spat.item() if isinstance(L_spat, torch.Tensor) else 0.0,
            "L_calib": L_calib.item() if isinstance(L_calib, torch.Tensor) else 0.0
        }
