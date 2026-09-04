# Q4 report — renderer and execution statements

Slice: `specs/gnn-bridge-q4-renderer-execution-statements/` (Direction 2
stage Q4, alignment statement 5). Date: 2026-09-04. Spec:
[README.md](README.md). Evidence classification follows the bridge
contract's evidence firewall (section 7): everything below is the *native
Lean compilation* plane — it establishes that the named statements compile
and the named proofs hold on the carriers; it establishes nothing about GNN
pipeline behavior.

## Artifacts

| Artifact | Change |
| --- | --- |
| `src/fep_lean/formal/gnn_render_statements.lean` | new foundation resource, namespace `FEP.GnnRenderStatements` |
| `src/fep_lean/formal/manifest.py` | one FOUNDATION row appended (`gnn_render_statements.lean` / `FepSketches.gnn_render_statements` / `FEP.GnnRenderStatements`), immediately after the Q3 worker's `gnn_denotation_continuous` row |
| `lean/FepSketches/gnn_render_statements.lean` | script-owned projection (never hand-edited) |
| `docs/formalism-coverage.md`, `docs/formalism-coverage.json`, `docs/lean-landscape.md` | script-owned projections regenerated after the roster grew by both new modules |
| `tests/test_formal_composition.py` | the manifest-roster pin (`foundation_resources` tuple and the `declaration_namespace` tuple) extended with both new resources — this shared pin was broken by the roster growth of Q3's row first and Q4's row second; both rows are pinned in manifest order |
| `specs/gnn-bridge-q4-renderer-execution-statements/{README.md,REPORT.md}` | the slice's spec and evidence record |

No edits to the Q1 AST module, the Q2 denotation module, the Q3 continuous
denotation module, any existing Lean carrier, `composed.lean`, or
`fep_all.lean` (catalogue-driven).

## Per-target disposition

Render targets (step 11, `GeneralizedNotationNotation/src/render/render.py`
`RENDER_CLI_TARGETS`):

| Target | Disposition | Lean statement | Proof status |
| --- | --- | --- | --- |
| `pymdp` | statable (discrete matrix fragment) | `Statement5Pymdp` | proved (shared `statement5DiscreteMatrices_holds`) |
| `rxinfer` | no-go — Julia `@model` factor graph; no message-passing semantics in fep_lean | — | — |
| `rxinfer_toml` | no-go — TOML configuration artifact; no operational semantics | — | — |
| `activeinference_jl` | statable (discrete matrix fragment) | `Statement5ActiveInferenceJl` | proved (shared) |
| `discopy` | no-go — string diagram; functorial semantics lives DisCoPy-side | — | — |
| `discopy_combined` | no-go — same artifact class | — | — |
| `bnlearn` | no-go for program semantics; CPT-layout fragment deferred (pgmpy parent-instantiation enumeration unfrozen on the GNN side) | — | — |
| `jax` | statable (discrete matrix fragment); continuous fragment not stated — the Q3 carrier consumes only the prior gauge, so no `F`/`H`/`Q`/`R` counterpart field exists | `Statement5Jax` | discrete fragment proved (shared) |
| `jax_pomdp` | statable (discrete matrix fragment) | `Statement5JaxPomdp` | proved (shared) |

