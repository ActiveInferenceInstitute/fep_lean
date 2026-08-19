"""Public fep_lean API.

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

__version__ = "1.0.0"

# 1. Catalogue
# 6. Pipeline
from _paths import project_root
from catalogue.topics import FEPTopicCatalogue, TopicEntry

# 3. Gauss
from gauss.cli import check_gauss_cli
from gauss.client import OpenGaussClient, SessionRecord
from gauss.runner import GaussRunner, TopicRunResult

# 4. LLM
from llm.hermes import HermesAPIError, HermesConfig, HermesExplainer, HermesResult

# 5. Output
from output.figures import write_all_catalogue_figures
from output.manuscript import (
    build_manuscript_vars,
    build_unified_formalism_appendix_markdown,
    write_manuscript_vars,
    write_unified_formalism_appendix_markdown,
)
from output.reporter import Reporter, ReportPaths, validate_report_receipt
from pipeline.core import FEPPipeline, PipelineResult, StepResult
from pipeline.orchestrator import run_pipeline, run_single_topic

# 2. Verification
from verification.environment import run_validation_checks
from verification.lean_verifier import LeanVerifier, VerifyResult

__all__ = [
    # Pipeline
    "FEPPipeline",
    # Catalogue
    "FEPTopicCatalogue",
    "GaussRunner",
    "HermesAPIError",
    # LLM
    "HermesConfig",
    "HermesExplainer",
    "HermesResult",
    # Verification
    "LeanVerifier",
    # Gauss
    "OpenGaussClient",
    "PipelineResult",
    "ReportPaths",
    "Reporter",
    "SessionRecord",
    "StepResult",
    "TopicEntry",
    "TopicRunResult",
    "VerifyResult",
    "build_manuscript_vars",
    "build_unified_formalism_appendix_markdown",
    "check_gauss_cli",
    "project_root",
    "run_pipeline",
    "run_single_topic",
    "run_validation_checks",
    "validate_report_receipt",
    # Output
    "write_all_catalogue_figures",
    "write_manuscript_vars",
    "write_unified_formalism_appendix_markdown",
]
