# Horizon 1 exit handoff

Status: **accepted, archived, and closed**.

Start with the durable [`README.md`](README.md), then consult
[`choices.md`](choices.md) for the decision history and the program
[handoff](../../../docs/design/fep-research-program/handoff.md) for the current
cross-horizon gate.

## What is safe to reuse

The maintained H1 modules provide independently owned seams for finite
scientific countermodels, native KL and decision risk, selected-model posterior
learning, posterior-indexed one-step decision/action, conditional blanket
factorization, action-indexed semigroups, and the final shared-carrier
composition. Their canonical roster and workspace projections are owned by
`src/fep_lean/formal/manifest.py`; do not create another module list.

The terminal theorem
`FEPComposed.FiniteReferenceAgent.finiteReferenceAgent_terminal` is the only
accepted H1 vertical certificate. It must be cited with the limitations in the
README. The adjacent public no-go theorems are deliberate regression evidence,
not obsolete scaffolding.

## Frozen boundaries

- Preserve Lean `v4.33.1`, Mathlib `v4.33.1`, and revision
  `0df444a360eaa60ab8c11dca51a86af692955474` as one pin.
- Preserve the recognition-to-posterior KL orientation and the separate
  native extended-KL support boundary.
- Preserve the missing finite/native epistemic-value translation as a no-go.
- Preserve the distinction between one-step posterior-dependent decision and
  transition-aware or expected-free-energy-optimal planning.
- Preserve the genuine sensory--active conditioner and same-carrier,
  same-kernel strict KL chain.
- Keep the hold branch non-strict; strict contraction belongs to positive-time
  refresh from a nonuniform law.
- Keep physical thermodynamics, causal identification, empirical adequacy, and
  universal-FEP language outside the H1 theorem claim.

## Accepted barrier

The final serialized native build completed for `FepSketches.fep_all` and
`FepSketches.composed`. The focused H1/formal matrix passed, projections were
byte-current, and the five terminal public theorem probes reported only the
standard axioms `propext`, `Classical.choice`, and `Quot.sound`. Independent
Lean, domain, and skeptical reviews accepted the final theorem and wording.

The exact final run counts are retained in the program handoff linked above;
red-to-green behavior is pinned by the named H1 tests. The durable scientific
reasons, dead ends, canonical pointers, and final evidence boundary live in the
README.

## Resume point

Open H2.0 from the [Horizon 2 design](../../../docs/design/fep-research-program/horizon-2-smooth-stochastic.md).
Keep Lean/Lake compilation serialized. H3 remains closed until H2.7 and H3.G0.
Release-wide native, formal, Python, browser, manuscript, and bundle receipts
must be regenerated only after the final source tree is frozen; this archived
H1 record is not a current release receipt.
