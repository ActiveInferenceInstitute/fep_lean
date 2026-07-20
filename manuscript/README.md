# Manuscript sources

The chapters are rendered from this directory with the local Pandoc/XeLaTeX
toolchain. Run `uv run fep-lean catalogue` first to generate
`manuscript_vars.yaml` and `09z_unified_formalism_catalogue.md`.

`config.yaml` contains static metadata. Runtime values are emitted by
`src/output/manuscript.py`; unresolved `{{...}}` expressions are a publication
failure. The generated appendix is derived from the validated catalogue and
contains one Lean block and one equation group for every topic.

The discussion chapters include `05b_execution_integrity.md`, which documents
the real compiler, HTTP, and SQLite execution contract.
