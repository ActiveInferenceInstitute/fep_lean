# Changelog

## Unreleased — 2026-07-31

### Verified in the local audit

- Repaired bounded Lean setup so it resolves the declared Lean 4.29.0
  toolchain directly, acquires Mathlib v4.29.0, and fails rather than masking
  installer or build errors.
- Built `FepSketches` successfully and passed the native 50-topic compile
  sweep with no compile errors or `sorry` results.
- Repaired the documented `scripts/03_lean_verify_only.py` path by adding the
  first-class `fep-lean verify` command, which performs the same 50-topic
  native sweep without Hermes or OpenGauss.
- Hardened full-mode fail-closed behavior, Hermes preflight budget restoration,
  SQLite session cleanup, selected-topic report denominators, nested artifact
  hashes, and custom manuscript output-root isolation.
- Added the strict `mypy` development gate and reconciled the test census at
  331 collected tests across 29 modules.
- Reconciled repository documentation and operator metadata with the 1.0.0
  checkout.
- Added `HANDOFF.md` with the next-reviewer protocol, evidence receipt, and
  remaining extension scope.

### Still externally gated

- A permitted `OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` is still required to
  exercise the live Hermes/OpenGauss/Lean full-mode smoke and complete-catalogue
  runs. No credential is stored in this repository.
