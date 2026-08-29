# Horizon 3 reference study

Status: **H3.G0 is accepted and closed. H3.0 v1-v6 were WITHHELD. H3.0 v7 is
the active append-only repair candidate; it is not accepted and H3.1-H3.7 remain
closed.**

This README is navigation only. It is not part of the candidate hash graph and
cannot accept a gate, open an execution lane, or authorize outcome inspection.

## Current H3.0 package

- [preregistration.yaml](preregistration.yaml) is the strict v7 protocol and
  lifecycle contract.
- [h3-0-choices.md](h3-0-choices.md) explains the principles behind its
  scientific and lifecycle choices.
- [tests/test_h3_preregistration.py](../../tests/test_h3_preregistration.py)
  owns strict parsing, semantic mutation probes, algorithm known answers,
  receipt fixtures, and the no-self-acceptance boundary.
- [transition-state-snapshot-v7.json](transition-state-snapshot-v7.json)
  binds terminal v6 history and capture-time v7 absence declarations without
  turning later request presence into an error.
- [preregistration-v6-freeze.json](preregistration-v6-freeze.json) and
  [preregistration-v6-withheld.json](preregistration-v6-withheld.json)
  preserve the exact predecessor package and all three exact review decisions.

The review request is a phase-aware external descendant. It may be absent before
minting or present and valid while review is open; neither state changes the
frozen candidate bytes, and request presence is never approval. Acceptance and
WITHHELD are mutually exclusive terminal descendants that must bind the same
request, reviewed package, and freeze map. There is currently no H3.0 acceptance
receipt.

## Preserved v6 review hashes

This navigation ledger is outside the reviewed hash graph. The immutable v6
values are repeated here only to make the predecessor boundary easy to inspect.

| Artifact | SHA-256 |
| --- | --- |
| Candidate YAML, raw | e6ae75a01c5e49a4f0f07ca85e7fdb0bed185f770edc6f3cc0962d37a17d8549 |
| Candidate payload, canonical | 136b6ade197379ba939bd03ca9fbbc0285c39ba50483d6ed6a65e4e4678fc398 |
| Choice ledger, raw | b70cd333886bc1592d63e8c3ac1f40e7a13ed73cdfeabd3994d239a39a8d0a62 |
| Canonical test, raw | 976bc144d8e3f83fcc9e684c948181fd4354197f7154afcfb11191cb6b2e5ca8 |
| V6 transition snapshot, raw | 18b7f7824d48770365c3e9f2aca5953947f68368cd81d0db2290925eb0a0d3c3 |
| V6 review request, raw | 27a1c95fb177be0925830f82b9740237b5cb499a60e7be7905b266af9eea8caa |
| V6 freeze map, raw | 70458eb3a5e54aad282945c85cc0f77cf1770f2a57cfd9ff626857effbed8a01 |
| V6 WITHHELD record, raw | d5ea4cbb68706a955c100bd813c8a5755693c6fb9b6787109f136de1c5ff9548 |
| Reviewed binding, canonical | f7162d2e74a16a6b53674caefc525a48af52c9348052b2f67cfcb2951f29dcff |

## Append-only rule

Each withheld candidate remains byte-preserved under versioned paths. A repair
adds a forward-only transition and candidate package; its later request, freeze,
and terminal disposition remain descendants. No parent hashes a descendant, so
minting or completing review never requires editing the reviewed candidate.

The unversioned protocol, choices, and canonical test name the current candidate
only. They become authority solely through a separate exact acceptance receipt
with three independent approvals.

## Review boundary

V7 review is synthetic-only. It covers the model boundary, statistics,
formal/evidence lifecycle, executable-owner contract, and one-shot outcome lock.
Its append-only repair makes registered BCa effect criteria and same-ID Holm
decisions jointly authoritative for aggregate results and claims, with every
claim activation resolved from an exact upstream predicate roster. The v6 seed
root and RNG known answers remain unchanged.
It does not inspect protected results, prove a future Lean gate, authenticate a
reviewer, establish empirical eligibility, or claim that a future sandboxed
H3.6S process already ran.

Future formal gates must independently compile and review their typed
interfaces. Future H3.6S evidence must come from the registered fail-closed
external sandbox and exact collection/execution transcripts. The H3.0 fixtures
exercise those schemas but are not compiler, subprocess, sandbox, syscall, or
fsync provenance.

## Closed surfaces

Until a separate exact v7 acceptance receipt validates the frozen request and
all three reviews:

- H3.1 and every formal successor remain closed.
- Development RNG, protected synthetic execution, publication, and outcome
  inspection remain closed.
- H3.6E, empirical, real-causal, thermodynamic, heat, physical, energetic, and
  universal-FEP claims remain closed.
- No candidate, fixture, receipt schema, navigation file, or mere file presence
  is a study result.

## Stable upstream authorities

The accepted G0 carrier boundary and synthetic-versus-empirical split remain
owned by the existing G0 artifacts. V7 does not edit H1, H2, G0, live formal
owners, manifests, or outcome authority.

- [Accepted G0 receipt](carrier-acceptance.json)
- [G0 choices](choices.md)
- [Synthetic data capability boundary](data-capability-snapshot.json)
- [Horizon dependency map](../../docs/design/fep-research-program/dependency-map.md)
- [H3 scientific design](../../docs/design/fep-research-program/horizon-3-scientific-case-study.md)
