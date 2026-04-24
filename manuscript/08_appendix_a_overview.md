# Appendix A: Formalisms Overview {#sec:appendix_comprehensive_formalisms_overview}

**Appendices B and C (material)** are one auto-generated file, `09z_unified_formalism_catalogue.md`, produced during Manuscript Artifacts. It juxtaposes, per `fep-NNN` topic, the fenced Lean body and the typeset display-math blocks (former appendices B and C). The committed SSOT is still one **row per topic** in `topics.yaml` (`lean_sketch` and `latex_equations`), regenerated from `scripts/catalogue_sketches.py` (`SKETCHES`) and `scripts/theorem_latex_signatures.py` via `scripts/_maint_build_topics_catalogue.py`. The PDF build prefers `LATEX_EQUATIONS` from `catalogue_sketches` at render time, with YAML as fallback. Each topic has one display-math **block** per `theorem` (typically `aligned`), with ids `eq:fep-NNN-k` for `\Cref{…}`. Counts and verification come from `manuscript_vars.yaml`. See `docs/_generated/canonical_facts.md` for status.

## Complete Topic Catalogue {#sec:complete_topic_catalogue}

The **per-topic index** (id, human title, area, primary Mathlib path, and full `lean_sketch`) is not duplicated here: it appears in the **unified formalism appendix** (§\ref{sec:appendix_b_full_topic_lean_catalogue}), with stable per-topic anchors `#sec:catalogue-fep-NNN` (Lean sketch) and `#sec:eqs-fep-NNN` (typeset LaTeX equations) for each `fep-NNN`. That file is regenerated from `config/topics.yaml` on every Manuscript Artifacts pass, so titles and bodies cannot drift from the committed catalogue.

Native compilation status for the full roster is **`{{compile_rate.total}}`** (from `manuscript_vars.yaml`, derived from `verification_manifest.json` when present) against Mathlib **`{{mathlib_tag}}`** / Lean **`{{lean_toolchain}}`**. Diagnostics and verifier fields are summarized in §\ref{sec:quantitative_execution_metrics}.

**Summary**: All {{total_topics}} rows are `mathlib_status: real` in `topics.yaml`. Per-area rates are **`{{compile_rate.by_area.FEP}}`** (FEP core), **`{{compile_rate.by_area.ActiveInference}}`** (Active Inference), **`{{compile_rate.by_area.InfoGeometry}}`** (Information Geometry), **`{{compile_rate.by_area.BayesianMechanics}}`** (Bayesian Mechanics), and **`{{compile_rate.by_area.Thermodynamics}}`** (Thermodynamics); see §\ref{sec:aggregate_metrics}.

## Area Breakdown {#sec:area_breakdown_overview}

| Area | Topics | Native compile (verifier) | Primary Mathlib Modules |
|------|--------|---------------------------|-------------------------|
| FEP (core) | {{areas.FEP.count}} | `{{compile_rate.by_area.FEP}}` | `MeasureTheory.Measure.*`, `Analysis.SpecialFunctions.Log.*` |
| Active Inference | {{areas.ActiveInference.count}} | `{{compile_rate.by_area.ActiveInference}}` | `Data.Finset.*`, `Algebra.BigOperators.*`, `Order.Basic` |
| Information Geometry | {{areas.InfoGeometry.count}} | `{{compile_rate.by_area.InfoGeometry}}` | `Analysis.InnerProductSpace.*`, `Topology.MetricSpace.*` |
| Bayesian Mechanics | {{areas.BayesianMechanics.count}} | `{{compile_rate.by_area.BayesianMechanics}}` | `LinearAlgebra.Matrix.*`, `MeasureTheory.Measure.MeasureSpace` |
| Thermodynamics | {{areas.Thermodynamics.count}} | `{{compile_rate.by_area.Thermodynamics}}` | `Analysis.SpecialFunctions.Log.*`, `Analysis.SpecialFunctions.Exp.*` |
| **Total** | **{{total_topics}}** | **`{{compile_rate.total}}`** | — |

