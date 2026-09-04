# GNN bridge P4 continuous spike — boundary record

Status: **opened and closed at the extraction boundary — no GNN document
emitted, by the do-not-force-fit rule** (contract section 9; Direction 1
P4 no-go: "if continuous parameters cannot be projected mechanically,
the family stays out of scope"). P3 landed green first, so this slice
was opened per the round assignment; its deliverable is the boundary
finding below, not a rendered artifact. Spec-first: this file precedes
any code (no code was needed).

## Candidate instance (pinned workspace, explicit values)

The H2.7 composition module names a fully concrete scalar OU filter:

| Field | Lean source | file:line | Value |
| --- | --- | --- | --- |
| OU rate | `selectedDynamics.rate := 1` | `lean/FepSketches/compositions/smooth_reference_kernel.lean:49-54` (def at :49) | 1 |
| OU center | `selectedDynamics.center := 0` | same, :52 | 0 |
| Diffusion variance rate | `selectedDynamics.diffusionVarianceRate := 2` | same, :53 | 2 |
| Prior mean | `selectedPrior.mean := 0` | `lean/FepSketches/compositions/smooth_reference_kernel.lean:66-68` (mean at :67) | 0 |
| Step duration | `selectedFilter.stepDuration := 1` | `lean/FepSketches/compositions/smooth_reference_kernel.lean:72-75` (:74) | 1 |
| Observation noise | `selectedFilter.observationNoise := selectedGaussianFamily` | same (:75); family at `lean/FepSketches/posterior_convergence.lean:38-40` | variance = 1 |
| Stationary variance | `selectedDynamics_stationaryVariance` (= 1, proved) | `lean/FepSketches/compositions/smooth_reference_kernel.lean:96-101`; also `finOne_stationaryVariance` = rate⁻¹, `lean/FepSketches/linear_gaussian_semigroup.lean:1228-1233` | 1 |

A second concrete dynamics exists (`alternativeDynamics`, def at
`smooth_reference_kernel.lean:58`: rate = 1, center = 0, diffusion
variance rate = 4) and changes no conclusion below.

## Mechanically projectable fields (exact, terminating decimals)

- `prior_mean = 0`, `prior_cov = [[1]]` — proved stationary variance.
- `H = [[1]]` — the `ScalarGaussianFilterModel` observation model is
  additive noise on the state (`lean/FepSketches/compositions/gaussian_filter.lean:46-49`,
  fields `dynamics`/`stepDuration`/`observationNoise`; likelihood
  `N(x, observationNoise.variance)`), i.e. identity readout.
- `R = [[1]]` — `selectedGaussianFamily.variance := 1`
  (`posterior_convergence.lean:38-40`).

## Boundary finding (why no document is emitted)

- `F` must be the one-step transition matrix:
  `decay(model, t) = Real.exp(-rate·t)`
  (`lean/FepSketches/scalar_gaussian_semigroup.lean:42-43`), so
  `F = [[e^{-1}]] ≈ [[0.367879…]]` for the selected instance; the
  equivalent `LinearGaussianParameters` route gives
  `evolution = Matrix.exp(precision·t)` with entry `e^{-1}`
  (`finOne_evolution_entry`, `lean/FepSketches/linear_gaussian_semigroup.lean:1217-1226`).
- `Q` must be the one-step transition covariance:
  `transitionVariance(1) = rate⁻¹(1 − e^{-2·rate·1}) = 1 − e^{-2} ≈ 0.864665…`.
- Both decimal expansions are non-terminating. By the Lindemann–Weierstrass
  theorem `e^{algebraic≠0}` is transcendental, and the carriers require
  `0 < rate` (`rate_pos`; OU) and positive-definite precision
  (`precision_posDef` excludes the identity-evolution degenerate), so
  **every** instance of both carriers has transcendental positive-time
  evolution entries. The boundary is family-wide, not instance-specific.
- The bridge contract fixes the rounding policy once, in its first
  slice (`specs/gnn-bridge-p1-finite-spike/README.md`): exact
  terminating decimals only; a non-terminating expansion is a no-go,
  never rounded. Under the policy of record, `F` and `Q` are
  unprojectable. Extending the policy for transcendental parameters is
  a contract edit (both repositories, same working session — contract
  section 8), which is an owner action outside this worker's file
  scope (`docs/design/gnn-bridge/*` is explicitly off-limits here).

## What would unblock P4

1. A contract-level rounding extension for the continuous family
   (e.g. "emit `float64` value of the exact Lean real, provenance
   digest of the exact formula"), fixed by the contract owners in both
   checkouts; then a P4 slice re-opens with the table above as the
   extraction record and only `F`/`Q` change status.
2. Alternatively a discrete-step OU carrier with algebraic decay on the
   Lean side (none exists in the pinned workspace today).

## Acceptance checklist

- [x] P4.1 — spec-first: this file precedes any code (no code needed).
- [x] P4.2 — extraction table complete with file:line for every value.
- [x] P4.3 — boundary finding stated with exact formulas and the
      family-wide argument.
- [x] P4.4 — stop honored: no document emitted, no backend forced, no
      `unsupported`-class render attempted.
- [x] P4.5 — `REPORT.md` written with the honest phase boundary.

## No-go registry (slice-local)

- `F` and `Q` no-go as above (transcendental vs the fixed exact-decimal
  policy). Not hand-fitted; not rounded; not defaulted.
- No GNN-side `continuous`-keyword document exists in this slice;
  consequently no render/execution run was performed and the shared
  `output/` question does not arise.
