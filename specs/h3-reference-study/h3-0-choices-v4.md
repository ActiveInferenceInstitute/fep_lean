# H3.0 v4 choice ledger

This ledger explains the prospective H3.0 v4 decisions that are not obvious
from file names alone. The exact machine contract lives in
[`preregistration.yaml`](preregistration.yaml), and the independent semantic
probes live in
[`tests/test_h3_preregistration.py`](../../tests/test_h3_preregistration.py).
This document is not an acceptance receipt, an execution lock, or permission to
inspect outcomes.

## Current disposition

V1, v2, and v3 were WITHHELD. Their versioned protocols, choice ledgers, tests,
review requests, transition records, and disposition history are immutable
inputs to v4. V4 is an append-only repair candidate frozen for three exact
re-reviews. Its adjacent request is the sole review envelope; all decision and
reviewer fields remain null until independent review, and no downstream gate is
open.

The v3 freeze map and WITHHELD record deliberately precede the v4 transition
snapshot in the hash graph. The transition snapshot precedes the v4 package;
the review request follows the frozen v4 package. No candidate or request is
allowed to hash a descendant and create a provenance cycle.

## Why v3 was withheld

The exact reviewer identities and reviewed hashes live in
[`preregistration-v3-withheld.json`](preregistration-v3-withheld.json). Their
findings converge on three principles:

- A statistical formula is not fixed unless an independent implementation can
  recompute it and a refreshed outer digest cannot hide a changed leaf.
- A formal receipt is not proof merely because it names a compiler, test, or
  declaration. It must bind reviewed interfaces, immutable source, actual
  compiler evidence, exact consumers, and recursively validated predecessors.
- An execution lock is not one-shot merely because a JSON field says so. Its
  filesystem transitions, dependencies, output roster, durability limits, and
  crash states must be defined before any protected random draw.

V4 addresses those findings without changing any v3 byte.

## Statistical choices

### Whole-trajectory inference

The independent unit is one complete trajectory. Bootstrap positions preserve
duplicates and order, and every component of a composite row reuses the same
position vector. Streams are never reused across registered test IDs.

BCa acceleration centers the 128 leave-one-trajectory-out estimates at their
arithmetic mean. The full-sample statistic is not that center. This is the
specific v3 ambiguity that could change every adjusted endpoint.

All scalar reductions have one owner: binary64 values, `math.fsum`, and the
named scientific order. Exact counters and discrete tails remain Python
integers and `Fraction` values until the decision boundary. Pooled-first,
unordered, parallel, NumPy-default, or mean-of-unit-ratios substitutions are
not equivalent implementations.

### Exact discrete algorithms

SBC rank tails use the registered sparse integer dynamic program, not a
chi-square approximation. The recurrence accumulates multinomial weights and
checks its total mass. Resource exhaustion fails closed; it never authorizes an
approximation. Small structural, near-uniform, and extreme-tail known answers
make recurrence or endpoint substitutions observable.

Coverage tails use inclusive exact binomial sums. DKW uses the registered
inclusive empirical CDF and fixed binary64 expression. Add-one tails, exact win
tails, and Holm comparisons use `Fraction`; float conversion before Holm is a
contract violation.

The normal CDF and inverse CDF surface is the named `statistics.NormalDist`
API. Python implementation/build, libc/libm, NumPy, BLAS/LAPACK, platform, and
thread identity therefore belong to the environment lock. One-ULP differences
from substituting a direct `erf` expression are real substitutions, not harmless
formatting.

### Semantic mutation policy

Every result-changing repaired clause is tested by changing one leaf, computing
the mutant's own canonical digest, and requiring the semantic checker to reject
it. Complete owner subpayload digests protect BCa, numeric aggregation, SBC
multinomial/DKW/binomial, add-one, win, and Holm mappings against unenumerated
leaf drift. Algorithm known answers remain separate so a correct hash cannot
stand in for correct computation.

## Formal-gate choices

### What H3.0 owns

H3.0 owns prospective module owners, direct-import order and source authority,
public declaration names/order, full-versus-new roster semantics, scientific
scope, no-go boundaries, gate DAG, focused-test roster, and receipt schemas.
The exact gate contracts and proposed semantic/value obligations live in the
candidate rather than being duplicated here.

H3.0 does not pretend that unimplemented Lean declarations already have
machine-checked exact types. A gate-specific typed-interface contract is
created only after isolated owner and typed-consumer compilation. Two
independent signature reviewers must approve that immutable interface before a
proof contract or exit receipt can bind it. The typed consumer exposes implicit
parameters with `@Qualified.name`; holes, metavariables, self-derived types, and
tactic placeholders are forbidden.

This reslicing prevents both failure modes: inventing untypechecked H3.0 types,
and allowing a future proof author to self-select a trivial but internally
consistent type.

### Evidence, not self-report

Future receipts bind canonical toolchain paths, exact owner and consumer compile
commands, raw transcripts, a compiler-derived public-environment census,
per-theorem axiom reports, exact focused test functions parsed from immutable
Python source, and a strict parsed focused result. Lean source census is
comment-aware and fail-closed for alternate imports, modifiers, hidden
declarations, attributes, axioms, unsafe/partial/private surfaces, and
unregistered public commands.

