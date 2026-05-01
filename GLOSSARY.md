# Glossary

A plain-English reference for the technical terms used in
`Solar_PV_Forecasting.ipynb`. Skim this if anything in the
notebook reads as acronym-heavy — most entries are one or two sentences.

Grouped by topic for browsability; alphabetical within each group.

---

## Solar PV physics & instrumentation

**AC power (`ac_power_kw`)** — Alternating-current electrical output of the
solar inverter, measured in kilowatts. The *target variable* this notebook
is trying to predict.

**AOI — Angle of Incidence** — The angle between the sun's rays and the
direction the solar panel is pointing. At AOI = 0° the sun is hitting the
panel face-on (maximum power); at 90° the sun is grazing the panel surface
(no power). Computed in §7 from sun position + panel tilt/azimuth.

**Array** — A collection of PV panels wired together. The NIST Ground-1
array is rated 270.7 kW.

**Azimuth** — Compass direction the panels face. South-facing (180°) is
optimal in the Northern Hemisphere.

**Capacity / nameplate** — The maximum rated power output of a PV system
under standard test conditions (1000 W/m² irradiance, 25 °C cell temp).
For System 4902, capacity = 270.7 kW.

**Clear-sky POA (`clear_sky_poa`)** — A *modeled* value of what POA
irradiance *would be* if the sky were perfectly clear, computed from
sun position and atmospheric turbidity (Ineichen model in §7).
Acts as the physical ceiling for measured POA.

**Clear-sky index (`clear_sky_index`)** — Ratio `measured POA / clear-sky POA`.
Equals 1.0 when the sky is empty, drops toward 0 under heavy cloud cover.
A direct quantification of cloud-driven irradiance attenuation.

**DC power (`dc_power_kw`)** — Direct-current power produced by the panels
*before* the inverter converts it to AC. Always ≥ AC power (inverter
efficiency loss, typically ~5%).

**DHI — Diffuse Horizontal Irradiance** — Sunlight that has been scattered
by the atmosphere and arrives at a horizontal surface from all sky directions.
Dominates on overcast days.

**DNI — Direct Normal Irradiance** — Sunlight arriving in a straight beam
from the sun, measured on a surface perpendicular to that beam. Dominates
on clear days.

**Fixed-tilt array** — Panels mounted at a permanent tilt angle (no tracking).
The NIST Ground-1 array is fixed at 20° tilt facing south.

**GHI — Global Horizontal Irradiance** — Total solar irradiance reaching
a horizontal surface (DHI + DNI × cos(zenith angle)). The standard "how sunny
is it?" measurement.

**IAM — Incidence Angle Modifier** — Correction factor accounting for
reflection losses when sunlight hits the panel at an oblique angle (high AOI).
Mentioned in references [3]; not used directly in this notebook but related
to the AOI feature.

**Inverter** — Electronic device that converts DC power from the panels into
grid-compatible AC power. Introduces ~5% conversion loss.

**Irradiance** — Solar power per unit area, measured in W/m². The fundamental
input to PV power production.

**Module** — A single PV panel. Modules are wired together into arrays.

**Module temperature (`temp_module_c`)** — Surface temperature of the panel
itself. Always ≥ ambient when the panel is producing (panels heat up under
sun). PV efficiency drops ~0.4 % per °C above the 25 °C reference.

**Nowcast** — A short-horizon forecast (typically 0–6 hours) that combines
the current state of the atmosphere with a near-term prediction of how it
will evolve. In this notebook, the full Ridge model is a same-time nowcast
diagnostic, not an operational forecast.

**POA — Plane-of-Array irradiance (`poa_irradiance_wm2`)** — Solar irradiance
hitting the *tilted panel surface*, not the horizontal ground. The most
directly relevant irradiance measurement for PV output. Measured by
pyranometers mounted in the plane of the panels.

**Pyranometer** — Instrument that measures broadband solar irradiance
(W/m²) at the location it's mounted. The NIST site uses two redundant
POA pyranometers; we average them in §4.3.

**PV — Photovoltaic** — Technology that converts sunlight directly into
electricity. The system this notebook forecasts.

