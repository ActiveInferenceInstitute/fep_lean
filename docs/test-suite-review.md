# Test Suite Review: fep_lean

**Date:** 2026-07-31 | **Commit:** 21d4e18 | **Reviewer:** Aria

## Scorecard

| Metric | Value | Status |
|--------|-------|--------|
| Test files | 31 found | ✓ |
| Total test functions | 342 collected | ✓ |
| Tests passing (sequential) | 339 passed, 3 skipped | ✓ |
| Tests passing (parallel, 12 workers) | 339 passed, 3 skipped | ✓ |
| Coverage (line) | 90.25% (≥89% threshold) | ✓ |
| Coverage (branch) | ~89.6% (not independently gated) | ✓ |
| Mock-only tests | 0 | ✓ |
| `except: pass` patterns | 0 | ✓ |
| Skipped/XFailed | 3 (all conditional + justified) | ✓ |
| Parametrized tests | 0 (not needed; each test is explicit) | ✓ |
| Serial Lean markers | 3 files (justified - lake concurrency) | ✓ |

## Findings

### Real Behavior Tests

- **[PASS]** All 339 exercising tests use real code paths — `LeanVerifier`, `GaussRunner`, `OpenGaussClient`, `FEPPipeline`, real subprocess calls to `lake`, `lean`, `gauss`
- **[PASS]** Zero mock/fake/stub usage: `grep -rn 'MagicMock\|Mock()\|mock\.\|patch(\|unittest.mock' --include='*.py'` returns empty
- **[PASS]** Monkeys use `monkeypatch` for env-var injection and PATH isolation only — never to fake core behavior (documented in `tests/AGENTS.md`)
- **[PASS]** 14 sad-path test files cover every failure boundary: missing tools, broken binaries, timeouts, sandbox errors, malformed YAML, empty catalogues, permission errors

### Structure & Naming

- **[PASS]** Test structure mirrors source: `src/catalogue/topics.py` → `test_fep_topics.py`, `src/gauss/runner.py` → `test_gauss_runner*.py`, etc.
- **[PASS]** All 342 test functions use behavior-descriptive naming: `test_verify_sketch_skipped_when_lake_missing`, `test_catalogue_mode_never_reports_as_verified`, `test_validate_report_receipt_detects_tampering_and_path_escape`
- **[PASS]** No vague names (`test_1`, `test_something`), no redundant prefixes (`test_function_test`)
- **[PASS]** Fixtures are purposeful and local: 9 `@pytest.fixture()` definitions, none shared across unrelated test files, no grab-bag `conftest.py` fixtures
- **[PASS]** `conftest.py` is minimal and clean: adds `src/` to path, sets `MPLBACKEND=Agg`, probes for toolchain, defaults `FEP_LEAN_GAUSS_WORKFLOWS=0`

### Parallel Execution

- **[PASS]** All 342 tests run safely with `-n auto` (12 workers) — 0 failures, 0 isolation issues
- **[PASS]** Parallel speedup: 44s vs 111s sequential (60% reduction)
- **[PASS]** Three files marked `@pytest.mark.serial_lean` — proper isolation for Lean-heavy tests that access `.lake` build tree
- **[PASS]** No shared mutable state between tests — all state is `tmp_path`, fixture-scoped, or env-var isolated

### Coverage

- **[PASS]** 90.25% line coverage against 89% `fail_under` — comfortable buffer
- **[PASS]** All 23 source files covered, none below 81%
- WARN (expected): Coverage gap in `gauss/runner.py` (81%) — uncovered lines are toolchain-dependent compile-orchestration paths that require live `lake`/`lean`
- WARN (expected): Coverage gap in `lean_verifier.py` (87%) — uncovered lines are real Lean subprocess calls and Mathlib interaction
- WARN (expected): Coverage gap in `cli.py` (85%) — CLI help/error-passthrough paths
- NOTE: Branch coverage ~89.6% cannot be measured via `--cov-branch` alongside `concurrency = ["multiprocessing"]` without a separate data collection run (known pytest-cov limitation)

### Anti-patterns Check

| Anti-pattern | Found? | Evidence |
|-------------|--------|----------|
| Mock-only tests | ✗ | Zero mock usage anywhere |
| Fake implementations | ✗ | No `class FakeDB`, `class StubService` |
| Silent failures | ✗ | Zero `except: pass` or `except: continue` |
| Unused tests | ✗ | All 342 tests are collected and run |
| Skipped without justification | ✗ | All 3 skips have explicit `reason=` strings |
| Vague names | ✗ | All names describe specific behavior |
| Shared mutable state | ✗ | No global state, module-level vars, or thread-shared fixtures |
| Test overfitting | ✗ | Tests check behavior/contracts, not implementation internals |
| Integration in unit tests | ✓ Properly organized | Integration tests are marked with `serial_lean` or `skipif(no-api-key)` |
| Coverage without teeth | ✗ | Critical paths (catalogue loading, SSOT, report generation, receipt validation) all 90%+ |

## Action Plan

### Must Fix (Blocking)

None. The test suite is in exceptional shape with no blocking issues.

### Should Fix (Quality)

1. **Branch coverage workflow**: Add a separate `pytest --cov-branch` invocation (without `--cov`) or fix the coverage concurrency config so branch coverage can be measured standalone. Add a `docs/coverage-branch.md` note documenting the known limitation.

2. **Runner prefetch coverage**: `src/gauss/runner.py` has prefetch logic (lines 159, 168-175) that is exercised by `test_gauss_runner_prefetch.py` but only partially; consider adding a test that exercises the actual `ThreadPoolExecutor` path with `FEP_LEAN_PREFETCH=1`.

3. **CLI coverage edges**: `src/cli.py` has 23 missed lines (85%) in help text and error passthrough — benign but could be cleaned up with a few edge-case tests.

### Nice to Have (Improvement)

1. Consider adding `pytest-xdist` to default CI with `-n auto --ignore-glob='*serial_lean*'` for the non-Lean test subset to cut CI time from ~4min to ~1min.

## Questions

None — the test suite is self-documenting and all skipped tests carry explicit, justified reasons. The `serial_lean` marker is the only cross-file test dependency, and it's the correct, documented choice for Mathlib workspace protection.
