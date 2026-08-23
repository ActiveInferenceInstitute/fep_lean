# Verification package contract

This folder owns three different surfaces:

1. `run_validation_checks` is a read-only capability probe. It must not fetch a
   toolchain, build Mathlib, create a database, or write a report.
2. `LeanVerifier` compiles an explicitly supplied sketch in the pinned Lake
   workspace and returns a structured result. It must preserve errors,
   warnings, `sorry`, skip reason, failure kind, toolchain identity, and timing
   as separate fields.
3. `run_formalism_audit` resolves every reviewed primary/evidence declaration
  through `FepSketches.composed`, the import aggregate over manifested
  composition leaves, requires parsed axiom output for every declaration,
  records the actual Lean version and resolved Mathlib revision, and fails on
  missing evidence, stale projections, warnings, compiler errors, `sorryAx`,
  or any axiom outside the versioned trusted set (`propext`,
  `Classical.choice`, and `Quot.sound`).

`preflight.py` is an adapter for `fep-lean preflight`; it is not a second public
console script. Installation and dependency acquisition belong to
`fep-lean setup`.

## Invariants

- Resolve `lean` and `lake` through `_toolchain.py`; do not create a parallel
  executable search path.
- Keep batch verification serial around the shared `.lake` tree.
- Delete only verifier-owned `_verify_*.lean` temporary files.
- A successful process exit with warnings or `sorry` is not a clean result.
- The formalism audit receipt is declaration/axiom evidence, not a replacement
  for an exact sealed-roster native receipt.
- `check_mathlib_built()` is a presence probe, not proof that the current
  catalogue compiled.
- Full-mode validation requires every local capability and a permitted Hermes
  credential; catalogue mode remains offline.

## Focused checks

```bash
uv run pytest tests/test_lean_verifier.py \
  tests/test_lean_verifier_sad_paths.py \
  tests/test_environment_checks.py \
  tests/test_environment_sad_paths.py \
  tests/test_preflight.py -q --no-cov
uv run fep-lean preflight
uv run fep-lean verify --fail-on-warnings \
  --receipt output/native-verification.json
uv run python scripts/audit_formalisms.py \
  --receipt output/formalism-audit.json
```

The credentialed full-mode probe is an external acceptance stage. Never add a
secret to tests, documentation, receipts, or the checkout.
