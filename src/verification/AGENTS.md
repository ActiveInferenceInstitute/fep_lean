# fep_lean/src/verification/ — Lean 4 Compilation & Environment Checks

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

## Purpose

Three verification surfaces:

1. **Lean 4 compilation** — `LeanVerifier` invokes `lake env lean` on a refined sketch and returns a structured `VerifyResult`; methods: `verify_sketch(topic_id, lean_code)`, `verify_batch(items)`, `check_lake_available()`, `lean_version()`.
2. **Environment validation** — `run_validation_checks()` runs **13** named checks (including `mathlib_built`) before pipeline stage 3.
3. **CLI preflight** — `run_preflight()` in `preflight.py` prints a human-readable toolchain probe (`gauss`, `lake`/`lean`, Mathlib oleans). Entry point: `fep-lean-preflight` ([`pyproject.toml`](../../pyproject.toml)). Not wired into `environment.py`; optional before long builds or debugging CI.

## Files

- `environment.py` — `run_validation_checks`
- `lean_verifier.py` — `LeanVerifier`, `VerifyResult`
- `preflight.py` — `run_preflight`, `main` for `fep-lean-preflight`
- `__init__.py` — re-exports `LeanVerifier`, `VerifyResult`, `run_validation_checks` only

## Public API

| Symbol | Kind | Description |
| --- | --- | --- |
| `LeanVerifier` | class | Runs `lake env lean` against a Lean sketch and parses output |
| `VerifyResult` | dataclass | Fields: `compiles`, `has_sorry`, `errors`, `warnings`, `stdout`, `stderr`, `duration_s`, `lean_version`, `topic_id`, `lean_file`, `skip_reason`; property `status` |
| `run_validation_checks` | function | 13-check project + toolchain validation |
| `run_preflight` | function | Optional exit-code CLI probe (`from verification.preflight import run_preflight`) |

## Imports

```python
from verification.environment import run_validation_checks
from verification.lean_verifier import LeanVerifier, VerifyResult
from verification.preflight import run_preflight
```

## Notes

- `LeanVerifier` is shell-out heavy; tests use real fixture Lean files plus `tmp_path` rather than direct execution.
- `run_validation_checks` is called by `pipeline/orchestrator.py` before stage 3 so the pipeline fails fast on a missing toolchain.

## See Also

- [`README.md`](README.md)
- [`../AGENTS.md`](../AGENTS.md)
- [`../pipeline/AGENTS.md`](../pipeline/AGENTS.md) — pipeline that consumes both the preflight and the Lean check