**Solar elevation** — Angle of the sun above the horizon, in degrees.
0° = on the horizon (sunrise/sunset), 90° = directly overhead.

**Solar zenith** — Angle between straight up and the sun, the complement
of elevation (zenith = 90° − elevation).

**Tilt** — Angle of the panels relative to horizontal ground.
NIST Ground-1 tilt = 20°.

---

## Time series & statistics

**ACF — Autocorrelation Function** — Plot of how correlated a time series
is with itself at increasing lags. For PV power, the ACF shows large
spikes at lags 24, 48, 72 hours — the daily cycle. Computed in §6.6.

**ADF — Augmented Dickey-Fuller test** — Statistical test for whether a
time series has a "unit root" (trending behavior that does not mean-revert).
Used in §6.6 to test stationarity.

**Cyclical encoding** — Using sin/cos transformations of time (e.g., hour,
day-of-year) so that the model treats 23:00 and 00:00 as adjacent rather
than as the most-distant points on a number line. Used in §7.4.

**Differencing** — Subtracting each value from a previous value to remove
trend or seasonality. *Seasonal differencing* at lag 24 (`y[t] - y[t-24]`)
removes the daily cycle from PV power. Required for SARIMAX (§6.6).

**Diurnal** — "Daily-cycle" — the regular within-day variation in a quantity.
Solar PV is overwhelmingly diurnal.

**Exogenous variable** — In SARIMAX terminology, an external regressor used
to predict the target — distinct from the target's own lagged values.
Examples here: cloud cover, temperature, AOI. (The "X" in SARIMAX stands
for eXogenous.)

**Forward-fill (`ffill`)** — Imputation method that propagates the last
known value forward. Used in §9.2 to project hourly Open-Meteo data onto
the 15-min PVDAQ cadence.

**Interpolation** — Estimating a missing value from its neighbors.
Linear time-interpolation in §4.1 fills small sensor gaps.

**IQR — Interquartile Range** — The middle 50 % of a distribution
(75th percentile − 25th percentile). Used with the 1.5 × IQR "fence" rule
[13] to flag statistical outliers in §5.3.

**Lag** — A time offset. "Lag 24 (hours)" means "the value 24 hours ago".

**MA — Moving Average (in ARMA terms)** — A model component that uses past
*forecast errors* to predict the current value. Order *q* in SARIMAX.

**MAPE — Mean Absolute Percentage Error** — Average percentage error
between predicted and actual. Reported in §10 only on daytime samples
(AC > 10 kW) to avoid divide-by-zero at night.

**MAE — Mean Absolute Error** — Average of the absolute gaps between
predicted and actual, in the original units (kW).

**Pearson r** — Correlation coefficient between two variables, ranging
−1 (perfect inverse) through 0 (uncorrelated) to +1 (perfect positive).
POA vs AC power has r = 0.98.

**PACF — Partial Autocorrelation Function** — ACF after partialling out
the influence of all shorter lags. Identifies the order *p* of the AR
component in SARIMAX. Computed in §6.6.

