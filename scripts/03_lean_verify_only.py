#!/usr/bin/env python3
"""Thin orchestrator: run only Lean 4 compilation on catalogue sketches (no LLM / Gauss).

Uses ``LeanVerifier`` directly; does not set or require ``FEP_LEAN_GAUSS_WORKFLOWS``.
Logs per-topic outcomes to stdout and writes a canonical
``output/reports/verify_<timestamp>/verification_manifest.json`` bundle (built via
``Reporter.build_verification_manifest``) so downstream consumers — including
``output/manuscript.build_manuscript_vars`` — see the same JSON shape produced by
the full pipeline.

Run from ``projects/fep_lean``::

    uv run python scripts/03_lean_verify_only.py

From repository root::

    uv run --directory projects/fep_lean python scripts/03_lean_verify_only.py
"""

from __future__ import annotations

import argparse
import os
import sys

os.environ.setdefault("MPLBACKEND", "Agg")

from pathlib import Path
root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "projects" / "fep_lean" / "src"))

from infrastructure.core.logging.utils import get_logger
from pipeline.orchestrator import project_root

logger = get_logger(__name__)


def main() -> None:
    import logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Verify existing Lean sketches without calling LLM.")
    parser.add_argument("--topic", help="Specific topic ID to verify (e.g. fep-003). If not provided, tests all.")
    args = parser.parse_args()

    root = project_root()
    logger.info("fep_lean: running lean verification only from %s", root)

    from verification.lean_verifier import LeanVerifier
    from catalogue.topics import FEPTopicCatalogue

    cat = FEPTopicCatalogue.from_yaml(root / "config" / "topics.yaml")

    topics_to_run = cat.topics
    if args.topic:
        topics_to_run = [t for t in cat.topics if t.id == args.topic]
        if not topics_to_run:
            logger.error("Unknown topic: %s", args.topic)
            sys.exit(1)

    verifier = LeanVerifier(root / "lean", root)
    if not verifier.check_lake_available():
        logger.warning(
            "lake executable not found or not working — Lean verification skipped. "
            "Install elan (https://github.com/leanprover/elan) to enable."
        )
        sys.exit(0)

    mathlib_ok, mathlib_msg = verifier.check_mathlib_built()
    if not mathlib_ok:
        logger.warning("Mathlib not ready: %s. Building automatically to ensure no degradation...", mathlib_msg)
        try:
            import subprocess
            import os
            env = os.environ.copy()
            # Try to fetch the cache first (may fail due to dyld on newer Apple Silicon, ignore errors)
            logger.info("Running auto-build step 1/2: lake exe cache get")
            subprocess.run(["lake", "exe", "cache", "get"], cwd=verifier._lean_dir, env=env, check=False)
            logger.info("Running auto-build step 2/2: lake build")
            subprocess.run(["lake", "build"], cwd=verifier._lean_dir, env=env, check=True)
            logger.info("Mathlib auto-build completed successfully.")
        except Exception as e:
            logger.error("Auto-build failed: %s", e)
            sys.exit(1)
        
        # Verify again
        mathlib_ok, mathlib_msg = verifier.check_mathlib_built()
        if not mathlib_ok:
            logger.error("Mathlib still not ready after auto-build: %s", mathlib_msg)
            sys.exit(1)
    
    logger.info("Mathlib preflight: %s", mathlib_msg)

    logger.info("Verifying %d topics with lake...", len(topics_to_run))

    items = [(t.id, t.lean_sketch) for t in topics_to_run]
    results = verifier.verify_batch(items)

    successful = sum(1 for r in results if r.compiles)
    with_sorry = sum(1 for r in results if r.compiles and r.has_sorry)

    for r in results:
        status = "OK" if r.compiles else "ERROR"
        if r.compiles and r.has_sorry:
            status = "OK (sorry)"
        logger.info("[%s] %s: %s", status, r.topic_id, f"{len(r.errors)} errors, {len(r.warnings)} warnings")
        if r.errors:
            for err in r.errors:
                logger.error("  %s", err.strip())

    logger.info(
        "Lean verification complete: %d / %d compiled (%d with sorry)",
        successful,
        len(topics_to_run),
        with_sorry,
    )

    import json
    from datetime import datetime, timezone
    from output.reporter import Reporter

    manifest_payload = Reporter.build_verification_manifest(results)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = root / "output" / "reports" / f"verify_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "verification_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info("Wrote verification manifest: %s", manifest_path)

    if successful < len(topics_to_run):
        logger.error(
            "%d topic(s) failed to compile; see error lines above.",
            len(topics_to_run) - successful,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
