"""Markov-chain incidence-state simulation for paper stress tests.

This module is intentionally descriptive. It estimates incidence-state
transitions from observed country-year reported incidence, then simulates
plausible future reported-case distributions. It is not a substitute for
external validation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


STATE_LABELS = ("zero", "low", "high")


@dataclass(frozen=True)
class MarkovSimulationResult:
    transition_matrix: pd.DataFrame
    state_thresholds: dict[str, float]
    simulation_summary: pd.DataFrame


def assign_incidence_states(data: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    """Assign zero/low/high states from reported incidence per 100,000."""
    working = data.copy()
    if "incidence_per_100k" not in working:
        working["incidence_per_100k"] = working["cases"] / working["population"] * 100_000

    positive = working.loc[working["incidence_per_100k"] > 0, "incidence_per_100k"]
    if positive.empty:
        low_high_cut = 0.0
    else:
        low_high_cut = float(positive.median())

    working["incidence_state"] = np.select(
        [
            working["incidence_per_100k"] <= 0,
            working["incidence_per_100k"] <= low_high_cut,
        ],
        ["zero", "low"],
        default="high",
    )
    return working, {"zero_cut": 0.0, "low_high_cut": low_high_cut}


def estimate_transition_matrix(data: pd.DataFrame, smoothing: float = 1.0) -> pd.DataFrame:
    """Estimate a smoothed one-year incidence-state transition matrix."""
    if smoothing < 0:
        raise ValueError("smoothing must be nonnegative")

    state_data, _ = assign_incidence_states(data)
    counts = pd.DataFrame(smoothing, index=STATE_LABELS, columns=STATE_LABELS)
    for _, group in state_data.sort_values(["iso3", "year"]).groupby("iso3"):
        states = group["incidence_state"].tolist()
        for current_state, next_state in zip(states, states[1:]):
            counts.loc[current_state, next_state] += 1.0
    return counts.div(counts.sum(axis=1), axis=0)


def simulate_next_year(
    data: pd.DataFrame,
    n_simulations: int = 5000,
    reporting_multiplier: float = 1.0,
    random_seed: int = 20260512,
) -> MarkovSimulationResult:
    """Simulate next-year reported cases by country from incidence-state transitions."""
    if n_simulations <= 0:
        raise ValueError("n_simulations must be positive")
    if reporting_multiplier <= 0:
        raise ValueError("reporting_multiplier must be positive")

    state_data, thresholds = assign_incidence_states(data)
    transition = estimate_transition_matrix(state_data)
    latest = state_data.sort_values("year").groupby("iso3", as_index=False).tail(1)

    state_rates = (
        state_data.groupby("incidence_state")["incidence_per_100k"]
        .agg(["mean", "std"])
        .reindex(STATE_LABELS)
        .fillna(0.0)
    )
    rng = np.random.default_rng(random_seed)
    rows = []
    for _, country in latest.iterrows():
        current_state = country["incidence_state"]
        probabilities = transition.loc[current_state].to_numpy(dtype=float)
        sampled_states = rng.choice(STATE_LABELS, size=n_simulations, p=probabilities)
        simulated_counts = np.zeros(n_simulations, dtype=float)
        for state in STATE_LABELS:
            state_mask = sampled_states == state
            if not state_mask.any():
                continue
            mean_rate = max(float(state_rates.loc[state, "mean"]) * reporting_multiplier, 0.0)
            mean_count = mean_rate / 100_000 * float(country["population"])
            simulated_counts[state_mask] = rng.poisson(mean_count, size=int(state_mask.sum()))

        rows.append(
            {
                "iso3": country["iso3"],
                "country": country["country"],
                "source_system": country["source_system"],
                "current_state": current_state,
                "reporting_multiplier": reporting_multiplier,
                "mean_cases": float(np.mean(simulated_counts)),
                "median_cases": float(np.quantile(simulated_counts, 0.5)),
                "q05_cases": float(np.quantile(simulated_counts, 0.05)),
                "q95_cases": float(np.quantile(simulated_counts, 0.95)),
                "prob_any_case": float(np.mean(simulated_counts > 0)),
                "prob_above_current": float(np.mean(simulated_counts > country["cases"])),
            }
        )

    return MarkovSimulationResult(
        transition_matrix=transition,
        state_thresholds=thresholds,
        simulation_summary=pd.DataFrame.from_records(rows),
    )
