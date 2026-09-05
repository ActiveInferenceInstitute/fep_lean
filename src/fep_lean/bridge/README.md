# GNN bridge operations

This package owns source custody, deterministic emission, and numerical
comparison for the finite Boolean and scalar-OU GNN bridge examples.
The model interchange remains a GNN document; JSON receipts are evidence.

```text
explicit source pin → deterministic GNN document → renderer artifact
                                                → numerical comparison receipt
```

Use `uv run fep-lean bridge --help`. Every operation names `--gnn-root`.
`status`, `emit --check`, `verify-certificate`, and `certify` without
`--receipt` perform no writes. `pin`, `emit`, and `certify --receipt PATH`
are explicit mutations. `emit --refresh-digests` refuses content drift.

The source pin records commit references and the actual working-tree owner
hashes. It never claims that uncommitted bytes belong to the recorded commit.
Unrelated commits do not stale a document. Changed, added, or missing owners
do stale it. Pin changes do not reclassify old execution evidence.

A comparison receipt establishes agreement for an identified result artifact,
not that the current source produced it. `execution_source_verified` and
`native_claim_ready` remain false. Concrete renderer proofs have their own
artifact/proof receipt. Historical P3 comparisons remain historical.

The standard package test suite includes standalone fixture tests with no
sibling checkout. Live two-repository checks are explicit integration probes.
