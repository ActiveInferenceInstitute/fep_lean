# fep_lean review and extension handoff

**Date:** 2026-07-31
**Repository:** `ActiveInferenceInstitute/fep_lean`
**Checkout:** `/home/trim/Documents/Git/HumOS/projects/outside_of_hum/fep_lean`
**Publication target:** `origin/main`

## Mission

Continue reviewing, extending, improving, and refining this standalone
repository without weakening its evidence boundary. The repository contains a
50-topic FEP catalogue, generated Lean source, an exact Lean/Mathlib
workspace, Hermes model integration, OpenGauss persistence, manuscript
projections, and strict reports. Catalogue mode is deterministic and offline;
only native Lean or strict full-mode receipts count as verification evidence.

The governing documents are [`ISA.md`](ISA.md) for ideal-state criteria and
anti-criteria, [`TODO.md`](TODO.md) for open work only, and
[`CHANGELOG.md`](CHANGELOG.md) for retained audit evidence.

## Current state

- The canonical sources are `config/topics.yaml`,
  `scripts/catalogue_sketches.py`, and the generated
  `lean/FepSketches/fep_all.lean`.
- The pinned workspace is Lean 4.29.0 with Mathlib v4.29.0.
- The OpenGauss CLI is installed locally and `gauss doctor` is healthy.
- The Lean-only path is available as `uv run fep-lean verify`; the numbered
  `scripts/03_lean_verify_only.py` wrapper uses that path and does not call
  Hermes or OpenGauss.
- Full mode remains externally gated by a permitted
  `OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY`. Never copy credentials into the
  repository, its reports, or this handoff.

## Verified evidence

Run from the repository root after dependencies are available:

```bash
uv sync --locked --extra dev
uv run python scripts/_maint_build_fep_all_lean.py
uv run pytest tests/ -q --cov=src --cov-fail-under=89
uv run mypy src
uv run fep-lean setup
uv run fep-lean catalogue
uv run fep-lean verify
uv run python docs/check_links.py --strict --include-root
uv run python docs/md_hygiene.py --strict
uv run python docs/pin_audit.py
uv run python docs/xref_audit.py
```

The latest completed audit recorded:

- `339 passed, 3 skipped`, 90.24% coverage, with 342 collected tests.
- `lake build FepSketches` completed successfully with 8,250 jobs.
- The native 50-topic sweep completed with `complete: true`,
  `verified_topics: 50`, and no `sorry` results.
- Catalogue mode completed with 50 catalogue topics and zero verified topics.
- The theorem-maturity audit now covers all 50 primary theorems and preserves
  explicit scope/assumption gaps without upgrading their claims.
- The independent report-receipt checker accepts catalogue bundles as
  structurally valid but not claim-ready.
- Ruff is explicitly informational for this checkout; the current 216-finding
  measurement (following the prior 222-finding baseline), owner, and staged
  promotion plan are recorded in `docs/quality.md`.
- `mypy`, lock/dependency checks, aggregate regeneration, and all four
  documentation audits passed.
- Full-mode preflight failed only for the absent Hermes provider credential;
  `uv run fep-lean run --topic fep-001` failed closed with no report.

## Review protocol for the next change

1. Read the applicable `AGENTS.md` files and inspect `git status -sb` before
   touching files. Keep this repository independent from the parent HumOS
   worktree and all sibling repositories.
2. Preserve the source hierarchy. Edit catalogue bodies in
   `scripts/catalogue_sketches.py`, regenerate YAML and the aggregate, and
   never hand-edit generated outputs as authoring sources.
3. Review five boundaries together: exact Lean/toolchain resolution, Python
   subprocess and file/database lifecycle, Hermes/Gauss failure handling,
   report/manuscript provenance, and operator documentation/cross-references.
4. Treat a passing unit test as component evidence only. For user-visible or
   cross-stage behavior, exercise the CLI and inspect the emitted structured
   result and artifacts.
5. Keep validation read-only. Dependency acquisition belongs only to
   `fep-lean setup`, bounded by `FEP_LEAN_SETUP_TIMEOUT_SEC`.
6. Update `TODO.md` only with behavior-based open work. Remove a row only when
   its acceptance probe passes in the current checkout and the evidence is
   retained in tests, documentation, or the changelog.
7. Before publication, inspect the intended diff, run `git diff --check`, run
   the applicable full gates, fetch `origin/main`, commit intentionally, push,
   and verify the remote commit and clean `main...origin/main` state.

## Remaining scope

The open backlog is intentionally small:

- `FEP-FULL-002`: run the real Hermes + OpenGauss + Lean smoke and complete
  selected catalogue after credentials are supplied out of band.
- `FEP-PROV-003`: independently recompute the final complete-run artifact
  hashes and reconcile the verification/run manifests.

No release or mathematical claim should imply that the credentialed full-mode
path has passed until its acceptance evidence is available.
