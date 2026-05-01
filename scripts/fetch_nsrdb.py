"""Fetch NSRDB hourly weather for NIST Ground-1 (PVDAQ System 4902) and cache locally.

Reads ``NREL_API_KEY`` and ``NREL_EMAIL`` from the environment or from a ``.env``
file at the capstone repo root. Pulls one calendar year per API call (2014-2018)
via ``pvlib.iotools.get_nsrdb_psm4_conus`` and writes a single concatenated
parquet to ``data/nsrdb_nist_4902_hourly.parquet``.

Run from anywhere:
    python scripts/fetch_nsrdb.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pandas as pd
from pvlib.iotools import get_nsrdb_psm4_conus

# NIST Ground-1 / PVDAQ System 4902 (Gaithersburg, MD) — matches CONFIG in the notebook.
LATITUDE  = 39.1319
LONGITUDE = -77.2141
YEARS     = list(range(2014, 2019))  # 2014..2018 inclusive
PARAMS    = [
    'air_temperature', 'dew_point', 'relative_humidity',
    'ghi', 'dni', 'dhi', 'clearsky_ghi', 'clearsky_dni', 'clearsky_dhi',
    'cloud_type', 'surface_albedo', 'surface_pressure',
    'wind_direction', 'wind_speed',
]

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH  = REPO_ROOT / 'data' / 'nsrdb_nist_4902_hourly.parquet'


def load_dotenv(path: Path) -> None:
    """Minimal .env loader — sets os.environ from KEY=VALUE lines, no quotes assumed."""
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, val = line.partition('=')
        key, val = key.strip(), val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


def main() -> int:
    load_dotenv(REPO_ROOT / '.env')
    api_key = os.environ.get('NREL_API_KEY')
    email   = os.environ.get('NREL_EMAIL')
    if not api_key or not email:
        print('ERROR: set NREL_API_KEY and NREL_EMAIL (env or .env file).',
              file=sys.stderr)
        return 1

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    frames = []
    for year in YEARS:
        print(f'[{year}] requesting NSRDB PSM4 CONUS …', flush=True)
        df, meta = get_nsrdb_psm4_conus(
            latitude=LATITUDE,
            longitude=LONGITUDE,
            api_key=api_key,
            email=email,
            year=year,
            time_step=60,           # hourly
            parameters=PARAMS,
            map_variables=True,
            utc=False,              # local standard time, matches PVDAQ convention
        )
        print(f'[{year}] {len(df):,} rows  cols={list(df.columns)[:6]}…',
              flush=True)
        frames.append(df)
        time.sleep(1)               # be polite to the API

    combined = pd.concat(frames).sort_index()
    # Drop any leap-day duplicates that span year boundaries.
    combined = combined[~combined.index.duplicated(keep='first')]
    combined.to_parquet(OUT_PATH)
    print(f'\nwrote {OUT_PATH}  ({len(combined):,} rows, '
          f'{combined.index.min()} → {combined.index.max()})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
