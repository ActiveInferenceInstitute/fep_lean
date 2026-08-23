# fep_lean package

This directory is the sole import root installed by the distribution. Internal
imports must use `fep_lean.*`; do not recreate the removed collision-prone
top-level packages (`catalogue`, `pipeline`, `output`, `verification`, `gauss`,
or `llm`).

## Boundaries

- `catalogue` owns typed metadata/semantic validation, the family-body registry,
  theorem-signature projection, and deterministic catalogue projections.
- `formal` owns the explicit foundation/composition manifest, canonical Lean
  resources, and exact workspace projection; its `composed.lean` resource is an
  import-only aggregate.
- `verification` owns read-only environment checks and native Lean execution.
- `llm` owns Hermes/provider interaction; `gauss` owns SQLite sessions and
  per-topic orchestration.
- `pipeline` composes those layers. Catalogue mode must remain offline; full
  mode must fail closed when a required capability is unavailable.
- `output` owns receipts, reports, figures, variables, and source-preserving
  rendering. Catalogue, native, and full-run evidence must remain distinct.

Public exports belong in the narrow subpackage `__init__.py` and, only for
stable high-level operations, `fep_lean/__init__.py`. Add import-surface and
isolated-wheel tests whenever that contract changes.

Run the project-root checks in [../../AGENTS.md](../../AGENTS.md).
