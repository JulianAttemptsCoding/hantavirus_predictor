"""
HantaST-PINN-FM: Evaluation & Statistical Validation
File: src/evaluation/metrics.py, src/evaluation/significance.py
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import binom_test, ttest_1samp
from typing import Dict, List, Tuple, Optional
import warnings


# ============ metrics.py ============

class ForecastMetrics:
    """Comprehensive forecast evaluation metrics."""

    @staticmethod
    def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Mean Absolute Error."""
        return np.mean(np.abs(y_true - y_pred))

    @staticmethod
    def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Root Mean Squared Error."""
        return np.sqrt(np.mean((y_true - y_pred) ** 2))

    @staticmethod
    def mape(y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-8) -> float:
        """Mean Absolute Percentage Error."""
        mask = y_true > epsilon
        if not mask.any():
            return np.nan
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / (y_true[mask] + epsilon))) * 100

    @staticmethod
    def crps(y_true: np.ndarray, y_samples: np.ndarray) -> float:
        """Continuous Ranked Probability Score.

        Args:
            y_true: [N] observed values
            y_samples: [N, M] Monte Carlo samples from predictive distribution
        """
        N, M = y_samples.shape

        # Sort samples
        y_sorted = np.sort(y_samples, axis=1)

        # Compute empirical CDF
        alpha = (np.arange(M) + 0.5) / M

        # CRPS = integral (F(y) - 1_{y >= obs})^2 dy
        crps_values = np.zeros(N)
        for i in range(N):
            F = np.mean(y_samples[i] <= y_sorted[i], axis=0)
            indicator = (y_sorted[i] >= y_true[i]).astype(float)
            crps_values[i] = np.trapz((F - indicator) ** 2, y_sorted[i])

        return np.mean(crps_values)

    @staticmethod
    def wis(y_true: np.ndarray, y_quantiles: np.ndarray, 
            alphas: Optional[List[float]] = None) -> float:
        """Weighted Interval Score (Bracher et al. 2021).

        Args:
            y_true: [N] observed values
            y_quantiles: [N, K] predicted quantiles (symmetric, including median)
            alphas: [K//2] confidence levels (e.g., [0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5])
        """
        if alphas is None:
            alphas = [0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]

        N, K = y_quantiles.shape
        assert K == 2 * len(alphas) + 1, "Quantiles must be symmetric around median"

        scores = []

        for k, alpha in enumerate(alphas):
            lower = y_quantiles[:, k]
            upper = y_quantiles[:, -(k + 1)]

            # Interval score
            interval_width = upper - lower
            penalty_lower = (2 / alpha) * (lower - y_true) * (y_true < lower)
            penalty_upper = (2 / alpha) * (y_true - upper) * (y_true > upper)

            iscore = interval_width + penalty_lower + penalty_upper
            w_k = alpha / 2
            scores.append(w_k * iscore)

        # Median term
        median = y_quantiles[:, len(alphas)]
        scores.append(0.5 * np.abs(y_true - median))

        return np.mean(np.sum(scores, axis=0))

    @staticmethod
    def coverage(y_true: np.ndarray, lower: np.ndarray, upper: np.ndarray,
                 alpha: float = 0.1) -> float:
        """Empirical coverage probability.

        Args:
            y_true: [N] observed values
            lower: [N] lower prediction bound
            upper: [N] upper prediction bound
            alpha: nominal miscoverage rate (default 0.1 for 90% PI)
        """
        covered = (y_true >= lower) & (y_true <= upper)
        return np.mean(covered)

    @staticmethod
    def mpiw(lower: np.ndarray, upper: np.ndarray) -> float:
        """Mean Prediction Interval Width."""
        return np.mean(upper - lower)

    @staticmethod
    def brier_score(y_true: np.ndarray, y_prob: np.ndarray) -> float:
        """Brier score for probabilistic binary predictions."""
        return np.mean((y_prob - y_true) ** 2)

    @staticmethod
    def roc_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
        """ROC-AUC for binary classification."""
        from sklearn.metrics import roc_auc_score
        return roc_auc_score(y_true, y_score)

    @staticmethod
    def pr_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
        """PR-AUC for imbalanced binary classification."""
        from sklearn.metrics import average_precision_score
        return average_precision_score(y_true, y_score)

    @staticmethod
    def morans_i(residuals: np.ndarray, weights_matrix: np.ndarray) -> float:
        """Moran's I for spatial autocorrelation.

        Args:
            residuals: [N] model residuals
            weights_matrix: [N, N] spatial weights
        """
        N = len(residuals)
        z = residuals - np.mean(residuals)

        numerator = np.sum(weights_matrix * np.outer(z, z))
        denominator = np.sum(z ** 2)
        W = np.sum(weights_matrix)

        return (N / W) * (numerator / denominator)

    @classmethod
    def compute_all(cls, y_true: np.ndarray, y_pred: np.ndarray,
                    y_lower: Optional[np.ndarray] = None,
                    y_upper: Optional[np.ndarray] = None,
                    y_prob: Optional[np.ndarray] = None) -> Dict[str, float]:
        """Compute all metrics at once."""
        metrics = {
            "MAE": cls.mae(y_true, y_pred),
            "RMSE": cls.rmse(y_true, y_pred),
            "MAPE": cls.mape(y_true, y_pred),
        }

        if y_lower is not None and y_upper is not None:
            metrics["Coverage_90"] = cls.coverage(y_true, y_lower, y_upper, alpha=0.1)
            metrics["MPIW"] = cls.mpiw(y_lower, y_upper)

        if y_prob is not None:
            metrics["Brier"] = cls.brier_score((y_true > 0).astype(int), y_prob)

        return metrics


# ============ significance.py ============

class StatisticalTests:
    """Statistical significance tests for model comparison."""

    @staticmethod
    def diebold_mariano(y_true: np.ndarray, pred_a: np.ndarray, 
                        pred_b: np.ndarray, loss: str = "mse",
                        h: int = 1) -> Dict:
        """Diebold-Mariano test for forecast accuracy comparison.

        H0: Models A and B have equal forecast accuracy
        H1: Model A is significantly better than B (if t_stat < 0)

        Args:
            y_true: [T] observed values
            pred_a: [T] predictions from model A
            pred_b: [T] predictions from model B
            loss: "mse" or "mae"
            h: forecast horizon (for HAC standard error)
        """
        T = len(y_true)

        if loss == "mse":
            d = (y_true - pred_a) ** 2 - (y_true - pred_b) ** 2
        elif loss == "mae":
            d = np.abs(y_true - pred_a) - np.abs(y_true - pred_b)
        elif loss == "wis":
            # Requires quantile predictions - simplified
            d = np.abs(y_true - pred_a) - np.abs(y_true - pred_b)
        else:
            raise ValueError(f"Unknown loss: {loss}")

        # Mean loss differential
        d_bar = np.mean(d)

        # HAC variance estimator (Newey-West)
        gamma_0 = np.var(d, ddof=1)

        # Autocovariances up to lag h-1
        var_adjusted = gamma_0
        for lag in range(1, h):
            gamma_lag = np.cov(d[:-lag], d[lag:])[0, 1]
            weight = 1 - lag / h
            var_adjusted += 2 * weight * gamma_lag

        # Test statistic
        se = np.sqrt(var_adjusted / T)
        t_stat = d_bar / se

        # Two-tailed p-value
        p_value = 2 * (1 - stats.t.cdf(np.abs(t_stat), df=T - 1))

        return {
            "d_bar": d_bar,
            "t_stat": t_stat,
            "p_value": p_value,
            "better_model": "A" if d_bar < 0 else "B",
            "significant": p_value < 0.05
        }

    @staticmethod
    def clarke_test(y_true: np.ndarray, pred_a: np.ndarray, 
                    pred_b: np.ndarray) -> Dict:
        """Clarke test for pairwise model dominance.

        Non-parametric test based on sign of loss differential.
        """
        d = np.abs(y_true - pred_a) - np.abs(y_true - pred_b)

        n_plus = np.sum(d < 0)   # A better than B
        n_minus = np.sum(d > 0)  # B better than A
        n_total = n_plus + n_minus

        if n_total == 0:
            return {"n_plus": 0, "n_minus": 0, "p_value": 1.0, "significant": False}

        # Binomial test under H0: p = 0.5
        p_value = binom_test(n_plus, n_total, p=0.5)

        return {
            "n_plus": int(n_plus),
            "n_minus": int(n_minus),
            "n_total": int(n_total),
            "p_value": p_value,
            "better_model": "A" if n_plus > n_minus else "B",
            "significant": p_value < 0.05
        }

    @staticmethod
    def wilcoxon_signed_rank(y_true: np.ndarray, pred_a: np.ndarray,
                             pred_b: np.ndarray) -> Dict:
        """Wilcoxon signed-rank test for paired forecast errors."""
        err_a = np.abs(y_true - pred_a)
        err_b = np.abs(y_true - pred_b)

        diff = err_a - err_b

        # Remove zeros
        diff = diff[diff != 0]

        if len(diff) == 0:
            return {"statistic": 0, "p_value": 1.0, "significant": False}

        statistic, p_value = stats.wilcoxon(diff)

        return {
            "statistic": statistic,
            "p_value": p_value,
            "better_model": "A" if np.median(diff) < 0 else "B",
            "significant": p_value < 0.05
        }

    @staticmethod
    def mcb_test(y_true: np.ndarray, predictions: Dict[str, np.ndarray],
                 alpha: float = 0.05) -> Dict:
        """Model Confidence Set (Hansen et al. 2011).

        Identifies the set of models that are not significantly worse
        than the best model.

        Args:
            y_true: [T] observed values
            predictions: Dict[str, [T]] model predictions
            alpha: confidence level
        """
        model_names = list(predictions.keys())
        n_models = len(model_names)
        T = len(y_true)

        # Compute loss for each model
        losses = {}
        for name, pred in predictions.items():
            losses[name] = (y_true - pred) ** 2

        # Relative performance
        d_ij = np.zeros((T, n_models, n_models))
        for i, name_i in enumerate(model_names):
            for j, name_j in enumerate(model_names):
                d_ij[:, i, j] = losses[name_i] - losses[name_j]

        # Bootstrap confidence intervals
        n_bootstrap = 1000
        bootstrap_stats = np.zeros((n_bootstrap, n_models))

        for b in range(n_bootstrap):
            idx = np.random.choice(T, size=T, replace=True)
            d_boot = d_ij[idx]

            for i in range(n_models):
                # Average relative loss vs all others
                rel_loss = np.mean([np.mean(d_boot[:, i, j]) 
                                   for j in range(n_models) if j != i])
                bootstrap_stats[b, i] = rel_loss

        # Compute p-values
        p_values = {}
        for i, name in enumerate(model_names):
            p_values[name] = np.mean(bootstrap_stats[:, i] >= 0)

        # Model confidence set
        mcs = [name for name, p in p_values.items() if p > alpha]

        return {
            "p_values": p_values,
            "mcs": mcs,
            "best_model": model_names[np.argmin([np.mean(losses[n]) for n in model_names])]
        }


class CalibrationDiagnostics:
    """Calibration assessment for probabilistic forecasts."""

    @staticmethod
    def reliability_diagram(y_true: np.ndarray, y_prob: np.ndarray,
                           n_bins: int = 10) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compute reliability diagram data.

        Returns:
            bin_centers: [n_bins] bin centers
            observed_freq: [n_bins] observed frequency in each bin
            predicted_freq: [n_bins] mean predicted probability in each bin
        """
        bin_edges = np.linspace(0, 1, n_bins + 1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        observed_freq = np.zeros(n_bins)
        predicted_freq = np.zeros(n_bins)
        bin_counts = np.zeros(n_bins)

        for i in range(n_bins):
            mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])
            if i == n_bins - 1:  # Include right edge
                mask = (y_prob >= bin_edges[i]) & (y_prob <= bin_edges[i + 1])

            if mask.sum() > 0:
                observed_freq[i] = y_true[mask].mean()
                predicted_freq[i] = y_prob[mask].mean()
                bin_counts[i] = mask.sum()

        return bin_centers, observed_freq, predicted_freq

    @staticmethod
    def calibration_slope_intercept(y_true: np.ndarray, 
                                    y_prob: np.ndarray) -> Dict:
        """Fit calibration curve and report slope/intercept."""
        from sklearn.linear_model import LogisticRegression

        # Fit isotonic regression or logistic calibration
        X = y_prob.reshape(-1, 1)

        # Platt scaling (logistic calibration)
        model = LogisticRegression()
        model.fit(X, y_true)

        # Slope and intercept of calibrated probabilities
        # logit(p_cal) = a + b * logit(p_raw)
        # Approximate: use linear regression on logit scale

        # Avoid logit(0) and logit(1)
        eps = 1e-8
        p_clipped = np.clip(y_prob, eps, 1 - eps)
        logit_p = np.log(p_clipped / (1 - p_clipped))

        # Fit linear model: y_true ~ logit_p
        from sklearn.linear_model import LinearRegression
        lr = LinearRegression()
        lr.fit(logit_p.reshape(-1, 1), y_true)

        return {
            "slope": lr.coef_[0],
            "intercept": lr.intercept_,
            "r2": lr.score(logit_p.reshape(-1, 1), y_true)
        }

    @staticmethod
    def pit_histogram(y_true: np.ndarray, y_samples: np.ndarray,
                     n_bins: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """Probability Integral Transform histogram.

        For well-calibrated forecasts, PIT values should be uniform.
        """
        # Compute empirical CDF at observed values
        pits = np.mean(y_samples <= y_true.reshape(-1, 1), axis=1)

        # Histogram
        counts, bin_edges = np.histogram(pits, bins=n_bins, range=(0, 1))
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        return bin_centers, counts / len(pits)


class AblationStudy:
    """Systematic ablation of model components."""

    COMPONENT_CONFIGS = {
        "full": {"use_pinn": True, "use_fm": True, "use_stgat": True, "use_physics": True},
        "no_pinn": {"use_pinn": False, "use_fm": True, "use_stgat": True, "use_physics": False},
        "no_fm": {"use_pinn": True, "use_fm": False, "use_stgat": True, "use_physics": True},
        "no_stgat": {"use_pinn": True, "use_fm": True, "use_stgat": False, "use_physics": True},
        "no_physics": {"use_pinn": True, "use_fm": True, "use_stgat": True, "use_physics": False},
        "baseline_xgb": {"model": "xgboost"},
        "baseline_sarima": {"model": "sarima"},
        "baseline_lstm": {"model": "lstm"}
    }

    def __init__(self, base_config: Dict):
        self.base_config = base_config

    def run(self, data_module, test_data) -> pd.DataFrame:
        """Run all ablation configurations and compare."""
        results = []

        for name, config in self.COMPONENT_CONFIGS.items():
            print(f"Running ablation: {name}")

            # Modify config
            modified_config = self._modify_config(self.base_config, config)

            # Train and evaluate
            # (Placeholder - actual implementation would train model)
            metrics = self._evaluate_config(modified_config, data_module, test_data)

            results.append({
                "config": name,
                **metrics
            })

        return pd.DataFrame(results)

    def _modify_config(self, base: Dict, modifications: Dict) -> Dict:
        """Apply modifications to base config."""
        import copy
        config = copy.deepcopy(base)
        config.update(modifications)
        return config

    def _evaluate_config(self, config: Dict, data_module, test_data) -> Dict:
        """Evaluate a single configuration."""
        # Placeholder - would actually train and evaluate
        return {
            "MAE": 0.0,
            "RMSE": 0.0,
            "WIS": 0.0,
            "Coverage": 0.0
        }
