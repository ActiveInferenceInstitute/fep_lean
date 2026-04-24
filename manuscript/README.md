# Manuscript

Markdown + YAML for PDF/HTML via root infrastructure. Configure metadata in `config.yaml`; render via `infrastructure/rendering/_pdf_combined_renderer.py` (or any pipeline pass that exercises the **Manuscript Artifacts** stage in `src/pipeline/core.py::FEPPipeline._stage_manuscript_artifacts`).

`preamble.md` is LaTeX-only. `09z_unified_formalism_catalogue.md` (Lean + typeset LaTeX juxtaposed per topic) is generated; the header and structure come from `src/output/manuscript.py` (`_UNIFIED_FORMALISM_MD_HEADER` and `build_unified_formalism_appendix_markdown`).

Running the fep_lean pipeline’s **Manuscript Artifacts** stage regenerates `manuscript_vars.yaml` and `09z_unified_formalism_catalogue.md` from `config/topics.yaml`. **LaTeX block strings** for PDF rendering prefer `LATEX_EQUATIONS` from `scripts/catalogue_sketches.py` when importable, else each row’s `latex_equations` in YAML. Regenerate committed YAML with `scripts/theorem_latex_signatures.py` and `scripts/_maint_build_topics_catalogue.py`, in step with `SKETCHES`. Counts and `{{verify.*}}` reflect the catalogue and, when present, the latest `verification_manifest.json` after a verify-enabled run.

## Chapter index

Numeric prefixes drive both rendering order and section anchors. The split is:

- `01_abstract.md` — paper abstract.
- `02a_introduction.md`, `02b_background.md` — motivation, FEP background, related work.
- `03_methodology.md`, `03a_lean4_primer.md`, `03b_mathlib4_measure_theory.md`, `03c_sorry_maturity.md`, `03d_hermes_llm_pipeline.md`, `03e_lean_compilation.md`, `03f_pipeline_architecture.md` — methodology, Lean 4 / Mathlib4 primer, Hermes LLM pipeline, Lean compilation surface, end-to-end pipeline architecture.
- `04a_framework_fep.md`, `04b_framework_active_inference.md`, `04c_framework_sophisticated_dynamics.md`, `04d_framework_thermodynamics.md`, `04e_quantitative_metrics.md` — formalization results per area + headline metrics.
- `05a_mathlib_maturity.md`, `05b_zero_mock_standard.md`, `05c_fep_debate_implications.md`, `05d_comparative_analysis.md`, `05e_broader_impact_limitations.md` — discussion: Mathlib maturity surface, zero-mock standard, debate implications, comparative analysis, broader impact / limitations.
- `06_conclusion.md`, `07_references.md` — conclusion and human-readable reference list.
- `08_appendix_a_overview.md`, `09z_unified_formalism_catalogue.md` — appendix A (overview); unified B+C material (auto-generated: Lean + LaTeX per topic, one `equation` block per `theorem` with `\label{eq:…}` for `\Cref{…}`).
- `references.bib` — single source of bibliographic truth, consumed by Pandoc/biblatex.

`AGENTS.md` (sibling) catalogues every `{{…}}` placeholder rendered into these chapters and the file in `src/output/manuscript.py` that emits it.
