from __future__ import annotations

from test_feature_ablation import _example_panel

from hantavirus_predictor.models.count_models import run_penalized_poisson_models


def test_penalized_poisson_models_emit_metrics() -> None:
    bundle = run_penalized_poisson_models(_example_panel())

    assert not bundle.predictions.empty
    assert not bundle.metrics.empty
    assert not bundle.tuning.empty
    assert {
        "mean_wis",
        "relative_wis_observed_mean",
        "coverage_90",
        "mean_interval_width_90",
        "poisson_deviance",
        "brier_any_case",
    }.issubset(bundle.metrics.columns)
    assert set(bundle.metrics["model"]) == {"penalized_poisson_glm"}
