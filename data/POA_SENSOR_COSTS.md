# POA Irradiance Sensor Cost Estimates

**Site:** NREL PVDAQ System 4902 — NIST Ground-1, Gaithersburg MD

**Channel:** `poa_irradiance_wm2`

Pricing researched in April 2026. Two of the three sensors are quote-only
at the manufacturer level; the numbers below combine distributor list
prices, public retailer listings, and established market ranges. Treat
them as **rough order-of-magnitude estimates**, not procurement quotes.

---

## Per-sensor cost

| # | Instrument | Class | Price (USD) | Source / basis |
|---|---|---|---|---|
| 1 | **Kipp & Zonen CMP 21** | Secondary-standard thermopile pyranometer (ISO 9060 Class A) | **~$4,500–$5,500** (sensor only, quote-only) | Distributor pricing is not publicly listed; long-standing market range for the Kipp & Zonen secondary-standard line. Quote required from Campbell Scientific / OTT HydroMet. |
| 1a | **Kipp & Zonen CVF 3 ventilator** (paired with CMP 21) | Active ventilation/heater unit | **~$900–$1,200** | CVF 3 now obsolete; replacement CVF 4 in similar price band, sold via Campbell Scientific. |
| 2 | **IMT Solar Si-I-420TC** | Silicon reference cell, 4–20 mA loop, temp-compensated | **€398 (~$430)** | JEDS Energy listing (confirmed). |
| 3 | **Apogee SP-230-SS** | Heated silicon-cell pyranometer | **$338.87** | Scaled Instruments listing (confirmed). |

---

## Total instrumented POA channel cost

The NIST Ground-1 array runs all three POA sensors **in parallel**, so
the per-site instrumentation outlay for the POA measurement alone is
roughly:

| Item | Low | High |
|---|---:|---:|
| CMP 21 thermopile | $4,500 | $5,500 |
| CVF 3 ventilator | $900 | $1,200 |
| IMT Si-420TC | $430 | $430 |
| Apogee SP-230-SS | $340 | $340 |
| **Subtotal — sensors only** | **~$6,170** | **~$7,470** |

Not included: NREL **BORCAL calibration** (recurring, every 12–24 months,
typically a few hundred dollars per radiometer), datalogger channel
allocation (Campbell Scientific CR-class), mounting hardware, cabling,
and labor.

---

## Why the order-of-magnitude spread

- **Thermopile vs. silicon** is roughly a 10× cost gap. The CMP 21 is a
  metrology-grade instrument (ISO 9060 Class A, broadband 285–2800 nm,
  zenith-dependent calibration). The Si cells are inexpensive
  photodiode-based devices with narrower spectral response.
- That gap is exactly *why* sites like NIST run both: the thermopile
  anchors absolute irradiance; the Si cells track what the modules
  spectrally see, at a fraction of the cost.
- For commercial/utility PV monitoring, an Si cell alone is often
  sufficient. Research-grade plants pay the thermopile premium for
  traceable broadband measurement.

---

## References

| Source | URL |
|---|---|
| Kipp & Zonen CMP 21 product page (quote-only) | https://www.kippzonen.com/Product/478/CMP21-Pyranometer |
| Campbell Scientific CMP21 ordering page | https://www.campbellsci.com/cmp21 |
| OTT HydroMet CMP21 listing | https://www.otthydromet.com/en/p-kippzonen-cmp21-pyranometer/0362920 |
| Campbell Scientific CVF3-L ventilation unit | https://www.campbellsci.com/cvf3 |
| Kipp & Zonen CVF4 (current replacement for CVF3) | https://www.kippzonen.com/Product/262/CVF4-Ventilation-Unit |
| JEDS Energy — IMT Si-I-420TC listing (€398) | https://www.jedsenergy.com/products/solar-irradiance-sensor-si-i-420tc |
| SolarTraders — IMT Si-I-420TC | https://www.solartraders.com/en/products/accessories/imt-technology-si-i-420tc-solar-irradiance-sensor |
| Scaled Instruments — Apogee SP-230-SS ($338.87) | https://www.scaledinstruments.com/shop/apogee-instruments/pyranometer/apogee-sp-230-ss-all-season-heated-pyranometer/ |
| Apogee Instruments — SP-230-SS product page | https://www.apogeeinstruments.com/sp-230-ss-all-season-heated-pyranometer/ |
| Campbell Scientific — SP230SS | https://www.campbellsci.com/sp230ss |
