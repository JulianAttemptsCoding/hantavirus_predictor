"""Create IJHG-ready country-level maps for the ECDC benchmark."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib
import pandas as pd
from matplotlib.colors import ListedColormap

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

DEFAULT_CASES = ROOT / "data" / "processed" / "international_country_year.csv"
DEFAULT_METRICS = ROOT / "data" / "processed" / "feature_ablation_metrics.csv"
DEFAULT_PREDICTIONS = ROOT / "data" / "processed" / "feature_ablation_predictions.csv"
DEFAULT_BOUNDARIES = ROOT / "data" / "raw" / "natural_earth" / "ne_50m_admin_0_countries.zip"
DEFAULT_FIGURES = ROOT / "figures"
DEFAULT_REPORT = ROOT / "reports" / "06_ijhg_maps.md"

EUROPE_PROJECTION = "EPSG:3035"
PANEL_EXTENT = (-5_500_000, 5_200_000, -4_800_000, 5_300_000)


def _load_boundaries(path: Path, cases: pd.DataFrame) -> gpd.GeoDataFrame:
    boundaries = gpd.read_file(path)
    boundaries["join_iso3"] = boundaries["ISO_A3"].where(
        boundaries["ISO_A3"].ne("-99"), boundaries["ADM0_A3"]
    )
    selected = boundaries[boundaries["join_iso3"].isin(set(cases["iso3"]))].copy()
    return selected.to_crs(EUROPE_PROJECTION)


def _style_axis(ax: plt.Axes) -> None:
    ax.set_xlim(PANEL_EXTENT[0], PANEL_EXTENT[1])
    ax.set_ylim(PANEL_EXTENT[2], PANEL_EXTENT[3])
    ax.set_axis_off()


def _plot_context(ax: plt.Axes, countries: gpd.GeoDataFrame) -> None:
    countries.boundary.plot(ax=ax, color="#4D4D4D", linewidth=0.25)


def _save_single_map(
    countries: gpd.GeoDataFrame,
    column: str,
    title: str,
    output: Path,
    cmap: str = "viridis",
    legend_label: str | None = None,
) -> None:
    fig, ax = plt.subplots(figsize=(7.4, 7.0))
    countries.plot(
        ax=ax,
        column=column,
        cmap=cmap,
        linewidth=0.35,
        edgecolor="#FFFFFF",
        missing_kwds={"color": "#D9D9D9", "label": "No data"},
        legend=True,
        legend_kwds={"label": legend_label or column, "shrink": 0.7},
    )
    _plot_context(ax, countries)
    ax.set_title(title)
    _style_axis(ax)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300)
    plt.close(fig)


def _save_completeness_map(countries: gpd.GeoDataFrame, output: Path) -> None:
    categories = ["comprehensive", "not_comprehensive", "unspecified"]
    palette = ListedColormap(["#009E73", "#D55E00", "#CC79A7"])
    plot_data = countries.copy()
    plot_data["completeness_code"] = pd.Categorical(
        plot_data["surveillance_completeness"], categories=categories
    ).codes
    fig, ax = plt.subplots(figsize=(7.4, 7.0))
    plot_data.plot(
        ax=ax,
        column="completeness_code",
        cmap=palette,
        linewidth=0.35,
        edgecolor="#FFFFFF",
        missing_kwds={"color": "#D9D9D9"},
    )
    _plot_context(ax, plot_data)
    handles = [
        plt.Line2D([0], [0], marker="s", color="none", markerfacecolor=color, markersize=9)
        for color in ["#009E73", "#D55E00", "#CC79A7"]
    ]
    ax.legend(handles, categories, title="Completeness", loc="lower left", frameon=True)
    ax.set_title("ECDC surveillance completeness metadata, 2023")
    _style_axis(ax)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300)
    plt.close(fig)


def _best_primary_test_predictions(metrics: pd.DataFrame, predictions: pd.DataFrame) -> pd.DataFrame:
    primary = metrics[metrics["split"].eq("primary_test_2023")]
    best = primary.sort_values("mean_wis").iloc[0]
    return predictions[
        predictions["split"].eq("primary_test_2023")
        & predictions["feature_set"].eq(best["feature_set"])
    ].copy()


def _save_predicted_observed_map(countries: gpd.GeoDataFrame, output: Path) -> None:
    vmax = max(
        float(countries["observed_incidence_per_100k"].max()),
        float(countries["predicted_incidence_per_100k"].max()),
    )
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 6.8))
    for ax, column, title in [
        (axes[0], "observed_incidence_per_100k", "Observed incidence, 2023"),
        (axes[1], "predicted_incidence_per_100k", "Predicted median incidence, 2023"),
    ]:
        countries.plot(
            ax=ax,
            column=column,
            cmap="viridis",
            vmin=0,
            vmax=vmax,
            linewidth=0.3,
            edgecolor="#FFFFFF",
            legend=True,
            legend_kwds={"label": "Cases per 100,000", "shrink": 0.62},
        )
        _plot_context(ax, countries)
        ax.set_title(title)
        _style_axis(ax)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300)
    plt.close(fig)


def _write_report(report_path: Path, best_feature_set: str) -> None:
    lines = [
        "# IJHG Map Figure Notes",
        "",
        "Status: generated static country-level geospatial figures for the ECDC-only manuscript path.",
        "",
        "## Methods",
        "",
        "- Boundaries: Natural Earth 1:50m Admin 0 countries.",
        "- Projection: ETRS89 / LAEA Europe (`EPSG:3035`).",
        "- Unit of analysis: country-year; fills are country-level only.",
        "- Palettes: `viridis`, `cividis`, and Okabe-Ito categorical colors for colorblind-safe rendering.",
        "- Primary prediction map uses the best 2023 feature-ablation model by mean WIS: "
        f"`{best_feature_set}`.",
        "",
        "## Generated Figures",
        "",
        "- `figures/ijhg_incidence_choropleth_2023.png`",
        "- `figures/ijhg_surveillance_completeness_2023.png`",
        "- `figures/ijhg_predicted_observed_incidence_2023.png`",
        "- `figures/ijhg_uncertainty_interval_width_2023.png`",
        "",
        "## Caption Guardrail",
        "",
        "Captions should state that maps show country-level reported incidence and model uncertainty; "
        "they should not imply within-country spatial precision.",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--boundaries", default=str(DEFAULT_BOUNDARIES))
    parser.add_argument("--figures", default=str(DEFAULT_FIGURES))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    cases = pd.read_csv(args.cases)
    metrics = pd.read_csv(args.metrics)
    predictions = pd.read_csv(args.predictions)
    cases_2023 = cases[cases["year"].eq(2023)].copy()
    boundaries = _load_boundaries(Path(args.boundaries), cases_2023)
    map_data = boundaries.merge(cases_2023, left_on="join_iso3", right_on="iso3", how="left")

    figure_dir = Path(args.figures)
    _save_single_map(
        map_data,
        "incidence_per_100k",
        "ECDC reported hantavirus incidence, 2023",
        figure_dir / "ijhg_incidence_choropleth_2023.png",
        cmap="viridis",
        legend_label="Reported cases per 100,000",
    )
    _save_completeness_map(map_data, figure_dir / "ijhg_surveillance_completeness_2023.png")

    best_predictions = _best_primary_test_predictions(metrics, predictions)
    best_feature_set = str(best_predictions["feature_set"].iloc[0])
    prediction_map = map_data.merge(
        best_predictions[
            ["iso3", "q50", "q95", "q05", "observed"]
        ],
        on="iso3",
        how="left",
        suffixes=("", "_prediction"),
    )
    prediction_map["observed_incidence_per_100k"] = (
        prediction_map["observed"] / prediction_map["population"] * 100_000
    )
    prediction_map["predicted_incidence_per_100k"] = (
        prediction_map["q50"] / prediction_map["population"] * 100_000
    )
    prediction_map["interval_width_per_100k"] = (
        (prediction_map["q95"] - prediction_map["q05"]) / prediction_map["population"] * 100_000
    )
    _save_predicted_observed_map(
        prediction_map,
        figure_dir / "ijhg_predicted_observed_incidence_2023.png",
    )
    _save_single_map(
        prediction_map,
        "interval_width_per_100k",
        "Prediction interval width, 2023",
        figure_dir / "ijhg_uncertainty_interval_width_2023.png",
        cmap="cividis",
        legend_label="90 percent interval width per 100,000",
    )
    _write_report(Path(args.report), best_feature_set)

    print(f"Wrote IJHG maps to {figure_dir}")
    print(f"Wrote map notes to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
