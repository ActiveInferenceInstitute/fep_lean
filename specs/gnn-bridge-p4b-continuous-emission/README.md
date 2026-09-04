# GNN bridge P4b — continuous emission under contract v0.2

Status: **verified end-to-end: strict validation exit 0; steps 3, 5, 11,
12 all successful (0 warnings); 5/5 continuous-capable backends rendered
and 4 executed (pytorch skipped: torch not installed); the four
discrete-only backends reported `unsupported` — see [REPORT.md](REPORT.md)
for the evidence record**. Last updated: 2026-09-04.

This slice reopens Direction 1 stage P4 (continuous linear-Gaussian
emission) under [bridge contract](../../docs/design/gnn-bridge/bridge-contract.md)
**v0.2** — the float64 rounding extension that P4's boundary record
(`specs/gnn-bridge-p4-continuous-spike/README.md`, "What would unblock
P4") names as its unblock path. The P4 no-go is superseded by the
contract edit landed in both checkouts in the same working session
(`docs(bridge): contract v0.2 — float64 rounding extension for
non-terminating exact reals`, fep_lean commit `a4bd477`; mirror edited
same session). Spec-first: this file precedes any code.

## Extraction table (reused unchanged from the P4 boundary record)

The instance is the concrete scalar OU filter of the H2.7 composition
module (P4 README table, reproduced here; exact values verified against
that README before coding):

| Field | Lean source | file:line | Exact value |
| --- | --- | --- | --- |
| OU rate | `selectedDynamics.rate := 1` | `lean/FepSketches/compositions/smooth_reference_kernel.lean:49-54` | 1 |
| OU center | `selectedDynamics.center := 0` | same, :52 | 0 |
| Diffusion variance rate | `selectedDynamics.diffusionVarianceRate := 2` | same, :53 | 2 |
| Prior mean | `selectedPrior.mean := 0` | `lean/FepSketches/compositions/smooth_reference_kernel.lean:66-68` | 0 |
| Step duration | `selectedFilter.stepDuration := 1` | `lean/FepSketches/compositions/smooth_reference_kernel.lean:72-75` | 1 |
| Observation noise | `selectedFilter.observationNoise := selectedGaussianFamily` | same (:75); family at `lean/FepSketches/posterior_convergence.lean:38-40` | variance = 1 |
| Stationary variance | `selectedDynamics_stationaryVariance` | `lean/FepSketches/compositions/smooth_reference_kernel.lean:96-101` | 1 |

Derived one-step fields (the formulas the contract v0.2 rounding row
governs; step duration `t = 1`, rate `λ = 1`):

| Field | Formula (recorded verbatim in provenance) | Exact form | float64 (shortest round-trip repr) |
| --- | --- | --- | --- |
| `F` | one-step decay `decay(1) = exp(-rate·t)` (`lean/FepSketches/scalar_gaussian_semigroup.lean:42-43`) | `exp(-1)` | `0.36787944117144233` |
| `Q` | one-step transition covariance `transitionVariance(1) = rate⁻¹(1 − e^{-2·rate·1})` (`lean/FepSketches/linear_gaussian_semigroup.lean:1217-1233`) | `1 - exp(-2)` | `0.8646647167633873` |
| `H` | identity readout (additive observation noise on the state; `lean/FepSketches/compositions/gaussian_filter.lean:46-49`) | `1` | `1.0` |
| `R` | `selectedGaussianFamily.variance` (`lean/FepSketches/posterior_convergence.lean:38-40`) | `1` | `1.0` |
| `prior_mean` | `selectedPrior.mean` | `0` | `0.0` |
| `prior_cov` | proved stationary variance (P4 table, `selectedDynamics_stationaryVariance`) | `1` | `1.0` |

## What this slice delivers

1. **Emitter** — `specs/gnn-bridge-p4b-continuous-emission/projection_continuous.py`
   (structure follows the accepted P1 emitter
   `specs/gnn-bridge-p1-finite-spike/projection.py`): deterministic
   emission of `specs/gnn-bridge-p4b-continuous-emission/gnn-input/FepLeanContinuousOU.md`,
   `GNNSection FepLeanContinuousOU continuous`, GNN v1 syntax, with a
   `--check` freshness mode. Same inputs → byte-identical output.
2. **Values under contract v0.2.** Terminating decimals emit exactly
   (`H`, `R`, `prior_mean`, `prior_cov`). The non-terminating exact Lean
   reals (`exp(-1)`, `1 - exp(-2)`) emit as float64 shortest round-trip
   reprs; the provenance `Signature` records the exact formulas
   (`exp(-1)`, `1 - exp(-2)`) verbatim alongside the usual
   repo/commit/Lean-module/definition/`projection_tool`/`target_syntax`
   rows and the contract v0.2 rounding-policy line. Consumers treat the
   floats as approximations, never as the Lean values.
3. **GNN pipeline run (read-only on the fep_lean side).** From the GNN
   repo root, on the emitted document:
   - `uv run gnn validate <p4b>/gnn-input/FepLeanContinuousOU.md --strict`
     → exit 0;
   - `uv run python src/main.py --target-dir <p4b>/gnn-input --output-dir
     <p4b>/gnn_output --only-steps "3,5,11,12" --verbose`.
   Expected per the contract's `unsupported` rule and the GNN v3.2.0
   model-kind split: continuous backends (jax, pytorch, numpyro, stan,
   rxinfer) render; discrete-only backends (pymdp, activeinference_jl,
   discopy, bnlearn) report `status: unsupported` and are excluded from
   the success denominator; step 12 executes the rendered continuous
   scripts. Per-backend statuses are recorded honestly in the REPORT —
   `unsupported` ≠ `failed`.

## Boundaries

- fep_lean-side artifacts only (emitter, emitted document, slice
  README/REPORT); the GNN pipeline run reads them and writes only under
  this slice's `gnn_output/`.
- No edits to the P4 boundary record, the P1 slice, or any accepted
  slice's scripts.
- Cross-repo references are inline code paths, never markdown links.

## Acceptance

- [x] Bounded spec slice opened before any code (this file).
- [x] `projection_continuous.py` emits
      `gnn-input/FepLeanContinuousOU.md` deterministically with a
      `--check` freshness mode and contract v0.2 rounding.
- [x] GNN strict validation exits 0.
- [x] GNN pipeline steps 3, 5, 11, 12 run on the emitted document;
      continuous backends render; discrete-only backends report
      `unsupported`; step 12 writes its execution summary.
- [x] `REPORT.md` written with digests, acceptance table, commands, exit
      codes, and the P4 no-go supersession note.
- [ ] Bridge README checklist P4 row updated to point at this slice.
