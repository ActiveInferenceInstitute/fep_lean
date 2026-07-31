# fep_lean — canonical backlog

Only open work belongs here. Completed work is represented by passing evidence
in the repository history or an eventual changelog; do not add struck-through
rows or a completed-work archive to this table.

| ID | Outcome | Acceptance probe | Dependencies | Priority | Evidence source |
| --- | --- | --- | --- | --- | --- |
| FEP-FULL-002 | Exercise a real Hermes plus OpenGauss plus Lean full-mode smoke run and then the complete selected catalogue. | With credentials supplied out of band, `uv run fep-lean preflight` is `status: ok`; `uv run fep-lean run --topic fep-001` and `uv run fep-lean run` return `complete: true`, with matching report and verification manifest counts. | A permitted provider key, healthy `gauss doctor`, and writable `GAUSS_HOME`. | P0 | `ISA.md` ISA-05/06; `src/pipeline/core.py`; `src/gauss/runner.py` |
| FEP-PROV-003 | Confirm the report receipt independently on a real complete full-mode run. | After FEP-FULL-002, recompute every `summary.json.artifact_hashes` entry, verify relative paths stay inside the run directory, and confirm the verification/run manifests agree with `complete`, mode, selected count, and topic rows. | FEP-FULL-002 and the checked-in report schema. | P1 | `src/output/reporter.py`; `tests/test_reporter.py`; `ISA.md` ISA-07 |
| FEP-MATH-006 | Review theorem meaning beyond sorry-free compilation, prioritizing statements whose assumptions or conclusions may be weaker than their FEP-facing prose. | Add a maintained theorem-maturity audit that names the intended invariant, checks non-vacuity/assumption strength, records a theorem-level acceptance probe, and links any status change to native compiler evidence; do not relabel a topic from `real` without that review. | Mathematical review and explicit theorem-author choices. | P2 | `config/topics.yaml`; `scripts/catalogue_sketches.py`; `docs/topics-reference.md` |
| FEP-QUAL-007 | Decide whether Ruff is a supported repository gate and, if so, remove the existing 222-error baseline without broad mechanical churn. | Either add a pinned Ruff dev dependency and make `uv run ruff check src tests scripts docs` plus its format gate pass in CI, or document the 222-error baseline as explicitly non-gating with an owner and staged debt plan. | Maintainer choice about style policy and Unicode/math-string exceptions. | P2 | `pyproject.toml`; `uv run ruff check src tests scripts docs`; `ISA.md` ISA-03 |

## Closure rule

An item leaves this table only when its acceptance probe passes in the current
checkout, the evidence is retained in a test/report/documentation change where
appropriate, and the result is recorded in the repository's changelog or
release notes. Until then, the row remains open even if a partial local probe
looks promising.
