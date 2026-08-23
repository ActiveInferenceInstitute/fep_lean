# Scripts

The public command is `uv run fep-lean`. The numbered files remain thin local
wrappers for environments that discover Python scripts automatically:

- `01_fep_catalogue_and_figures.py` → `fep-lean catalogue`
- `02_run_single_topic.py` → `fep-lean topic ID`
- `03_lean_verify_only.py` → `fep-lean verify` (Lean only; no Hermes/Gauss)
- `04_generate_reports.py` → `fep-lean report`

Maintenance adapters are prefixed with `_maint_`. Canonical topic bodies live
in family modules under `src/fep_lean/catalogue/bodies/` and are merged by the
validated registry; metadata, semantic review, novelty, and relation review
live in their corresponding `config/*.yaml` owners. Regenerate all tracked
projections after editing those sources:

```bash
uv run python scripts/_maint_build_topics_catalogue.py
uv run python scripts/_maint_build_fep_all_lean.py
uv run python scripts/_maint_build_formal_modules.py
uv run python scripts/theorem_maturity_audit.py --write
uv run python scripts/build_formalism_coverage.py
uv run python scripts/build_formalism_atlas.py
uv run python scripts/build_formal_kernel_dashboard.py
```

Every generator supports `--check`, which performs a non-mutating freshness
test suitable for CI.

The atlas is the authored topic/capability/module relation projection. The
formal-kernel dashboard is a separate deterministic numerical-witness
projection. Neither generator creates proof evidence; native compilation and
the declaration/axiom audit remain separate gates.

`audit_formalisms.py` is not a generator. It compiles a declaration-resolution
probe against the pinned Lake workspace, checks every semantic/formal witness
with `#print axioms`, requires one parsed result per canonical declaration,
normalizes Lean's hard-wrapped output, rejects warnings and `sorryAx`, and can
write an atomic receipt:

```bash
uv run python scripts/audit_formalisms.py \
  --receipt output/formalism-audit.json
```

`render_manuscript.py` is the fail-closed source-to-build renderer. Its check
mode validates the stable typed-variable projection, the exact generated
appendix, and every authored placeholder without writing output. Run-local
receipt/provider values are rebuilt from independently validated evidence; the
default mode writes the resolved files under `output/manuscript/`:

```bash
uv run python scripts/render_manuscript.py --check
uv run python scripts/render_manuscript.py
```

Do not invoke repository-root modules or set a monorepo-specific `PYTHONPATH`;
each wrapper resolves this checkout's `src/` directory directly.
