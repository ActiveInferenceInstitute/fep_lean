---
title: fep_lean Ideal State Assessment
status: active
phase: local-readiness
updated: 2026-07-31
---

# fep_lean Ideal State Assessment

## Problem

`fep_lean` combines a 50-row catalogue, generated Lean source, a pinned
Lean/Mathlib workspace, Hermes model calls, OpenGauss persistence, manuscript
projections, and strict run reports. The repository must distinguish a
deterministic offline catalogue from real theorem verification. A green local
command is only meaningful when its capability boundary and evidence are
explicit.

## Vision

A fresh checkout can reproduce the catalogue, acquire the exact declared Lean
toolchain, compile the canonical aggregate, and expose a bounded full-run
workflow whose report proves what was actually verified. Missing external
credentials or failed topics stop full mode without producing a misleading
success report.

## Scope

This assessment covers the standalone repository boundary:

- SSOT parity among `config/topics.yaml`, `scripts/catalogue_sketches.py`, and
  `lean/FepSketches/fep_all.lean`.
- Python dependency installation, tests, coverage, type checking, and local
  subprocess/file/database behavior.
- Exact Lean 4.29.0 and Mathlib `v4.29.0` acquisition and compilation.
- Hermes, OpenGauss, SQLite session lifecycle, report provenance, and generated
  manuscript artifacts.
- Documentation links, cross-references, pinned dependency claims, and this
  repository's operator contracts.

## Out of scope

- Publishing, pushing, or merging changes to GitHub.
- Changing the parent HumOS repository or any sibling repository.
- Treating catalogue mode, a cached response, or a generated manuscript value
  as proof that a theorem was verified.
- Supplying, inventing, or storing provider credentials.
- Making mathematical claims stronger than the source theorem statements and
  the compiler evidence support.

## Ideal-state criteria

| ID | Criterion | Required evidence |
| --- | --- | --- |
| ISA-01 | The 50-topic catalogue is complete and parity-safe. | The SSOT tests pass; the aggregate generator is deterministic and leaves no diff. |
| ISA-02 | Offline mode is deterministic and honest. | `uv run fep-lean catalogue` completes, emits reproducible artifacts, and reports `verified_topics: 0`. |
| ISA-03 | The local Python boundary is reproducible. | `uv sync --locked --extra dev`, `uv pip check`, the coverage gate, and `uv run mypy src` pass. |
| ISA-04 | The pinned Lean workspace is real, not merely configured. | Direct pinned Lean/Lake version probes, Mathlib cache/build, `lake build FepSketches`, and a 50-topic native compile sweep pass. |
| ISA-05 | Full mode is fail-closed. | Preflight requires Gauss, writable state, exact Lean/Lake/Mathlib, and Hermes credentials; any failure returns an error without a successful report. |
| ISA-06 | The live full path is end-to-end. | A permitted Hermes provider answers a bounded smoke run, OpenGauss persists and closes sessions, Lean verifies each selected topic, and the report/manifest agree. |
| ISA-07 | Reports are provenance-safe. | Selected-topic denominators, source/config digests, nested artifact hashes, verification source, and completion state are internally consistent. |
| ISA-08 | Generated manuscript projections use the requested output root. | A custom output-root run cannot consume a stale report from the default `output/reports` tree. |
| ISA-09 | Operator documentation matches behavior. | Link, Markdown hygiene, pin, and cross-reference audits pass after catalogue generation; counts and setup commands are current. |
| ISA-10 | Every primary theorem proxy has a non-vacuity and assumption-strength review on record. | `config/theorem_maturity.yaml` has a `non_vacuity` field for every topic, and the generated `docs/theorem-maturity-audit.md` renders it. The `non_vacuity` entry documents whether the statement has a real witness or is structural/vacuous; topics with `non_vacuity: structural` or `non_vacuity: witnessed` are accepted; topics missing the field are flagged. |

## Anti-criteria

The repository is not in the ideal state if any of these occurs:

- catalogue mode reports a verified topic or full mode reports success after a
  failed capability check;
- a generated aggregate, report, or manuscript projection is treated as an
  authoring source of truth;
- setup silently accepts the wrong Lean version, a partial Mathlib checkout, or
  a failed build;
- a report calls failed Hermes rows `hermes_refined`, uses the full catalogue
  as a filtered-run denominator, or records stale artifact hashes;
- an unexpected runner failure leaves an open SQLite session or a live worker;
- validation acquires dependencies, prints credentials, or makes unbounded
  network calls;
- external credentials are committed, copied into tracked files, or inferred
  from a successful local fixture;
- stale test counts, version claims, or links make the documented operator path
  disagree with the checked-out tree.

## Verification strategy

Run these probes from the repository root, in order when a full local audit is
needed:

```bash
uv sync --locked --extra dev
uv run python scripts/_maint_build_fep_all_lean.py
uv run pytest tests/ -q --cov=src --cov-fail-under=89
uv run mypy src
uv run fep-lean catalogue
uv run fep-lean setup
uv run fep-lean verify
uv run python docs/check_links.py --strict --include-root
uv run python docs/md_hygiene.py --strict
uv run python docs/pin_audit.py
uv run python docs/xref_audit.py
uv run fep-lean preflight
```

`preflight` reports the external full-mode capability boundary. A complete
local assessment must also run the direct Lean gate and the bounded full
workflow after credentials are supplied through the operator's existing secret
mechanism:

```bash
cd lean
lake build FepSketches
cd ..
FEP_LEAN_CATALOGUE_COMPILE_TEST=1 uv run pytest tests/test_catalogue_sketches_compile.py -q --no-cov
uv run fep-lean run --topic fep-001
uv run fep-lean run
```

The smoke run is accepted only when its result is `complete: true`; the full
run is accepted only when all selected topics are cleanly verified and the
report's verification manifest agrees with the result. If credentials are not
available, record the exact preflight failure and leave the full-run criterion
open in [TODO.md](TODO.md).

## Current assessment

The deterministic catalogue path, Python tests, strict type gate, report
regressions, OpenGauss CLI installation, and exact Lean workspace are locally
exercised. The pinned Lean 4.29.0/Mathlib v4.29.0 workspace builds
successfully, and the native 50-topic sweep passes with no compile errors or
`sorry` results. The maintained theorem-maturity audit separately records the
semantic scope and assumption review for every primary theorem without treating
compilation as a stronger FEP claim. The CLI setup path is repeatable and `preflight` confirms all
local capabilities except the missing Hermes provider credential.

Full mode remains intentionally blocked at one external boundary:
`OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` is not configured. A topic run
fails closed with `complete: false`, `verified_topics: 0`, and no report
directory. Therefore ISA-01 through ISA-04, the fail-closed branch of ISA-05,
and ISA-07 through ISA-09 have local evidence after the documented gates pass;
ISA-05's successful-credential branch, ISA-06, and the final complete-run
provenance receipt remain open in [TODO.md](TODO.md).

## Release boundary

This repository is ready for a local full-verification claim only after ISA-01
through ISA-09 have evidence in the same checkout and the final `main` worktree
diff is inspected. This task does not authorize publication.
