# fep_lean — canonical backlog

Only open work belongs here. Completed work is represented by passing evidence
in the repository history or an eventual changelog; do not add struck-through
rows or a completed-work archive to this table.

| ID | Outcome | Acceptance probe | Dependencies | Priority | Evidence source |
| --- | --- | --- | --- | --- | --- |
| FEP-FULL-002 | Exercise a real Hermes plus OpenGauss plus Lean full-mode smoke run and then the complete selected catalogue. | With credentials supplied out of band, `uv run fep-lean preflight` is `status: ok`; `uv run fep-lean run --topic fep-001` and `uv run fep-lean run` return `complete: true`, with matching report and verification manifest counts. | A permitted provider key, healthy `gauss doctor`, and writable `GAUSS_HOME`. | P0 | `ISA.md` ISA-05/06; `src/pipeline/core.py`; `src/gauss/runner.py` |
| FEP-PROV-003 | Confirm the report receipt independently on a real complete full-mode run. | After FEP-FULL-002, recompute every `summary.json.artifact_hashes` entry, verify relative paths stay inside the run directory, and confirm the verification/run manifests agree with `complete`, mode, selected count, and topic rows. | FEP-FULL-002 and the checked-in report schema. | P1 | `src/output/reporter.py`; `tests/test_reporter.py`; `ISA.md` ISA-07 |

## Closure rule

An item leaves this table only when its acceptance probe passes in the current
checkout, the evidence is retained in a test/report/documentation change where
appropriate, and the result is recorded in the repository's changelog or
release notes. Until then, the row remains open even if a partial local probe
looks promising.
