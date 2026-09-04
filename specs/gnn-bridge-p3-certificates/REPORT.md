# GNN bridge P3 certificate protocol — REPORT

Status: **P3 done** — protocol defined AND run; every statable
certificate (C1, C2) carries both evidence planes and passes; C3 is a
recorded boundary (conditionally statable, condition not met); the O1
cross-convention divergence is filed with exact numbers. Date:
2026-09-03. Digests at run time: fep_lean
`315e32994b59fd80e327b5b654c9f7852fad9933`,
GeneralizedNotationNotation `12a565b2f18db7f18c3a799568ad057834ba0358`
(unchanged from P1/P2 acceptance). No Lean compilation was performed;
no git state-changing command was run in either repo.

## Protocol instance

Model: `FEP.ActiveInference.symmetricBoolModel trueBiasedPolicyPrior`
(`lean/FepSketches/active_inference.lean:743-749`); executed artifact:
the accepted P1 document `FepLeanSymmetricBool.md`, re-run under P3
custody (input read-only from the P1 slice, output dedicated to
`gnn_output/` here).

## Acceptance items

| Item | Status | Evidence |
| --- | --- | --- |
| P3.1 spec-first | PASS | this slice's README precedes certify.py and the run |
| P3.2 custody run | PASS | steps 3/5/11 exit 0; ontology 12/12 exit 0; step 12 exit 1 caused solely by rxinfer (P1 finding F1 signature, recorded verbatim) |
| P3.3 script gates | PASS | `uv run ruff check`: "All checks passed!"; `uv run mypy` (strict): "Success: no issues found in 1 source file" |
| P3.4 C1 | PASS | executed `policy_posterior[0] = (0.25, 0.7500000596046448)` vs Lean `Q(π) = (1/4, 3/4)` exact (theorem :816-826 + prior :731-734); |Δtrue| = 5.960e-08 ≤ 1e-6; argmax = true on both sides |
| P3.4 C2 | PASS | executed `variational_free_energy[0] = 0.6931471824645996` vs Lean closed form `log 2 = 0.6931471805599453`; |Δ| = 1.905e-09 ≤ 1e-6 |
| P3.5 C3 | BOUNDARY | not run: one-step instance (`num_timesteps: 1`) and no Lean-witnessed decrease family on the Boolean carrier (README C3) |
| P3.6 O1 | FILED | executed `expected_free_energy[0] = 0.5` (pymdp `neg_efe`; linear utility `Σ q(o)·C(o)`, `pymdp/control.py:422-445`) vs Lean `expectedFreeEnergy = log 2 = 0.6931471805599453` (:148-150, :789-812); Δ = 0.193147; three C-conventions coexist (pymdp payoff vector / GNN exemplar "log-probabilities" + `C=LogPreferenceVector` / Lean probability law + `risk = finiteKL`, :128-131) |
| P3.7 report | DONE | this file |

Gate: `certify.py` exit 0 (C1 and C2 within tolerance 1e-6).

## Commands and exit codes

From the GNN repo root:

```text
uv run python src/main.py \
  --target-dir <p1-slice>/gnn-input \
  --output-dir <p3-slice>/gnn_output \
  --only-steps "3,5,11,12" --verbose
  -> exit 2: steps 3,5,11 SUCCESS; step 12 exit 1 (rxinfer backend rc=1,
     same artifacts-then-fail signature as P1 finding F1)
uv run python src/10_ontology.py --target-dir <p1-slice>/gnn-input \
  --output-dir <p3-slice>/gnn_output --verbose
  -> exit 0, "Validated 12 annotations: 12 valid, 0 invalid"
```

From the fep_lean repo root:

```text
uv run ruff check specs/gnn-bridge-p3-certificates/certify.py
  -> exit 0, "All checks passed!"
uv run mypy specs/gnn-bridge-p3-certificates/certify.py
  -> exit 0 (strict)
uv run python specs/gnn-bridge-p3-certificates/certify.py
  -> exit 0; C1 PASS, C2 PASS, O1 finding printed, gate PASS
```

## Evidence planes (as carried by the comparisons)

- **C1.** Lean side: native Lean compilation (pinned workspace,
  theorem `policyPosterior = policyPrior`, :816-826) + numerical
  witness (exact rationals 1/4, 3/4 evaluated as exact decimals).
  Executed side: GNN pipeline execution (pymdp `infer_policies`
  posterior serialized in `simulation_results.json`).
- **C2.** Lean side: native Lean compilation (proved equalities
  :209-214, :762-773, :121-125, :745) + numerical witness (float64
  `math.log(2)` evaluation of the proved closed form). Executed side:
  GNN pipeline execution (pymdp `infer_states` VFE serialized by the
  executed runner, `src/execute/pymdp/pymdp_simulation.py:450,468`).
- **O1.** Same planes as above for the EFE pair, compared
  informatively: the quantities differ by convention, so no plane is
  reclassified and no equality is claimed. The GNN-side question this
  raises (which C-convention `expected_free_energy` serialization
  promises) is filed for the GNN side, with pymdp 1.0.0's linear
  utility (`pymdp/control.py:422-445`) contradicting the GNN exemplar's
  own "log-probabilities" comment and the `LogPreferenceVector`
  binding.
- Statistic-level rule honored: the certificate compares the executed
  policy-posterior distribution to the Lean distribution; the executed
  `actions[0] = 1` sample is used only as an argmax consistency
  observation, never as a distribution claim.

## Artifact list (this slice)