*Rates come from measured verifier output in `manuscript_vars.yaml` / `verification_manifest.json`. Current state (templated, refreshed each run): `verify.run_id={{verify.run_id}}; verify.verify_lean_ran={{verify.verify_lean_ran}}; verify.compiles_true={{verify.compiles_true}}; verify.compiles_false={{verify.compiles_false}}; verify.topics_with_result={{verify.topics_with_result}}`. Re-run `scripts/03_lean_verify_only.py` after any toolchain or sketch change to refresh these fields.*

## Representative topics (pointers only) {#sec:representative_lean_sketches}

To avoid duplicating Lean that can drift from the SSOT, this appendix does **not** paste catalogue fences. Three representative rows illustrate how to navigate the generated appendices:

| Topic | Role | Appendix B (Lean) | Appendix C (display math / `\Cref`) |
|-------|------|-------------------|----------------------------------------|
| fep-001 | Measure-theoretic backbone for variational bounds | §\ref{sec:catalogue-fep-001} | §\ref{sec:eqs-fep-001} (e.g. \Cref{eq:fep-001-1}) |
| fep-031 | Boltzmann–Gibbs weights (`Real.exp`) | §\ref{sec:catalogue-fep-031} | §\ref{sec:eqs-fep-031} |
| fep-046 | Stick-breaking / ordered-field bookkeeping | §\ref{sec:catalogue-fep-046} | §\ref{sec:eqs-fep-046} |

## Mathlib4 Imports Used Across the Catalogue {#sec:mathlib4_imports_catalogue}

Every **shipped row in Appendix B** uses **fine-grained Mathlib4 imports** (typically one to four `import Mathlib.…` lines per topic) rather than the blanket `import Mathlib`; this keeps `lake env lean` cold-cache time bounded and makes each sketch's Mathlib dependency surface auditable. (Pedagogical snippets in early methodology sections may use `import Mathlib` for exposition only; they are not catalogue SSOT.) The key Mathlib4 modules that catalogue topics depend on include:

- `Mathlib.MeasureTheory.Measure.MeasureSpace` — measure subadditivity, monotonicity (fep-001, fep-006, fep-009, fep-014, fep-015)
- `Mathlib.MeasureTheory.Measure.Typeclasses.Probability` — `prob_measure_univ` (fep-002)
- `Mathlib.Analysis.SpecialFunctions.Log.Basic` — `Real.log_nonneg`, `Real.log_le_log` (fep-011, fep-013, fep-024)
- `Mathlib.Analysis.SpecialFunctions.Exp` — `Real.exp_pos`, `Real.exp_le_exp` (fep-010, fep-012, fep-031)
- `Mathlib.Algebra.BigOperators.Group.Finset.Basic` + `Mathlib.Algebra.Order.BigOperators.Group.Finset` — `Finset.sum_nonneg`, `Finset.sum_le_sum` (fep-003, fep-004, fep-007, fep-017, fep-019, fep-039, fep-041)
- `Mathlib.Analysis.InnerProductSpace.Basic` / `…PiL2` — Cauchy–Schwarz, Fisher metric (fep-004, fep-018, fep-038)
- `Mathlib.Topology.MetricSpace.Basic` — `dist_triangle`, `dist_self` (fep-018)
- `Mathlib.LinearAlgebra.Matrix.Defs` — finite-dimensional matrix lemmas (fep-025)
- `Mathlib.Data.Finset.Basic` / `Data.Finset.Max` — `Finset.exists_min_image`, `Finset.filter` (fep-005, fep-008, fep-023)
- `Mathlib.Algebra.Order.Field.Basic` / `Algebra.Order.Ring.Basic` — `mul_nonneg`, `sub_nonneg` (fep-021, fep-046, fep-049)

## Formalization Epistemology: Realism vs. Illusionism {#sec:formalization_epistemology}

The catalogue offers a structural way to engage the FEP philosophical debate between realist and illusionist readings of consciousness (Solms, Dołęga, Wiese, 2023–2025) [@brainsblog2023]. Expressing generative models in Lean 4's dependent type system shows how active-inference "beliefs" (for example `q` as densities) chain as measure-theoretic objects with explicit type boundaries rather than as unindexed prose claims.

For machine-checked compilation per topic, enable native verification (Gauss path above, or `scripts/03_lean_verify_only.py`) and read the latest `verification_manifest.json` under `output/reports/run_*/`; its aggregated `verify.*` summary is injected into the PDF when `manuscript_vars.yaml` is regenerated.
