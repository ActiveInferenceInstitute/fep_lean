#!/usr/bin/env python3
"""Thin orchestrator: re-run the lightweight pipeline and refresh Markdown/JSON reports.

Calls ``run_pipeline`` with ``FEP_LEAN_GAUSS_WORKFLOWS=0`` (default here), so stages are:
load catalogue, validation, skipped Gauss, manuscript artifacts (vars + unified 09z formalism + figures), then
``Reporter.generate`` from the orchestrator. This is **not** a SQLite-session replay; it
recomputes from the current ``config/topics.yaml`` and environment.
"""

from __future__ import annotations

import os

from infrastructure.core.logging.utils import get_logger

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("FEP_LEAN_GAUSS_WORKFLOWS", "0")

from pipeline.orchestrator import project_root, run_pipeline

logger = get_logger(__name__)


def main() -> None:
    root = project_root()
    logger.info("fep_lean: regenerating reports for FEP pipeline")

    res = run_pipeline(interactive=False)

    if res.run_dir:
        logger.info("Reports regenerated at: %s", res.run_dir)
    if res.status != "ok":
        logger.warning("Pipeline encountered errors during report generation.")


if __name__ == "__main__":
    main()
