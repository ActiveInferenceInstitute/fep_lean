"""Deterministic manuscript, figure, and run-report artifacts."""

from output.figures import write_all_catalogue_figures
from output.manuscript import (
    build_lean_catalogue_markdown,
    build_manuscript_vars,
    build_typeset_equations_markdown,
    build_unified_formalism_appendix_markdown,
    write_manuscript_vars,
    write_typeset_equations_markdown,
    write_unified_formalism_appendix_markdown,
)
from output.reporter import Reporter, ReportPaths, validate_report_receipt

__all__ = [
    "ReportPaths",
    "Reporter",
    "build_lean_catalogue_markdown",
    "build_manuscript_vars",
    "build_typeset_equations_markdown",
    "build_unified_formalism_appendix_markdown",
    "validate_report_receipt",
    "write_all_catalogue_figures",
    "write_manuscript_vars",
    "write_typeset_equations_markdown",
    "write_unified_formalism_appendix_markdown",
]
