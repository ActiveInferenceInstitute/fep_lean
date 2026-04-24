# Lean workspace — FEP Sketches

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

Lake package with full **Mathlib4 v4.29.0** dependency (see `lakefile.lean` / `lake-manifest.json`).

## One-Time Setup

Run from a regular (non-sandboxed) terminal:

```bash
# From the project root (directory containing pyproject.toml)
bash scripts/_maint_bootstrap_lean_toolchain.sh
# (``00_lean_mathlib_setup.sh`` is a thin wrapper to the same bootstrap.)
```

Or manually:

```bash
cd lean
lake update        # fetch Mathlib4
lake exe cache get # download ~3 GB prebuilt .olean cache
lake build         # build FepSketches
```

## Manual Verification

```bash
cd lean && lake build
```

## Smoke Test

```bash
cd lean
lake env lean FepSketches/Basic.lean
```

## Environment Variables

| Variable | Purpose |
|---|---|
| `FEP_LEAN_LAKE_EXE` | Override path to `lake` binary |
| `FEP_LEAN_LEAN_EXE` | Override path to `lean` binary |
| `ELAN_HOME` | Override elan home (default: `/tmp/fep_lean_elan`) |
| `FEP_LEAN_VERIFY_TIMEOUT` | Compilation timeout in seconds (default: 300) |
