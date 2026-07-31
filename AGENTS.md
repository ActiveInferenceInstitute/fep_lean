# AGENTS.md — fep_lean

## Purpose

Standalone 50-topic FEP / Active Inference / Bayesian Mechanics / Information
Geometry / Thermodynamics catalogue with Lean 4 source, Hermes integration,
OpenGauss SQLite persistence, deterministic manuscript artifacts, and strict
reports.

## Source of truth

- `config/topics.yaml` — validated catalogue rows.
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
- `run_validation_checks` is read-only. Dependency acquisition belongs only to
  `uv run fep-lean setup` and is bounded by `FEP_LEAN_SETUP_TIMEOUT_SEC`.

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
