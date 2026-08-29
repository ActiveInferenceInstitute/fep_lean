# Horizon 3 reference study

Status: **H3.G0 is a continuous-branch candidate pending independent
probability/dynamics and skeptical review. H3.0-H3.7 remain closed.**

## Carrier candidate

[`carrier-acceptance.json`](carrier-acceptance.json) is the canonical,
source-bound H3.G0 review candidate. It applies the pre-outcome program policy:
the positive accepted H2.7 terminal selects the primary continuous Fin4
Gaussian carrier for review. This is not final gate acceptance, and no
protected outcome was inspected to make the selection.

The archived H1 finite carrier remains accepted fallback and negative-control
evidence. It can replace the continuous candidate only after an explicit,
reviewed H2 terminal no-go and a reviewed H3 DAG revision. Its no-go
declarations remain boundary evidence and do not transfer Gaussian covariance,
diffusion, conditioning, or continuous-time semantics to the finite model.

## Capability boundary

No governed H3 candidate dataset or preregistration is present in the
repository. License, axis-variable, unit, sampling, and intervention metadata
are therefore unavailable. This blocks the H3.6E real-data branch. It does not
preclude the formal H3.1-H3.5 or synthetic H3.6S study after their required G0
review and H3.0 preregistration gates pass; it opens none of them now.

## Review and test ownership

H3.G0 remains read-only and opens no downstream gate until independent
probability/dynamics and skeptical reviewers approve the same candidate README,
canonical pre-review receipt payload, and G0 test hashes. The artifact records
those pending review fields and their acceptance rule.

[`tests/test_h3_g0_carrier_acceptance.py`](../../tests/test_h3_g0_carrier_acceptance.py)
owns this candidate gate. `tests/test_h3_preregistration.py` is reserved for
H3.0 and does not exist before H3.0 opens. The open-gate H3 design and dependency
map are retained as a named pre-decision authority snapshot rather than a live
final-status source binding; this avoids a provenance cycle when their status
eventually advances.

## Canonical owners

- [H3 scientific design](../../docs/design/fep-research-program/horizon-3-scientific-case-study.md)
- [Horizon dependency map](../../docs/design/fep-research-program/dependency-map.md)
- [Accepted H2.7 exit](../horizon-2-smooth-stochastic/readiness/exits/07-smooth-reference-kernel.json)
- [Archived H1 acceptance](../done/horizon-1-finite-synthesis/README.md)

## Review boundary

Candidate evidence covers source bytes, source/projection parity, named
declarations, receipts, pre-outcome capability state, and downstream closure.
It proves no new theorem and makes no empirical, causal, thermodynamic, or
universal-FEP claim. GitNexus coverage is unavailable for this nested checkout,
so graph confidence is reduced; exact source hashes and direct consumer tracing
replace graph validation here.
