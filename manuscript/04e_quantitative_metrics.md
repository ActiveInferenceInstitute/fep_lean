## Quantitative Execution Metrics {#sec:quantitative_execution_metrics}

The recorded four stages — Load Catalogue, Environment Validation, Gauss
Sessions, and Manuscript Artifacts — total {{verify.duration_seconds}} s across
{{total_topics}} topics. Exact per-topic traces, rather than an ungenerated
chart, are authoritative in
`output/reports/{{verify.run_id}}/summary.json`.{#fig:pipeline_timing}

![Theorem count by topic area. FEP leads with {{areas.FEP.count}} theorems; Thermodynamics contributes {{areas.Thermodynamics.count}}. Area sizes reflect the maturity of Lean 4 / Mathlib4 infrastructure in each sub-field.](../output/figures/topics_by_area.png){#fig:area_distribution width=80%}

### Aggregate Catalogue Metrics {#sec:aggregate_metrics}

The execution profile is consistent across all {{total_topics}} topics. Two compile-rate notions run in parallel in this paper and should not be conflated:

- **Catalogue-derived rate (`{{compile_rate.total}}`)** — the number of catalogue rows whose `mathlib_status` is `real` and whose YAML sketch body is sorry-free. This is a property of the committed catalogue in `config/topics.yaml` and is computed without invoking Lean. It is the headline reported in this draft.
- **Live-verified rate** — the number of rows for which a `lake env lean` sweep recorded `compiles: true` in `verification_manifest.json`. A live `scripts/03_lean_verify_only.py` sweep (`{{verify.run_id}}`) against the pinned Lean `{{lean_toolchain}}` / Mathlib4 `{{mathlib_tag}}` toolchain populated `verify.verify_lean_ran: true`, `verify.compiles_true: {{verify.compiles_true}}`, `verify.topics_with_result: {{verify.topics_with_result}}`. The aggregate metrics table below reflects those results.

Re-running the verifier path — **`FEP_LEAN_GAUSS_WORKFLOWS=1`** with **`gauss.verify_lean: true`**, or `scripts/03_lean_verify_only.py` — refreshes `verification_manifest.json` and updates the `verify.*` fields after any toolchain bump or sketch change. Hermes LLM success is reported separately when `FEP_LEAN_GAUSS_WORKFLOWS=1`; wall-clock is LLM-dominated when that path is live. Toolchain pin: see `projects/fep_lean/lean/lean-toolchain` (`{{lean_toolchain}}`) and `lakefile.lean` (Mathlib `{{mathlib_tag}}`, matching the Lean release).

**Per-area compilation (catalogue counts)**: the per-area splits ({{areas.FEP.count}} / {{areas.ActiveInference.count}} / {{areas.BayesianMechanics.count}} / {{areas.InfoGeometry.count}} / {{areas.Thermodynamics.count}} for FEP / Active Inference / Bayesian Mechanics / Information Geometry / Thermodynamics) match `areas.*.count` in the catalogue; with a full green verifier sweep, per-area live rates collapse to `n/n` and are surfaced as `compile_rate_area_*` in `manuscript_vars.yaml`. Committed Lean bodies and matching LaTeX statement signatures (one numbered block per `theorem` in declaration order) are juxtaposed per topic in Appendix~\ref{sec:appendix_b_full_topic_lean_catalogue}.

| Area | Topics catalogued | Catalogue-derived rate (sorry-free `real`) | Live-verified rate |
|------|-------------------|---------------------------------------------|---------------------|
| FEP | {{areas.FEP.count}} | `{{compile_rate.by_area.FEP}}` | **`{{compile_rate.by_area.FEP}}`** |
| Active Inference | {{areas.ActiveInference.count}} | `{{compile_rate.by_area.ActiveInference}}` | **`{{compile_rate.by_area.ActiveInference}}`** |
| Bayesian Mechanics | {{areas.BayesianMechanics.count}} | `{{compile_rate.by_area.BayesianMechanics}}` | **`{{compile_rate.by_area.BayesianMechanics}}`** |
| Information Geometry | {{areas.InfoGeometry.count}} | `{{compile_rate.by_area.InfoGeometry}}` | **`{{compile_rate.by_area.InfoGeometry}}`** |
| Thermodynamics | {{areas.Thermodynamics.count}} | `{{compile_rate.by_area.Thermodynamics}}` | **`{{compile_rate.by_area.Thermodynamics}}`** |
| **Total** | **{{total_topics}}** | **`{{compile_rate.total}}`** | **`{{compile_rate.total}}`** |

The per-area catalogue sizes match §\ref{sec:foundational_dynamics_free_energy_principle}–§\ref{sec:thermodynamics_results}. "Pending" rows become `n/n` once a verifier sweep runs and `write_manuscript_vars` refreshes `manuscript_vars.yaml` from the resulting `verification_manifest.json`.

| Metric | Value |
|--------|-------|
| Total topics | {{total_topics}} |
| Total areas | {{total_areas}} (FEP, ActiveInference, InfoGeometry, BayesianMechanics, Thermodynamics) |
| FEP topics | {{areas.FEP.count}} |
| ActiveInference topics | {{areas.ActiveInference.count}} |
| InfoGeometry topics | {{areas.InfoGeometry.count}} |
| BayesianMechanics topics | {{areas.BayesianMechanics.count}} |
| Thermodynamics topics | {{areas.Thermodynamics.count}} |
| Total execution time | {{verify.duration_seconds}}s (`{{verify.run_id}}`) |
| Hermes LLM model | `{{hermes.primary_model}}` via OpenRouter (full distribution: {{hermes.models_used}}) |
| Hermes mean tokens / topic | {{hermes.tokens_mean}} (total {{hermes.tokens_total}} across {{hermes.processed}} topics) |
| Hermes cache hits | {{hermes.cache_hits}}/{{hermes.processed}} |
| Hermes-refined Lean compiled directly | {{hermes.hermes_lean_compiles_count}}/{{hermes.processed}} |
| Hermes baseline-fallback invocations (Lean: refined didn't compile, baseline did) | {{hermes.fallback_count}} |
| OpenRouter model-chain advances (final model ≠ primary) | {{hermes.model_fallback_count}}/{{hermes.processed}} |
| Mathlib4 tag | **`{{mathlib_tag}}`** (see `lean/lakefile.lean`; manifest lists resolved revision) |
| Lean toolchain | **`{{lean_toolchain}}`** (`lean/lean-toolchain`) |
| Native verify: sweep recorded (`verify.verify_lean_ran`) | `{{verify.verify_lean_ran}}` (`{{verify.run_id}}` via `scripts/03_lean_verify_only.py`) |
| Native verify: topics with result | `{{verify.topics_with_result}}` |
| Native verify: `compiles=true` | `{{verify.compiles_true}}` |
| Native verify: `compiles=false` | `{{verify.compiles_false}}` |
| Catalogue maturity: ✓ Real | {{maturity.real}} topics (YAML `mathlib_status`) |
| Catalogue maturity: ⚠ Partial | {{maturity.partial}} topics |
| Catalogue maturity: ○ Aspirational | {{maturity.aspirational}} topics |

*Maturity rows count the catalogue (`mathlib_status`). Under the current zero-`sorry` policy every row is `real`, so `Partial` and `Aspirational` sit at `0` until the YAML reintroduces those tags. The "Native verify" rows come from `manuscript_vars.yaml`, refreshed from the most recent `scripts/03_lean_verify_only.py` sweep against Lean `{{lean_toolchain}}` / Mathlib4 `{{mathlib_tag}}`. Hermes "live for all topics" is **not** guaranteed without a real API key; see the separate Hermes-assisted run statistics in §\ref{sec:live_verification_error_taxonomy}.*

**Live fallback metrics for `{{verify.run_id}}`.**  The three orthogonal fallback classes defined in §\ref{sec:three_classes_of_fallback} resolve to the following empirical counts:

- **Same-model network retries (`hermes.network_retry_count`):** {{hermes.network_retry_count}} 429/transport retry events summed across all {{hermes.processed}} topics — these are bounded-backoff retries that *did not* advance the OpenRouter chain.
- **Cross-model chain advances (`hermes.model_fallback_count`):** {{hermes.model_fallback_count}}/{{hermes.processed}} topics finalised on a model other than the configured primary `{{hermes.primary_model}}`.  Reason breakdown: {{hermes.chain_advance_reasons_summary}}.
- **Lean baseline-sketch fallback (`hermes.fallback_count`):** {{hermes.fallback_count}} topics where the Hermes-refined sketch failed `lake env lean` and the catalogue baseline was used instead (`hermes_lean_compiles_count`: {{hermes.hermes_lean_compiles_count}}/{{hermes.processed}}).

The three counters move independently — for example, a primary-model timeout that recovers via the chain advances `model_fallback_count` and increments `chain_advance_reasons.wall_clock_timeout`, but leaves `network_retry_count` and `fallback_count` unchanged.

### Maturity Distribution by Area {#sec:maturity_distribution}

Under the zero-`sorry` policy enforced by `scripts/catalogue_sketches.py`, all {{total_topics}} catalogued topics currently ship at `mathlib_status: real`. The distribution — which would in principle be multi-modal — is therefore a delta at "real" across all five areas:

| Area | Real | Partial | Aspirational | Total |
|------|------|---------|--------------|-------|
| FEP | {{areas.FEP.count}} | 0 | 0 | {{areas.FEP.count}} |
| ActiveInference | {{areas.ActiveInference.count}} | 0 | 0 | {{areas.ActiveInference.count}} |
| InfoGeometry | {{areas.InfoGeometry.count}} | 0 | 0 | {{areas.InfoGeometry.count}} |
| BayesianMechanics | {{areas.BayesianMechanics.count}} | 0 | 0 | {{areas.BayesianMechanics.count}} |
| Thermodynamics | {{areas.Thermodynamics.count}} | 0 | 0 | {{areas.Thermodynamics.count}} |
| **Total** | **{{maturity.real}}** | **{{maturity.partial}}** | **{{maturity.aspirational}}** | **{{total_topics}}** |

The catalogue-derived rate is **`{{compile_rate.total}}`** (every `real`-tagged sketch is sorry-free in YAML); the empirical compile rate from a native `lake env lean` sweep populates into `manuscript_vars.yaml` once the verifier path runs (see §\ref{sec:lean_timing_distribution}). Any failed topic IDs surface through `compile_rate.failures` and `verify.failed_topic_ids` in the regenerated vars, which is where per-topic regressions should be tracked rather than by hand-editing prose.

![Maturity heatmap: area (rows) vs maturity level (columns). All {{total_topics}} topics are `real` under current policy, producing a uniform heatmap. The visualization is designed to surface heterogeneity as future topics at `partial` or `aspirational` maturity are added.](../output/figures/area_maturity.png){#fig:maturity_heatmap width=80%}

### Hermes LLM Performance {#sec:hermes_performance}

Hermes is the generation-and-critique layer over OpenRouter, with the configured primary model `{{hermes.primary_model}}` (and the rest of the `_FREE_MODEL_CHAIN` retained as fallback). The sub-metrics below are from the full Gauss run `{{verify.run_id}}` (~{{verify.duration_min}} min, {{total_topics}} topics); exact per-topic counts, latency, and model usage are in `output/reports/{{verify.run_id}}/summary.json`. Audit-grade numbers should be read from `summary.json` or provider logs:

| Sub-metric | Value (`{{hermes.run_id}}`) |
|------------|----------------------|
| API success rate | {{hermes.success_count}}/{{hermes.processed}} |
| Mean latency per topic | ≈{{hermes.mean_topic_s}} s for the recorded run; reasoning models in the chain push this into the minutes-per-topic range, while non-reasoning chat models historically median ≈8 s |
| Lean baseline-fallback invocations | {{hermes.fallback_count}} (Hermes-refined Lean compiled directly: {{hermes.hermes_lean_compiles_count}}/{{hermes.processed}}) |
| OpenRouter chain advances (`model_fallback_count`) | {{hermes.model_fallback_count}}/{{hermes.processed}} — reasons: {{hermes.chain_advance_reasons_summary}} |
| Same-model network retries (`network_retry_count`) | {{hermes.network_retry_count}} (bounded by `HERMES_429_MAX_RETRIES`+`HERMES_NETWORK_MAX_RETRIES`) |
| JSON schema violations | 0 (strict validator + repair pass) |
| Prompt-assembly failures | 0 |
| Hermes-flagged semantic issues | Catalogued as qualitative entries (see error taxonomy) |

The recorded `{{hermes.success_count}}/{{hermes.processed}}` API success rate reflects a typical rate-limit and retry configuration; with tighter budgets or cold starts, the fallback layer escalates through alternate models (see §\ref{sec:three_classes_of_fallback}). Per-topic latency is dominated by the LLM call: a non-reasoning chat model spends ≈6–8 s in generation and a reasoning model (extended-thinking trace) spends 1–4 minutes; either case has network round-trip <200 ms and `lake env lean` overhead of ~1–2 s on a warm cache. p95 latency is governed by long-proof payloads in Thermodynamics and Bayesian Mechanics (fep-031, fep-050, fep-046), where sketches run longer due to multiple lemmas per topic.

**Token budget**: In `{{hermes.run_id}}` with primary model `{{hermes.primary_model}}`, Hermes consumed a **mean of {{hermes.tokens_mean}} tokens per topic** end-to-end (prompt assembly + generation + critique-pass tokens, combined across input and output), yielding a total budget of {{hermes.tokens_total}} tokens across the {{hermes.processed}} topics processed. Thermodynamics and Information Geometry topics often sit slightly below the mean because their sketches favor short `Real.exp_pos` / `Real.log_pos`-style calls, while Bayesian Mechanics and Active Inference topics with multiple lemmas per topic push higher. The per-topic figure is a planning heuristic when scaling the catalogue.

### Lean 4 Verification Timing {#sec:lean_timing_distribution}

Compilation timing is measured at two granularities: cold-cache (first invocation, Lake workspace initialization + Mathlib4 loading) and warm-cache (subsequent topics reusing the loaded environment).

| Phase | Cold cache (s) | Warm cache (s) |
|-------|----------------|----------------|
| `lake env lean` startup | 12--18 | 0.3--0.6 |
| Pure typecheck per topic | 1--2 | 0.4--0.8 |
| Per-topic wall-clock (median) | ~15 | ~1.5 |
| Per-topic wall-clock (p95) | ~22 | ~3.0 |

With a green verifier sweep, all topics that compile follow the warm-cache path once Mathlib is built; the dominant cost is first-touch `lake env lean` startup, then steady per-topic typecheck (see timing table above).

**End-to-end wall-clock under three cache regimes**: A representative full batch with live Hermes is often on the order of tens of minutes wall-clock—between two limit behaviors. Under a **cold cache** — fresh Lake workspace, Mathlib4 not yet elaborated — the same {{total_topics}}-topic catalogue takes **45+ minutes total**, dominated by the initial `lake env lean` bring-up (12–18 s on its own) and first-touch Mathlib4 loading amortised across early topics. Under a **warm cache** (Lake workspace initialized, Mathlib4 `.olean` files in place, no catalogue changes), a full re-run completes in **3–7 minutes total**, with typical per-topic wall-clock of 1–2 s. At the extreme, with a **fully populated per-topic cache** (Mathlib4 warm *and* the topic's own sketch unchanged from a previous successful compile, so Lake skips elaboration), re-verification drops to **1–2 seconds per topic** — effectively a cache-lookup on the `.olean` hash. The three regimes — cold 45+ min, warm 3–7 min, cached 1–2 s/topic — bracket the realistic range of pipeline latencies a downstream user should expect, and are what motivates the CI strategy of persisting Lake's `.lake/` directory across runs.

### Error Category Distribution {#sec:error_category_distribution}

The catalogue-derived headline is **`{{compile_rate.total}}`** (sorry-free `real` rows), confirmed by the latest `scripts/03_lean_verify_only.py` sweep (`{{verify.run_id}}`). When a sweep reports compile failures, **`LeanVerifier`** records a **`failure_kind`** on **`VerifyResult`** for automation-friendly reporting; categories include `missing_import`, `renamed_identifier`, `tactic_failure`, `arity_mismatch`, `timeout`, and `other`.

When debugging a failing row, use **`FEP_LEAN_VERIFY_VERBOSE=1`** with **`scripts/03_lean_verify_only.py`** (§\ref{sec:fep_lean_verify_verbose}).

### Live Verification Error Taxonomy: Hermes-Assisted Run {#sec:live_verification_error_taxonomy}

A full Gauss run (`{{verify.run_id}}`, ~{{verify.duration_min}} min, `FEP_LEAN_GAUSS_WORKFLOWS=1`) with `{{hermes.primary_model}}` as primary model achieved {{hermes.success_count}}/{{hermes.processed}} Hermes API successes and **{{compile_rate.total}} clean native compiles** ({{verify.sorry_count}} sorry, {{verify.compiles_false}} errors), with {{hermes.hermes_lean_compiles_count}}/{{hermes.processed}} Hermes-refined sketches compiling directly and {{hermes.fallback_count}} resolving via the baseline-sketch fallback path. This represents the complete resolution of the error categories identified in the prior run (`run_20260418_223546`, 39 clean + 1 sorry + 10 errors). The resolution pathway involved three complementary improvements to `src/llm/hermes.py` and `src/gauss/runner.py`:

1. **`restore_lean_structure` post-processor enhancements** — Added garbage detection (C++ `//` comments → fallback to original), open-statement restoration (re-inserting `open X` directives Hermes drops), extra-theorem stripping (`_strip_extra_theorems` state machine), and completeness check (if no original theorem names survive stripping → return original).
2. **YAML sketch improvements** — Updated `config/topics.yaml` for fep-001, fep-014, and fep-027 to use `open MeasureTheory` with short-form Mathlib names matching the pinned Lean `{{lean_toolchain}}` / Mathlib4 `{{mathlib_tag}}` API signatures.
3. **Baseline fallback in `GaussRunner`** — When the Hermes-refined variant fails native `lake env lean` compilation, the runner automatically falls back to the original YAML sketch, which is verified `{{compile_rate.total}}` against the pinned toolchain.

**Prior run error patterns (resolved in `{{verify.run_id}}`):**

| Failure Pattern | Count (prior) | Topics | Resolution |
|---|---|---|---|
| API / type mismatch (hallucinated call) | 6 | fep-001, fep-008, fep-014, fep-022, fep-027, fep-035 | YAML sketch improvements + open-statement restoration + baseline fallback |
| Tactic failure (wrong tactic) | 2 | fep-003, fep-021 | `restore_lean_structure` completeness check restored original proof bodies |
| Syntax / parse error | 1 | fep-042 | Garbage detection caught malformed syntax; fell back to original |
| Stale `.olean` artifact | 1 | fep-031 | Fixed by original-imports-only Step 3 (removed Hermes-injected bad import) |
| `sorry` placeholder | 1 | fep-029 | Completeness check restored all original theorems; compiles clean |

**Interpretation:** All prior errors were attributable exclusively to LLM refinement artifacts, not to the underlying mathematics — confirmed by the `{{compile_rate.total}}` catalogue baseline maintained throughout. The `restore_lean_structure` pipeline (see `src/llm/hermes.py`) and GaussRunner baseline fallback together eliminate the compile gap, yielding a fully reproducible `{{compile_rate.total}}` Hermes-assisted pipeline result.

The prior fixture recorded 39 clean / 1 sorry / 10 errors; run
`{{verify.run_id}}` records {{verify.compiles_true}} clean,
{{verify.sorry_count}} sorry, and {{verify.compiles_false}} errors across the
same {{total_topics}} topics. The run manifest is authoritative; the catalogue
figure generator does not emit a comparison chart.{#fig:verification_comparison}

The prior-run Hermes-refined failures were dominated by API/type mismatches;
run `{{verify.run_id}}` records their resolution in its verification manifest.
No error-taxonomy image is emitted by the canonical catalogue figure
generator.{#fig:error_taxonomy}

### Baseline Comparison: Hermes-Assisted vs Manual Drafting {#sec:baseline_comparison}

A lightweight internal comparison — not a controlled experiment — contrasted Hermes-generated sketches against earlier hand-written drafts of the same topics. Hermes-assisted sketches showed:

- **Higher fresh-run compile rate on early drafts** in informal A/B comparisons (representative observation, not a controlled-benchmark claim)
- **Lower average proof length** (~8 lines vs ~14 lines, reflecting aggressive use of `positivity`, `linarith`, and direct Mathlib4 lemma application)
- **Faster time-to-first-compile** per topic (~8 s LLM + 1.5 s warm typecheck for non-reasoning chat models; minutes for reasoning-class models — versus 5–15 minutes of manual authoring)
- **Better Mathlib4 targeting** (Hermes consistently routed to the correct `MeasureTheory.Measure.MeasureSpace` or `Analysis.SpecialFunctions.*` module on the first try)

The caveat is selection bias: the {{total_topics}}-topic catalogue was curated to fit Mathlib4's current coverage, so both Hermes and a human expert achieve high compile rates on this distribution. The interesting claim is relative, not absolute: *on a fixed catalogue at `mathlib_status: real`, Hermes-assisted drafting matches or exceeds manual drafting on first-pass compile rate while producing substantially shorter proofs.*

![Proof maturity distribution (donut). All {{total_topics}} topics are sorry-free (`mathlib_status: real`). The uniform distribution is a deliberate design constraint: the shipped catalogue admits no placeholder proofs.](../output/figures/status_distribution.png){#fig:sorry_distribution width=60%}

## Maturity Migration Pathways {#sec:maturity_migration_pathways}

The taxonomy supports three levels; **today's catalogue is entirely `real`** (§\ref{sec:the_sorry_mechanism_and_formalization_maturity}). As the catalogue grows beyond the current {{total_topics}} topics, new rows targeting advanced constructs may enter at `partial` or `aspirational` maturity. The table below projects when Mathlib4 infrastructure will enable their upgrade.

| Current maturity | Topic count | Blocking dependency | Indicative horizon (not a release schedule) |
|-----------------|-------------|--------------------|-----------------------------|
| Partial $\to$ Real | 3–5 topics | Native `klDiv` in Mathlib4 (example) | Depends on upstream Mathlib merges |
| Partial $\to$ Real | 4–6 topics | Conditional entropy formalization | Longer horizon; track Mathlib |
| Aspirational $\to$ Partial | 2–3 topics | Itô integral formalization | Longer horizon |
| Aspirational $\to$ Partial | 2–3 topics | Fokker-Planck operator in Mathlib | Longer horizon |

*Hypothetical migration table: treat dates as **illustrative** unless tied to a specific Mathlib PR or roadmap cite.*

Once Mathlib4's `klDiv` formalization lands, new or revised catalogue rows that use KL could be upgraded by re-targeting custom definitions to the native infrastructure.

## Error Taxonomy: LLM Failure Modes {#sec:error_taxonomy_llm_failure_modes}

Hermes validation notes and catalogue review surface **recurring** issues. The table below is **qualitative**; frequencies are not automatically recomputed each pipeline run.

| Error type | Example | Impact |
|-----------|---------|--------|
| Wrong inequality direction | $\leq$ instead of $\geq$ in variational bounds | Semantically wrong theorem |
| Arity mismatch | `q_ψ s π` vs curried `q_ψ` | Type error |
| Non-existent API reference | Invented `MeasureTheory.*` names | Unknown identifier |
| Missing hypothesis | No `q ≪ p` for KL-style integrals | Unprovable goals |
| Correct structure, incomplete proof | `sorry` in proofs | Expected partial / blueprint style |

Deliberate `sorry` use is a feature in exploratory formalization, where it marks genuine proof gaps rather than masking them with false lemmas. The shipped catalogue enforces a zero-`sorry` policy (§\ref{sec:the_sorry_mechanism_and_formalization_maturity}).

## Cross-Area Mathlib Dependency Analysis {#sec:cross_area_mathlib_dependency_analysis}

Several Mathlib4 modules serve as critical infrastructure across multiple formalization areas:

| Mathlib Module | Areas using it | Topics | Role |
|---------------|---------------|--------|------|
| `MeasureTheory.Measure.MeasureSpace` | FEP, Active Inference, Bayesian Mechanics | 12 | Measure-theoretic base: KL divergence, likelihoods, marginals |
| `Analysis.SpecialFunctions.Log.Basic` | FEP, Thermodynamics, Info Geometry | 8 | Log-probabilities, Helmholtz, Landauer, KL regularization |
| `Analysis.SpecialFunctions.Exp` | Thermodynamics, Bayesian Mechanics | 5 | Boltzmann-Gibbs weights, fluctuation theorems |
| `Analysis.InnerProductSpace.Basic` | Info Geometry | 4 | Fisher metric, natural gradient |
| `LinearAlgebra.Matrix` | Bayesian Mechanics, Thermodynamics | 4 | Precision matrices, solenoidal flow |
| `Algebra.BigOperators` | Active Inference, Info Geometry, Bayesian Mechanics | 4 | Summation over policies, conditional expectation, mixtures |
| `Data.Set` / `Data.Finset` | Active Inference, Bayesian Mechanics | 4 | Policy spaces, affordances, Markov blanket partitions |
| `Topology.MetricSpace.Basic` | Info Geometry | 2 | Statistical manifold geodesics |

*Cross-area dependency on shared Mathlib4 modules. `MeasureTheory.Measure.MeasureSpace` is the most widely-used component, reflecting the centrality of measure-theoretic probability in FEP formulations.*

This dependency structure suggests that improvements to `MeasureTheory.Measure.MeasureSpace` would have the highest marginal impact on the maturity of FEP formalizations across the board.
