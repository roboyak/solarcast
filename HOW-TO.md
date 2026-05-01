# HOW-TO

This repo is intentionally small: one notebook, cached data files, and a few
helper scripts.

## 1. Create the environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Run the smoke check

```bash
python scripts/reproduce.py smoke
```

This verifies imports, parquet readability, data coverage, and a tiny Ridge
baseline without executing the full notebook.

## 3. Execute the notebook

```bash
python scripts/reproduce.py notebook
```

This writes `Solar_PV_Forecasting.executed.ipynb` and leaves the committed
notebook untouched.

## 4. Rebuild optional data caches

Open-Meteo / ERA5 reanalysis cache:

```bash
python scripts/reproduce.py fetch-openmeteo
```

Optional NSRDB / PSM4 weather cache:

```bash
cp .env.example .env
# fill in NREL_API_KEY and NREL_EMAIL
python scripts/reproduce.py fetch-nsrdb
```

The committed notebook uses the cached parquet files already in `data/`, so
fetching is only needed when rebuilding the dataset from source.
