# NUMPYRO Rendering Results

Generated from GNN POMDP Model: **FepLean Continuous OU Linear-Gaussian Model**

## Model Information

- **Model Name**: FepLean Continuous OU Linear-Gaussian Model
- **Model Description**: Bridge P4b slice: the fep_lean scalar OU filter instance
(rate=1, center=0, diffusionVarianceRate=2, stepDuration=1,
observation noise variance=1) projected deterministically to
GNN v1 continuous linear-Gaussian syntax under contract v0.2
rounding. Extraction record (file:line in the fep_lean
checkout at the commit recorded under Signature):
- F one-step decay = exp(-rate*t) = exp(-1)
[scalar_gaussian_semigroup.lean:42-43]
- Q one-step transition covariance = rate^-1*(1 - exp(-2*rate*t))
= 1 - exp(-2) [linear_gaussian_semigroup.lean:1217-1233]
- H identity readout [gaussian_filter.lean:46-49]
- R observation noise variance = 1
[posterior_convergence.lean:38-40]
- prior_mean = 0, prior_cov = stationary variance = 1 (proved)
[smooth_reference_kernel.lean:66-68, 96-101]
- **Generation Date**: 2026-09-04 12:18:42

## POMDP Dimensions

- **Number of States**: 1
- **Number of Observations**: 1
- **Number of Actions**: 1

## Active Inference Matrices

### Available Matrices/Vectors:


## Generated Files

- `FepLean_Continuous_OU_Linear-Gaussian_Model_numpyro.py` - numpyro simulation script


## Usage

Refer to the main numpyro documentation for information on how to run the generated simulation scripts.

## Framework-Specific Information

- **Framework**: numpyro
- **File Extension**: .py
- **Multi-Modality Support**: ✅
- **Multi-Factor Support**: ✅
