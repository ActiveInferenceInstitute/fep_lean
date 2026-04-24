# Reporter — fep_lean Output Generation

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

## Overview

`output/reporter.py` (`Reporter`) writes the timestamped directory under `output/reports/run_*/`. It is invoked from `pipeline/orchestrator.run_pipeline` via `Reporter.generate(catalogue, pipeline_result)` after `FEPPipeline.run()` completes.

Template **Stage 02** (`scripts/02_run_analysis.py` from the repo root) must finish the analysis scripts that feed `run_pipeline` so `PipelineResult` and the report bundle stay consistent with the same catalogue run. If Stage 02 kills a script on timeout, downstream stages may see partial or stale inputs — see [troubleshooting.md](troubleshooting.md).

---

## Output Directory Structure

```text
output/reports/run_YYYYMMDD_HHMMSS/
├── index.md                 ← Master report: pipeline summary + stage table
├── summary.json             ← Machine-readable PipelineResult
├── hermes_report.md         ← Per-topic Hermes explanation status
├── lean_report.md           ← Per-topic Lean 4 compilation status
├── validation_report.md     ← 13 environment check details
└── topics/                  ← Per-topic `fep-NNN.md` (full catalogue row)
```



---

## File Contents

### `index.md` — Master Report

Sections:

1. **Header**: Run timestamp, pipeline status (`ok` / `partial` / `error`), total duration
2. **Stage table**: Step name, status (✅/❌/⏭️), message, duration
3. **Summary stats**: topics ok/error, Hermes successes, Lean compile ok, duration
4. **Quick links**: to the other report files and `topics/`

Example stage table (names from `FEPPipeline`):

```markdown
| Stage | Status | Message | Duration |
|-------|--------|---------|----------|
| Load Catalogue | ✅ ok | 50 topics | 0.017s |
| Environment Validation | ✅ ok | 13 checks, 0 failed | 0.998s |
| Gauss Sessions | ⏭️ skipped | workflows disabled | 0s |
| Manuscript Artifacts | ✅ ok | vars + unified 09z formalism + figures | 0.004s |
```

### `hermes_report.md` — Hermes Status

Per-topic table with:
- Topic ID and title
- Hermes success (✅/❌) and model used
- Explanation (first 200 chars)
- Duration

### `lean_report.md` — Lean Verification

Per-topic table with:
- Topic ID and title
- `VerifyResult.status` (`compiles_clean` / `compiles_with_sorry` / `compile_error` / `skipped`)
- Has `sorry` flag
- Lean version
- Duration

### `validation_report.md` — Environment Checks

Per-check section with pass/fail status for all **13** `run_validation_checks` results. The checks (declared at `src/verification/environment.py:328-343`) are:

1. `math_inc_gauss_cli` — `gauss` (math-inc/OpenGauss) on PATH, `gauss doctor` passes
2. `lean_cli` — `lean --version` resolves under elan/FEP overrides
3. `open_gauss_config_dir` — `~/.gauss/` (or `$GAUSS_HOME`) is writable
4. `lean_workspace` — `lean/lakefile.lean` and `lean-toolchain` exist
5. `mathlib_built` — `.lake/build/lib/Mathlib.olean` is present
6. `topics_yaml` — `config/topics.yaml` parses with 50 entries
7. `project_layout` — `src/`, `tests/`, `scripts/`, `manuscript/` present
8. `python_scientific_stack` — `numpy`, `matplotlib`, `pyyaml` importable
9. `output_writable` — `output/` directory writable
10. `manuscript_config` — `manuscript/config.yaml` parses
11. `scripts_tests_layout` — thin-orchestrator script files exist
12. `catalogue_loader` — `catalogue/topics.py` imports and loads the YAML
13. `references_bib` — `manuscript/references.bib` present

### `summary.json` — Machine-Readable Result

Shape follows `PipelineResult.as_dict()` plus fields the reporter may add when serializing:

```json
{
  "status": "ok",
  "total_duration": 52.3,
  "run_dir": "output/reports/run_20260406_120000",
  "stages": [
    {"name": "Load Catalogue", "status": "ok", "duration_s": 0.017, "error": null}
  ],
  "lean_stats": {"total_processed": 0, "compiles_clean": 0, ...}
}
```

---

## `Reporter` API

```python
class Reporter:
    def __init__(self, project_root: Path, run_id: str | None = None) -> None

    def generate(
        self,
        catalogue: FEPTopicCatalogue,
        result: PipelineResult,
    ) -> ReportPaths

@dataclass
class ReportPaths:
    index_md: Path
    summary_json: Path
    hermes_md: Path
    lean_md: Path
    validation_md: Path   # path to validation_report.md on disk
    topics_dir: Path

    def all_paths(self) -> list[Path]
    def as_dict(self) -> dict[str, str]
```

---

## Design Rules

1. **Never overwrite**: Each run creates a new timestamped `run_YYYYMMDD_HHMMSS/` directory.
2. **Partial-safe**: If Hermes/Lean stages were skipped, their reports show the skip reason.
3. **No external deps**: Reports are written with stdlib only (no Jinja, no pandas).
4. **Self-contained**: Each run directory is fully self-contained — no symlinks, no shared state.

---

## Navigation

- [← Hermes](hermes.md)
- [Pipeline →](pipeline.md)
- [← docs/README.md](README.md)
