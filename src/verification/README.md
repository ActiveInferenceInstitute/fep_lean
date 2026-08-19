# fep_lean/src/verification/

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

Lean 4 / Lake compilation checks and toolchain-environment validation for
`fep_lean`. Depends only on `gauss.cli.check_gauss_cli` plus the stdlib; does
not import the LLM or pipeline layer.

## Modules

| Module | Role |
| ------ | ---- |
| [`environment.py`](environment.py) | `run_validation_checks` — **13** named checks used by `FEPPipeline` stage 2. |
| [`lean_verifier.py`](lean_verifier.py) | `LeanVerifier`, `VerifyResult` — runs `lake env lean` on sketches under `lean/FepSketches/`. |
| [`preflight.py`](preflight.py) | `run_preflight()` — interactive toolchain smoke test (`gauss`, `lake`/`lean`, Mathlib oleans). Console script **`fep-lean-preflight`** in [`pyproject.toml`](../../pyproject.toml). Not imported by `environment.py`; call it before long `lake build`s or CI. |

## `LeanVerifier`

Constructor: `LeanVerifier(lean_dir, project_root)`. The verifier writes a
sketch to a temp file inside `lean/FepSketches/` and calls `lake env lean`.
Sketches that contain `sorry` are classified as *compile with warnings*
rather than *fail*.

### Methods

- `verify_sketch(topic_id, lean_code) → VerifyResult` — compile a single
  sketch. Wraps the body with the canonical Mathlib imports and `open`
  statements.
- `verify_batch(items) → list[VerifyResult]` — sequential (`max_workers=1`);
  do not lower — parallel `lake env lean` hits a macOS ELAN sandbox
  deadlock.
- `check_mathlib_built() → bool` — probes that the Mathlib `.olean` cache
  is present (fast smoke check; does not run `lake build`).
- `check_lake_available() → bool` — checks that `lake` / `lean` are on PATH
  or resolvable from `~/.elan/toolchains/` / the `FEP_LEAN_LAKE_EXE` and
  `FEP_LEAN_LEAN_EXE` overrides.
- `lean_version() → str | None` — cached `lean --version`.

### `VerifyResult` fields

| Field | Type | Meaning |
| ----- | ---- | ------- |
| `compiles` | `bool` | `True` iff `lake env lean` exited `0`. |
| `has_sorry` | `bool` | `True` iff the sketch contains a `\bsorry\b` token. |
| `errors` | `list[str]` | Compiler error lines (`.+ error:` pattern). |
| `warnings` | `list[str]` | Compiler warning lines. |
| `stdout` | `str` | Full combined output. |
| `duration_s` | `float` | Elapsed seconds. |
| `lean_version` | `str` | `lean --version` string (cached). |
| `topic_id` | `str` | Catalogue row id. |
| `lean_file` | `Path \| None` | Temp file used; cleaned up on success. |

## `run_validation_checks` (13 checks)

Called from pipeline stage 2. The full list, in order: `gauss` CLI,
`lake`/`lean` CLIs, `lean/` workspace directory, Mathlib build probe,
`config/topics.yaml` YAML validity, project layout, Python interpreter
stack, writable output directories, manuscript `config.yaml`, `scripts/`
and `tests/` directories present, catalogue import round-trip, and an
optional `references.bib` check.

## `preflight.py`

`run_preflight()` is the console-script entry point bound to
**`fep-lean-preflight`** via `pyproject.toml`. It is an interactive
smoke-check for the toolchain: `gauss` CLI, `lake` / `lean`, Mathlib
oleans. Not imported by `environment.py` — call before a long `lake build`
or CI run to surface toolchain drift early.

See [`AGENTS.md`](AGENTS.md) for the import-contract notes (especially the
macOS ELAN sandbox workarounds in `_toolchain.py`) and the cross-wiring
from `gauss.runner.GaussRunner` (verify-stage).
