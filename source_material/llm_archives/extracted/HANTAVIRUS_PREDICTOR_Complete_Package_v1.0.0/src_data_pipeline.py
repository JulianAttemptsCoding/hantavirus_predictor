"""
Hantavirus Data Pipeline
Files: src/data/ingestion.py, src/data/features.py, src/data/augmentation.py
"""

# ============ ingestion.py ============

import os
import requests
import pandas as pd
import numpy as np
import xarray as xr
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CDCDataIngestor:
    """Ingest CDC NNDSS hantavirus case data."""

    BASE_URL = "https://wonder.cdc.gov/controller/datarequest/D76"

    def __init__(self, output_dir: str = "data/raw/cdc"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_cases(self, years: List[int]) -> pd.DataFrame:
        """Fetch hantavirus cases by year from CDC WONDER.

        Note: CDC WONDER requires manual query submission. This method
        reads pre-downloaded CSV files. For automation, use the
        CDC WONDER API or request bulk data access.
        """
        frames = []
        for year in years:
            filepath = self.output_dir / f"cdc_hanta_{year}.csv"
            if filepath.exists():
                df = pd.read_csv(filepath)
                df["year"] = year
                frames.append(df)
            else:
                logger.warning(f"File not found: {filepath}")

        if not frames:
            raise FileNotFoundError("No CDC data files found. Download from CDC WONDER.")

        return pd.concat(frames, ignore_index=True)

    def process_cases(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize CDC case data."""
        df = df.rename(columns={
            "County Code": "county_fips",
            "County": "county_name",
            "Cases": "cases",
            "Deaths": "deaths"
        })
        df["county_fips"] = df["county_fips"].astype(str).str.zfill(5)
        df["date"] = pd.to_datetime(df["year"].astype(str) + "-01-01")
        df = df.sort_values(["county_fips", "date"])
        return df


class NEONDataIngestor:
    """Ingest NEON small mammal trapping data."""

    API_BASE = "https://data.neonscience.org/api/v0"

    def __init__(self, output_dir: str = "data/raw/neon", api_token: Optional[str] = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.api_token = api_token
        self.headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}

    def fetch_small_mammal_data(self, site_ids: List[str], 
                                 start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch small mammal trapping data from NEON API.

        Product: DP1.10072.001 (Small mammal box trapping)
        """
        all_data = []

        for site_id in site_ids:
            url = f"{self.API_BASE}/data/DP1.10072.001/{site_id}"
            params = {
                "startDate": start_date,
                "endDate": end_date,
                "package": "basic"
            }

            try:
                response = requests.get(url, params=params, headers=self.headers, timeout=60)
                response.raise_for_status()
                data = response.json()

                # Parse trapping data
                if "data" in data and "files" in data["data"]:
                    for file_info in data["data"]["files"]:
                        if "pertrapnight" in file_info["name"]:
                            file_url = file_info["url"]
                            df = pd.read_csv(file_url)
                            df["site_id"] = site_id
                            all_data.append(df)

            except Exception as e:
                logger.error(f"Error fetching {site_id}: {e}")
                continue

        if not all_data:
            raise RuntimeError("No NEON data retrieved")

        return pd.concat(all_data, ignore_index=True)

    def compute_seroprevalence(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute monthly seroprevalence by site."""
        df["collectDate"] = pd.to_datetime(df["collectDate"])
        df["year_month"] = df["collectDate"].dt.to_period("M")

        # Seroprevalence = positive tests / total tested
        sero = df.groupby(["site_id", "year_month"]).agg({
            "testResult": lambda x: (x == "Positive").sum(),
            "tagID": "nunique"
        }).reset_index()

        sero.columns = ["site_id", "year_month", "positive", "total_tested"]
        sero["seroprevalence"] = sero["positive"] / (sero["total_tested"] + 1e-8)
        sero["year_month"] = sero["year_month"].dt.to_timestamp()

        return sero


class MODISDataIngestor:
    """Ingest MODIS NDVI and LST data."""

    def __init__(self, output_dir: str = "data/raw/modis"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_modis(self, product: str, tiles: List[str], 
                       dates: List[str], username: str, password: str) -> List[Path]:
        """Download MODIS HDF files from NASA LP DAAC.

        Args:
            product: e.g., "MOD13Q1" (NDVI) or "MOD11A1" (LST)
            tiles: List of MODIS tile IDs, e.g., ["h09v05", "h10v05"]
            dates: List of dates in "YYYY-MM-DD" format
            username: NASA Earthdata username
            password: NASA Earthdata password
        """
        from subprocess import run

        downloaded = []
        for date_str in dates:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            year = date.year
            doy = date.timetuple().tm_yday

            for tile in tiles:
                filename = f"{product}.A{year}{doy:03d}.{tile}.061.*.hdf"
                url = f"https://e4ftl01.cr.usgs.gov/MOLT/{product}.061/{date_str}/{filename}"

                output_path = self.output_dir / filename
                if not output_path.exists():
                    cmd = [
                        "wget", "--user", username, "--password", password,
                        "-P", str(self.output_dir), url
                    ]
                    run(cmd, capture_output=True)

                downloaded.append(output_path)

        return downloaded

    def process_ndvi(self, hdf_files: List[Path], 
                     bounds: Optional[Tuple[float, float, float, float]] = None) -> xr.Dataset:
        """Process MODIS NDVI HDF files to xarray Dataset."""
        datasets = []

        for hdf_file in hdf_files:
            if not hdf_file.exists():
                continue

            # Open with rasterio
            ds = xr.open_dataset(hdf_file, engine="rasterio")

            # Extract NDVI band (scale factor = 0.0001)
            if "250m 16 days NDVI" in ds:
                ndvi = ds["250m 16 days NDVI"] * 0.0001
                ndvi = ndvi.where(ndvi > -0.2)  # Filter invalid
                ndvi = ndvi.where(ndvi < 1.0)
                datasets.append(ndvi.to_dataset(name="NDVI"))

        if not datasets:
            raise ValueError("No valid NDVI data found")

        combined = xr.concat(datasets, dim="time")
        combined = combined.sortby("time")

        if bounds:
            minx, miny, maxx, maxy = bounds
            combined = combined.sel(
                x=slice(minx, maxx),
                y=slice(maxy, miny)
            )

        return combined


class ERA5DataIngestor:
    """Ingest ERA5 reanalysis data from Copernicus CDS."""

    def __init__(self, output_dir: str = "data/raw/era5"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_era5(self, variables: List[str], years: List[int],
                      months: List[int], area: List[float],
                      output_file: str) -> Path:
        """Download ERA5 data via CDS API.

        Requires: pip install cdsapi
        Requires: ~/.cdsapirc with API key

        Args:
            variables: e.g., ["2m_temperature", "total_precipitation"]
            years: e.g., [2014, 2015, 2016]
            months: e.g., [1, 2, ..., 12]
            area: [N, W, S, E] bounding box
            output_file: output NetCDF filename
        """
        try:
            import cdsapi
        except ImportError:
            raise ImportError("Install cdsapi: pip install cdsapi")

        client = cdsapi.Client()

        output_path = self.output_dir / output_file

        if output_path.exists():
            logger.info(f"ERA5 file already exists: {output_path}")
            return output_path

        request = {
            "product_type": "reanalysis",
            "variable": variables,
            "year": [str(y) for y in years],
            "month": [f"{m:02d}" for m in months],
            "day": [f"{d:02d}" for d in range(1, 32)],
            "time": [f"{h:02d}:00" for h in range(24)],
            "area": area,
            "format": "netcdf"
        }

        client.retrieve(
            "reanalysis-era5-single-levels",
            request,
            str(output_path)
        )

        return output_path

    def compute_monthly_aggregates(self, ds: xr.Dataset) -> xr.Dataset:
        """Compute monthly mean temperature and total precipitation."""
        monthly = ds.resample(time="1MS").mean()

        # For precipitation, sum instead of mean
        if "tp" in monthly:
            monthly["tp"] = ds["tp"].resample(time="1MS").sum() * 1000  # m -> mm

        return monthly


# ============ features.py ============

class FeatureEngineer:
    """Engineer features for hantavirus prediction."""

    LAG_CONFIG = {
        "ndvi": [6, 12, 18, 24],
        "precip": [12, 18, 24],
        "soil_temp_april": [24],
        "sunshine_sep": [24],
        "soil_temp_sep": [12],
        "cases": [1, 2, 3, 6, 12],
        "seroprevalence": [1, 3, 6, 12]
    }

    def __init__(self, lag_config: Optional[Dict] = None):
        self.lag_config = lag_config or self.LAG_CONFIG

    def create_lag_features(self, df: pd.DataFrame, 
                            group_col: str = "county_fips") -> pd.DataFrame:
        """Create lagged features for time series forecasting."""
        df = df.copy()
        df = df.sort_values([group_col, "date"])

        for var, lags in self.lag_config.items():
            if var not in df.columns:
                continue
            for lag in lags:
                df[f"{var}_lag{lag}m"] = df.groupby(group_col)[var].shift(lag)

        return df

    def create_rolling_features(self, df: pd.DataFrame, 
                                group_col: str = "county_fips",
                                windows: List[int] = [3, 6, 12]) -> pd.DataFrame:
        """Create rolling mean/std features."""
        df = df.copy()

        for var in ["ndvi", "precip", "cases"]:
            if var not in df.columns:
                continue
            for window in windows:
                df[f"{var}_roll_mean_{window}m"] = (
                    df.groupby(group_col)[var]
                    .rolling(window, min_periods=1)
                    .mean()
                    .reset_index(0, drop=True)
                )
                df[f"{var}_roll_std_{window}m"] = (
                    df.groupby(group_col)[var]
                    .rolling(window, min_periods=1)
                    .std()
                    .reset_index(0, drop=True)
                )

        return df

    def create_climate_indices(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add ENSO, PDO, NAO indices."""
        # These would be merged from external sources
        # For now, placeholder
        df["enso_oni"] = 0.0  # Merge from NOAA
        df["pdo_index"] = 0.0  # Merge from JISAO
        df["nao_index"] = 0.0  # Merge from NCAR
        return df

    def create_exposure_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create human-rodent contact exposure index."""
        # Composite index from SVI, rurality, housing age
        components = []
        for col in ["svi_overall", "rurality_code", "housing_age"]:
            if col in df.columns:
                components.append(df[col])

        if components:
            df["exposure_index"] = np.mean(components, axis=0)
        else:
            df["exposure_index"] = 0.5

        return df

    def create_target_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create binary outbreak labels and count targets."""
        # Outbreak: cases > 95th percentile within county
        df["outbreak_threshold"] = df.groupby("county_fips")["cases"].transform(
            lambda x: x.quantile(0.95)
        )
        df["is_outbreak"] = (df["cases"] > df["outbreak_threshold"]).astype(int)

        # Log-transform counts for stability
        df["log_cases"] = np.log1p(df["cases"])

        return df


# ============ augmentation.py ============

class SyntheticDataGenerator:
    """Generate synthetic SEIR trajectories for pretraining."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)

    def sample_parameters(self, n_samples: int) -> List[Dict]:
        """Sample biologically plausible parameter sets."""
        params_list = []

        for _ in range(n_samples):
            params = {
                "beta_m": self.rng.uniform(0.01, 0.5),
                "beta_f": self.rng.uniform(0.005, 0.2),
                "gamma_m": self.rng.uniform(1/60, 1/14),
                "gamma_f": self.rng.uniform(1/45, 1/10),
                "delta": self.rng.uniform(1/21, 1/7),
                "a": self.rng.uniform(0.005, 0.02),
                "c": self.rng.uniform(5e-5, 5e-4),
                "b": self.rng.uniform(0.05, 0.2),
                "K": self.rng.uniform(100, 10000),
                "initial_infected_m": self.rng.randint(1, 50),
                "initial_infected_f": self.rng.randint(1, 50),
                "t_max": 730,
                "dt": 1.0
            }
            params_list.append(params)

        return params_list

    def generate_trajectory(self, params: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """Generate a single SEIR trajectory."""
        from scipy.integrate import solve_ivp

        def seir_rhs(t, y, p):
            S_m, E_m, I_m, R_m, S_f, E_f, I_f, R_f = y
            N_m = S_m + E_m + I_m + R_m
            N_f = S_f + E_f + I_f + R_f
            N = N_m + N_f

            beta_m, beta_f = p["beta_m"], p["beta_f"]
            beta_mf = (beta_m + beta_f) / 2.0
            gamma_m, gamma_f = p["gamma_m"], p["gamma_f"]
            delta = p["delta"]
            a, c, b = p["a"], p["c"], p["b"]
            K = p["K"]

            d_N = a + c * N
            B = 2 * b * (N_m * N_f) / (N_m + N_f + 1e-8)

            dS_m = B/2 - S_m * d_N - S_m * (beta_m * I_m + beta_mf * I_f)
            dE_m = S_m * (beta_m * I_m + beta_mf * I_f) - delta * E_m - E_m * d_N
            dI_m = delta * E_m - gamma_m * I_m - I_m * d_N
            dR_m = gamma_m * I_m - R_m * d_N

            dS_f = B/2 - S_f * d_N - S_f * (beta_mf * I_m + beta_f * I_f)
            dE_f = S_f * (beta_mf * I_m + beta_f * I_f) - delta * E_f - E_f * d_N
            dI_f = delta * E_f - gamma_f * I_f - I_f * d_N
            dR_f = gamma_f * I_f - R_f * d_N

            return [dS_m, dE_m, dI_m, dR_m, dS_f, dE_f, dI_f, dR_f]

        K = params["K"]
        I_m0 = params["initial_infected_m"]
        I_f0 = params["initial_infected_f"]
        S_m0 = K * 0.45 - I_m0
        S_f0 = K * 0.45 - I_f0

        y0 = [S_m0, 0, I_m0, 0, S_f0, 0, I_f0, 0]
        t_span = [0, params["t_max"]]
        t_eval = np.arange(0, params["t_max"], params["dt"])

        sol = solve_ivp(
            lambda t, y: seir_rhs(t, y, params),
            t_span, y0, t_eval=t_eval, method='RK45', rtol=1e-6
        )

        # Add observation noise
        noise = self.rng.normal(0, 0.01, sol.y.shape)
        y_noisy = sol.y + noise
        y_noisy = np.maximum(y_noisy, 0)  # Ensure non-negative

        return sol.t, y_noisy

    def generate_dataset(self, n_trajectories: int = 10000,
                        output_path: Optional[str] = None) -> pd.DataFrame:
        """Generate full synthetic dataset."""
        params_list = self.sample_parameters(n_trajectories)

        records = []
        for i, params in enumerate(params_list):
            t, y = self.generate_trajectory(params)

            for j, time_point in enumerate(t):
                record = {
                    "trajectory_id": i,
                    "time": time_point,
                    "S_m": y[0, j], "E_m": y[1, j], "I_m": y[2, j], "R_m": y[3, j],
                    "S_f": y[4, j], "E_f": y[5, j], "I_f": y[6, j], "R_f": y[7, j],
                    **params
                }
                records.append(record)

        df = pd.DataFrame(records)

        if output_path:
            df.to_parquet(output_path, compression="zstd")
            logger.info(f"Saved synthetic dataset to {output_path}")

        return df
