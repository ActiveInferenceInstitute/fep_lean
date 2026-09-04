# GNN bridge P1 finite spike — REPORT

Status: **P1 accepted; P2 accepted.** Date: 2026-09-03.
Provenance digests at run time: fep_lean
`315e32994b59fd80e327b5b654c9f7852fad9933`, GeneralizedNotationNotation
`12a565b2f18db7f18c3a799568ad057834ba0358`. Spec of record: `README.md`
in this directory. No Lean compilation was performed (task constraint;
none needed). No git state-changing command was run in either repo.

## Model projected

`FEP.ActiveInference.symmetricBoolModel trueBiasedPolicyPrior :
GenerativeModel Bool Bool Bool` from
`lean/FepSketches/active_inference.lean:743-749` (component defs:
`fairBoolLaw` :719-722, `fairBoolKernel` :725-728,
`trueBiasedPolicyPrior` :731-734; one-step semantics `predictedState`
:30-32). Every emitted value is an exact Lean literal with a file:line
comment in the artifact. Full extraction table: `README.md`,
"Extraction record".

## Acceptance items

| Item | Status | Evidence |
| --- | --- | --- |
| A1 instance + file:line | PASS | Extraction table in `README.md`; every value a source literal |
| A2 spec-first | PASS | `README.md` written before emitter/execution |
| A3 deterministic emitter in-slice | PASS | `projection.py`; 3 regenerations byte-identical (`cmp` clean, 5591 bytes) |
| A4 `gnn validate --strict` | PASS | exit 0 — "valid (12 variables, 9 connections)" |
| A5 pipeline steps 3,5,11,12 | PASS (with backend finding) | steps 3/5/11 exit 0; step 12 ran to completion, summaries written; its overall FAILED status is caused solely by the rxinfer backend (finding F1); pymdp + 5 more backends executed rc=0 |
| A6 ontology bindings canonical | PASS | supplementary step 10: 12 annotations, 12 valid, 0 invalid, exit 0; independent programmatic check against `act_inf_ontology_terms.json`: NONE non-canonical |
| A7 this report | DONE | — |
| P2.1 byte-identical regeneration | PASS | `cmp` clean across reruns (twice) |
| P2.2 `--check` freshness gate | PASS | fresh: exit 0; tamper test: injected byte → exit 1 with DRIFT reason; restored → exit 0 |
| P2.3 ruff + mypy from fep_lean root | PASS | `uv run ruff check` "All checks passed!"; `uv run mypy` strict "Success: no issues found in 1 source file" |

## Commands and exit codes (commands of record)

Run from the GNN repo root
(`GeneralizedNotationNotation/`):

```text
uv run gnn validate <slice>/gnn-input/FepLeanSymmetricBool.md --strict
  -> exit 0, "valid (12 variables, 9 connections)"

uv run python src/main.py \
  --target-dir <slice>/gnn-input \
  --output-dir   <slice>/gnn_output \
  --only-steps "3,5,11,12" --verbose
  -> exit 2 (runs 1, 2, and 3): steps 3,5,11 SUCCESS (exit 0);
     step 12 exit 1 (overall FAILED) — rxinfer backend returned 1

uv run python src/10_ontology.py --target-dir <slice>/gnn-input \
  --output-dir <slice>/gnn_output --verbose
  -> exit 0, "Validated 12 annotations: 12 valid, 0 invalid"
```

Run from the fep_lean repo root:

```text
uv run ruff check specs/gnn-bridge-p1-finite-spike/projection.py
  -> exit 0, "All checks passed!"
uv run mypy specs/gnn-bridge-p1-finite-spike/projection.py
  -> exit 0 (strict)
uv run python specs/gnn-bridge-p1-finite-spike/projection.py
  -> exit 0; byte-identical regeneration (cmp verified)
uv run python specs/gnn-bridge-p1-finite-spike/projection.py --check
  -> exit 0 (FRESH); exit 1 under an injected-byte tamper test
```

## Key summary numbers (run 2, verbatim from summaries)

- Render (`11_render_output/render_processing_summary.json`):
  `total_files 1, successful_files 1, failed_files 0,
  unsupported_framework_renderings [], total_framework_attempts 9,
  successful_framework_renderings 9, framework_success_rate 100.0` —
  pymdp (categorical backend, 536-LOC runner), jax, pytorch, numpyro,
  rxinfer, stan, activeinference_jl, discopy, bnlearn all rendered.
- Execute (`12_execute_output/summaries/execution_summary.json`):
  `total_scripts_found 9, successful_executions 6, failed_executions 1,
  skipped_executions 2`.
  - success rc=0: `activeinference_jl` 22.0s, `discopy` 0.8s, `jax`
    2.5s, `numpyro` 3.0s, `pymdp` 9.8s, `stan` 13.9s.
  - failed rc=1: `rxinfer` 32.5s — wrote
    `simulation_results.json`, `simulation.log`, `simulation_log.json`,
    and PNG plots to stdout before exiting 1 with empty stderr
    (finding F1). Distinct from `unsupported`: the backend executed.
  - skipped (dependency not installed): `bnlearn`, `pytorch`.
- Pipeline: 4/4 steps ran, 3 SUCCESS + 1 FAILED (step 12), duration
  126.9s; summary at
  `gnn_output/00_pipeline_summary/pipeline_execution_summary.json`.