The H3.0 lifecycle fixtures exercise schemas and state transitions only. They
simulate compiler and focused-result bytes; they are never evidence that Lean or
pytest ran for a future gate. Native gate capture and independent review supply
that evidence later.

### Shared owners and capture order

Some gates extend one source owner. Scientific predecessor edges remain distinct
from the administrative immutable chain that proves retained declarations and
typed ascriptions are byte-identical. The active action route must capture its
consumer of the case-study owner before the information-only H3.5 extension is
appended. The passive route may skip action capture and permanently freeze the
null-action family.

Alternate H3.3 owner paths, modules, manifest entries, and duplicate owner
tuples remain forbidden after acceptance, not merely at transition time.

### Prospective authority refinements

These refinements take effect only if the exact v4 package is later accepted:

- H3.1 reuses the accepted Fin4 carrier and has one direct project import. It
  does not recreate the carrier or silently inherit the older broader import
  sketch.
- H3.3 owns analytic Fin4 propagation, conditioning normal equations, and
  uniqueness. It does not claim an unsupported native multivariate posterior
  theorem or variational optimum.
- H3.4 has a dedicated action owner and a continuous-observation quadratic
  two-step Bellman/open-loop boundary. It does not expose EFE, causal, reset,
  impulse, or future-observation anticipation claims.
- H3.5 depends on H3.3, not the optional action gate. It owns only registered
  two-dimensional observational Gaussian-law/KL nonidentification and
  mechanically excludes thermodynamic, heat, physical, energetic, and
  empirical interpretation.

## Executable-owner choices

H3.6S has one Python owner and one package-level export surface. Public API,
package export order, focused-test roster, source snapshot, dependency lock,
and predecessor receipt/snapshot bytes are part of the owner contract. A
focused validator cannot depend on the live receipt it is meant to precede.

Static contract materialization is idempotent only when existing canonical
bytes are identical. Action freeze, development, pre-run arming, and protected
execution are one-way no-overwrite transitions. Arming owns pre-run creation
and performs zero protected RNG work.

## Execution-lifecycle choices

### Semantic dependencies

Execution, seed, metric, baseline, and fixture artifacts are strict projections
of the accepted protocol. Their values are reparsed and recomputed; an opaque
hash wrapper is insufficient. Development train and validation manifests bind
the accepted protocol and action lock, validate the complete expected data
domain and bytes, and exclude held-out/protected namespaces.

The durable action-activation lock is created before development RNG. It binds
the accepted H3.0 receipt, protocol, static projections, mandatory inference and
executable-owner receipts, and either the permanent null-action choice or both
active action proofs. Development selection and pre-run both revalidate the
same immutable lock, so action status cannot change after seeing development
results.

### One-shot protected execution

The pre-run lock and fixed candidate-wide claim use exclusive, no-follow,
mode-restricted creation and bind every semantic dependency plus the literal
protected output roster. The execution identifier is safe operator data, not a
self-hash. Inputs are held and revalidated across claim creation before the
first protected RNG draw.

Protected output paths, roles, media types, record expectations, and namespaces
are registered before execution. The manifest cannot discover authority from
whatever files happen to exist. Publication is no-replace, manifest follows
complete output publication, and the result is written last.

The total observed-state classes are armed, consumed-incomplete, completed, and
invalid-terminal. Any claim, even malformed or crash-partial, consumes v4 and
cannot be retried under another identifier. Lexical existence includes broken
symlinks; staging, modes, special files, extras, omissions, empty completion,
and content bindings are validated according to state.

Local files cannot prove that a privileged actor never deleted an earlier claim
or reconstruct historical syscall/fsync order. The one-shot guarantee therefore
assumes non-destructive filesystem actors; stronger historical provenance needs
an external append-only or live syscall trace. Unit tests pin intended behavior
but do not upgrade that threat model.

## Decision audit

The following choices are retained because their alternatives would reopen
post-outcome discretion:

- **Sound:** jackknife-mean BCa centering, exact integer/Fraction discrete
  decisions, fixed reduction orders, whole-trajectory resampling, and stable
  bootstrap tie authority.
- **Sound with an exact runtime lock:** binary64 `math.fsum`, `NormalDist`, and
  NumPy linear quantiles.
- **Sound but fail-closed on resources:** exact sparse multinomial DP. No
  approximate fallback is accepted.
- **Prospective and independently reviewable:** pooled covariance/precision,
  stationarity reductions, formal declaration semantics, action control, and
  typed Lean interfaces. They are choices, not inherited theorems.
- **Unsound and rejected:** opaque dependency hashes, self-asserted timing,
  filesystem-discovered output rosters, `Path.exists()` for security state,
  mutable action activation, fabricated compiler/focused evidence, trivial
  self-selected Lean types, or static receipts that independently open
  execution lanes or claims.

Any reversal requires a new preserved candidate version, fresh exact reviews,
and no inspection of protected outcomes. It cannot be made by editing an
accepted package in place.

## Closed boundaries

Until a separate final acceptance receipt validates the frozen request and all
three exact approvals:

- H3.1 and every later formal gate remain closed.
- Development RNG, protected synthetic execution, and outcome inspection remain
  closed.
- H3.6E, empirical eligibility, causal claims, thermodynamic claims, and
  universal-FEP claims remain closed.
- No artifact in this package is a study result or scientific acceptance.
