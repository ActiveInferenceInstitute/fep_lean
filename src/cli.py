"""Single canonical command-line interface for fep_lean."""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Sequence

from _paths import project_root
from pipeline.orchestrator import run_pipeline, run_single_topic
from verification.environment import run_validation_checks


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def _setup(root: Path) -> int:
    lean_dir = root / "lean"
    lake = os.environ.get("FEP_LEAN_LAKE_EXE") or shutil.which("lake")
    if not lake:
        print("lake executable is unavailable", flush=True)
        return 1
    timeout = int(os.environ.get("FEP_LEAN_SETUP_TIMEOUT_SEC", "1800"))
    for command in ((lake, "exe", "cache", "get"), (lake, "build")):
        try:
            result = subprocess.run(command, cwd=lean_dir, timeout=timeout, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"setup failed: {exc}", flush=True)
            return 1
        if result.returncode:
            print(f"setup failed with exit code {result.returncode}: {' '.join(command)}", flush=True)
            return result.returncode
    return 0


def _print_result(result: object) -> int:
    payload = result.as_dict() if hasattr(result, "as_dict") else result
    print(json.dumps(payload, indent=2, default=str))
    return 0 if getattr(result, "complete", False) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fep-lean", description="Strict FEP Lean catalogue and verification pipeline")
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("setup", help="explicitly acquire/build the pinned Lean workspace")
    sub.add_parser("preflight", help="run read-only full-mode capability checks")
    catalogue = sub.add_parser("catalogue", help="generate deterministic offline catalogue artifacts")
    catalogue.add_argument("--area")
    catalogue.add_argument("--topic", action="append", dest="topics")
    run = sub.add_parser("run", help="run full Hermes, Lean, and SQLite verification")
    run.add_argument("--area")
    run.add_argument("--topic", action="append", dest="topics")
    run.add_argument("--workflow", choices=("verify", "draft", "prove", "review"), default="verify")
    topic = sub.add_parser("topic", help="verify one exact topic")
    topic.add_argument("topic_id")
    topic.add_argument("--workflow", choices=("verify", "draft", "prove", "review"), default="verify")
    sub.add_parser("report", help="run catalogue mode and emit a complete report")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _configure_logging(args.verbose)
    if args.project_root is not None:
        os.environ["PROJECT_DIR"] = str(args.project_root.resolve())
    root = project_root()
    if args.command == "setup":
        return _setup(root)
    if args.command == "preflight":
        result = run_validation_checks(root, mode="full")
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "ok" else 1
    if args.command == "catalogue":
        return _print_result(run_pipeline(mode="catalogue", area_filter=args.area, topic_filter=args.topics))
    if args.command == "run":
        return _print_result(run_pipeline(mode="full", area_filter=args.area, topic_filter=args.topics, workflow=args.workflow))
    if args.command == "topic":
        return _print_result(run_single_topic(args.topic_id, mode="full", workflow=args.workflow))
    if args.command == "report":
        return _print_result(run_pipeline(mode="catalogue"))
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
