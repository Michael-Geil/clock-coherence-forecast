Clock Coherence Forecast

This repository contains the full reproducible analysis pipeline used in:

Emergent Causality and Unaligned Geometry: Predictive Clock Phase Correlations

The code tests whether relative phase between international atomic clocks exhibits out-of-sample predictability in a pre-registered 8–12 day frequency band using strictly walk-forward forecasting and multiple surrogate null models.

What This Repository Does

Downloads and parses Circular-T UTC–UTC(k) data from BIPM

Builds per-laboratory time series

Extracts band-limited analytic phase

Performs walk-forward phase forecasting

Evaluates predictive skill

Quantifies statistical significance using:

Circular-shift surrogates

Phase-randomized surrogates

Band-limited surrogates

Generates all figures and tables reported in the paper

Quick Start
pip install -r requirements.txt
python run_all.py


All results will be reproduced automatically.

Data Source

Raw clock data are published by the Bureau International des Poids et Mesures (BIPM):

https://webtai.bipm.org/ftp/pub/tai/Circular-T/

Reproducibility

All random seeds are fixed.
All hyperparameters are hard-coded.
The full pipeline runs deterministically.
