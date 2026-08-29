# Horizon 3 reference study

Status: **H3.G0 is accepted and closed.**

**H3.0 v2 candidate pending three exact re-reviews; it is not accepted.
H3.1-H3.7 remain closed.**

Navigation only: this README is not a review, acceptance, pre-run, or outcome
authority and is deliberately excluded from candidate hash bindings.

## Next Agent Prompt

As of 2026-08-24, review the synthetic-only H3.0 v2
[candidate](preregistration.yaml), [choices](h3-0-choices.md), immutable
[transition snapshot](transition-state-snapshot-v2.json), and
[review request](preregistration-review-request-v2.json). Do not edit the
preserved [v1 protocol](preregistration-v1.yaml),
[v1 choices](h3-0-choices-v1.md),
[v1 test snapshot](test-snapshots/h3-0-v1/test_h3_preregistration.py),
[v1 request](preregistration-review-request-v1.json), or
[v1 WITHHELD history](preregistration-v1-withheld.json). Do not create an
acceptance receipt, ratchet status, execute synthetic outcomes, inspect
protected outcomes, or open H3.1-H3.7. Acceptance requires statistical,
model/domain/action, and implementation/provenance/outcome-lock approvals over
the exact v2 request binding. Data-owner review is N/A for this synthetic-only
candidate and never grants H3.6E eligibility.

## H3.0 candidate binding

The v2 request binds the strict-parsed candidate, H3.0 choices, live future-safe
test, transition snapshot, v1 WITHHELD history, G0 receipt, and strict lifecycle
addendum. Reviewers bind both its canonical reviewed-binding digest and its raw
request hash. A future acceptance event must append a separate receipt without
changing the reviewed v2 package. Canonical unversioned paths are only the
current v2 candidate until that receipt exists.

## Append-only lifecycle

The [final acceptance receipt](carrier-acceptance.json) and
[stable acceptance signpost](carrier-acceptance-signpost.md) close H3.G0. The
receipt records the two independent approvals and binds only immutable review
artifacts, authority snapshots, the stable signpost, and the final G0 test.
This README is the mutable navigation hub and is deliberately not receipt-bound.

The [v1 WITHHELD history](carrier-candidate-v1-withheld.json) preserves the two
independent WITHHOLD decisions and their exact binding. Its
[candidate snapshot](carrier-candidate-v1.json) and
[historical signpost](carrier-candidate-v1-signpost.md) are retained byte for
byte. The accepted [v2 candidate](carrier-candidate.json),
[candidate signpost](carrier-candidate-v2-signpost.md),
[review request](carrier-review-request-v2.json), choices, and capability
snapshot also remain immutable historical inputs; acceptance appends a receipt
rather than rewriting their pending state.

The [reviewed predecision policy snapshot](authority-snapshots/v2/snapshot-map.json)
preserves what both reviewers assessed. The
[acceptance-time status snapshot](authority-snapshots/g0-accepted/snapshot-map.json)
preserves the later live status bytes without making mutable authority files
permanent receipt inputs.

## Branch policy

The pre-outcome program policy applies exactly one carrier to the formal and
synthetic study: positive accepted H2.7 evidence selects the continuous Fin4
Gaussian carrier for H3.1-H3.5 and H3.6S. The accepted H1 finite carrier remains
a fallback and negative control. It can be selected only after an explicit
reviewed H2 terminal no-go and a reviewed H3 DAG revision. Nothing in H3.G0
transfers Gaussian covariance, diffusion, conditioning, or continuous-time
semantics to that finite model.

Acceptance opens H3.0 preregistration only. H3.1-H3.7 and protected-outcome
inspection remain closed.

## Capability boundary

`data-capability.yaml` is the single canonical owner for governed interface,
license, axis-variable, unit, sampling, and intervention metadata. That owner
remains absent. The source-bound
[`data-capability-snapshot.json`](data-capability-snapshot.json) therefore keeps
H3.6E empirical eligibility and causal claims blocked without inspecting
protected outcomes. It makes no global claim about datasets elsewhere in the
repository. The H3.0 candidate is synthetic-only; its presence cannot repair
the metadata no-go or transfer it onto the formal/synthetic carrier.

## Review and test ownership

[`tests/test_h3_g0_carrier_acceptance.py`](../../tests/test_h3_g0_carrier_acceptance.py)
owns the complete H3.G0 lifecycle, source, review, branch, capability, and
downstream-closure contract.
[`tests/test_h3_preregistration.py`](../../tests/test_h3_preregistration.py)
owns only the H3.0 candidate, synthetic protocol, mutation probes, review
request, and no-acceptance boundary. The G0 artifacts remain unchanged; a later
H3.0 acceptance must append its own receipt.

## Canonical authorities

- [H3 scientific design](../../docs/design/fep-research-program/horizon-3-scientific-case-study.md)
- [Horizon dependency map](../../docs/design/fep-research-program/dependency-map.md)
- [Accepted H2.7 exit](../horizon-2-smooth-stochastic/readiness/exits/07-smooth-reference-kernel.json)
- [Archived H1 acceptance](../done/horizon-1-finite-synthesis/README.md)
- [H3.G0 implementation choices](choices.md)
- [H3.0 candidate choices](h3-0-choices.md)

The authority snapshot maps above are the stable receipt inputs. The linked
live design documents remain navigation authorities whose future status edits
do not invalidate the closed G0 receipt.

## Review boundary

Accepted evidence covers exact source bytes, source/projection parity, named
accepted H1/H2 declarations, prior receipts, the canonical-path capability
snapshot, two independent review tokens, and downstream closure. It proves no
new theorem and makes no empirical, causal, thermodynamic, or universal-FEP
claim. No protected outcomes were inspected. GitNexus coverage is unavailable
for this nested checkout, so graph confidence is reduced; exact hashes and
direct source/consumer tracing provide the scoped evidence here.
