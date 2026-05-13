"""Create EID submission figures: Figure 1 (incidence map) and Figure 2 (calibration-sharpness).

Figure 1: Country-level reported hantavirus incidence per 100,000, EU/EEA 2023.
Figure 2: Calibration-sharpness tradeoff scatter for 2023 one-year-ahead forecasts.

Outputs go to docs/submission_eid/figures/ as Figure_1.tif and Figure_2.tif at 600 dpi.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

DEFAULT_CASES = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_BASELINE_METRICS = ROOT / "data" / "processed" / "international_baseline_metrics.csv"
DEFAULT_ABLATION_METRICS = ROOT / "data" / "processed" / "feature_ablation_metrics.csv"
DEFAULT_COUNT_METRICS = ROOT / "data" / "processed" / "count_model_metrics.csv"
DEFAULT_BOUNDARIES = ROOT / "data" / "raw" / "natural_earth" / "ne_50m_admin_0_countries.zip"
DEFAULT_OUTPUT = ROOT / "docs" / "submission_eid" / "figures"

EUROPE_PROJECTION = "EPSG:3035"
PANEL_EXTENT = (-5_500_000, 5_200_000, -4_800_000, 5_300_000)

EID_RC = {
    "font.family": "Arial",
    "font.size": 10,
    "axes.titlesize": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
}


def _save_figure_tif(fig: plt.Figure, path: Path, dpi: int = 600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fig.savefig(
            path,
            dpi=dpi,
            bbox_inches="tight",
            pil_kwargs={"compression": "tiff_lzw"},
        )
    except Exception:
        # Fallback to PNG if PIL TIFF fails
        png_path = path.with_suffix(".png")
        fig.savefig(png_path, dpi=dpi, bbox_inches="tight")
        print(f"  Saved as PNG fallback: {png_path}")
    else:
        print(f"  Saved: {path}")


def _create_figure1_map(cases: pd.DataFrame, boundaries_path: Path, output: Path) -> None:
    """Country-level incidence choropleth, 2023 — EID Figure 1."""
    import geopandas as gpd

    cases_2023 = cases[cases["year"].eq(2023)].copy()
    boundaries = gpd.read_file(boundaries_path)
    boundaries["join_iso3"] = boundaries["ISO_A3"].where(
        boundaries["ISO_A3"].ne("-99"), boundaries["ADM0_A3"]
    )
    selected = boundaries[boundaries["join_iso3"].isin(set(cases_2023["iso3"]))].copy()
    selected = selected.to_crs(EUROPE_PROJECTION)
    map_data = selected.merge(cases_2023, left_on="join_iso3", right_on="iso3", how="left")

    plt.rcParams.update(EID_RC)
    fig, ax = plt.subplots(figsize=(7.4, 7.0))
    map_data.plot(
        ax=ax,
        column="incidence_per_100k",
        cmap="viridis",
        linewidth=0.35,
        edgecolor="#FFFFFF",
        missing_kwds={"color": "#D9D9D9", "label": "No data / not reported"},
        legend=True,
        legend_kwds={
            "label": "Reported cases per 100,000 population",
            "shrink": 0.7,
        },
    )
    map_data.boundary.plot(ax=ax, color="#4D4D4D", linewidth=0.2)
    ax.set_xlim(PANEL_EXTENT[0], PANEL_EXTENT[1])
    ax.set_ylim(PANEL_EXTENT[2], PANEL_EXTENT[3])
    ax.set_axis_off()
    fig.tight_layout()
    _save_figure_tif(fig, output / "Figure_1.tif")
    plt.close(fig)


def _create_figure2_tradeoff(
    baseline_metrics: pd.DataFrame,
    ablation_metrics: pd.DataFrame,
    count_metrics: pd.DataFrame,
    output: Path,
) -> None:
    """Calibration-sharpness tradeoff scatter — EID Figure 2."""
    plt.rcParams.update(EID_RC)

    FAMILY_STYLE = {
        "Simple baseline": {"marker": "o", "color": "#0072B2", "zorder": 5},
        "NB baseline": {"marker": "s", "color": "#009E73", "zorder": 5},
        "Covariate block": {"marker": "^", "color": "#D55E00", "zorder": 4},
        "Penalized Poisson": {"marker": "D", "color": "#CC79A7", "zorder": 4},
    }

    # Collect data points
    rows: list[dict] = []

    # Simple baselines and NB baselines from baseline metrics (2023)
    bl_2023 = baseline_metrics[baseline_metrics["target_year"].eq(2023)].copy()
    simple_models = {"last_observed_country_rate", "country_historical_mean_rate",
                     "region_syndrome_mean_rate"}
    nb_models = {"empirical_negative_binomial_rate", "hierarchical_negative_binomial_rate"}
    for _, r in bl_2023.iterrows():
        model = str(r["model"])
        if model in simple_models:
            family = "Simple baseline"
            label = model.replace("_rate", "").replace("_", " ").title()
            if "last_observed" in model:
                label = "Last-observed rate"
            elif "historical_mean" in model:
                label = "Historical mean rate"
            else:
                label = "Region mean rate"
        elif model in nb_models:
            family = "NB baseline"
            label = "Empirical NB" if "empirical" in model else "Hierarchical NB"
        else:
            continue
        rows.append({
            "label": label,
            "family": family,
            "wis": float(r["mean_wis"]),
            "width": float(r["mean_interval_width_90"]),
            "coverage": float(r["coverage_90"]),
        })

    # Covariate blocks from ablation metrics (primary_test_2023)
    abl_2023 = ablation_metrics[ablation_metrics["split"].eq("primary_test_2023")].copy()
    for _, r in abl_2023.iterrows():
        fs = str(r["feature_set"])
        label_map = {
            "surveillance_only": "Surv. only",
            "context": "+ Context",
            "land_use": "+ Land use",
            "climate": "+ Climate",
            "all_public": "+ All public",
        }
        label = label_map.get(fs, fs)
        rows.append({
            "label": label,
            "family": "Covariate block",
            "wis": float(r["mean_wis"]),
            "width": float(r["mean_interval_width_90"]),
            "coverage": float(r["coverage_90"]),
        })

    # Penalized Poisson from count metrics (2023)
    if not count_metrics.empty:
        ct_2023 = count_metrics[count_metrics["target_year"].eq(2023)].copy()
        for _, r in ct_2023.iterrows():
            fs = str(r["feature_set"])
            label_map = {
                "surveillance_only": "PP: surv.",
                "context": "PP: context",
                "land_use": "PP: land use",
                "climate": "PP: climate",
                "all_public": "PP: all public",
            }
            label = label_map.get(fs, f"PP: {fs}")
            rows.append({
                "label": label,
                "family": "Penalized Poisson",
                "wis": float(r["mean_wis"]),
                "width": float(r["mean_interval_width_90"]),
                "coverage": float(r["coverage_90"]),
            })

    df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    annotate_set = {
        "Last-observed rate", "Empirical NB", "PP: land use", "+ Land use"
    }

    for family, style in FAMILY_STYLE.items():
        sub = df[df["family"].eq(family)]
        if sub.empty:
            continue
        ax.scatter(
            sub["width"],
            sub["wis"],
            marker=style["marker"],
            color=style["color"],
            s=60,
            zorder=style["zorder"],
            label=family,
            alpha=0.85,
        )
        for _, row in sub.iterrows():
            if row["label"] in annotate_set:
                ax.annotate(
                    row["label"],
                    xy=(row["width"], row["wis"]),
                    xytext=(6, 3),
                    textcoords="offset points",
                    fontsize=8,
                    color=style["color"],
                )

    ax.set_xlabel("Mean 90% prediction interval width (cases per 100,000)")
    ax.set_ylabel("Mean weighted interval score (WIS; lower = better)")
    ax.legend(loc="upper left", frameon=True, framealpha=0.9)

    # Annotate nominal 90% coverage reference
    ax.axhline(y=0, color="none")  # baseline for layout

    fig.tight_layout()
    _save_figure_tif(fig, output / "Figure_2.tif")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--baseline-metrics", default=str(DEFAULT_BASELINE_METRICS))
    parser.add_argument("--ablation-metrics", default=str(DEFAULT_ABLATION_METRICS))
    parser.add_argument("--count-metrics", default=str(DEFAULT_COUNT_METRICS))
    parser.add_argument("--boundaries", default=str(DEFAULT_BOUNDARIES))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    cases = pd.read_csv(args.cases)
    baseline_metrics = pd.read_csv(args.baseline_metrics)
    ablation_metrics = pd.read_csv(args.ablation_metrics)

    count_path = Path(args.count_metrics)
    count_metrics = pd.read_csv(count_path) if count_path.exists() else pd.DataFrame()

    boundaries_path = Path(args.boundaries)
    if not boundaries_path.exists():
        print(f"WARNING: boundaries file not found: {boundaries_path}")
        print("Skipping Figure 1. Run tools/download_natural_earth_countries.py first.")
    else:
        print("Creating Figure 1 (incidence map)...")
        _create_figure1_map(cases, boundaries_path, output)

    print("Creating Figure 2 (calibration-sharpness tradeoff)...")
    _create_figure2_tradeoff(baseline_metrics, ablation_metrics, count_metrics, output)

    print(f"\nEID figures written to: {output}")
    print("Verify DPI: python -c \"from PIL import Image; from pathlib import Path; "
          "[print(p.name, Image.open(p).info.get('dpi')) "
          "for p in Path('docs/submission_eid/figures').glob('*')]\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
