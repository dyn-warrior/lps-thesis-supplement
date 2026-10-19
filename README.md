# Supplementary material — LPS thesis

Supplementary figures for the BS-MS thesis *Forecasting Monsoon Low-Pressure Systems over the
Indian Subcontinent with AI Weather Models: A Track-Based Verification against the ECMWF Ensemble*
(Ratul Tarafder, IISER Pune, 2026).

Browse: https://dyn-warrior.github.io/lps-thesis-supplement/

`figures/` is organised as: `comparison/{all-storms,lows,depressions}`,
`ai-vs-ecmwf/{all-storms,lows,depressions}`, `per-model/<model>`, `case-study-2024`, `schematics`.

Every statistical figure comes in two versions:

- **Resampled** (in the folders above): 95% intervals from 1000 bootstrap replicates that
  resample whole storms (shaded bands, error bars). These are the figures used in the thesis.
- **Raw** (in a `raw/` subfolder beside each one, e.g. `comparison/all-storms/raw/`): the same
  figure without resampling, showing only the statistic.

The case-study maps and the schematic contain no averaged statistic and have one version only.