Counts: 4 statable-and-proved targets, 1 statable-discrete target with its
continuous fragment not statable today (`jax`), 5 documented no-gos
(including bnlearn's deferred fragment). No fake statements: every no-go
row carries no Lean declaration.

Execute targets (step 12): the Direction 2 table assigns the *family
denotations* as the Lean target for this row, realized here as the proved
execution semantics (`policyRollout`, below); `pymdp`, `activeinference_jl`,
`jax`, and `pytorch` can carry it conditionally per program via
`DiscreteExecutionSemantics`; `rxinfer`, `discopy`, `numpyro`, and `stan`
are no-go rows (message-passing / diagram-execution / NUTS-SVI / HMC
sampling semantics have no formal counterpart in fep_lean).

## Statements and proof status

In `FEP.GnnRenderStatements`:

| Declaration | Kind | Status |
| --- | --- | --- |
| `DiscreteTargetTables` | structure (frozen target layout) | definition |
| `DiscreteTargetFaithful` | Prop (frozen layout contract) | definition |
| `Statement5DiscreteMatrices` | Prop (statement 5, matrix fragment) | statement |
| `statement5DiscreteMatrices_holds` | theorem | **proved** |
| `Statement5Pymdp` / `Statement5ActiveInferenceJl` / `Statement5Jax` / `Statement5JaxPomdp` | Prop per render target | statements (instances of the shared proved shape) |
| `policyRollout` | def (stepwise executed rollout) | definition |
| `policyRollout_kernelPower` | theorem (execution semantics = `kernelPower` composition) | **proved** |
| `policyRollout_add` | theorem (time additivity, `kernelPower_add`) | **proved** |
| `rolloutKernel_replicate` | theorem (constant plan = `kernelPower`; ties into `active_inference.lean`'s existing `rolloutKernel` machinery via `kernel_comp_power_comm`) | **proved** |
| `policyRollout_eq_plannedState` | theorem (Q4 execution semantics = the carrier's existing `plannedState` open-loop machinery) | **proved** |
| `DiscreteExecutionSemantics` | Prop (conditional per-program preservation for execute targets) | statement |
| `discreteExecutionSemantics_holds` | theorem (trajectory uniqueness) | **proved** |
| `symBoolDoc_policyRollout_kernelPower` | theorem (P1 exemplar corollary) | **proved** |

Deferred (proof-schedule table in the README): full program-denotation
equality per statable target (needs a formalized target-language program
surface — none exists in fep_lean); jax continuous matrix fragment (needs a
continuous carrier with consumed dynamics fields; the Q3 carrier consumes
only the prior gauge); bnlearn CPT-layout fragment (needs the GNN side to
freeze pgmpy's enumeration convention); observation-update (filtering)
fragment (alignment statement 4 territory).

## Commands and exit codes

| Command | Exit | Result |
| --- | --- | --- |
| `cd lean && lake build FepSketches` | 0 | `Build completed successfully (8764 jobs).` — zero errors, zero warnings |
| `lake env lean /tmp/q4_axiom_probe.lean` (probe over all seven proved theorems) | 0 | every theorem: `[propext, Classical.choice, Quot.sound]` — no `sorry`, no new axioms |
| `uv run python scripts/_maint_build_formal_modules.py --check` | 0 | `OK: formal Lean workspace projections are current` |
| `uv run python scripts/_maint_build_fep_all_lean.py --check` | 0 | `OK: lean/FepSketches/fep_all.lean is current` |
| `uv run python scripts/build_formalism_coverage.py --check` | 0 | `OK: formalism coverage projections are current` |
| `uv run python scripts/_maint_build_lean_landscape.py --check` | 0 | `OK: lean landscape projection is current` |
| `uv run python docs/check_links.py --strict --include-root` | 0 | `OK: 47 file(s) scanned (strict; anchors validated) — no broken links.` |
| `uv run python docs/md_hygiene.py --strict` | 0 | `OK: 43 file(s) scanned — no hygiene issues.` |
| `uv run pytest tests/test_formal_composition.py tests/test_native_evidence.py -q` | 0 | `43 passed` |

## Coordination record

- The Q3 worker was first mover on `src/fep_lean/formal/manifest.py`; this
  slice waited for the `gnn_denotation_continuous` row, then appended its
  FOUNDATION row immediately after it, then ran the projection scripts.
- One interaction is recorded honestly: the first projection run captured
  the Q3 module mid-edit (its canonical file changed 130 s after the row
  appeared) and the aggregate build then failed inside
  `gnn_denotation_continuous.lean` — a file outside this slice's
  boundaries. After the Q3 file settled, projections were re-run and the
  full build went green; no Q3 file was edited from this slice.
- `specs/gnn-bridge-p3-certificates/REPORT.md` appears modified in the
  working tree — not from this slice (verified via `git diff`: P3 README
  reconciliation content, presumably a concurrent worker). No Q4 file
  touches it; left as found.
- One self-correction is recorded for evidence honesty: after extending the
  statement module with the open-loop theorems, a targeted
  `lake build FepSketches.gnn_render_statements` reported success against
  the then-stale mirror (pre-edit projection) before the projection
  resync; the subsequent full build caught the real compile error
  (argument-order slip in the new statement), which was fixed, the mirror
  re-projected, and the full build went green. Canonical
  `src/fep_lean/formal/` remained the only edit surface throughout.

## Honest boundary (evidence firewall, section 7)

- What is proved: the conditional matrix-fragment statements (faithful
  emission under the frozen target layout consumes exactly the carrier
  masses of the denoted model), the kernel-power execution semantics and
  its time additivity, trajectory uniqueness under per-step carrier
  faithfulness, and the P1 exemplar corollary — all on the Lean carriers,
  warning-free, no `sorry`, no new axioms.
- What is NOT established by this slice: that any GNN renderer produces a
  faithful emission (the antecedents are the renderers' layout contracts,
  not verified pipeline behavior); that any executed script realizes
  `policyRollout` (the per-program faithfulness is a GNN-side obligation);
  anything about the no-go targets; anything about GNN pipeline behavior at
  all. A future execution-derived statistic vs Lean-witness comparison is a
  Direction 1 / S5 certificate question, not a consequence of this module.
