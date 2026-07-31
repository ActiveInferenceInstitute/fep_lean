"""Single canonical command-line interface for fep_lean."""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import time
from collections.abc import Sequence
from pathlib import Path

from _paths import project_root
from catalogue.topics import FEPTopicCatalogue
from pipeline.orchestrator import run_pipeline, run_single_topic
from verification._toolchain import find_executable, subprocess_env
from verification.environment import run_validation_checks
from verification.lean_verifier import LeanVerifier


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _setup(root: Path) -> int:
    lean_dir = root / "lean"
    try:
        timeout = int(os.environ.get("FEP_LEAN_SETUP_TIMEOUT_SEC", "1800"))
    except ValueError:
        print("setup failed: FEP_LEAN_SETUP_TIMEOUT_SEC must be an integer", flush=True)
        return 1
    if timeout < 1:
        print("setup failed: FEP_LEAN_SETUP_TIMEOUT_SEC must be positive", flush=True)
        return 1

    lake = find_executable("lake", lean_dir)
    deadline = time.monotonic() + timeout
    if not lake:
        bootstrap = root / "scripts" / "_maint_bootstrap_lean_toolchain.sh"
        if not bootstrap.is_file():
            print(
                "lake executable is unavailable and the bootstrap script is missing",
                flush=True,
            )
            return 1
        bootstrap_env = dict(os.environ)
        elan_home = bootstrap_env.get("ELAN_HOME", str(Path.home() / ".elan"))
        bootstrap_env["ELAN_HOME"] = elan_home
        bootstrap_env["PATH"] = (
            str(Path(elan_home) / "bin") + ":" + bootstrap_env.get("PATH", "")
        )
        try:
            result = subprocess.run(
                ["bash", str(bootstrap)],
                cwd=root,
                env=bootstrap_env,
                timeout=max(1, int(deadline - time.monotonic())),
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"setup failed: {exc}", flush=True)
            return 1
        if result.returncode:
            print(
                f"setup failed with exit code {result.returncode}: {bootstrap}",
                flush=True,
            )
            return result.returncode
        return 0

    env = subprocess_env(lean_dir)
    for command in ((lake, "update"), (lake, "exe", "cache", "get"), (lake, "build")):
        try:
            remaining = max(1, int(deadline - time.monotonic()))
            result = subprocess.run(
                command, cwd=lean_dir, env=env, timeout=remaining, check=False
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"setup failed: {exc}", flush=True)
            return 1
        if result.returncode:
            print(
                f"setup failed with exit code {result.returncode}: {' '.join(command)}",
                flush=True,
            )
            return result.returncode
    return 0


def _print_result(result: object) -> int:
    payload = result.as_dict() if hasattr(result, "as_dict") else result
    print(json.dumps(payload, indent=2, default=str))
    return 0 if getattr(result, "complete", False) else 1


def _verify(root: Path, topic_ids: list[str] | None, area: str | None) -> int:
    """Compile catalogue sketches with Lean only, without Hermes or Gauss."""
    try:
        catalogue = FEPTopicCatalogue.from_yaml(root / "config" / "topics.yaml")
        topics = catalogue.topics
        if topic_ids:
            known = {topic.id for topic in topics}
            unknown = sorted(set(topic_ids) - known)
            if unknown:
                raise ValueError(f"unknown topic ids: {', '.join(unknown)}")
            topics = [topic for topic in topics if topic.id in topic_ids]
        if area:
            topics = [topic for topic in topics if topic.area == area]
        if not topics:
            raise ValueError("no catalogue topics matched the requested filters")
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "mode": "lean-only",
                    "complete": False,
                    "failure_reason": str(exc),
                }
            )
        )
        return 1

    verifier = LeanVerifier(lean_dir=root / "lean", project_root=root)
    mathlib_ok, mathlib_message = verifier.check_mathlib_built()
    if not mathlib_ok:
        print(
            json.dumps(
                {
                    "status": "error",
                    "mode": "lean-only",
                    "complete": False,
                    "catalogue_topics": len(topics),
                    "verified_topics": 0,
                    "mathlib": mathlib_message,
                    "results": [],
                },
                indent=2,
            )
        )
        return 1

    results = verifier.verify_batch([(topic.id, topic.lean_sketch) for topic in topics])
    result_payload = []
    for result in results:
        row = result.as_dict()
        # The verifier removes its temporary source file before returning;
        # do not publish a path that is already stale in the CLI receipt.
        row["lean_file"] = None
        result_payload.append(row)
    clean = sum(result.compiles and not result.has_sorry for result in results)
    complete = len(results) == len(topics) and clean == len(topics)
    print(
        json.dumps(
            {
                "status": "ok" if complete else "error",
                "mode": "lean-only",
                "complete": complete,
                "catalogue_topics": len(topics),
                "verified_topics": clean,
                "mathlib": mathlib_message,
                "results": result_payload,
            },
            indent=2,
            default=str,
        )
    )
    return 0 if complete else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fep-lean",
        description="Strict FEP Lean catalogue and verification pipeline",
    )
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("setup", help="explicitly acquire/build the pinned Lean workspace")
    sub.add_parser("preflight", help="run read-only full-mode capability checks")
    verify = sub.add_parser("verify", help="compile catalogue sketches with Lean only")
    verify.add_argument("--area")
    verify.add_argument("--topic", action="append", dest="topics")
    catalogue = sub.add_parser(
        "catalogue", help="generate deterministic offline catalogue artifacts"
    )
    catalogue.add_argument("--area")
    catalogue.add_argument("--topic", action="append", dest="topics")
    run = sub.add_parser("run", help="run full Hermes, Lean, and SQLite verification")
    run.add_argument("--area")
    run.add_argument("--topic", action="append", dest="topics")
    run.add_argument(
        "--workflow", choices=("verify", "draft", "prove", "review"), default="verify"
    )
    topic = sub.add_parser("topic", help="verify one exact topic")
    topic.add_argument("topic_id")
    topic.add_argument(
        "--workflow", choices=("verify", "draft", "prove", "review"), default="verify"
    )
    sub.add_parser("report", help="run catalogue mode and emit a complete report")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _configure_logging(args.verbose or os.environ.get("FEP_LEAN_VERIFY_VERBOSE") == "1")
    previous_project_dir = os.environ.get("PROJECT_DIR")
    if args.project_root is not None:
        os.environ["PROJECT_DIR"] = str(args.project_root.resolve())
    try:
        root = project_root()
        if args.command == "setup":
            return _setup(root)
        if args.command == "preflight":
            result = run_validation_checks(root, mode="full")
            print(json.dumps(result, indent=2))
            return 0 if result["status"] == "ok" else 1
        if args.command == "verify":
            return _verify(root, args.topics, args.area)
        if args.command == "catalogue":
            return _print_result(
                run_pipeline(
                    mode="catalogue", area_filter=args.area, topic_filter=args.topics
                )
            )
        if args.command == "run":
            return _print_result(
                run_pipeline(
                    mode="full",
                    area_filter=args.area,
                    topic_filter=args.topics,
                    workflow=args.workflow,
                )
            )
        if args.command == "topic":
            return _print_result(
                run_single_topic(args.topic_id, mode="full", workflow=args.workflow)
            )
        if args.command == "report":
            return _print_result(run_pipeline(mode="catalogue"))
        parser.error(f"unsupported command: {args.command}")
        return 2
    finally:
        if args.project_root is not None:
            if previous_project_dir is None:
                os.environ.pop("PROJECT_DIR", None)
            else:
                os.environ["PROJECT_DIR"] = previous_project_dir


if __name__ == "__main__":
    raise SystemExit(main())
