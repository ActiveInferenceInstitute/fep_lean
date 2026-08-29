# Horizon 3 G0 choices ledger

This ledger audits implementation decisions that were not already fixed by the
H3.G0 repair instructions. It is grouped by verdict. The v1 review decisions
themselves remain in `carrier-candidate-v1-withheld.json`; this file explains
how the corrected v2 package avoids repeating those failures. This ledger is a
material v2 review input: `carrier-candidate.json` source-binds its exact bytes,
and `carrier-review-request-v2.json` names the same binding for both reviewers.

## Needs-user

None.

## Unsound

None retained.

## Sound

### Separate candidate, review-request, and final-receipt ownership

- **When:** Rebuilding the lifecycle after the two independent v1 WITHHOLD
  decisions.
- **The choice:** Keep the immutable v2 candidate in `carrier-candidate.json`,
  place the exact pending-review binding in
  `carrier-review-request-v2.json`, and reserve the absent
  `carrier-acceptance.json` for a later final event. The rejected alternative
  was one artifact whose review fields and decision changed in place.
- **The gap:** An artifact cannot safely bind its own eventual review result or
  the mutable final-status surfaces without a self-reference or provenance
  cycle.
- **The reach:** Each review can approve fixed candidate, signpost, payload, and
  test hashes. A future final receipt can append review decisions and bind final
  authority/README/test bytes without rewriting v1 or v2.
- **Verdict:** Sound. Ownership follows lifecycle state rather than filename
  convenience.
- **Confidence:** High.

### Bind a stable signpost while leaving the lifecycle README mutable

- **When:** Choosing the v2 source map before independent review.
- **The choice:** Bind `carrier-candidate-v2-signpost.md` as the immutable short
  description of v2, while keeping `README.md` outside the candidate source
  map. The rejected alternative was binding the live README that must later
  report review and acceptance status.
- **The gap:** A truthful status update to a candidate-bound README would
  invalidate the candidate immediately after review.
- **The reach:** The signpost remains reproducible, the README can remain the
  current navigation owner, and a future final receipt can bind its final
  version explicitly.
- **Verdict:** Sound. Stable evidence and mutable navigation have different
  owners.
- **Confidence:** High.

### Scope capability absence to canonical governed paths

- **When:** Replacing the v1 repository-wide data-absence inference.
- **The choice:** Use `data-capability.yaml` as the sole prospective metadata
  owner and record its exact absence, plus the exact preregistration-path
  absence, in `data-capability-snapshot.json`. The rejected alternative was a
  broad scan followed by a claim that no candidate dataset exists anywhere.
- **The gap:** A scan outside a canonical interface cannot establish global
  absence and risks inspecting protected outcomes.
- **The reach:** H3.6E and causal claims fail closed, while the H2.7-authorized
  formal H3.1--H3.5 and synthetic H3.6S carrier remain scientifically distinct
  from empirical eligibility.
- **Verdict:** Sound. The absence claim is exact, governed, and no stronger than
  the inspected evidence.
- **Confidence:** High.

### Freeze authority bytes as candidate inputs, not final-status owners

- **When:** Source-binding v2 after repairing the H3 design and dependency map.
- **The choice:** Record the corrected authority hashes in the immutable v2
  source snapshot and capability snapshot. Describe them as candidate-input
  bytes; require a future final receipt to bind the then-current final authority
  bytes separately. The rejected alternative was treating mutable authority
  status text as a live self-updating field of v2.
- **The gap:** Advancing H3.G0 status in an authority document necessarily
  changes that document after candidate review.
- **The reach:** Reviewers can reproduce the policy used to construct v2
  without preventing a later append-only status transition.
- **Verdict:** Sound. Historical review inputs and final status evidence remain
  distinguishable.
- **Confidence:** High.

### Bind both raw candidate bytes and a canonical JSON payload

- **When:** Defining the two independent review bindings.
- **The choice:** Record the raw file SHA-256 and a UTF-8 canonical JSON SHA-256
  computed with sorted keys and compact separators. The rejected alternatives
  were raw bytes alone or an undocumented semantic digest.
- **The gap:** Raw bytes detect every formatting change but do not distinguish
  formatting from payload changes; an unspecified canonicalization cannot be
  independently reproduced.
- **The reach:** Review receipts can identify the exact reviewed file and its
  ordering/indentation-independent JSON meaning.
- **Verdict:** Sound. The test independently recomputes both bindings.
- **Confidence:** High.

### Pin exact schema membership without pinning JSON insertion order

- **When:** Refactor-clean and code review after the first eight-test green run.
- **The choice:** Assert the exact candidate and source-map key sets while
  leaving object insertion order unconstrained. The rejected alternative was
  tuple equality over parser-preserved key order.
- **The gap:** JSON object order is not part of the receipt semantics, so an
  order-only change should not masquerade as a schema violation.
- **The reach:** Missing or extra contract fields still fail, while harmless
  reordering remains outside the behavioral test boundary.
- **Verdict:** Sound. The test pins the lifecycle contract rather than a
  serialization accident.
- **Confidence:** High.

### Preserve superseded v1 prose as explicitly historical evidence

- **When:** Applying refactor-clean to stale-looking v1 signpost text.
- **The choice:** Retain the v1 candidate and signpost byte-for-byte and label
  them as superseded only from the new lifecycle hub and WITHHELD history. The
  rejected alternative was correcting their prose in place.
- **The gap:** Cleaning historical text would break the hashes reviewed by both
  v1 reviewers and erase the exact object that was withheld.
- **The reach:** Stale v1 claims cannot act as live authority, yet the review
  record remains independently reproducible.
- **Verdict:** Sound. Append-only correction is more truthful than historical
  mutation.
- **Confidence:** High.
