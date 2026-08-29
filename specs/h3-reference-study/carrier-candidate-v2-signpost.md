# H3.G0 carrier candidate v2

Status: **immutable continuous formal/synthetic candidate pending two new
independent reviews. No downstream gate is open.**

## Decision seam

Positive accepted H2.7 evidence selects the exact continuous Fin4 Gaussian
carrier for the H3.1-H3.5 formal and H3.6S synthetic scopes. Empirical metadata
does not choose that carrier. The accepted H1 finite carrier remains fallback
and negative-control evidence; selecting it requires both an explicit reviewed
H2 terminal no-go and a reviewed H3 DAG revision.

## Capability seam

[`data-capability-snapshot.json`](data-capability-snapshot.json) checks only the
canonical `data-capability.yaml` and `preregistration.yaml` paths. Both are
absent, protected outcomes are uninspected, and H3.6E plus causal claims fail
closed. This is not a global claim that no dataset exists, and it does not
invalidate the formal or synthetic carrier scopes.

## Lifecycle seam

[`carrier-candidate.json`](carrier-candidate.json) is the immutable v2 candidate.
[`carrier-review-request-v2.json`](carrier-review-request-v2.json) binds its raw
bytes, canonical JSON payload, this signpost, and the focused G0 test for two
new reviews. Prior v1 bytes and WITHHOLD decisions remain separate immutable
history. `carrier-acceptance.json` is reserved for a later final receipt and is
absent until both v2 reviews approve the exact same binding.

## Firewalls

H3.G0 adds no Lean resource, manifest entry, import, theorem, empirical result,
or H1/H2 mutation. H3.0-H3.7 and protected-outcome inspection remain closed.
The candidate makes no causal, thermodynamic, empirical-adequacy, or universal
FEP claim.
