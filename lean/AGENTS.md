# fep_lean/lean/

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

Full **Lake** workspace with **Mathlib4** dependency for FEP theorem verification.

## Toolchain

- **Lean**: `leanprover/lean4:v4.29.0` (see `lean-toolchain`)
- **Mathlib**: `v4.29.0` — see `lake-manifest.json` `rev` (e.g. `8a178386ffc0f5fef0b77738bb5449d50efeea95` for the current lockfile)

## Layout

| File / Dir | Purpose |
|---|---|
| `lakefile.lean` | Lake package: declares `require mathlib` |
| `lean-toolchain` | Pins Lean 4 toolchain version |
| `lake-manifest.json` | Pins Mathlib4 git commit for reproducibility |
| `FepSketches/` | Library root; temporary verification files written here |
| `.lake/packages/mathlib/` | Downloaded Mathlib4 source (after `lake exe cache get`) |

## One-Time Setup (non-sandboxed terminal)

```bash
# From the project root

# 1. Run the automated bootstrap script
bash scripts/_maint_bootstrap_lean_toolchain.sh
# (`fep-lean setup` wraps the same script.)

# Or manually:
cd lean
lake update           # fetch Mathlib4 @ v4.29.0 (see `lakefile.lean`)
lake exe cache get    # download ~3 GB prebuilt .olean cache
lake build            # build FepSketches against Mathlib
```

## Verification Workflow

After setup, `LeanVerifier` in `src/verification/lean_verifier.py` calls:

```bash
lake env lean FepSketches/_verify_{topic_id}_{random}.lean
```

This inherits the full Mathlib4 environment so all 50 topic sketches
with `import Mathlib.*` resolve correctly.

## macOS Sandbox Bypass

The elan proxy may fail with `settings.toml: Operation not permitted`
in sandboxed AI agent shells.  `LeanVerifier` bypasses this by:

1. Setting `ELAN_HOME=/tmp/fep_lean_elan` (writable temp dir)
2. Resolving `lake`/`lean` via direct toolchain path:
   `~/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lake`
3. Respecting `FEP_LEAN_LAKE_EXE` / `FEP_LEAN_LEAN_EXE` env overrides

## Lessons Learned: Concurrency & Lock Contention

During pipeline hardening, attempting to parallelize `lake env lean` operations via multi-threading (`ThreadPoolExecutor`) triggered systemic failure. macOS ELAN sandbox proxies do not resolve isolated container paths efficiently when invoked simultaneously across 10+ subshells.
This lock contention results in silent import masking—the `lean` parser successfully spins up but cannot load `Mathlib` files from the cache, wildly returning mathematical false positives (e.g., `unknown identifier 'measure_union_le'`).

**The Agentic Rule**: Always execute formal theorem verification instances **serially** (`max_workers=1`). The minimal overhead of sequential processing strictly outweighs the orchestration deadlocks and non-deterministic logic anomalies caused by local thread saturation.

## See also

- [../AGENTS.md](../AGENTS.md) — project-level documentation
- [../docs/lean4.md](../docs/lean4.md) — Lean4 + Mathlib4 context
- [../scripts/_maint_bootstrap_lean_toolchain.sh](../scripts/_maint_bootstrap_lean_toolchain.sh) — setup automation (`fep-lean setup` delegates here)
- [math-inc/OpenGauss](https://github.com/math-inc/OpenGauss) — optional CLI integration
