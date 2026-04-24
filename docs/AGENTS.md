# AGENTS.md — `docs/` (fep_lean)

**Version**: v0.7.1 | **Last Updated**: 2026-04-24 (aligned with canonical_facts.md)

Conventions for editing **this documentation tree** only. System behaviour, pipeline contracts, and layout live in [`../AGENTS.md`](../AGENTS.md) and [`../SPEC.md`](../SPEC.md). If anything here disagrees with those files, update **this folder** (or the manuscript cross-links), not the project spec.

## Scope

| Audience | Use |
| -------- | --- |
| Humans | Install, operate, extend, and review `fep_lean` without spelunking `src/` blindly |
| Agents | Ground-truthed paths, env vars, test counts, and SSOT rules |

## Catalogue and Lean SSOT

- **Authoring bodies**: [`../scripts/catalogue_sketches.py`](../scripts/catalogue_sketches.py) (`SKETCHES`). Bodies omit a leading `import`; [`LeanVerifier`](../src/verification/lean_verifier.py) prepends Mathlib + opens.
- **Regenerated YAML**: [`../scripts/_maint_build_topics_catalogue.py`](../scripts/_maint_build_topics_catalogue.py) writes [`../config/topics.yaml`](../config/topics.yaml).
- **Drift test**: [`../tests/test_catalogue_sketches_ssot.py`](../tests/test_catalogue_sketches_ssot.py) enforces YAML ↔ `SKETCHES` equality.
- **Docs must not** imply that hand-editing `topics.yaml` alone is the default workflow without updating `SKETCHES`.

## lean4-skills and editor workflows

- **Project map**: [lean4.md](lean4.md) — how `/lean4:*` commands relate to `SKETCHES`, `LeanVerifier`, Gauss/Hermes, and Lake.
- **Plugin doctor** (`/lean4:doctor` in lean4-skills): diagnoses elan, `LEAN4_SCRIPTS`, Lake cache, and plugin layout. **In-repo analogue**: `uv run fep-lean-preflight` + [troubleshooting.md](troubleshooting.md) (Mathlib cache, `_verify_*` hygiene). They are complementary; preflight is authoritative for *this* Lake workspace under [`../lean/`](../lean/).

## Claims and metrics

See [`docs/_generated/canonical_facts.md`](../../../docs/_generated/canonical_facts.md) (monorepo root) for live test counts, coverage (≥89% combined line+branch gate for `src/`; see `pyproject.toml`), and roster. Use paths relative to the **project root** (e.g. `src/verification/lean_verifier.py`). Manuscript numbered sections may use pedagogical Lean; catalogue parity is in Appendix B and `SKETCHES` (see `../manuscript/AGENTS.md`).

## Edit checklist

Run from this `docs/` directory:

```bash
uv run python check_links.py --strict --include-root  # internal links + anchor fragments
uv run python md_hygiene.py --strict                  # heading/list spacing, trailing WS, tabs
uv run python pin_audit.py                            # toolchain + primary-model pin drift
uv run python xref_audit.py                           # \ref / \eqref vs {#id} + \label{id}
```

The four gates are intentionally narrow and fast (each runs in well under a second on a clean checkout):

- **`check_links.py`** — verifies every relative markdown link target exists; with `--strict` also resolves heading-fragment anchors. Catches stale paths after a rename.
- **`md_hygiene.py`** — header/list-marker spacing, trailing newline, duplicate H1, optional trailing-WS / tab / orphan-bracket checks. Catches authoring slips.
- **`pin_audit.py`** — reads canonical pins from [`../lean/lean-toolchain`](../lean/lean-toolchain), [`../lean/lakefile.lean`](../lean/lakefile.lean), and [`../config/settings.yaml`](../config/settings.yaml) (`hermes.model` + cross-checked `gauss.default_model`), then walks every `*.md` outside `manuscript/` (which uses `{{...}}` placeholders) and `_generated/` (build output) to flag any literal that drifts from canonical. Supports `--verbose` and `--json`.
- **`xref_audit.py`** — walks `manuscript/*.md`, builds the union of pandoc `{#id}` anchors and LaTeX `\label{id}` definitions, and verifies every `\ref{...}` / `\eqref{...}` resolves against that union. Both definition styles are accepted because pandoc-citeproc + `pandoc-crossref` resolve both at render time.

After edits that affect behaviour, run `uv run python scripts/01_run_tests.py --project fep_lean` from the repository root (no mocks). See `docs/_generated/canonical_facts.md` for current status.

## Navigation

- [README.md](README.md) — index
- [SPEC.md](SPEC.md) — documentation-folder specification
- [← Project AGENTS](../AGENTS.md)
