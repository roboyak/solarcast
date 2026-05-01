"""Fast repository smoke check.

This is intentionally smaller than a full notebook execution. It verifies that
the pinned environment can import the required stack, the cached parquet files
are readable, the Open-Meteo reanalysis window spans the PVDAQ window, and a
tiny Ridge baseline can fit without shape or preprocessing surprises.
"""
from __future__ import annotations

import importlib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


REPO_ROOT = Path(__file__).resolve().parents[1]
PVDAQ_PATH = REPO_ROOT / "data" / "nist_ground_4902_15min.parquet"
OPENMETEO_PATH = REPO_ROOT / "data" / "openmeteo_nist_4902_hourly.parquet"

REQUIRED_MODULES = [
    "numpy",
    "pandas",
    "pyarrow",
    "matplotlib",
    "seaborn",
    "sklearn",
    "statsmodels",
    "pvlib",
    "requests",
    "nbconvert",
]

PVDAQ_REQUIRED_COLUMNS = {
    "ac_power_kw",
    "dc_power_kw",
    "poa_irradiance_wm2",
    "poa_irradiance2_wm2",
    "temp_ambient_c",
    "temp_ambient2_c",
    "temp_module_c",
    "wind_speed_ms",
    "wind_speed2_ms",
}

OPENMETEO_REQUIRED_COLUMNS = {
    "cloud_cover",
    "cloud_cover_low",
    "cloud_cover_mid",
    "cloud_cover_high",
    "shortwave_radiation",
    "direct_normal_irradiance",
    "diffuse_radiation",
    "temperature_2m",
    "windspeed_10m",
    "relative_humidity_2m",
    "surface_pressure",
}


def assert_imports() -> None:
    missing = [name for name in REQUIRED_MODULES if importlib.util.find_spec(name) is None]
    if missing:
        raise RuntimeError(f"Missing required modules: {', '.join(missing)}")


def load_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_parquet(path)
    if "measured_on" in df.columns:
        df["measured_on"] = pd.to_datetime(df["measured_on"])
        df = df.set_index("measured_on")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(f"{path.name} must have a DatetimeIndex or measured_on column")
    if not df.index.is_monotonic_increasing:
        raise ValueError(f"{path.name} index is not sorted")
    return df


def assert_data_contracts(pvdaq: pd.DataFrame, openmeteo: pd.DataFrame) -> None:
    missing_pvdaq = PVDAQ_REQUIRED_COLUMNS.difference(pvdaq.columns)
    missing_om = OPENMETEO_REQUIRED_COLUMNS.difference(openmeteo.columns)
    if missing_pvdaq:
        raise ValueError(f"PVDAQ missing columns: {sorted(missing_pvdaq)}")
    if missing_om:
        raise ValueError(f"Open-Meteo missing columns: {sorted(missing_om)}")
    if openmeteo.index.min() > pvdaq.index.min() or openmeteo.index.max() < pvdaq.index.max():
        raise ValueError("Open-Meteo coverage does not span the PVDAQ window")


def fit_tiny_baseline(pvdaq: pd.DataFrame) -> float:
    df = pvdaq.copy()
    df["poa_irradiance_wm2"] = df[["poa_irradiance_wm2", "poa_irradiance2_wm2"]].mean(axis=1)
    df["temp_ambient_c"] = df[["temp_ambient_c", "temp_ambient2_c"]].mean(axis=1)
    df["wind_speed_ms"] = df[["wind_speed_ms", "wind_speed2_ms"]].mean(axis=1)

    hour = df.index.hour + df.index.minute / 60.0
    df["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    df["hour_cos"] = np.cos(2 * np.pi * hour / 24)

    cols = [
        "poa_irradiance_wm2",
        "temp_ambient_c",
        "temp_module_c",
        "wind_speed_ms",
        "hour_sin",
        "hour_cos",
    ]
    work = df[["ac_power_kw", *cols]].dropna().head(8000)
    split_idx = int(len(work) * 0.8)
    train = work.iloc[:split_idx]
    test = work.iloc[split_idx:]

    model = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
    model.fit(train[cols], train["ac_power_kw"])
    pred = np.clip(model.predict(test[cols]), 0, 270.7)
    r2 = float(r2_score(test["ac_power_kw"], pred))
    if r2 < 0.65:
        raise AssertionError(f"Tiny Ridge baseline R2 too low: {r2:.3f}")
    return r2


def main() -> int:
    assert_imports()
    pvdaq = load_frame(PVDAQ_PATH)
    openmeteo = load_frame(OPENMETEO_PATH)
    assert_data_contracts(pvdaq, openmeteo)
    r2 = fit_tiny_baseline(pvdaq)

    print("Smoke check passed")
    print(f"  PVDAQ rows:      {len(pvdaq):,}")
    print(f"  Open-Meteo rows: {len(openmeteo):,}")
    print(f"  Tiny Ridge R2:   {r2:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
