# Lean 4 workspace

The workspace pins `leanprover/lean4:v4.29.0` and Mathlib `v4.29.0`.

```bash
uv run fep-lean setup
uv run fep-lean verify
cd lean
lake build
lake build FepSketches
```

The catalogue body source is
[`scripts/catalogue_sketches.py`](../scripts/catalogue_sketches.py). The
tracked aggregate [`lean/FepSketches/fep_all.lean`](../lean/FepSketches/fep_all.lean)
is regenerated with
[`scripts/_maint_build_fep_all_lean.py`](../scripts/_maint_build_fep_all_lean.py).
CI rejects regeneration drift and proof holes in the aggregate.

## Catalogue source of truth {#catalogue-source-of-truth}

The YAML and `SKETCHES` sources must match exactly; the strict loader checks this
before execution.

## Cursor Lean 4 commands {#cursor-lean4-commands}

Use the canonical local commands above. Editor integrations should invoke the
same pinned Lake workspace rather than a separately discovered compiler.

## Mathlib4 modules used in fep_lean {#mathlib4-modules-used-in-fep_lean}

Topic rows declare their primary Mathlib module in `config/topics.yaml`; the
aggregate imports the built Mathlib environment through Lake.

`LeanVerifier` writes only transient `_verify_*.lean` files beneath
`lean/FepSketches/`; these are removed after each compilation.
