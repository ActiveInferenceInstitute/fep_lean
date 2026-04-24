#!/usr/bin/env python3
"""Thin orchestrator: run the FEP pipeline for a single catalogue topic."""

from __future__ import annotations

import argparse
import os
import sys

from infrastructure.core.logging.utils import get_logger

# Ensure headless figures if figures happen to generate (they only generate in run_pipeline)
os.environ.setdefault("MPLBACKEND", "Agg")

from pipeline.orchestrator import project_root, run_single_topic

logger = get_logger(__name__)

_DEFAULT_TOPIC = "fep-008"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run FEP Lean pipeline for a single topic (e.g. fep-001).",
    )
    parser.add_argument(
        "topic_id",
        nargs="?",
        default=None,
        help=f"Topic ID (e.g. fep-001). Default: {_DEFAULT_TOPIC} if omitted.",
    )
    parser.add_argument(
        "--topic",
        dest="topic_flag",
        default=None,
        metavar="ID",
        help=f"Same as positional topic id. Default: {_DEFAULT_TOPIC} if neither is set.",
    )
    parser.add_argument(
        "--workflow",
        choices=["verify", "draft", "prove", "review"],
        default="verify",
        help=(
            "GaussRunner workflow stage (default: verify). "
            "Stages other than 'verify' require FEP_LEAN_GAUSS_WORKFLOWS=1."
        ),
    )
    parser.add_argument(
        "--skip-gauss",
        action="store_true",
        help="Disable Gauss workflows (Hermes + SQLite + GaussRunner); sets FEP_LEAN_GAUSS_WORKFLOWS=0",
    )
    args = parser.parse_args()

    if args.skip_gauss:
        os.environ["FEP_LEAN_GAUSS_WORKFLOWS"] = "0"

    topic = args.topic_id or args.topic_flag or _DEFAULT_TOPIC
    workflow: str = args.workflow

    root = project_root()
    logger.info("fep_lean: running single topic %s (workflow=%s) from %s", topic, workflow, root)

    # For non-verify workflows, bypass the full pipeline and call GaussRunner directly
    # so the workflow kwarg is honoured (the pipeline only uses "verify").
    if workflow != "verify":
        from catalogue.topics import FEPTopicCatalogue
        from gauss.runner import GaussRunner

        try:
            cat = FEPTopicCatalogue.from_yaml(root / "config" / "topics.yaml")
            topic_obj = next((t for t in cat.topics if t.id == topic), None)
            if topic_obj is None:
                logger.error("Unknown topic ID: %s", topic)
                sys.exit(1)
        except Exception as e:
            logger.error("Failed to load catalogue: %s", e)
            sys.exit(1)

        try:
            runner = GaussRunner.create_default(root)
            run_result = runner.run_topic(topic_obj, workflow=workflow)
        except RuntimeError as e:
            logger.error("GaussRunner setup failed: %s", e)
            sys.exit(1)

        if not run_result.success:
            logger.error("Topic %s failed (status=%s): %s", topic, run_result.status, run_result.error)
            sys.exit(1)

        logger.info("Successfully executed %s (workflow=%s)", topic, run_result.workflow)
        logger.info("Lean compiles: %s (sorry=%s)", run_result.lean_compiles, run_result.lean_has_sorry)
        if run_result.stage_results:
            logger.info("Stage results: %d supplementary result(s)", len(run_result.stage_results))
        return

    result = run_single_topic(topic, interactive=False)

    if result.get("status") == "error":
        logger.error(
            "Failed to run topic %s: %s",
            topic,
            result.get("message", "Unknown error"),
        )
        sys.exit(1)

    logger.info("Successfully executed %s", topic)
    logger.info("Run directory: %s", result.get("run_dir"))
    if result.get("hermes_success"):
        logger.info("Hermes LLM returned success.")
    logger.info("Lean compiles: %s (sorry=%s)", result.get("lean_compiles", False), result.get("lean_has_sorry", False))


if __name__ == "__main__":
    main()
