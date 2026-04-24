"""Thin programmatic wrapper for the `fep_lean` project pipeline.

Provides `run_pipeline` and `run_single_topic` for CLI scripts, abstracting
away the directory injection and initialization logic.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from _paths import project_root
from catalogue.topics import FEPTopicCatalogue
from gauss.cli import workflows_enabled
from pipeline.core import FEPPipeline
from output.manuscript import write_manuscript_vars
from output.reporter import Reporter

log = logging.getLogger(__name__)


def run_pipeline(
    *,
    interactive: bool = False,
    area_filter: str | None = None,
    topic_filter: list[str] | None = None,
    output_root: Path | None = None,
) -> Any:
    """Execute the pipeline and generate reports when the catalogue loads.

    If `FEP_LEAN_GAUSS_WORKFLOWS=1` is NOT set, LLM and Lean workflows are skipped,
    and only catalogue validation / figure generation runs.

    Parameters:
        interactive: If True, log verbosely to console.
        area_filter: If set, only process topics matching this area (e.g. "FEP").
        topic_filter: If set, restrict to these topic IDs.
        output_root: Override for ``output/`` (reports + cache); defaults
            to ``$FEP_LEAN_OUTPUT_ROOT`` or ``project_root / "output"``.
            Tests should set this (or the env var) so spawned pipeline runs
            do not pollute the canonical reports tree.

    Returns:
        PipelineResult object spanning the executed DAG.
    """
    if interactive:
        logging.getLogger("fep_lean").setLevel(logging.DEBUG)

    root = project_root()
    log.info("Starting FEP Lean Pipeline... [root=%s]", root)

    if not workflows_enabled():
        log.warning("FEP_LEAN_GAUSS_WORKFLOWS is disabled. LLM/Lean steps will SKIP.")

    pipeline = FEPPipeline(root, output_root=output_root)
    result = pipeline.run(area_filter=area_filter, topic_filter=topic_filter)

    # Final Stage: Reporting
    if hasattr(pipeline, "_catalogue") and pipeline._catalogue:
        reporter = Reporter(root, output_root=pipeline.output_root)
        paths = reporter.generate(pipeline._catalogue, result)
        result.run_dir = str(paths.index_md.parent)
        log.info("Reports generated at: %s", result.run_dir)
        # Refresh manuscript_vars.yaml so the hermes/verify blocks reflect the
        # summary.json this run just wrote (the manuscript-artifacts stage above
        # ran before Reporter.generate and could only see the prior run).
        try:
            write_manuscript_vars(root, pipeline._catalogue)
        except Exception as exc:
            log.warning("Failed to refresh manuscript_vars.yaml after reporting: %s", exc)
    else:
        log.error("Catalogue failed to load; skipping report generation.")

    return result


def run_single_topic(
    topic_id: str,
    *,
    interactive: bool = False,
    output_root: Path | None = None,
) -> Any:
    """Run formalization over exactly one topic.

    See :func:`run_pipeline` for the meaning of ``output_root``.
    """
    if interactive:
        logging.getLogger("fep_lean").setLevel(logging.DEBUG)

    root = project_root()

    # Early validation that topic exists
    try:
        cat = FEPTopicCatalogue.from_yaml(root / "config" / "topics.yaml")
        if topic_id not in [t.id for t in cat.topics]:
            log.error("Unknown topic ID: %s", topic_id)
            return {"status": "error", "message": f"Topic '{topic_id}' not found in catalogue."}
    except Exception as e:
        log.error("Failed to read topics catalogue: %s", e)
        return {"status": "error", "message": str(e)}

    pipeline = FEPPipeline(root, output_root=output_root)
    result = pipeline.run(topic_filter=[topic_id])

    # Generate the same report bundle as the full pipeline so the single-topic
    # path is auditable.  The reporter iterates the entire catalogue and renders
    # "not run" sections for the 49 untouched rows, which is exactly the right
    # behaviour for a focused one-topic audit.
    if (
        result.status in ("ok", "warning")
        and hasattr(pipeline, "_catalogue")
        and pipeline._catalogue
    ):
        reporter = Reporter(root, output_root=pipeline.output_root)
        paths = reporter.generate(pipeline._catalogue, result)
        result.run_dir = str(paths.index_md.parent)
        log.info("Single-topic reports generated at: %s", result.run_dir)
        # Refresh manuscript_vars.yaml so the hermes block reflects the new run.
        try:
            write_manuscript_vars(root, pipeline._catalogue)
        except Exception as exc:
            log.warning("Failed to refresh manuscript_vars.yaml after reporting: %s", exc)

    topic_res: dict[str, Any] = {}
    for stage in result.stages:
        if "Gauss" in stage.name and stage.payload and "topics" in stage.payload:
            topics_out = stage.payload["topics"]
            if topics_out:
                topic_res = dict(topics_out[0])

    if result.status == "error":
        topic_res["status"] = "error"
        topic_res["message"] = "Pipeline execution error"
    elif "status" not in topic_res:
        topic_res["status"] = result.status

    topic_res["run_dir"] = result.run_dir
    return topic_res
