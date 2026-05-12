import pytest
import numpy as np
import pandas as pd
from src.data.pipeline import FeatureEngineer, SyntheticDataGenerator


class TestFeatureEngineer:
    def test_lag_features(self):
        df = pd.DataFrame({
            "county_fips": ["001"] * 12,
            "date": pd.date_range("2020-01", periods=12, freq="MS"),
            "cases": range(12),
            "ndvi": np.random.randn(12)
        })

        fe = FeatureEngineer()
        result = fe.create_lag_features(df)

        assert "cases_lag1m" in result.columns
        assert "cases_lag6m" in result.columns
        assert "cases_lag12m" in result.columns
        assert result["cases_lag1m"].iloc[1] == 0
        assert result["cases_lag6m"].iloc[6] == 0

    def test_outbreak_label(self):
        df = pd.DataFrame({
            "county_fips": ["001"] * 100,
            "cases": np.random.poisson(2, 100)
        })

        fe = FeatureEngineer()
        result = fe.create_target_variables(df)

        assert "is_outbreak" in result.columns
        assert result["is_outbreak"].dtype == int
        assert result["is_outbreak"].sum() > 0


class TestSyntheticDataGenerator:
    def test_trajectory_generation(self):
        gen = SyntheticDataGenerator(seed=42)
        params = {
            "beta_m": 0.1, "beta_f": 0.03,
            "gamma_m": 1/30, "gamma_f": 1/21,
            "delta": 1/14, "a": 0.01, "c": 1e-4,
            "b": 0.1, "K": 1000,
            "initial_infected_m": 10, "initial_infected_f": 5,
            "t_max": 100, "dt": 1.0
        }

        t, y = gen.generate_trajectory(params)

        assert len(t) == 100
        assert y.shape == (8, 100)
        assert np.all(y >= 0)  # Non-negative
        assert np.all(y.sum(axis=0) > 0)  # Population persists

    def test_dataset_generation(self):
        gen = SyntheticDataGenerator(seed=42)
        df = gen.generate_dataset(n_trajectories=10)

        assert len(df) > 0
        assert "trajectory_id" in df.columns
        assert "S_m" in df.columns
        assert df["trajectory_id"].nunique() == 10
