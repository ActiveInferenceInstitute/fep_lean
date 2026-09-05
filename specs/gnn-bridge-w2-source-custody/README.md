# W2: source custody and read-only bridge operations

Status: implemented and verified, 2026-09-04. See [delivery evidence](REPORT.md).
Design owner: [GNN bridge](../../docs/design/gnn-bridge/README.md).

## Goal

Make finite/continuous emission and certificate checks deterministic against an
explicit owner snapshot. End self-referential HEAD-refresh commits and reject
content drift, stale owners, malformed receipts, and invalid numeric policies.

## Criteria

- [x] W2-1: status and certificate evaluation leave bytes and mtimes unchanged.
- [x] W2-2: reordered/deleted/duplicated content cannot pass a custody refresh.
- [x] W2-3: relevant owner additions, deletions, and mutations invalidate pins.
- [x] W2-4: both finite and continuous documents regenerate from the same pin.
- [x] W2-5: certificate tampering and nonfinite numeric inputs fail closed.
- [x] W2-6: CLI and legacy entry points use the tested package operations.
- [x] Anti W2-7: comparisons never claim native proof or current execution.

Probe: `uv run pytest tests/test_gnn_bridge_operations.py -q --no-cov`.
Integration: explicit `fep-lean bridge status --gnn-root PATH`, followed by
both emitters' `--check` and independently validated comparison receipts.

## Decisions

- Source commits are descriptive custody references; owner hashes identify
  actual working-tree bytes. The pin and emitted documents are excluded from
  owner digests so a commit containing them does not invalidate itself.
- A pin operation is explicit. It does not accept syntax drift, prove source
  correctness, or establish that an old execution result used those sources.
- Native compilation, semantic review, concrete artifact proofs, and numerical
  comparison retain separate acceptance paths.
- Later expansion order: concrete PyMDP artifacts, then backend-specific
  ActiveInference.jl extraction, then reviewed continuous dynamics. H3 follows
  its independent accepted predecessor gates.
