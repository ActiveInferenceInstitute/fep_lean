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
