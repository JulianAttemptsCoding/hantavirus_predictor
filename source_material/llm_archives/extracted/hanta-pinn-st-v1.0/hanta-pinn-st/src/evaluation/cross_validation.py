"""
Spatiotemporal cross-validation for epidemic forecasting.
Prevents data leakage across time and space.
"""
import numpy as np
from sklearn.model_selection import BaseCrossValidator


class SpatiotemporalBlockCV(BaseCrossValidator):
    """
    Block cross-validation that respects temporal and spatial structure.

    - Temporal: Rolling origin with configurable train/gap/test windows
    - Spatial: Leave-one-biome-out for spatial generalization testing
    """
    def __init__(self, n_splits=5, train_years=5, gap_years=0, 
                 test_years=1, spatial_groups=None):
        super().__init__()
        self.n_splits = n_splits
        self.train_years = train_years
        self.gap_years = gap_years
        self.test_years = test_years
        self.spatial_groups = spatial_groups

    def split(self, X, y=None, groups=None):
        """
        Generate train/test indices.

        Args:
            X: DataFrame with 'year' and optional 'biome' columns
            y: unused (for sklearn compatibility)
            groups: unused
        """
        years = sorted(X['year'].unique())

        for fold in range(self.n_splits):
            # Determine temporal windows
            test_start_idx = fold
            test_end_idx = min(test_start_idx + self.test_years, len(years))

            test_years_list = years[test_start_idx:test_end_idx]
            train_end_idx = max(0, test_start_idx - self.gap_years)
            train_years_list = years[max(0, train_end_idx - self.train_years):train_end_idx]

            # Temporal mask
            train_mask = X['year'].isin(train_years_list)
            test_mask = X['year'].isin(test_years_list)

            # Spatial mask (if groups provided)
            if self.spatial_groups is not None and 'biome' in X.columns:
                # Leave-one-biome-out
                held_out_biome = self.spatial_groups[fold % len(self.spatial_groups)]
                train_mask = train_mask & (X['biome'] != held_out_biome)
                test_mask = test_mask & (X['biome'] == held_out_biome)

            train_idx = X[train_mask].index.values
            test_idx = X[test_mask].index.values

            if len(train_idx) > 0 and len(test_idx) > 0:
                yield train_idx, test_idx

    def get_n_splits(self, X=None, y=None, groups=None):
        return self.n_splits


class RollingOriginCV(BaseCrossValidator):
    """
    Simple rolling origin temporal cross-validation.
    """
    def __init__(self, min_train_size=52, step=12, horizon=12):
        self.min_train_size = min_train_size
        self.step = step
        self.horizon = horizon

    def split(self, X, y=None, groups=None):
        n = len(X)
        indices = np.arange(n)

        start = self.min_train_size
        while start + self.horizon <= n:
            train_idx = indices[:start]
            test_idx = indices[start:start + self.horizon]
            yield train_idx, test_idx
            start += self.step

    def get_n_splits(self, X=None, y=None, groups=None):
        n = len(X)
        return max(0, (n - self.min_train_size - self.horizon) // self.step + 1)