- Reproducibility (run 3, 2026-09-03): with both repository digests
  unchanged (`315e3299…`, `12a565b2…`), `projection.py --check` exits 0,
  regeneration is byte-identical (5591 bytes, md5 `e233c2b5…`),
  `gnn validate --strict` exit 0 (12 variables, 9 connections), the
  full pipeline reproduces the document outcomes verbatim (render 9/9,
  `unsupported []`, pymdp rc=0; step 12 exit 1 with rxinfer as the sole
  backend failure, same artifacts-then-rc=1 signature), and step 10
  again validates 12/12. Runs 2 and 3 were compared by key numbers
  (render counts, per-framework status/return code), not bytes:
  pipeline summaries embed timestamps, so byte equality applies only
  to the regenerated document. Environment delta, not emitter drift: pytorch
  was installed in the GNN venv between runs 2 and 3 by concurrent
  work, so run 3 additionally executes pytorch rc=0 in 1.1s (7 success
  / 1 failed / 1 skipped). Run 2 is preserved at
  `gnn_output_run2_accepted/`; run 1 (annotated-connection document) is
  preserved at `gnn_output_run1_annotated/` as evidence for finding F2.

## Findings (no-go registry — recorded, none hand-fitted)

1. **F1 — rxinfer backend exit-code quirk (GNN side).** The rendered
   RxInfer.jl script produced all result artifacts (JSON, logs, PNGs)
   and then returned exit code 1 with empty stderr; step 12 therefore
   reports `failed_executions: 1` and the pipeline exits 2. Evidence
   plane: pipeline execution log
   `gnn_output_run2_accepted/12_execute_output/FepLeanSymmetricBool/rxinfer/execution_logs/`.
   Not caused by the emitted document (9/9 render succeeded; 6/9
   executed rc=0). Filed for the GNN side; not repaired here.
2. **F2 — pipeline parser vs v1.1 connection annotations (GNN side).**
   `doc/gnn/gnn_syntax.md` section 3 permits `A>B:label` and requires
   parsers to accept annotations, but `src/gnn/parsers/markdown_parser.py`
   `_parse_connection_definition` (lines 314-357) does not strip the
   annotation suffix, so step 3 warned "Connection references unknown
   target variables" for annotated edges. Observed in run-1 logs
   (`gnn_output_run1_annotated/00_pipeline_logs/pipeline.jsonl` and
   `pipeline.log`, identical): 3 warning lines naming
   `['s:prior_initialization']`, `['B:transition']`,
   `['s_prime:state_prediction']` — a summary-level count, not one line
   per edge (the run-1 document had 9 annotated edges; per-edge
   warnings are not individually observable in the logs), while
   `gnn validate --strict` (different code path) accepted the same
   file. The three flagged edges are the document's first three
   connections; the six later annotated edges (`s_prime-A` through
   `G>π`) produced no warnings in the same parse, so annotation
   handling is inconsistent even within a single step-3 pass.
   Mitigation inside this slice only: the emitter now emits plain
   v1.0 edges; semantic labels moved to ModelAnnotation/Equations
   comments. Filed for the GNN side.
3. **F3 — C emitted as probability law.** Lean
   `preferences : FiniteLaw Outcome` is a probability law; binding
   `C=Preferences` (canonical) is used, not `C=LogPreferenceVector`,
   because a log transform is a representation decision (and
   `log(1/2)` is non-terminating), not data derivable from the Lean
   definition. See `README.md` rounding policy.
4. **No `u`/Action surface.** `GenerativeModel` carries no Action type;
   emitting one would require interpretation (contract section 9
   trigger). Nothing emitted.

## Evidence planes (firewall, contract section 7)

- **Lean source reading (extraction).** Establishes: the projected
  literals match the named definitions at the cited file:line, in a
  workspace whose `src/fep_lean/formal/manifest.py:95-96` projects
  `active_inference.lean` into the pinned Lean workspace. Never
  establishes: theorem truth (that is the pinned workspace's
  compilation plane), semantic reach, or model correctness.
- **GNN pipeline run (steps 3/5/10/11/12).** Establishes: the document
  parses (12 variables, 9 connections), type-checks, renders on 9
  backends, and executes on 6 backends including the categorical pymdp
  backend. Never establishes: mathematical correctness of the model or
  any Lean claim. No execution statistic was compared with any
  Lean-witnessed property in this slice (that is P3).

## File list (this slice)

| File | Role |
| --- | --- |
| `README.md` | Spec slice: extraction record, rounding policy, ontology bindings, acceptance, findings |
| `projection.py` | Deterministic emitter + `--check` freshness gate (P2) |
| `gnn-input/FepLeanSymmetricBool.md` | Emitted GNN document (accepted artifact, 5591 bytes) |
| `gnn_output/` | Dedicated pipeline output for run 3 (fresh reproduction; never the shared GNN `output/`) |
| `gnn_output_run2_accepted/` | Preserved run-2 output (the originally accepted run) |
| `gnn_output_run1_annotated/` | Preserved run-1 output (evidence for finding F2) |
| `REPORT.md` | This file |

## Blockers

None for P1/P2. The three findings above are filed for the owning
repositories; none blocks this slice's acceptance criteria.
