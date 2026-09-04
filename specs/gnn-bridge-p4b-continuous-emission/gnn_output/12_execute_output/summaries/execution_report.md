# GNN Script Execution Report

**Generated:** 2026-09-04T12:18:42.845765
**Target Directory:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn-input
**Output Directory:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/12_execute_output

## Summary

- **Total Scripts Found:** 5
- **Successful Executions:** 4
- **Failed Executions:** 0
- **Skipped (dependency not installed):** 1

## Execution Details

### FepLean_Continuous_OU_Linear-Gaussian_Model_jax.py - ✅ SUCCESS

- **Framework:** jax
- **Executor:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/GeneralizedNotationNotation/.venv/bin/python
- **Path:** `/Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/11_render_output/FepLeanContinuousOU/jax/FepLean_Continuous_OU_Linear-Gaussian_Model_jax.py`
- **Return Code:** 0
- **Execution Time:** 0.85 seconds
- **Detailed Output:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/12_execute_output/FepLeanContinuousOU/jax/execution_logs/FepLean_Continuous_OU_Linear-Gaussian_Model_jax.py_execution.log

### FepLean_Continuous_OU_Linear-Gaussian_Model_numpyro.py - ✅ SUCCESS

- **Framework:** numpyro
- **Executor:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/GeneralizedNotationNotation/.venv/bin/python
- **Path:** `/Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/11_render_output/FepLeanContinuousOU/numpyro/FepLean_Continuous_OU_Linear-Gaussian_Model_numpyro.py`
- **Return Code:** 0
- **Execution Time:** 1.81 seconds
- **Detailed Output:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/12_execute_output/FepLeanContinuousOU/numpyro/execution_logs/FepLean_Continuous_OU_Linear-Gaussian_Model_numpyro.py_execution.log

### FepLean_Continuous_OU_Linear-Gaussian_Model_pytorch.py - ⏭️ SKIPPED

- **Framework:** pytorch
- **Executor:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/GeneralizedNotationNotation/.venv/bin/python
- **Path:** `/Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/11_render_output/FepLeanContinuousOU/pytorch/FepLean_Continuous_OU_Linear-Gaussian_Model_pytorch.py`
- **Reason:** Dependency not installed: torch

### FepLean_Continuous_OU_Linear-Gaussian_Model_rxinfer.jl - ✅ SUCCESS

- **Framework:** rxinfer
- **Executor:** julia
- **Path:** `/Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/11_render_output/FepLeanContinuousOU/rxinfer/FepLean_Continuous_OU_Linear-Gaussian_Model_rxinfer.jl`
- **Return Code:** 0
- **Execution Time:** 11.30 seconds
- **Detailed Output:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/12_execute_output/FepLeanContinuousOU/rxinfer/execution_logs/FepLean_Continuous_OU_Linear-Gaussian_Model_rxinfer.jl_execution.log

### FepLean_Continuous_OU_Linear-Gaussian_Model_stan.py - ✅ SUCCESS

- **Framework:** stan
- **Executor:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/GeneralizedNotationNotation/.venv/bin/python
- **Path:** `/Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/11_render_output/FepLeanContinuousOU/stan/FepLean_Continuous_OU_Linear-Gaussian_Model_stan.py`
- **Return Code:** 0
- **Execution Time:** 12.41 seconds
- **Detailed Output:** /Users/hum/Documents/GitHub/HumOS/projects/outside_of_hum/fep_lean/specs/gnn-bridge-p4b-continuous-emission/gnn_output/12_execute_output/FepLeanContinuousOU/stan/execution_logs/FepLean_Continuous_OU_Linear-Gaussian_Model_stan.py_execution.log

## Next Steps

Skipped scripts are due to missing optional dependencies or unavailable system runtimes. Run `uv sync` for core Python backends; add `uv sync --extra ml-ai --extra graphs` for optional Python extension groups, and install Julia/D2 system tools as needed.