| Artifact | Role |
| --- | --- |
| `README.md` | Spec slice: protocol definition, Lean closed forms with file:line, comparison policy, custody, acceptance, no-go registry |
| `certify.py` | Certificate runner (C1/C2 + O1 observation; ruff + mypy strict clean) |
| `certificates.json` | Machine-readable comparison output |
| `CERTIFICATES.md` | Human-readable certificate table with evidence planes |
| `gnn_output/` | Dedicated pipeline output for the P3 custody run (never the shared GNN `output/`) |
| `REPORT.md` | This file |

## Blockers

None. P3 is done as defined: the protocol is defined, was run under P3
custody, and every statable comparison carried its evidence planes; the
conditionally-statable C3 is recorded as a boundary, and the O1
divergence is filed with exact numbers rather than smoothed over.

## Verification (2026-09-04)

Independent end-to-end verification of the committed slice. No consumed
artifact was modified; `git status` is clean for the slice before and
after the re-run.

README reconciliation: the committed acceptance checklist was found
already fully checked (P3.1–P3.7 all `[x]`) — the briefing expected
P3.3 unchecked; only the status line ("active; P3 in progress —
protocol defined, run pending") was stale. Every named command behind
the boxes was independently re-verified here (all exit 0); this pass
flipped no box — the status line was the only checklist-area edit.

### Re-run (from the fep_lean repo root)

```text
uv run python specs/gnn-bridge-p3-certificates/certify.py
  -> exit 0; C1 PASS (|dfalse| = 0.000e+00, |dtrue| = 5.960e-08);
     C2 PASS (|d| = 1.905e-09); O1 finding printed; gate PASS
     (tolerance 1e-06)
uv run ruff check specs/gnn-bridge-p3-certificates/certify.py
  -> exit 0, "All checks passed!"
uv run mypy specs/gnn-bridge-p3-certificates/certify.py
  -> exit 0, "Success: no issues found in 1 source file"
     (pyproject [tool.mypy] strict = true)
```

Regenerated `certificates.json` and `CERTIFICATES.md` are byte-identical
to the committed artifacts (sha256 `98d10b09…a60bd9` and
`d2810b8d…31ddd` respectively).

### Custody re-check

- `gnn_output/00_pipeline_summary/pipeline_execution_summary.json`:
  `target_dir` = the P1 slice `gnn-input/` (read-only), `output_dir` =
  this slice's `gnn_output/`, `only_steps = "3,5,11,12"`; per-step
  `exit_code`: 3_gnn 0, 5_type_checker 0, 11_render 0, 12_execute 1
  (`framework_status`: 7 frameworks success, rxinfer failed rc=1,
  bnlearn skipped — the P1 finding F1 signature).
- Step 10 ontology (run separately, same custody): summary = 12
  annotations, 12 valid, 0 invalid, coverage 1.0.
- The shared GNN `output/`
  (`projects/outside_of_hum/GeneralizedNotationNotation/output/`)
  contains no `FepLean*` artifacts; its `pipeline.jsonl` and
  `pipeline_execution_summary.json` records end at the 2026-06-18
  `pomdp_gridworld` run. Directory/file mtimes there were touched
  2026-09-03 21:50 (before this slice's 21:57:48 custody run) with no
  new run records — noted for completeness; no consumed artifact is
  involved.
- Digest drift since the run: fep_lean was at
  `315e32994b59fd80e327b5b654c9f7852fad9933` at run time (commit present
  in history; current HEAD `9c6a7e5` reflects the landed Q2 slice — the
  P3 slice files are unchanged); GeneralizedNotationNotation was at
  `12a565b2f18db7f18c3a799568ad057834ba0358` at run time (commit
  present; current GNN HEAD `71aa9e3`). The certificate re-run consumes
  only committed `gnn_output/` artifacts, so neither move affects it.

### Certificate values confirmed (README claims)

| Claim | Verified |
| --- | --- |
| C1 `Q(π) = (1/4, 3/4)`, argmax true | executed `policy_posterior[0] = (0.25, 0.7500000596046448)`; `abs(dtrue) = 5.960e-08 ≤ 1e-6`; argmax = true on both sides (`actions[0] = 1` used as argmax-consistency observation only) |
| C2 VFE = log 2, delta ≤ 1e-6 | executed `variational_free_energy[0] = 0.6931471824645996` vs `log 2 = 0.6931471805599453`; `abs(d) = 1.905e-09 ≤ 1e-6` |
| C3 boundary, not run | one-step instance (`num_timesteps: 1` in the executed results); no Boolean-carrier decrease theorem exists (README C3) |
| O1 filed with both numbers | executed `expected_free_energy[0][0] = 0.5` vs Lean `expectedFreeEnergy = log 2 = 0.6931471805599453`; delta = 0.193147 |

Lean anchors spot-checked at verification time:
`trueBiasedPolicyPrior` (`lean/FepSketches/active_inference.lean:731-734`,
mass `if policy then 3 / 4 else 1 / 4`), `symmetricBoolModel` (:743-749),
`symmetricBoolModel_policyPosterior_eq_prior` (:816-826) — exactly as
cited in the README.

### Cross-check with the Q2 slice

The certificate target model and the Q2 denotation target are the same
instance: `FEP.ActiveInference.symmetricBoolModel trueBiasedPolicyPrior`
(`lean/FepSketches/active_inference.lean:743-749`). The Q2 slice
(`specs/gnn-bridge-q2-discrete-denotation/README.md`, "Fixed exemplar")
proves `denoteDiscrete symBoolDoc symBoolPayload symBoolConforms =
symmetricBoolModel trueBiasedPolicyPrior` over the same P1 document
`FepLeanSymmetricBool.md` whose P3 custody re-run supplies the executed
quantities certified here. Denotation (Lean plane) and execution (GNN
plane) therefore meet on one named model instance; no evidence plane is
merged (contract section 7).
