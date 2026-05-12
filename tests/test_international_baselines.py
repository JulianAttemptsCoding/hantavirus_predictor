import pandas as pd

from hantavirus_predictor.models.international_baselines import generate_baseline_forecasts


def test_generate_baseline_forecasts_outputs_quantiles_and_metrics():
    data = pd.DataFrame(
        {
            "iso3": ["AAA", "AAA", "AAA", "BBB", "BBB", "BBB"],
            "country": ["A", "A", "A", "B", "B", "B"],
            "region": ["Europe"] * 6,
            "syndrome": ["hantavirus_infection"] * 6,
            "source_system": ["ECDC"] * 6,
            "year": [2019, 2020, 2021, 2019, 2020, 2021],
            "cases": [1, 2, 3, 0, 1, 0],
            "population": [100_000] * 6,
            "rural_population_pct": [50] * 6,
            "gdp_per_capita_current_usd": [10_000] * 6,
        }
    )

    bundle = generate_baseline_forecasts(data, [2021])

    assert set(bundle.predictions["quantile"]) == {0.05, 0.5, 0.95}
    assert {"mean_wis", "coverage_90", "brier_any_case"}.issubset(bundle.metrics.columns)
