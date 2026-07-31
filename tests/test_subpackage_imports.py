"""Test verifying that all subpackages are importable standalone."""

from __future__ import annotations

import sys
from pathlib import Path


def test_root_package_init_importable():
    """Import the src/__init__.py as a package to cover its re-exports."""
    proj_root = Path(__file__).resolve().parent.parent
    src_parent = str(proj_root)
    added = src_parent not in sys.path
    if added:
        sys.path.insert(0, src_parent)
    try:
        import src

        assert src.__version__
        # Spot-check a few re-exported names
        assert hasattr(src, "FEPTopicCatalogue")
        assert hasattr(src, "LeanVerifier")
        assert hasattr(src, "HermesExplainer")
        assert hasattr(src, "FEPPipeline")
        assert hasattr(src, "Reporter")
        assert len(src.__all__) > 10
    finally:
        if added:
            sys.path.remove(src_parent)


def test_catalogue_imports():
    from catalogue.topics import FEPTopicCatalogue

    assert FEPTopicCatalogue is not None


def test_verification_imports():
    from verification.lean_verifier import LeanVerifier

    assert LeanVerifier is not None


def test_gauss_imports():
    from gauss.client import OpenGaussClient

    assert OpenGaussClient is not None


def test_llm_imports():
    from llm.hermes import HermesExplainer

    assert HermesExplainer is not None


def test_output_imports():
    from output.manuscript import (
        build_manuscript_vars,
        build_typeset_equations_markdown,
        build_unified_formalism_appendix_markdown,
        write_manuscript_vars,
        write_typeset_equations_markdown,
        write_unified_formalism_appendix_markdown,
    )

    assert callable(build_manuscript_vars)
    assert callable(write_manuscript_vars)
    assert callable(write_unified_formalism_appendix_markdown)
    assert callable(build_typeset_equations_markdown)
    assert callable(write_typeset_equations_markdown)
    assert callable(build_unified_formalism_appendix_markdown)
    assert callable(write_unified_formalism_appendix_markdown)
    from output.reporter import Reporter

    assert Reporter is not None


def test_pipeline_imports():
    from pipeline.core import FEPPipeline

    assert FEPPipeline is not None