**Percentile / quartile** — A percentile is the value below which a given
percentage of observations fall (e.g., the 25th percentile = "25 % of
values are below this"). Quartiles are the 25 / 50 / 75 percentiles.

**Quartile (Q1, Q3)** — Q1 = 25th percentile, Q3 = 75th percentile.
Used in IQR.

**R² — Coefficient of Determination** — Fraction of the variance in the
target that the model explains. R² = 1 is a perfect fit; R² = 0 means
the model is no better than predicting the mean.

**Residual** — The gap between the observed value and the model's
prediction (`actual − predicted`). Residual diagnostics in §10.2 expose
where the model systematically under- or over-predicts.

**RMSE — Root-Mean-Square Error** — Square-root of the mean squared
residual, in the same units as the target (kW). Penalizes large errors
more than small ones; the *primary* metric in §10.

**Seasonal decomposition** — Splitting a time series into trend +
seasonal + residual components. Used in §6.2 with `period = 96` to
isolate the 24 h diurnal cycle from the multi-day weather envelope.

**SARIMAX — Seasonal ARIMA with eXogenous regressors** — Classical time
series model. Notation: `SARIMAX(p, d, q) × (P, D, Q, s)` with optional
exogenous regressors. Order selection is done in §6.6; the model itself
is planned for follow-on work.

**Stationarity** — A time series is *stationary* if its statistical
properties (mean, variance, autocorrelation) do not change over time.
SARIMAX requires stationarity, which is achieved here via lag-24
seasonal differencing (§6.6).

**Stochastic** — Random / probabilistic — governed by a probability
distribution rather than fully determined by inputs. Cloud cover, wind,
and short-term temperature swings are stochastic outputs of weather, so
the irradiance and panel temperature that drive PV power inherit that
randomness. Used in the README rationale to motivate why a *regularized*
linear model is needed at all.

**Trend** — The slow-varying component of a time series — in §6.2,
the multi-day weather regime that remains after removing the daily cycle.

**Tukey's fence rule** — Standard outlier definition: any value beyond
Q1 − 1.5 × IQR or Q3 + 1.5 × IQR is flagged as a "tail" point.
Origin: Tukey 1977 [13].

**Unit root** — A property of non-stationary time series; informally,
"shocks do not decay". The ADF test in §6.6 tests for this.

---

## Machine learning models & evaluation

**Ablation** — Removing a feature (or set of features) from a model to
measure how much it contributed. §9.1 ablates measured POA; §9.2 then
adds back NWP-equivalent inputs.

**Baseline** — A simple model used as a comparison point for more complex
models. Ridge in §9 is the initial baseline.

**Coefficient (Ridge)** — The weight assigned to each feature by the
regression. After standardization, the magnitude of the coefficient is
directly comparable across features (§11 top-15 chart).

**Cross-validation (TimeSeriesSplit)** — Repeatedly training on an
expanding window of past data and validating on the immediately
following block, instead of random folds. Avoids leakage in time-series
problems. Out of scope for this initial submission; planned for follow-on
work.

**Feature** — A predictor variable input to the model. The notebook
uses 14 features: 7 weather/geometry, 5 cyclical-time, 2 interactions.

**Holdout** — The portion of the data reserved exclusively for final
evaluation, never used during training. Here the test set = the most
recent 20 % of the timeline.

**Hyperparameter** — A model setting chosen by the practitioner (vs
learned from data). For Ridge, the regularization strength `alpha` = 1.0.

**Lasso** — Linear regression using L1 regularization, which drives some
coefficients exactly to zero (automatic feature selection). Planned for
follow-on work.

**Leakage** — When a model accidentally gets information about the answer
through its features, inflating evaluation scores. Avoided here by
excluding `dc_power_kw` and any lag/rolling stats of the target.

**LSTM — Long Short-Term Memory** — A type of recurrent neural network
designed to handle long sequences. Planned for follow-on work.

**Nowcast vs forecast** — Nowcast: predict the present or next few hours
from current atmospheric information. Forecast: predict a future horizon.
The Ridge baseline in §9 is a same-time nowcast diagnostic; §9.2 is
deployment-realistic because it removes on-site sensors and uses
NWP-equivalent inputs.

**Pipeline** — Sequence of preprocessing + modeling steps applied
together. Here: `StandardScaler` (fit on train) → `Ridge`.

**Random Forest** — Ensemble model averaging many decision trees. Planned
for follow-on work as a non-linear baseline.

**Regularization** — Penalty added to the loss function to prevent
overfitting. Ridge uses L2 (sum of squared coefficients); Lasso uses L1.

**Ridge regression** — Linear regression with L2 regularization. Robust
to correlated predictors, which are common in this feature set. Used as the §9
baseline.

**StandardScaler** — Subtracts the mean and divides by the std-dev so
each feature has mean 0 and variance 1. Required for Ridge so the
regularization penalty applies fairly across features. Fit on train only.

**Train / test split** — Partitioning the data so the model learns from
one slice (train) and is evaluated on a never-seen slice (test).
Time-series split: train = older 80 %, test = newer 20 % (§8).

**XGBoost — eXtreme Gradient Boosting** — Tree-based ensemble that
sequentially fits trees to the residuals of the previous tree.
Planned for follow-on work as the expected top performer.

---

## Data sources & weather forecasting

**ERA5** — ECMWF's global atmospheric *reanalysis* — a best estimate of
historical weather computed by re-running NWP models with all observations
that were available after the fact. Higher quality than real-time forecast,
since it's hindsight. Used by Open-Meteo to power its historical API.

**Forecast skill (or just "skill")** — Predictive accuracy of a model,
typically expressed relative to a reference baseline (persistence,
climatology, or — in this report — the variance ceiling of the full Ridge
nowcast). When the README rationale says "how much skill survives," it
means how much R² remains when on-site sensors are replaced with ERA5/NWP
proxies; the §9 → §9.2 drop from R² 0.977 → 0.815 quantifies the loss.

**HRRR — High-Resolution Rapid Refresh** — NOAA's 3 km operational NWP
model over CONUS, updated hourly. Mentioned in §12 as a follow-on
candidate for NWP-quality cloud cover.

**NIST Ground-1** — Reference name for PVDAQ System 4902. Located on
the NIST Gaithersburg, MD campus.

**NREL — National Renewable Energy Laboratory** — U.S. Department of
Energy lab that hosts PVDAQ and NSRDB.

**NSRDB — National Solar Radiation Database** — NREL's authoritative
satellite-derived irradiance + weather dataset for U.S. sites.
Now exposed via the PSM4 GOES CONUS endpoint (2018+ only) — which is
why this submission falls back to Open-Meteo / ERA5 for the 2014–2017 portion
of the PVDAQ window.

**NWP — Numerical Weather Prediction** — Physics-based atmospheric
modeling that produces forecasts (e.g., GFS, HRRR). The "available
at deployment time" baseline of weather information.

**Open-Meteo** — Free, no-key-required weather API (free tier; optional
customer key). Backed by ERA5 reanalysis for historical data. Used in
this submission to supply cloud cover, GHI/DNI/DHI, temperature, wind,
humidity, and surface pressure for the §9.2 forecast-realistic Ridge.

**PSM4** — The current NSRDB v4 endpoint (GOES satellite-derived).
CONUS variant covers 2018+; earlier years require legacy products that
NREL has since deprecated.

**PVDAQ — Photovoltaic Data Acquisition** — NREL's public archive of
high-cadence PV plant performance data. The source of the
`nist_ground_4902_15min.parquet` file used here.

**Reanalysis** — A "best estimate" of historical weather produced by
running an NWP model with all observations that were eventually
available, including those that arrived after real-time. ERA5 is a
reanalysis. Higher quality than the real-time forecast it would have
produced at the time.

---

## Notebook tools & methodology

**CRISP-DM — Cross-Industry Standard Process for Data Mining** — A
six-phase methodology (Business Understanding → Data Understanding →
Data Preparation → Modeling → Evaluation → Deployment) used to structure
this notebook. The Table of Contents groups sections by CRISP-DM phase
and each top-level heading carries a phase tag.

**Jupyter notebook (`.ipynb`)** — Interactive document mixing markdown
text, executable code cells, and rendered output (plots, tables).
The format used for this entire submission.

**Matplotlib** — Foundational Python plotting library. All static plots
in the notebook.

**NumPy** — Core Python numerical / array library. Underpins everything.

**pandas** — Tabular data manipulation library; the notebook's primary
data structure is the `pandas.DataFrame`.

**Parquet** — Compressed columnar file format (`*.parquet`). Used for
both the PVDAQ cache and the Open-Meteo cache because it loads ~5×
faster than CSV at ~1/8 the file size.

**pvlib** — Open-source Python library for solar-energy modeling.
Used in §7 to compute solar position, AOI, and clear-sky POA.

**scikit-learn** — Python machine-learning library. Provides Ridge,
StandardScaler, train/test utilities, and the metric functions used
in §10.

**Seaborn** — Statistical-plotting library built on Matplotlib.
Used for the §6.4 correlation heatmap.

**statsmodels** — Python statistical-modeling library. Provides
`seasonal_decompose` (§6.2), `adfuller`, `plot_acf`, `plot_pacf` (§6.6),
and (planned for follow-on work) `SARIMAX`.
