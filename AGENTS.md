# AGENTS.md — fep_lean

## Purpose

Standalone 50-topic FEP / Active Inference / Bayesian Mechanics / Information
Geometry / Thermodynamics catalogue with Lean 4 source, Hermes integration,
OpenGauss SQLite persistence, deterministic manuscript artifacts, and strict
reports.

## Terminology

The Lean code for each catalogue row is called a **sketch** — it is a Lean
source body that type-checks against Mathlib and is intended as a partial
formalisation of the row's natural-language statement. The natural-language
statement itself, together with the formal Lean identifiers and assumptions
that define its scope, is called a **theorem proxy** — it stands in for the
FEP/Active Inference concept the row describes, and its semantic reach is
separately reviewed in `config/theorem_maturity.yaml`. A sketch that compiles
clean (no `sorry`) means the proxy's Lean body type-checks; it does not mean
the full FEP concept is proven.

## Source of truth

- `config/topics.yaml` — validated catalogue rows.
- `config/theorem_maturity.yaml` — maintained semantic review records for the
  catalogue theorem proxies; `docs/theorem-maturity-audit.md` is generated from
  this file.
- `scripts/catalogue_sketches.py` — Lean body source.
- `scripts/_maint_build_topics_catalogue.py` — YAML regeneration.
- `scripts/_maint_build_fep_all_lean.py` — tracked aggregate regeneration.
- `lean/FepSketches/fep_all.lean` — whole-catalogue Lean target.
- `ISA.md` — ideal-state criteria, anti-criteria, and evidence gates.
- `TODO.md` — canonical open-only backlog; completed work is not retained as
  struck-through rows.
- `HANDOFF.md` — next-reviewer protocol, evidence receipt, and remaining scope.

## Execution contract

- `uv run fep-lean catalogue` is explicit offline mode. It creates deterministic
  catalogue artifacts and reports zero verified topics.
- `uv run fep-lean verify` is the Lean-only native compile path. It requires
  the built pinned Mathlib cache but does not call Hermes, OpenGauss, or the
  full pipeline.
- `uv run fep-lean run` is strict full mode. It requires configured Hermes,
  OpenGauss, Lean, Lake, and a complete pinned Mathlib build.
- Missing capabilities, failed topics, or artifact errors produce a failed
  result and no successful report.
- `complete: true` means all *selected* topics passed (via `FEP_LEAN_MAX_TOPICS`
  filter or default full catalogue). The report's `catalogue_topics` field shows
  the selected count; a subset run may report `complete: true` with fewer than
  50 topics. The `validate_report_receipt` checker verifies `verified_topics ==
  selected_topics`, not `verified_topics == 50`.
- `run_validation_checks` is read-only. Dependency acquisition belongs only to
  `uv run fep-lean setup` and is bounded by `FEP_LEAN_SETUP_TIMEOUT_SEC`.
- `preflight` JSON output is advisory subject to additive field changes between
  releases. Stable referential queries use the CLI exit code and `status` field.

## Required checks

```bash
uv run python scripts/_maint_build_fep_all_lean.py
uv run pytest tests/ -q --cov=src --cov-fail-under=89
uv run mypy src
uv run python docs/check_links.py --strict --include-root
uv run python docs/md_hygiene.py --strict
uv run python docs/pin_audit.py
uv run python docs/xref_audit.py
```

Do not claim Lean verification from catalogue mode or from generated manuscript
values. Publish only a full result with `complete: true` and a matching artifact
manifest.
