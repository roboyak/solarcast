# Data Sources

## Primary — NREL PVDAQ System 4902 (NIST Ground-1)

- **Location:** Gaithersburg, MD — 39.1319°N, −77.2141°W, 138 m elevation
- **System:** 270.7 kW fixed ground-mount PV array
- **Cadence / span:** 15-minute, July 2014 → March 2018 (~112,000 rows)
- **Channels:** AC / DC power, dual-redundant POA irradiance, ambient and module temperature, wind
- **License:** Public, Creative Commons via NREL PVDAQ on AWS S3
- **Local file:** `data/nist_ground_4902_15min.parquet`

### Where it lives

| Source | URL |
|---|---|
| OEDI submission page (canonical) | https://data.openei.org/submissions/4568 |
| AWS S3 bucket (raw, partitioned by system_id/year/month/day) | `s3://oedi-data-lake/pvdaq/` |
| Systems metadata index | https://oedi-data-lake.s3.amazonaws.com/pvdaq/csv/systems.csv |
| DOE Data Explorer record | https://www.osti.gov/dataexplorer/biblio/1846021-photovoltaic-data-acquisition-pvdaq-public-datasets |
| OSTI biblio record | https://www.osti.gov/biblio/1846021 |
| data.gov mirror | https://catalog.data.gov/dataset/photovoltaic-data-acquisition-pvdaq-public-datasets |
| openEDI PVDAQ documentation | https://github.com/openEDI/documentation/blob/main/pvdaq.md |
| PVDAQ v3 API docs | https://developer.nrel.gov/docs/solar/pvdaq-v3/ |

### Sister systems at the NIST Gaithersburg site

- **4901** — NIST_Canopy_1
- **4902** — NIST_Ground_1 *(this dataset)*
- **4903** — NIST_Roof_1

Raw data reported at 15-minute increments in ISO 8601, partitioned by `system_id / year / month / day`.

---

## Secondary — Open-Meteo reanalysis (co-located)

- **Local file:** `data/openmeteo_nist_4902_hourly.parquet`
- **Cadence:** hourly, co-located to the NIST Ground-1 coordinates above
- **Source:** Open-Meteo Historical Weather API — https://open-meteo.com/en/docs/historical-weather-api
- **License:** CC BY 4.0 (attribution required)
