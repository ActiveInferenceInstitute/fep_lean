"""fep_lean src directory — Subpackaged for domain modularity.

The root of this package exports all public items for backward compatibility,
but internal modules prefer qualified subpackage paths (e.g. ``from catalogue.topics import ...``).

Subpackages
-----------
    catalogue/     — Data model and topics YAML
    verification/  — Lean 4 checker and environment validation
    gauss/         — OpenGauss API client, sessions, orchestrator
    llm/           — LLM backend wrapper (Hermes explainer)
    output/        — Artifact generators (figures, manuscript vars, reports)
    pipeline/      — 4-stage core DAG (Load Catalogue, Environment Validation,
                     Gauss Sessions, Manuscript Artifacts) and entry scripts
"""

from __future__ import annotations

__version__ = "0.7.1"

# 1. Catalogue
from catalogue.topics import FEPTopicCatalogue, TopicEntry

# 2. Verification
from verification.environment import run_validation_checks
from verification.lean_verifier import LeanVerifier, VerifyResult

# 3. Gauss
from gauss.cli import check_gauss_cli, workflows_enabled
from gauss.client import OpenGaussClient, SessionRecord
from gauss.runner import GaussRunner, TopicRunResult

# 4. LLM
from llm.hermes import HermesAPIError, HermesConfig, HermesExplainer, HermesResult

# 5. Output
from output.figures import write_all_catalogue_figures
from output.manuscript import (
    build_full_topic_lean_catalogue_markdown,
    build_manuscript_vars,
    build_topic_latex_equations_markdown,
    build_unified_formalism_appendix_markdown,
    write_full_topic_lean_catalogue_markdown,
    write_manuscript_vars,
    write_topic_latex_equations_markdown,
    write_unified_formalism_appendix_markdown,
)
from output.reporter import Reporter, ReportPaths

# 6. Pipeline
from _paths import project_root
from pipeline.core import FEPPipeline, PipelineResult, StepResult
from pipeline.orchestrator import run_pipeline, run_single_topic

__all__ = [
    # Catalogue
    "FEPTopicCatalogue",
    "TopicEntry",
    # Verification
    "LeanVerifier",
    "VerifyResult",
    "run_validation_checks",
    # Gauss
    "OpenGaussClient",
    "SessionRecord",
    "GaussRunner",
    "TopicRunResult",
    "check_gauss_cli",
    "workflows_enabled",
    # LLM
    "HermesConfig",
    "HermesExplainer",
    "HermesResult",
    "HermesAPIError",
    # Output
    "write_all_catalogue_figures",
    "write_manuscript_vars",
    "build_manuscript_vars",
    "build_full_topic_lean_catalogue_markdown",
    "build_topic_latex_equations_markdown",
    "build_unified_formalism_appendix_markdown",
    "write_full_topic_lean_catalogue_markdown",
    "write_topic_latex_equations_markdown",
    "write_unified_formalism_appendix_markdown",
    "Reporter",
    "ReportPaths",
    # Pipeline
    "FEPPipeline",
    "PipelineResult",
    "StepResult",
    "project_root",
    "run_pipeline",
    "run_single_topic",
]
