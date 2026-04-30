# How `poa_irradiance_wm2` Is Measured

**Site:** NREL PVDAQ System 4902 — NIST Ground-1, Gaithersburg MD

**Array:** five east–west sheds, modules tilted ~20° south

**Local file:** `data/nist_ground_4902_15min.parquet`

---

## What POA Is

**POA = Plane-of-Array irradiance** (W/m²): the solar power density hitting
the *tilted* surface of the PV modules — not the horizontal global (GHI).
POA is the dominant driver of array output, which is why NIST measures it
redundantly with sensors that use different physical principles.

---

## Sensors deployed at NIST Ground-1

All three are mounted **coplanar with the modules** (same 20° tilt, same
azimuth) so they see what the array sees.

| # | Instrument | Type | How it works |
|---|---|---|---|
| 1 | **Kipp & Zonen CMP 21** in a **CVF 3** ventilator | Secondary-standard **thermopile pyranometer** (ISO 9060 Secondary Standard) | Black-coated absorber under two glass domes heats up under sunlight. A thermopile beneath the absorber outputs μV proportional to absorbed broadband flux (≈ 285–2800 nm). The CVF 3 ventilator blows air across the outer dome to suppress dew, frost, and thermal offsets. |
| 2 | **IMT Solar Si-420TC** | Flat-plate **silicon reference cell** | A small mono-Si photodiode-class cell wired across a precision shunt resistor; short-circuit current is linear with irradiance. Spectral response matches the modules themselves, so it captures the band the array actually converts. `TC` = onboard temperature correction. |
| 3 | **Apogee SP-230** | Domed, **heated silicon-cell pyranometer** | Silicon photodiode under a diffuser/dome with cosine correction. An internal resistive heater suppresses dew/frost. Narrower spectral band than the thermopile. |

This redundancy is deliberate:
- The **thermopile** gives the broadband "true" irradiance.
- The **Si cells** track what the modules spectrally see.
- **Agreement or divergence** between them is itself a diagnostic
  (soiling, misalignment, snow, calibration drift).

---

## Signal chain

1. **Raw output**
   - Thermopile: microvolts (μV).
   - Si cells: milliamps across a precision shunt → millivolts.
2. **Datalogger:** Campbell Scientific (per NIST TN 1896) digitizes the
   high-rate stream.
3. **Conversion:** raw signal ÷ **responsivity** (μV per W/m²) → W/m².
4. **Aggregation:** the 15-minute rows in our parquet are downsampled
   from the underlying high-rate stream.

---

## Calibration

- Pyranometers are shipped to **NREL BORCAL** (Broadband Outdoor
  Radiometer Calibration) every **12–24 months**.
- BORCAL produces a **zenith-angle-dependent responsivity table** (every
  2° of solar zenith) with net-IR correction — *not* a single scalar.
- Calibration is therefore applied as a function of solar geometry, not
  a fixed multiplier.

---

## What this means for modeling

- The "**dual-redundant POA**" in our dataset is almost certainly the two
  CMP 21 thermopiles (or one CMP 21 + one Si). **Cross-check them**: a
  persistent gap >> a few percent is a soiling / misalignment /
  calibration-drift signal, not random noise.
- Thermopiles have a slow time constant (~5 s for CMP 21). Fine at
  15-minute cadence, but short cloud transients show up smeared.
- Thermopile vs. module spectral mismatch is real (~1–3%), so do not
  expect `P_ac / G_POA` to be perfectly flat across the year, even on a
  healthy array.
- Si reference cells are the better predictor of module current; the
  thermopile is the better predictor of *energy*.

---

## References

| Source | URL |
|---|---|
| NIST Tech Note 1896 — High-Speed Monitoring of Multiple Grid-Connected PV Arrays (definitive sensor list & wiring) | https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1896.pdf |
| NIST Tech Note 1913 — Weather Station for PV and Building System Research | https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1913.pdf |
| Boyd et al. — High-Speed Monitoring (open-access version of TN 1896) | https://pmc.ncbi.nlm.nih.gov/articles/PMC5489128/ |
| Boyd et al. — Comparative Performance of Three PV Array Configurations (uses this exact dataset) | https://pmc.ncbi.nlm.nih.gov/articles/PMC5769486/ |
| Sandia PVPMC — Plane of Array Irradiance (concept primer) | https://pvpmc.sandia.gov/modeling-guide/1-weather-design-inputs/plane-of-array-poa-irradiance/ |
| NREL — Optical Radiation Measurements for PV: Instrumentation (thermopile vs. Si physics) | https://docs.nrel.gov/docs/gen/fy04/36321.pdf |
| NREL TP-5200-55487 — Pyranometers vs. PV Reference Cells | https://docs.nrel.gov/docs/fy12osti/55487.pdf |
| Kipp & Zonen CMP 21 product page | https://www.kippzonen.com/Product/16/CMP-21-Pyranometer |
| Apogee SP-230 product page | https://www.apogeeinstruments.com/sp-230-all-season-heated-pyranometer/ |
| IMT Solar Si-420TC datasheet | https://www.imt-solar.com/silicon-irradiance-sensor/ |
