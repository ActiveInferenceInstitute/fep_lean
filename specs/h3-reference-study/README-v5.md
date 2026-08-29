# Horizon 3 reference study

Status: **H3.G0 is accepted and closed. H3.0 v4 was WITHHELD after two exact
approvals and one implementation/provenance WITHHOLD. H3.0 v5 is the active
append-only repair candidate. Its review request is absent while validation is
in progress; H3.0 is not accepted and H3.1-H3.7 remain closed.**

This README is navigation only. It is not part of the candidate hash graph and
cannot accept a gate, open an execution lane, or authorize outcome inspection.

## Current H3.0 package

- [`preregistration.yaml`](preregistration.yaml) is the strict v5 protocol and
  lifecycle contract.
- [`h3-0-choices.md`](h3-0-choices.md) explains the discretionary decisions,
  rejected alternatives, and reversal conditions.
- [`tests/test_h3_preregistration.py`](../../tests/test_h3_preregistration.py)
  owns strict parsing, semantic mutations, algorithm known answers, formal
  receipt fixtures, and the no-acceptance boundary.
- [`transition-state-snapshot-v5.json`](transition-state-snapshot-v5.json)
  records the immutable pre-candidate transition state.
- `preregistration-review-request-v5.json` is intentionally absent until the
  candidate, choices, canonical test, and transition bindings are green and
  byte-frozen.
- [`preregistration-v4-freeze.json`](preregistration-v4-freeze.json) and
  [`preregistration-v4-withheld.json`](preregistration-v4-withheld.json)
  preserve the exact predecessor package, both approvals, and the
  implementation/provenance WITHHOLD.

There is intentionally no H3.0 acceptance receipt. When v5 is frozen, its
separate request will record null decisions and reviewer identities until three
independent reviewers bind its exact raw hash and reviewed-binding digest. File
presence is not approval.

## Preserved v4 review hashes

This navigation-only ledger is outside the reviewed hash graph. These values
make the immutable WITHHELD v4 boundary easy to inspect without creating a
reverse edge. Mutable v5 hashes are deliberately omitted until freeze.

| Artifact | SHA-256 |
| --- | --- |
| Candidate YAML, raw | `0cbb2af1416d1fe52c726f45583f990eefb8698559bfe78951083ad63c6a99f2` |
| Candidate payload, canonical | `0fea0a056ec3443caf2fa43cbb54504ac517f404528f4b7351e4a277f7993f5e` |
| Choice ledger, raw | `4d349e95e694b34b6f0bcf2c89e87ed9104ae5a7f955ec010723169f2aa9fd59` |
| Canonical test, raw | `8b5b77da46c71a8be1976ad6513b5717ba9cf1c25d80944c621ac98b5bd0c93f` |
| V4 transition snapshot, raw | `44b02b123c1ce14c1e13c3392c83bc1d5fcd0ca1a6bd77f28817d8525903c28c` |
| Reviewed binding, canonical | `3c8ab0c5959db64215ba255855e138ed66f4d0bd46974975ffda41c1cf3f6d4a` |
| V4 review request, raw | `56c78e2744e63b3189c9902944d4eada7f04c8ffa0ef58648401a60a8c486ab2` |

## Append-only rule

Each withheld candidate remains byte-preserved under its versioned paths. A new
candidate repairs it by adding a forward-only freeze, disposition, transition,
candidate, request, and eventual acceptance chain. Later artifacts bind earlier
ones; earlier artifacts never hash mutable descendants.

The unversioned protocol, choices, and canonical test name the current candidate
only. They become authority solely through a separate exact acceptance receipt
that binds the reviewed request and three independent approvals.

## Review boundary

V5 review will be synthetic-only and cover the preregistered model boundary,
statistics, formal/evidence lifecycle, executable-owner contract, and one-shot
outcome lock. It does not review protected results, prove a future Lean gate,
or establish empirical eligibility.

The formal lifecycle deliberately separates H3.0's prospective scientific
rosters from future machine-checked Lean types. A gate-specific typed interface
must first compile in isolation and receive independent signature reviews; only
then may a proof contract and exit receipt bind it. H3.0's synthetic fixtures
exercise that schema but are not compiler provenance.

The protected lifecycle assumes non-destructive filesystem actors. Static files
and unit tests cannot prove that a privileged actor never deleted a prior claim
or reconstruct historical fsync order; stronger evidence requires an external
append-only or live syscall trace.

## Closed surfaces

Until a separate exact v5 acceptance receipt validates all three reviews:

- H3.1 and all formal successors remain closed.
- Development RNG, SBC, confirmatory execution, protected output publication,
  and outcome inspection remain closed.
- H3.6E, empirical, real-causal, thermodynamic, heat, physical, energetic, and
  universal-FEP claims remain closed.
- No candidate, fixture, receipt schema, or file presence is a study result.

## Stable upstream authorities

The accepted G0 carrier boundary and synthetic-versus-empirical split remain
owned by the existing G0 artifacts. V5 does not edit H1, H2, G0, live formal
owners, manifests, or outcome authority.

- [Accepted G0 receipt](carrier-acceptance.json)
- [G0 choices](choices.md)
- [Synthetic data capability boundary](data-capability-snapshot.json)
- [Horizon dependency map](../../docs/design/fep-research-program/dependency-map.md)
- [H3 scientific design](../../docs/design/fep-research-program/horizon-3-scientific-case-study.md)
