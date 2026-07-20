# fep_lean/manuscript/

Paper source for the template rendering pipeline: `config.yaml`, `preamble.md`, section `*.md`, `references.bib`.

After editing `references.bib`, keep the grouped HTML comment in [`07_references.md`](07_references.md) aligned (entry count and per-key summaries) so the human index matches citeproc input.

Paths in this file are relative to the **project root** (the directory containing `pyproject.toml`), except where a relative link is explicitly anchored to another manuscript file.

## Architectural Integration

Narrative sections live as numbered `*.md` files. The **{{total_topics}}-topic** roster is defined in [`config/topics.yaml`](../config/topics.yaml); every row is **`mathlib_status: real`** with a compiling Lean body from [`scripts/catalogue_sketches.py`](../scripts/catalogue_sketches.py) (`SKETCHES`, regenerated via `scripts/_maint_build_topics_catalogue.py`; drift-checked by `tests/test_catalogue_sketches_ssot.py`). Per-topic variables for PDF rendering are injected via `manuscript_vars.yaml`.

- **Unified formalism appendix (B+C material):** `09z_unified_formalism_catalogue.md` is **auto-generated** (typically gitignored) by `output.manuscript.write_unified_formalism_appendix_markdown` during the same **Manuscript Artifacts** stage as `manuscript_vars.yaml`. One **TopicEntry** per row in [`config/topics.yaml`](../config/topics.yaml) is the SSOT (`lean_sketch` + `latex_equations`); the appendix is a **projection** of that file, juxtaposing for each `fep-NNN` a **Lean sketch** subsection (`#sec:catalogue-fep-NNN`) and a **Typeset statement signatures** subsection (`#sec:eqs-fep-NNN`) with one LaTeX `equation` environment per `theorem`, each carrying `\label{eq:fep-NNN-k}` for `\Cref{…}` in prose. The PDF’s Appendix B / Appendix C **section references** are preserved: the file’s main heading carries `#sec:appendix_b_full_topic_lean_catalogue`, and a raw `\label{sec:appendix_c_latex_equations}` immediately follows (same physical chapter; both `\ref{…}` targets resolve). **LaTeX rows** for rendering prefer `LATEX_EQUATIONS` imported from `scripts/catalogue_sketches.py` (aligned with `SKETCHES` and `theorem_latex_signatures.py`); if import fails, the loaded YAML `latex_equations` is used. `write_unified_formalism_appendix_markdown` and `write_typeset_equations_markdown` are aliases that write the same unified path. [`08_appendix_a_overview.md`](08_appendix_a_overview.md) introduces the appendices; it does not duplicate their bodies.
- The text uses data-driven injection aligned with pipeline runs: `PipelineResult.stages` lists **four** named steps (Load Catalogue, Environment Validation, Gauss Sessions, Manuscript Artifacts); `Reporter.generate` runs **after** `FEPPipeline.run()` in `orchestrator.run_pipeline`. The six-node figure in `03f_pipeline_architecture.md` is an end-to-end story (orchestration + reporting), not the length of `stages`.
- `manuscript_vars.yaml` is overwritten by `output.manuscript.write_manuscript_vars` during **Manuscript Artifacts** and includes per-topic fields (`maturity`, `lean_chars`, `lean_sketch`, `nl_statement`, …) plus `verify.*` when manifests exist. Without that file, `{{…}}` stays visible in raw Markdown; the PDF step substitutes when the file is present (see §\ref{sec:expression_lifecycle_yaml_to_lake} in `03f_pipeline_architecture.md`).
- **Whether tracked in git:** `manuscript_vars.yaml` and `09z_unified_formalism_catalogue.md` are written into the source tree but their contents are pipeline-derived; treat them as build artifacts. Stale `09z_appendix_b_lean_catalogue.md` / `09zc_appendix_c_lean_equations.md` from older runs may be deleted (they are no longer written). They are intentionally regenerated on every Manuscript Artifacts pass so the rendered PDF reflects the most recent `topics.yaml` + `verification_manifest.json` — do **not** hand-edit generated appendices.

## Placeholder catalogue (read this before adding `{{…}}` references)

