# Horizon 3 reference study

Status: **H3.G0 is accepted and closed. H3.0 v1-v5 were WITHHELD. H3.0 v6 is
the active append-only repair candidate; it is not accepted and H3.1-H3.7 remain
closed.**

This README is navigation only. It is not part of the candidate hash graph and
cannot accept a gate, open an execution lane, or authorize outcome inspection.

## Current H3.0 package

- [preregistration.yaml](preregistration.yaml) is the strict v6 protocol and
  lifecycle contract.
- [h3-0-choices.md](h3-0-choices.md) explains the principles behind its
  scientific and lifecycle choices.
- [tests/test_h3_preregistration.py](../../tests/test_h3_preregistration.py)
  owns strict parsing, semantic mutation probes, algorithm known answers,
  receipt fixtures, and the no-self-acceptance boundary.
- [transition-state-snapshot-v6.json](transition-state-snapshot-v6.json)
  binds terminal v5 history and capture-time v6 absence declarations without
  turning later request presence into an error.
- [preregistration-v5-freeze.json](preregistration-v5-freeze.json) and
  [preregistration-v5-withheld.json](preregistration-v5-withheld.json)
  preserve the exact predecessor package and all three WITHHOLD decisions.

The review request is a phase-aware external descendant. It may be absent before
minting or present and valid while review is open; neither state changes the
frozen candidate bytes, and request presence is never approval. Acceptance and
WITHHELD are mutually exclusive terminal descendants that must bind the same
request, reviewed package, and freeze map. There is currently no H3.0 acceptance
receipt.

## Preserved v5 review hashes

This navigation ledger is outside the reviewed hash graph. The immutable v5
values are repeated here only to make the predecessor boundary easy to inspect.

| Artifact | SHA-256 |
| --- | --- |
| Candidate YAML, raw | 9c6ca8a8ccbb0b83d0beaadcd1dba4091deb521ccc4345ba2f53c3dfd513afac |
| Candidate payload, canonical | fcbc346cabd343f410ccf228e554bb490a4c3285f59ffa34a6b2e8109678f1f0 |
| Choice ledger, raw | 68ec7b5152179e0f594467a472385456b1179bead334d01723c09cea3afd4bc5 |
| Canonical test, raw | f1c037fa90c95dd96ae1fff7e36da416c0021cf2e15b407189555d513a689c95 |
| V5 transition snapshot, raw | 858e71dca2ab5fdb46da194ac4c486766a928a5e7cdb3eba096b205c7a0d290e |
| V5 review request, raw | 9b7ba2623ca7998988856870a2c4993ab7a6f51e46ffa67fbf73d4fe2e99a241 |
| V5 freeze map, raw | e18b9a595ca3f6c6426711c7bca6d9a761ef7f5cebaf064f7beeb7d5c31461cd |
| V5 WITHHELD record, raw | 857606b3dd52c5c06fb803bb02d007037d7498a0a22e9c7585ab445e4c273db0 |
| Reviewed binding, canonical | 742e4f63e2e267d61a51f60851a6f949289bed702a37d0b021a2746d289edabf |

## Append-only rule

Each withheld candidate remains byte-preserved under versioned paths. A repair
adds a forward-only transition and candidate package; its later request, freeze,
and terminal disposition remain descendants. No parent hashes a descendant, so
minting or completing review never requires editing the reviewed candidate.

The unversioned protocol, choices, and canonical test name the current candidate
only. They become authority solely through a separate exact acceptance receipt
with three independent approvals.

## Review boundary

V6 review is synthetic-only. It covers the model boundary, statistics,
formal/evidence lifecycle, executable-owner contract, and one-shot outcome lock.
It does not inspect protected results, prove a future Lean gate, authenticate a
reviewer, establish empirical eligibility, or claim that a future sandboxed
H3.6S process already ran.

Future formal gates must independently compile and review their typed
interfaces. Future H3.6S evidence must come from the registered fail-closed
external sandbox and exact collection/execution transcripts. The H3.0 fixtures
exercise those schemas but are not compiler, subprocess, sandbox, syscall, or
fsync provenance.

## Closed surfaces

Until a separate exact v6 acceptance receipt validates the frozen request and
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
owned by the existing G0 artifacts. V6 does not edit H1, H2, G0, live formal
owners, manifests, or outcome authority.

- [Accepted G0 receipt](carrier-acceptance.json)
- [G0 choices](choices.md)
- [Synthetic data capability boundary](data-capability-snapshot.json)
- [Horizon dependency map](../../docs/design/fep-research-program/dependency-map.md)
- [H3 scientific design](../../docs/design/fep-research-program/horizon-3-scientific-case-study.md)
