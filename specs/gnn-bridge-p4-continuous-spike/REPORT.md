# GNN bridge P4 continuous spike — REPORT

Status: **P4 closed at the extraction boundary (documented no-go)** —
the continuous family stays out of scope under the contract's fixed
rounding policy, per the Direction 1 P4 no-go row and the task's
stop rule. No GNN document was emitted; nothing was forced. Date:
2026-09-03. Digests unchanged from P1-P3: fep_lean
`315e32994b59fd80e327b5b654c9f7852fad9933`,
GeneralizedNotationNotation `12a565b2f18db7f18c3a799568ad057834ba0358`.

## What was done

1. P3 landed green (see `specs/gnn-bridge-p3-certificates/REPORT.md`),
   so the P4 slice was opened: `README.md` (spec-first boundary record).
2. The candidate instance was identified and every value anchored:
   `selectedDynamics` (rate = 1, center = 0, diffusion variance rate =
   2), `selectedFilter` (step duration = 1, observation noise =
   unit-variance `selectedGaussianFamily`), `selectedPrior` (mean 0) —
   full table with file:line in the slice README.
3. Mechanical extraction succeeded for `prior_mean = 0`,
   `prior_cov = [[1]]`, `H = [[1]]` (identity additive readout of
   `ScalarGaussianFilterModel`), `R = [[1]]`.
4. The boundary was hit and recorded: `F = [[e^{-1}]]` and
   `Q = 1 − e^{-2}` are transcendental (Lindemann–Weierstrass; the
   carriers force `rate > 0` and positive-definite precision, so the
   boundary is family-wide), while the contract's rounding policy —
   fixed once in the bridge's first slice — admits exact terminating
   decimals only. Extending the policy is a contract edit in both
   repositories, an owner action outside this worker's scope.

## What was NOT done (deliberately)

- No GNN document emitted, no `uv run gnn validate`, no pipeline run,
  no render/execution attempt, no `unsupported`-class observation. Per
  the task: "record the boundary and stop — do not force a fit."
- No rounding decision was made for the continuous family: that is the
  contract owners' call (section 9 fixes the policy once, in the first
  slice; this slice cannot re-fix it).

## Unblock path (recorded in the slice README)

A contract-level rounding extension for transcendental parameters
(e.g. float64 value of the exact Lean real with the exact formula in
provenance), fixed by both sides; the extraction table in the slice
README is then the ready-made record for a reopened P4 — only `F`/`Q`
change status.

## Artifact list (this slice)

| Artifact | Role |
| --- | --- |
| `README.md` | Boundary record: instance table, projectable fields, boundary finding, unblock path |
| `REPORT.md` | This file |

## Commands and exit codes

No pipeline or validation commands were run in this slice (nothing to
run — no document exists). Lean-side evidence is source reading
(`grep -n` / `sed -n` line lookups over
`lean/FepSketches/{compositions/smooth_reference_kernel.lean,posterior_convergence.lean,linear_gaussian_semigroup.lean,scalar_gaussian_semigroup.lean,compositions/gaussian_filter.lean}`),
the same semantic-review plane as P1/P3 extraction.

## Blockers

The P4 acceptance row (validate / Gaussian-capable render / categorical
`unsupported` exclusion) is unreachable without the contract-level
rounding extension described above. This is a recorded no-go per the
contract's own registry, not a failure of execution: the honest phase
boundary is "P4 boundary recorded; continuous family out of scope until
the owners extend the rounding policy."
