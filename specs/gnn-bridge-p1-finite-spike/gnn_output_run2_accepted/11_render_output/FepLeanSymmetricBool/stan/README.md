# STAN Rendering Results

Generated from GNN POMDP Model: **FepLean Symmetric Boolean Generative Model**

## Model Information

- **Model Name**: FepLean Symmetric Boolean Generative Model
- **Model Description**: Bridge P1 spike: the fep_lean active_inference.lean
GenerativeModel instance `symmetricBoolModel trueBiasedPolicyPrior`
(two policies, two hidden states, two observations, one step)
projected deterministically to GNN v1 syntax.
Extraction record (file:line in the fep_lean checkout at the
commit recorded under Signature):
- D initialState = fairBoolLaw (1/2, 1/2)
[def active_inference.lean:719-722; use :745]
- B transition = fairBoolKernel, policy-indexed, all entries 1/2
[def active_inference.lean:725-728; use :746]
- A likelihood = fairBoolKernel, all entries 1/2
[def active_inference.lean:725-728; use :747]
- C preferences = fairBoolLaw (1/2, 1/2)
[def active_inference.lean:719-722; use :748]
- E policyPrior = trueBiasedPolicyPrior: E(false)=1/4, E(true)=3/4
[def active_inference.lean:731-734; parameter :743,:749]
- Timescale: one transition application [active_inference.lean:30-32]
- The Lean GenerativeModel carries no Action type, so no `u`
variable or action edges are emitted.
- **Generation Date**: 2026-09-03 16:04:54

## POMDP Dimensions

- **Number of States**: 2
- **Number of Observations**: 2
- **Number of Actions**: 2

## Active Inference Matrices

### Available Matrices/Vectors:
- **A Matrix (Likelihood)**: 2×2 - Maps hidden states to observations
- **B Matrix (Transition)**: 2×2×2 - State transitions given actions
- **C Vector (Preferences)**: Length 2 - Preferences over observations
- **D Vector (Prior)**: Length 2 - Prior beliefs over states
- **E Vector (Habits)**: Length 2 - Policy priors


## Generated Files

- `FepLean_Symmetric_Boolean_Generative_Model_stan.py` - stan simulation script
- `FepLean_Symmetric_Boolean_Generative_Model_stan.stan` - stan simulation script


## Usage

Refer to the main stan documentation for information on how to run the generated simulation scripts.

## Framework-Specific Information

- **Framework**: stan
- **File Extension**: .stan
- **Multi-Modality Support**: ✅
- **Multi-Factor Support**: ✅
