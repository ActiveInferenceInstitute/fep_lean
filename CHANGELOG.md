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
  342 collected tests across 30 modules.
- Reconciled repository documentation and operator metadata with the 1.0.0
  checkout.
- Added `HANDOFF.md` with the next-reviewer protocol, evidence receipt, and
  remaining extension scope.
- Added a maintained semantic review for all 50 theorem proxies in
  `config/theorem_maturity.yaml`, with generated Markdown, theorem-name parity
  validation, explicit non-vacuity and assumption reviews, and native Lean
  acceptance probes. The audit records scope gaps honestly and changes no
  `mathlib_status` claim.
- Added the read-only `validate_report_receipt` API and
  `scripts/verify_report_receipt.py`. It recomputes every listed artifact hash,
  rejects report-directory escapes, and reconciles summary, run, and
  verification manifests. A real complete full-mode receipt is still required
  before FEP-PROV-003 can close.
- Re-ran `uv run fep-lean verify`: `complete: true`, 50/50 clean native Lean
  results, no `sorry` results. The catalogue CLI receipt also passed the new
  independent checker with `mode: catalogue` and `verified_topics: 0`.
- The complete Python gate passed with `339 passed, 3 skipped`, 90.24% line
  coverage, and 342 collected tests; strict receipt failure paths, including
  malformed boolean flags, are covered without lowering the 89% threshold.
- Recorded the Ruff policy decision in `docs/quality.md`: the current 216
  findings (down from the prior 222-finding baseline) are explicitly
  non-gating until Ruff is pinned, debt is reduced in staged batches, and the
  exact check and format commands run in CI.

### Still externally gated

- A permitted `OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` is still required to
  exercise the live Hermes/OpenGauss/Lean full-mode smoke and complete-catalogue
  runs. No credential is stored in this repository.
