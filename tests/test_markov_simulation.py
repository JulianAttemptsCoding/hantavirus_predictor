import pandas as pd

from hantavirus_predictor.simulations.markov_incidence import (
    estimate_transition_matrix,
    simulate_next_year,
)


def test_transition_matrix_rows_sum_to_one():
    data = pd.DataFrame(
        {
            "iso3": ["AAA", "AAA", "AAA", "BBB", "BBB", "BBB"],
            "country": ["A", "A", "A", "B", "B", "B"],
            "year": [2021, 2022, 2023, 2021, 2022, 2023],
            "cases": [0, 2, 4, 1, 0, 1],
            "population": [100_000] * 6,
        }
    )

    transition = estimate_transition_matrix(data)

    assert transition.sum(axis=1).round(10).eq(1.0).all()


def test_simulate_next_year_outputs_country_rows():
    data = pd.DataFrame(
        {
            "iso3": ["AAA", "AAA", "BBB", "BBB"],
            "country": ["A", "A", "B", "B"],
            "source_system": ["ECDC"] * 4,
            "year": [2022, 2023, 2022, 2023],
            "cases": [0, 3, 1, 0],
            "population": [100_000] * 4,
        }
    )

    result = simulate_next_year(data, n_simulations=100, random_seed=1)

    assert len(result.simulation_summary) == 2
    assert {"prob_any_case", "prob_above_current"}.issubset(result.simulation_summary.columns)
