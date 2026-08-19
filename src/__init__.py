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
from output.reporter import Reporter, ReportPaths
from pipeline.core import FEPPipeline, PipelineResult, StepResult
from pipeline.orchestrator import run_pipeline, run_single_topic

# 2. Verification
from verification.environment import run_validation_checks
from verification.lean_verifier import LeanVerifier, VerifyResult

# 6. Pipeline
from _paths import project_root

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
    # LLM
    "HermesConfig",
    "HermesExplainer",
    "HermesResult",
    "HermesAPIError",
    # Output
    "write_all_catalogue_figures",
    "write_manuscript_vars",
    "build_manuscript_vars",
    "build_unified_formalism_appendix_markdown",
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
