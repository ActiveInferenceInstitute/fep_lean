# H3.G0 carrier acceptance

Status: **accepted and closed. H3.0 preregistration is the sole open gate;
H3.1-H3.7 remain closed.**

## Accepted decision

The append-only [acceptance receipt](carrier-acceptance.json) accepts the exact
[v2 candidate](carrier-candidate.json) reviewed by both independent reviewers.
The continuous Fin4 Gaussian carrier is selected for formal H3.1-H3.5 and
synthetic H3.6S. The finite carrier remains fallback and negative-control
evidence and can be selected only after an explicit reviewed H2 terminal no-go
and a reviewed H3 DAG revision.

## Capability boundary

The canonical `data-capability.yaml` owner and `preregistration.yaml` remain
absent. H3.6E and causal claims therefore remain blocked, and no protected
outcomes were inspected. This empirical no-go does not reverse the accepted
continuous formal/synthetic carrier decision.

## Provenance boundary

The [v1 WITHHELD record](carrier-candidate-v1-withheld.json),
[v2 review request](carrier-review-request-v2.json), candidate signpost,
choices, and capability snapshot remain immutable. Reviewed predecision policy
bytes and acceptance-time status bytes live under
[`authority-snapshots/`](authority-snapshots/). This stable signpost and those
snapshots are receipt inputs; the mutable README and live status authorities
are not.

## Next gate

Only H3.0 preregistration may begin. `tests/test_h3_preregistration.py` remains
reserved for that gate; this acceptance creates no H3.0 protocol, data owner,
formal resource, import, theorem, or protected-outcome access.
