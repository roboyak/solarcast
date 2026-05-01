"""Fetch hourly historical weather from Open-Meteo for NIST Ground-1 (PVDAQ 4902).

Open-Meteo Historical Weather API is free, requires no API key, and uses ERA5
reanalysis under the hood. Covers 1940–present. We pull the PVDAQ window
(2014-07-29 → 2018-03-14) for the NIST coordinates and cache to
``data/openmeteo_nist_4902_hourly.parquet``.

Run from anywhere::

    python scripts/fetch_openmeteo.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import requests

LATITUDE  = 39.1319
LONGITUDE = -77.2141
START     = '2014-07-29'
END       = '2018-03-15'
TIMEZONE  = 'UTC'   # Pull UTC, then shift -5h to match PVDAQ fixed-offset (Etc/GMT+5).


def load_dotenv(path: Path) -> None:
    """Minimal .env loader — sets os.environ from KEY=VALUE lines."""
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, val = line.partition('=')
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

HOURLY_VARS = [
    'temperature_2m', 'relative_humidity_2m', 'dew_point_2m',
    'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high',
    'shortwave_radiation', 'direct_normal_irradiance', 'diffuse_radiation',
    'direct_radiation',
    'windspeed_10m', 'winddirection_10m',
    'surface_pressure',
    'precipitation', 'rain', 'snowfall',
]

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH  = REPO_ROOT / 'data' / 'openmeteo_nist_4902_hourly.parquet'

FREE_URL     = 'https://archive-api.open-meteo.com/v1/archive'
CUSTOMER_URL = 'https://customer-archive-api.open-meteo.com/v1/archive'


def fetch_chunk(start: str, end: str, api_key: str | None) -> pd.DataFrame:
    params = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'start_date': start,
        'end_date': end,
        'hourly': ','.join(HOURLY_VARS),
        'timezone': TIMEZONE,
    }
    if api_key:
        url = CUSTOMER_URL
        params['apikey'] = api_key
    else:
        url = FREE_URL
    r = requests.get(url, params=params, timeout=120)
    r.raise_for_status()
    payload = r.json()
    df = pd.DataFrame(payload['hourly'])
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time').sort_index()
    return df


def main() -> int:
    load_dotenv(REPO_ROOT / '.env')
    api_key = os.environ.get('OPENMETEO_API_KEY') or None
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    endpoint = 'customer endpoint (with key)' if api_key else 'free endpoint (no key)'
    print(f'Fetching {START} → {END}  for ({LATITUDE}, {LONGITUDE})  via {endpoint} …',
          flush=True)
    df = fetch_chunk(START, END, api_key)

    # PVDAQ uses fixed local-standard time (Etc/GMT+5, no DST).
    # We pulled UTC; shift by -5 hours to align.
    df.index = df.index - pd.Timedelta(hours=5)
    df.index.name = 'measured_on'
    df = df[~df.index.duplicated(keep='first')].sort_index()

    df.to_parquet(OUT_PATH)
    print(f'\nwrote {OUT_PATH}')
    print(f'  rows: {len(df):,}')
    print(f'  range: {df.index.min()} → {df.index.max()}')
    print(f'  columns: {list(df.columns)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
