#!/usr/bin/env python3
"""Analysis stage: validate environment, regenerate manuscript_vars.yaml and figures.

Environment variables
----------------------
FEP_LEAN_GAUSS_WORKFLOWS=1
    Enable the full Hermes LLM + Lean 4 compilation stage (real OpenRouter API
    calls + real ``lake env lean`` subprocess).  **Not set by default** — export
    ``FEP_LEAN_GAUSS_WORKFLOWS=1`` (or use ``FEP_LEAN_LIVE_TESTS=1`` below) before
    analysis when you want live workflows.

FEP_LEAN_LIVE_TESTS=1
    When ``FEP_LEAN_GAUSS_WORKFLOWS`` is unset, setting this to ``1`` enables
    workflows. If both are unset, workflows stay off (deterministic catalogue +
    figures only).

FEP_LEAN_MAX_TOPICS
    Optional positive integer: cap how many catalogue rows run in Gauss sessions
    (after filters). Useful for smoke tests.

ANALYSIS_SCRIPT_TIMEOUT_SEC
    Inherited from the Stage 02 orchestrator (repo root). Default 7200s per
    script (see infrastructure/core/analysis_timeout.py); use 0 for unlimited.

OPENROUTER_API_KEY  /  ~/.gauss/.env
    Required for the Hermes LLM stage when workflows are enabled.  Loaded
    automatically from ~/.gauss/.env by HermesConfig.from_settings().

FEP_LEAN_LAKE_EXE / FEP_LEAN_LEAN_EXE
    Override paths to the lake / lean binaries (resolved automatically via
    ~/.elan/toolchains/ if not set).
"""

from __future__ import annotations

import os

from infrastructure.core.logging.utils import get_logger

# Ensure headless figures (safe to force — never interactive in pipeline)
os.environ.setdefault("MPLBACKEND", "Agg")

# ── Workflow-enable logic ─────────────────────────────────────────────────────
# Priority:
#   1. FEP_LEAN_GAUSS_WORKFLOWS already set in parent env  →  use as-is
#   2. FEP_LEAN_LIVE_TESTS=1                               →  enable workflows
#   3. default                                             →  off (CI / core pipeline friendly)

if "FEP_LEAN_GAUSS_WORKFLOWS" not in os.environ:
    if os.environ.get("FEP_LEAN_LIVE_TESTS", "").strip().lower() in ("1", "true", "yes", "on"):
        os.environ["FEP_LEAN_GAUSS_WORKFLOWS"] = "1"
    else:
        os.environ["FEP_LEAN_GAUSS_WORKFLOWS"] = "0"
# else: already set by caller (run.sh, test fixture, or parent shell) — keep it

from pipeline.orchestrator import project_root, run_pipeline  # noqa: E402

logger = get_logger(__name__)


def main() -> None:
    root = project_root()
    wf_flag = os.environ.get("FEP_LEAN_GAUSS_WORKFLOWS", "0")
    logger.info("fep_lean analysis from %s  [FEP_LEAN_GAUSS_WORKFLOWS=%s]", root, wf_flag)
    if wf_flag != "1":
        logger.warning(
            "FEP_LEAN_GAUSS_WORKFLOWS is not enabled — Hermes LLM and Lean "
            "verification will be SKIPPED.  Set FEP_LEAN_GAUSS_WORKFLOWS=1 "
            "(or FEP_LEAN_LIVE_TESTS=1) to run real Lean + OpenRouter workflows."
        )

    result = run_pipeline(interactive=False)
    fig_dir = root / "output" / "figures"
    vars_path = root / "manuscript" / "manuscript_vars.yaml"
    print(str(fig_dir / "area_distribution.png"))
    print(str(fig_dir / "mathlib_coverage.png"))
    print(str(fig_dir / "pipeline_timing.png"))
    print(str(vars_path))
    if result.run_dir:
        print(result.run_dir)
    if result.status != "ok":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
