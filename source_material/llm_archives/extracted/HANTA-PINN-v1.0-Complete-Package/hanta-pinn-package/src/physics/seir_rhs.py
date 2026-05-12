"""Pure SEIR ODE right-hand side for synthetic data generation and validation."""
import numpy as np
from scipy.integrate import solve_ivp


def hantavirus_seir(t, y, params):
    """
    Sex-structured SEIR ODE right-hand side.

    Args:
        t: time (unused, for solve_ivp compatibility)
        y: [S_m, E_m, I_m, R_m, S_f, E_f, I_f, R_f]
        params: dict with keys beta_m, beta_mf, beta_f, gamma_m, gamma_f, delta, a, c, b, K

    Returns:
        dy_dt: [dS_m, dE_m, dI_m, dR_m, dS_f, dE_f, dI_f, dR_f]
    """
    S_m, E_m, I_m, R_m, S_f, E_f, I_f, R_f = y
    N_m = S_m + E_m + I_m + R_m
    N_f = S_f + E_f + I_f + R_f
    N_R = N_m + N_f
    K = params['K']

    # Density-dependent mortality
    d_N = params['a'] + params['c'] * N_R / K

    # Harmonic birth
    if N_m + N_f > 0:
        B = 2 * params['b'] * N_m * N_f / (N_m + N_f)
    else:
        B = 0

    # Forces of infection
    lambda_m = params['beta_m'] * I_m + params['beta_mf'] * I_f
    lambda_f = params['beta_mf'] * I_m + params['beta_f'] * I_f

    # ODEs
    dS_m = B / 2 - S_m * d_N - S_m * lambda_m
    dE_m = S_m * lambda_m - E_m * d_N - params['delta'] * E_m
    dI_m = params['delta'] * E_m - I_m * d_N - params['gamma_m'] * I_m
    dR_m = params['gamma_m'] * I_m - R_m * d_N

    dS_f = B / 2 - S_f * d_N - S_f * lambda_f
    dE_f = S_f * lambda_f - E_f * d_N - params['delta'] * E_f
    dI_f = params['delta'] * E_f - I_f * d_N - params['gamma_f'] * I_f
    dR_f = params['gamma_f'] * I_f - R_f * d_N

    return [dS_m, dE_m, dI_m, dR_m, dS_f, dE_f, dI_f, dR_f]


def generate_synthetic_trajectory(K=1000, t_max=365*5, **param_overrides):
    """Generate a single synthetic SEIR trajectory."""
    params = {
        'beta_m': np.random.uniform(0.01, 0.05),
        'beta_mf': np.random.uniform(0.005, 0.02),
        'beta_f': np.random.uniform(0.001, 0.01),
        'gamma_m': np.random.uniform(1/40, 1/20),
        'gamma_f': np.random.uniform(1/30, 1/15),
        'delta': 1/14,
        'a': 0.001,
        'c': np.random.uniform(1e-4, 1e-3),
        'b': np.random.uniform(0.005, 0.02),
        'K': K
    }
    params.update(param_overrides)

    y0 = [K/2 * 0.9, 0, K/2 * 0.1, 0, K/2 * 0.9, 0, K/2 * 0.1, 0]
    t_eval = np.arange(0, t_max, 7)

    sol = solve_ivp(
        hantavirus_seir, [0, t_max], y0,
        args=(params,), t_eval=t_eval, method='RK45'
    )

    # Add noise
    states = sol.y.T + np.random.normal(0, 5, size=sol.y.T.shape)
    states = np.clip(states, 0, None)

    return {
        't': t_eval,
        'states': states,
        'params': params,
        'seroprev': (states[:, 2] + states[:, 6]) / states.sum(axis=1)
    }


def generate_synthetic_dataset(n=10000, t_max=365*5, seed=42):
    """Generate full synthetic dataset for pretraining."""
    np.random.seed(seed)
    trajectories = []
    for _ in range(n):
        K = np.random.uniform(500, 5000)
        traj = generate_synthetic_trajectory(K=K, t_max=t_max)
        trajectories.append(traj)
    return trajectories