The placeholders rendered by the manuscript come from `output.manuscript.write_manuscript_vars` (see `src/output/manuscript.py`). The most frequently used groups are:

- **Catalogue counts:** `{{total_topics}}`, `{{areas.<Area>.count}}` (`FEP`, `ActiveInference`, `BayesianMechanics`, `InfoGeometry`, `Thermodynamics`), `{{maturity.real}}`, `{{maturity.partial}}`, `{{maturity.aspirational}}`.
- **Combined-area helpers** (derived in `build_manuscript_vars` via `_english_count_caps`): `{{combined_info_bayes_count}}` — sum of `InfoGeometry.count + BayesianMechanics.count` (used as a numeric total in tables); `{{combined_info_bayes_count_caps}}` — capitalised English word form (e.g. `Eighteen`), used in prose sentence openings in `04c_framework_sophisticated_dynamics.md`.
- **Compile-rate snapshot:** `{{compile_rate.total}}`, `{{compile_rate.by_area.<Area>}}` — derived from the catalogue `mathlib_status` (sorry-free `real` rows) and refreshed against `verification_manifest.json` when a verify-enabled run has emitted one.
- **Verification (latest run):** `{{verify.run_id}}`, `{{verify.duration_min}}`, `{{verify.compiles_true}}`, `{{verify.compiles_false}}`, `{{verify.topics_with_result}}`, `{{verify.sorry_count}}`, `{{verify.verify_lean_ran}}`, `{{verify.failed_topic_ids}}`.
- **Hermes (latest run):** `{{hermes.primary_model}}`, `{{hermes.processed}}`, `{{hermes.success_count}}`, `{{hermes.cache_hits}}`, `{{hermes.run_id}}`, `{{hermes.tokens_total}}`, `{{hermes.tokens_mean}}`, `{{hermes.mean_topic_s}}`, `{{hermes.fallback_count}}`, `{{hermes.hermes_lean_compiles_count}}`, `{{hermes.models_used}}`.
- **Three-classes-of-fallback metrics** (added in the recent pipeline rewrite — see §\ref{sec:three_classes_of_fallback} in `03d_hermes_llm_pipeline.md`): `{{hermes.network_retry_count}}`, `{{hermes.model_fallback_count}}`, `{{hermes.chain_advance_reasons}}` (per-reason map), `{{hermes.chain_advance_reasons_summary}}` (human-readable string used inline).
- **Toolchain pin:** `{{lean_toolchain}}` (e.g. `leanprover/lean4:v4.29.0`), `{{lean_version}}` (`4.29.0`), `{{mathlib_tag}}` (`v4.29.0`).
- **Tests:** `{{tests.collected}}`.

When you add a new placeholder anywhere in the source tree, also add an emitter for it in `src/output/manuscript.py::write_manuscript_vars` (or one of its `_*_block_from_*` helpers) and a regression assertion in `tests/test_manuscript_artifacts.py`.

## Conventions

- **Catalogue rows (`fep-NNN`):** cite Appendix B for Lean (`#sec:appendix_b_full_topic_lean_catalogue` / `#sec:catalogue-fep-NNN`) and Appendix C for display math (`#sec:appendix_c_latex_equations` / `#sec:eqs-fep-NNN` / `#eq:fep-NNN-k`). Do not paste full duplicate catalogue bodies into other sections.
- **Pedagogical chapters** (`03a_lean4_primer.md`, `03b_mathlib4_measure_theory.md`, `03c_sorry_maturity.md`): illustrative Lean is allowed; these snippets are **not** catalogue rows and must not replace `fep-NNN` canonical bodies in Appendix B.
- Code snippets should reflect raw Lean 4 (no pseudo-Lean) when claiming catalogue parity.
- Never hardcode topic counts, build times, maturity tallies, model names, toolchain versions, or per-area splits. Use the placeholders above (`{{maturity.real}}`, `{{total_topics}}`, `{{compile_rate.total}}`, `{{compile_rate.by_area.<Area>}}`, `{{lean_toolchain}}`, `{{mathlib_tag}}`, `{{hermes.primary_model}}`, …) so a re-run of the pipeline keeps the PDF honest.

## See also

- [../AGENTS.md](../AGENTS.md)
