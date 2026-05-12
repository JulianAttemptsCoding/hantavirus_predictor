"""
HantaST-PINN-FM: Publication-Ready Visualization
File: src/visualization/publication_figures.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import shapereader
import geopandas as gpd
import shap
from pathlib import Path

# Set publication style
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
})

# Custom colormap for risk (white -> yellow -> orange -> red -> dark red)
RISK_CMAP = LinearSegmentedColormap.from_list(
    'risk', ['#ffffff', '#fee08b', '#fdae61', '#f46d43', '#d73027', '#a50026']
)


class PublicationFigures:
    """Generate publication-ready figures for hantavirus prediction paper."""

    def __init__(self, output_dir: str = "outputs/figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fig1_architecture_diagram(self):
        """Figure 1: System architecture diagram (4 tiers)."""
        fig, axes = plt.subplots(1, 5, figsize=(16, 4))

        tiers = [
            ("Tier 1\nClimate Encoder", "3D CNN +\nTransformer", "#4A90D9"),
            ("Tier 2\nPINN-SEIR", "Differentiable\nODE Solver", "#50C878"),
            ("Tier 3\nFoundation Model", "TimesFM +\nLoRA", "#F5A623"),
            ("Tier 4\nST-GAT", "Graph Attention\n+ GRU", "#BD10E0"),
            ("Tier 5\nUQ + Explain", "Conformal +\nSHAP", "#D0021B"),
        ]

        for i, (title, subtitle, color) in enumerate(tiers):
            ax = axes[i]
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')

            # Draw box
            rect = mpatches.FancyBboxPatch(
                (0.05, 0.1), 0.9, 0.8,
                boxstyle="round,pad=0.02,rounding_size=0.05",
                facecolor=color, alpha=0.3, edgecolor=color, linewidth=2
            )
            ax.add_patch(rect)

            # Text
            ax.text(0.5, 0.65, title, ha='center', va='center',
                   fontsize=11, fontweight='bold', color=color)
            ax.text(0.5, 0.35, subtitle, ha='center', va='center',
                   fontsize=9, style='italic')

            # Arrow to next
            if i < 4:
                ax.annotate('', xy=(1.15, 0.5), xytext=(0.95, 0.5),
                           arrowprops=dict(arrowstyle='->', color='gray', lw=2))

        plt.suptitle('HantaST-PINN-FM: Five-Tier Architecture', 
                    fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'fig1_architecture.png', dpi=300)
        plt.close()
        print(f"Saved: fig1_architecture.png")

    def fig2_seir_dynamics(self, t, solution, params):
        """Figure 2: SEIR phase portraits and R0 vs K trajectories."""
        fig = plt.figure(figsize=(14, 5))

        # Panel A: Compartment trajectories
        ax1 = fig.add_subplot(131)
        ax1.plot(t, solution[:, 0], label='$S_m$', color='#4A90D9', lw=1.5)
        ax1.plot(t, solution[:, 2], label='$I_m$', color='#D0021B', lw=1.5)
        ax1.plot(t, solution[:, 4], label='$S_f$', color='#4A90D9', lw=1.5, ls='--')
        ax1.plot(t, solution[:, 6], label='$I_f$', color='#D0021B', lw=1.5, ls='--')
        ax1.set_xlabel('Time (days)')
        ax1.set_ylabel('Population')
        ax1.set_title('(A) Sex-Structured SEIR Dynamics')
        ax1.legend(loc='upper right', frameon=True)
        ax1.grid(True, alpha=0.3)

        # Panel B: Phase portrait (I_m vs S_m)
        ax2 = fig.add_subplot(132)
        ax2.plot(solution[:, 0], solution[:, 2], color='#D0021B', lw=1.5)
        ax2.set_xlabel('$S_m$ (Susceptible Males)')
        ax2.set_ylabel('$I_m$ (Infectious Males)')
        ax2.set_title('(B) Phase Portrait: $I_m$ vs $S_m$')
        ax2.grid(True, alpha=0.3)

        # Panel C: R0 vs K
        ax3 = fig.add_subplot(133)
        K_range = np.linspace(100, 10000, 100)
        beta_eff = (params['beta_m'] + params['beta_f']) / 2
        gamma = params['gamma_m']
        d_K = params['a'] + params['c'] * K_range
        R0 = (beta_eff * K_range) / (gamma + d_K)

        ax3.plot(K_range, R0, color='#50C878', lw=2)
        ax3.axhline(y=1.0, color='black', ls='--', lw=1, label='$R_0 = 1$')
        ax3.fill_between(K_range, 0, 1, alpha=0.2, color='green', label='Disease-free')
        ax3.fill_between(K_range, 1, R0.max(), alpha=0.2, color='red', label='Endemic')
        ax3.set_xlabel('Carrying Capacity $K$')
        ax3.set_ylabel('Basic Reproduction Number $R_0$')
        ax3.set_title('(C) $R_0$ vs $K$ Threshold')
        ax3.legend(loc='upper left')
        ax3.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / 'fig2_seir_dynamics.png', dpi=300)
        plt.close()
        print(f"Saved: fig2_seir_dynamics.png")

    def fig3_risk_map(self, risk_data, counties_gdf, region='us_southwest'):
        """Figure 3: Spatial risk map at 1km resolution."""
        fig, ax = plt.subplots(figsize=(12, 8), 
                              subplot_kw={'projection': ccrs.AlbersEqualArea(
                                  central_latitude=35, central_longitude=-110)})

        # Add map features
        ax.add_feature(cfeature.LAND, facecolor='#f5f5f5')
        ax.add_feature(cfeature.OCEAN, facecolor='#e8f4f8')
        ax.add_feature(cfeature.STATES, edgecolor='white', linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, edgecolor='gray', linewidth=0.5)

        # Plot risk data
        counties_gdf.plot(
            column='risk_score',
            cmap=RISK_CMAP,
            vmin=0, vmax=1,
            ax=ax,
            transform=ccrs.PlateCarree(),
            legend=True,
            legend_kwds={
                'label': 'Spillover Risk',
                'orientation': 'horizontal',
                'pad': 0.02,
                'shrink': 0.6
            }
        )

        # Add known case locations
        case_locs = risk_data[risk_data['cases'] > 0]
        ax.scatter(case_locs['lon'], case_locs['lat'],
                  c='black', s=20, marker='x', 
                  transform=ccrs.PlateCarree(),
                  label='Historical Cases', zorder=5)

        ax.set_title('Hantavirus Spillover Risk Map: US Southwest', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='lower left')

        # Scale bar
        from matplotlib_scalebar.scalebar import ScaleBar
        ax.add_artist(ScaleBar(1, location='lower right'))

        plt.savefig(self.output_dir / 'fig3_risk_map.png', dpi=300)
        plt.close()
        print(f"Saved: fig3_risk_map.png")

    def fig4_forecast_comparison(self, dates, y_true, predictions_dict):
        """Figure 4: Forecast comparison across models."""
        fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

        colors = {
            'HantaST-PINN-FM': '#D0021B',
            'XGBoost': '#4A90D9',
            'SARIMA': '#50C878',
            'LSTM': '#F5A623'
        }

        # Panel A: Time series
        ax1 = axes[0]
        ax1.plot(dates, y_true, 'k-', lw=1.5, label='Observed', alpha=0.7)

        for name, pred in predictions_dict.items():
            color = colors.get(name, 'gray')
            ax1.plot(dates, pred, color=color, lw=1.2, label=name, alpha=0.8)

        ax1.set_ylabel('Monthly Cases')
        ax1.set_title('(A) Forecast Comparison: Monthly Case Counts')
        ax1.legend(loc='upper left', ncol=5)
        ax1.grid(True, alpha=0.3)

        # Panel B: Cumulative error
        ax2 = axes[1]
        for name, pred in predictions_dict.items():
            color = colors.get(name, 'gray')
            cum_error = np.cumsum(np.abs(y_true - pred))
            ax2.plot(dates, cum_error, color=color, lw=1.5, label=name)

        ax2.set_xlabel('Date')
        ax2.set_ylabel('Cumulative Absolute Error')
        ax2.set_title('(B) Cumulative Forecast Error')
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / 'fig4_forecast_comparison.png', dpi=300)
        plt.close()
        print(f"Saved: fig4_forecast_comparison.png")

    def fig5_calibration(self, y_true, y_prob, y_samples):
        """Figure 5: Reliability diagram and PIT histogram."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Panel A: Reliability diagram
        ax1 = axes[0]
        n_bins = 10
        bin_edges = np.linspace(0, 1, n_bins + 1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        observed = np.zeros(n_bins)
        predicted = np.zeros(n_bins)

        for i in range(n_bins):
            mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])
            if i == n_bins - 1:
                mask = (y_prob >= bin_edges[i]) & (y_prob <= bin_edges[i + 1])
            if mask.sum() > 0:
                observed[i] = y_true[mask].mean()
                predicted[i] = y_prob[mask].mean()

        ax1.plot([0, 1], [0, 1], 'k--', lw=1, label='Perfect calibration')
        ax1.plot(predicted, observed, 'o-', color='#D0021B', lw=2, 
                markersize=8, label='Model')
        ax1.fill_between([0, 1], [0, 1], [0, 0], alpha=0.1, color='green')
        ax1.set_xlabel('Mean Predicted Probability')
        ax1.set_ylabel('Observed Frequency')
        ax1.set_title('(A) Reliability Diagram')
        ax1.legend(loc='upper left')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')

        # Panel B: PIT histogram
        ax2 = axes[1]
        pits = np.mean(y_samples <= y_true.reshape(-1, 1), axis=1)
        ax2.hist(pits, bins=10, range=(0, 1), color='#4A90D9', 
                edgecolor='white', alpha=0.7, density=True)
        ax2.axhline(y=1.0, color='black', ls='--', lw=1, label='Uniform')
        ax2.set_xlabel('Probability Integral Transform')
        ax2.set_ylabel('Density')
        ax2.set_title('(B) PIT Histogram')
        ax2.legend(loc='upper right')
        ax2.set_xlim(0, 1)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / 'fig5_calibration.png', dpi=300)
        plt.close()
        print(f"Saved: fig5_calibration.png")

    def fig6_shap_importance(self, shap_values, feature_names, X_sample):
        """Figure 6: SHAP feature importance (global + local)."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Panel A: Global importance (mean |SHAP|)
        ax1 = axes[0]
        mean_shap = np.abs(shap_values).mean(axis=0)
        idx = np.argsort(mean_shap)[-15:]  # Top 15

        ax1.barh(range(len(idx)), mean_shap[idx], color='#4A90D9')
        ax1.set_yticks(range(len(idx)))
        ax1.set_yticklabels([feature_names[i] for i in idx])
        ax1.set_xlabel('Mean |SHAP Value|')
        ax1.set_title('(A) Global Feature Importance')
        ax1.grid(True, alpha=0.3, axis='x')

        # Panel B: Local explanation (waterfall)
        ax2 = axes[1]
        # Simplified waterfall
        sample_idx = 0
        shap_sample = shap_values[sample_idx]
        idx_sorted = np.argsort(np.abs(shap_sample))[-10:]

        colors = ['#D0021B' if v > 0 else '#4A90D9' for v in shap_sample[idx_sorted]]
        ax2.barh(range(len(idx_sorted)), shap_sample[idx_sorted], color=colors)
        ax2.set_yticks(range(len(idx_sorted)))
        ax2.set_yticklabels([feature_names[i] for i in idx_sorted])
        ax2.set_xlabel('SHAP Value')
        ax2.set_title('(B) Local Explanation (Single Prediction)')
        ax2.axvline(x=0, color='black', lw=0.5)
        ax2.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()
        plt.savefig(self.output_dir / 'fig6_shap_importance.png', dpi=300)
        plt.close()
        print(f"Saved: fig6_shap_importance.png")

    def fig7_ablation(self, ablation_results):
        """Figure 7: Ablation study bar chart."""
        fig, ax = plt.subplots(figsize=(10, 6))

        configs = ablation_results['config'].values
        wis = ablation_results['WIS'].values
        colors = ['#D0021B' if c == 'full' else '#4A90D9' for c in configs]

        bars = ax.bar(range(len(configs)), wis, color=colors, edgecolor='white')
        ax.set_xticks(range(len(configs)))
        ax.set_xticklabels(configs, rotation=45, ha='right')
        ax.set_ylabel('Weighted Interval Score (WIS)')
        ax.set_title('Ablation Study: Component Contribution')
        ax.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for bar, val in zip(bars, wis):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{val:.3f}', ha='center', va='bottom', fontsize=9)

        # Legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#D0021B', label='Full Model'),
            Patch(facecolor='#4A90D9', label='Ablated')
        ]
        ax.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        plt.savefig(self.output_dir / 'fig7_ablation.png', dpi=300)
        plt.close()
        print(f"Saved: fig7_ablation.png")

    def fig8_attention_weights(self, edge_index, attention_weights, counties_gdf):
        """Figure 8: ST-GAT attention weights (spread corridors)."""
        fig, ax = plt.subplots(figsize=(12, 8),
                              subplot_kw={'projection': ccrs.AlbersEqualArea(
                                  central_latitude=35, central_longitude=-110)})

        ax.add_feature(cfeature.STATES, edgecolor='white', linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, edgecolor='gray', linewidth=0.5)

        # Plot edges with width proportional to attention weight
        for i, (src, dst) in enumerate(edge_index.T):
            weight = attention_weights[i]
            if weight > 0.1:  # Threshold
                src_geom = counties_gdf.iloc[src].geometry.centroid
                dst_geom = counties_gdf.iloc[dst].geometry.centroid

                ax.plot([src_geom.x, dst_geom.x], [src_geom.y, dst_geom.y],
                       color='#D0021B', alpha=weight, lw=weight*3,
                       transform=ccrs.PlateCarree(), zorder=3)

        ax.set_title('ST-GAT Attention Weights: Transmission Corridors',
                    fontsize=14, fontweight='bold')

        plt.savefig(self.output_dir / 'fig8_attention_weights.png', dpi=300)
        plt.close()
        print(f"Saved: fig8_attention_weights.png")

    def generate_all(self, **kwargs):
        """Generate all publication figures."""
        print("Generating all publication figures...")

        self.fig1_architecture_diagram()

        if 't' in kwargs and 'solution' in kwargs and 'params' in kwargs:
            self.fig2_seir_dynamics(kwargs['t'], kwargs['solution'], kwargs['params'])

        if 'risk_data' in kwargs and 'counties_gdf' in kwargs:
            self.fig3_risk_map(kwargs['risk_data'], kwargs['counties_gdf'])

        if 'dates' in kwargs and 'y_true' in kwargs and 'predictions' in kwargs:
            self.fig4_forecast_comparison(kwargs['dates'], kwargs['y_true'], kwargs['predictions'])

        if 'y_true_cal' in kwargs and 'y_prob' in kwargs and 'y_samples' in kwargs:
            self.fig5_calibration(kwargs['y_true_cal'], kwargs['y_prob'], kwargs['y_samples'])

        if 'shap_values' in kwargs and 'feature_names' in kwargs and 'X_sample' in kwargs:
            self.fig6_shap_importance(kwargs['shap_values'], kwargs['feature_names'], kwargs['X_sample'])

        if 'ablation_results' in kwargs:
            self.fig7_ablation(kwargs['ablation_results'])

        if 'edge_index' in kwargs and 'attention_weights' in kwargs and 'counties_gdf_attn' in kwargs:
            self.fig8_attention_weights(kwargs['edge_index'], kwargs['attention_weights'], kwargs['counties_gdf_attn'])

        print(f"All figures saved to {self.output_dir}")
