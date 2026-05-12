"""
Synthetic SEIR-SDE data generator for hantavirus.
Generates biologically plausible trajectories for pre-training.
"""
import numpy as np
import torch
from scipy.integrate import solve_ivp


class SyntheticHantaGenerator:
    """
    Generate synthetic hantavirus trajectories using gender-structured SEIR-SDE.

    Validates against NEON field data moments and literature parameters.
    """
    def __init__(self, n_trajectories=50000, t_max=730, dt=1.0, seed=42):
        self.n_trajectories = n_trajectories
        self.t_max = t_max
        self.dt = dt
        self.n_steps = int(t_max / dt)
        self.rng = np.random.RandomState(seed)

    def sample_params(self):
        """Sample biologically plausible parameters from literature priors."""
        return {
            'beta_m': self.rng.lognormal(-2.3, 0.3),
            'beta_mf': self.rng.lognormal(-2.6, 0.3),
            'beta_f': self.rng.lognormal(-3.2, 0.3),
            'gamma_m': self.rng.lognormal(-3.4, 0.2),
            'gamma_f': self.rng.lognormal(-3.0, 0.2),
            'delta': self.rng.lognormal(-2.0, 0.2),
            'a': self.rng.uniform(0.001, 0.003),
            'c': self.rng.uniform(0.0001, 0.0005),
            'b': self.rng.uniform(0.05, 0.15),
            'K0': self.rng.uniform(500, 5000),
            'alpha_K': self.rng.uniform(0.5, 2.0),
            'sigma': self.rng.uniform(0.01, 0.1),
            'spillover_eff': self.rng.lognormal(-8, 0.5),
        }

    def climate_forcing(self, t, params):
        """Generate synthetic climate forcing (ENSO + seasonal)."""
        enso = 0.5 * np.sin(2 * np.pi * t / 365.25 * 3.5)
        seasonal = 0.3 * np.sin(2 * np.pi * t / 365.25)
        ndvi = params['K0'] * (1 + params['alpha_K'] * (enso + seasonal))
        return np.clip(ndvi, 100, 20000)

    def seir_ode(self, t, y, params):
        """Deterministic SEIR ODE right-hand side."""
        S_m, E_m, I_m, R_m, S_f, E_f, I_f, R_f = y
        N_m = S_m + E_m + I_m + R_m
        N_f = S_f + E_f + I_f + R_f
        N = N_m + N_f

        d_N = params['a'] + params['c'] * N
        B = 2 * params['b'] * N_m * N_f / (N_m + N_f + 1e-10)
        K_t = self.climate_forcing(t, params)
        B = B * np.clip(K_t / (N + 1e-6), 0.5, 2.0)

        beta_mf = 0.74 * params['beta_m']
        lambda_m = params['beta_m'] * I_m + beta_mf * I_f
        lambda_f = beta_mf * I_m + params['beta_f'] * I_f

        dS_m = B / 2 - S_m * d_N - S_m * lambda_m
        dE_m = S_m * lambda_m - E_m * d_N - params['delta'] * E_m
        dI_m = params['delta'] * E_m - I_m * d_N - params['gamma_m'] * I_m
        dR_m = params['gamma_m'] * I_m - R_m * d_N

        dS_f = B / 2 - S_f * d_N - S_f * lambda_f
        dE_f = S_f * lambda_f - E_f * d_N - params['delta'] * E_f
        dI_f = params['delta'] * E_f - I_f * d_N - params['gamma_f'] * I_f
        dR_f = params['gamma_f'] * I_f - R_f * d_N

        return [dS_m, dE_m, dI_m, dR_m, dS_f, dE_f, dI_f, dR_f]

    def add_sde_noise(self, state, params):
        """Add Ito noise to state."""
        noise = np.zeros_like(state)
        for i in range(8):
            noise[i] = params['sigma'] * np.sqrt(max(state[i], 0)) * self.rng.normal()
        return noise

    def simulate_trajectory(self, params=None):
        """Simulate one trajectory with SDE noise."""
        if params is None:
            params = self.sample_params()

        # Initial conditions
        K0 = params['K0']
        y0 = [0.45*K0, 0.025*K0, 0.025*K0, 0, 
              0.45*K0, 0.025*K0, 0.025*K0, 0]

        t_eval = np.linspace(0, self.t_max, self.n_steps)

        # Deterministic solve
        sol = solve_ivp(
            lambda t, y: self.seir_ode(t, y, params),
            [0, self.t_max], y0, t_eval=t_eval, method='RK45'
        )

        trajectory = sol.y.T

        # Add SDE noise (Euler-Maruyama post-hoc)
        for i in range(1, len(trajectory)):
            dt = t_eval[i] - t_eval[i-1]
            noise = self.add_sde_noise(trajectory[i], params)
            trajectory[i] += noise * np.sqrt(dt)
            trajectory[i] = np.clip(trajectory[i], 0, None)

        # Compute human spillover
        I_total = trajectory[:, 2] + trajectory[:, 6]
        N_total = trajectory.sum(axis=1)
        spillover_rate = params['spillover_eff'] * I_total / (N_total + 1e-10)
        human_cases = self.rng.poisson(spillover_rate * 1000)  # per 1000 people

        return {
            'trajectory': trajectory,
            't': t_eval,
            'params': params,
            'human_cases': human_cases,
            'seroprevalence': I_total / (N_total + 1e-10),
            'male_seroprev': trajectory[:, 2] / (trajectory[:, :4].sum(axis=1) + 1e-10),
            'female_seroprev': trajectory[:, 6] / (trajectory[:, 4:].sum(axis=1) + 1e-10),
        }

    def generate(self, n=None):
        """Generate n trajectories."""
        if n is None:
            n = self.n_trajectories

        trajectories = []
        for i in range(n):
            if i % 1000 == 0:
                print(f"Generated {i}/{n} trajectories")
            traj = self.simulate_trajectory()
            trajectories.append(traj)

        return trajectories

    def validate(self, trajectories):
        """
        Validate synthetic data against biological constraints.

        Returns dict of pass/fail tests.
        """
        results = {}

        # 1. Seroprevalence distribution
        all_seroprev = np.concatenate([t['seroprevalence'] for t in trajectories])
        mean_seroprev = np.mean(all_seroprev)
        results['seroprevalence_mean'] = {
            'value': mean_seroprev,
            'target': (0.016, 0.026),  # 2.1% +/- 0.5%
            'pass': 0.016 <= mean_seroprev <= 0.026
        }

        # 2. R0 range
        r0_values = []
        for t in trajectories:
            p = t['params']
            beta_eff = (p['beta_m'] + p['beta_f']) / 2
            gamma_eff = (p['gamma_m'] + p['gamma_f']) / 2
            d_K = p['a'] + p['c'] * p['K0']
            r0 = beta_eff * p['K0'] / (gamma_eff + d_K)
            r0_values.append(r0)

        r0_in_range = np.mean([(1.0 <= r <= 2.5) for r in r0_values])
        results['r0_range'] = {
            'value': r0_in_range,
            'target': 0.95,
            'pass': r0_in_range >= 0.95
        }

        # 3. Sex ratio
        male_prevs = []
        female_prevs = []
        for t in trajectories:
            male_prevs.extend(t['male_seroprev'])
            female_prevs.extend(t['female_seroprev'])

        ratio = np.mean(male_prevs) / (np.mean(female_prevs) + 1e-10)
        results['sex_ratio'] = {
            'value': ratio,
            'target': (3.0, 4.5),
            'pass': 3.0 <= ratio <= 4.5
        }

        # 4. Human case sparsity
        total_cases = sum(t['human_cases'].sum() for t in trajectories)
        mean_cases = total_cases / len(trajectories)
        results['case_sparsity'] = {
            'value': mean_cases,
            'target': (0, 5),
            'pass': mean_cases < 5
        }

        return results
