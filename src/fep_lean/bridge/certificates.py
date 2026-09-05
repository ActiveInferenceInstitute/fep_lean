#!/usr/bin/env python3
"""Certificate protocol runner for the fep_lean <-> GNN bridge, phase P3.

Compares GNN-pipeline-executed quantities (pymdp 1.0.0 artifacts from the
P3 custody run) with Lean-witnessed claims for the P1 model instance

    FEP.ActiveInference.symmetricBoolModel trueBiasedPolicyPrior
      : GenerativeModel Bool Bool Bool   (active_inference.lean:743-749)

Certificates (see the slice README for the full protocol, evidence-plane
labels, and the tolerance justification):

  C1  policy-posterior agreement: executed `policy_posterior` vs the
      Lean-proved equality `policyPosterior = policyPrior`
      (active_inference.lean:816-826) with
      `trueBiasedPolicyPrior` = (1/4, 3/4) in (false, true) order
      (:731-734). Exact rationals; numerical-witness plane evaluation.
  C2  VFE agreement: executed `variational_free_energy` vs the proved
      closed form `VFE_initial = log 2` (variationalFreeEnergy
      :209-214; predictedOutcome = fairBoolLaw :762-773; posteriorState
      = initial belief :121-125,745; outcomeSurprisal :202-205),
      evaluated as math.log(2) in float64 (numerical-witness plane).
  C3  directional agreement: NOT RUN — recorded boundary (one-step
      instance; no Boolean-carrier decrease theorem on the Lean side).
  O1  informational divergence: executed `expected_free_energy` (pymdp
      `neg_efe`, linear-utility convention, pymdp/control.py:422-445)
      vs Lean `expectedFreeEnergy` = risk + ambiguity = log 2
      (:148-150, :789-812). Different conventions; filed with exact
      numbers, never averaged away.

Exit codes: 0 when every stated certificate (C1, C2) agrees within
tolerance; 1 on any disagreement or unstatable quantity. O1 never
changes the exit code.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

TOLERANCE = 1e-6  # jax float32 backend; see README "Comparison policy"

# Lean-witnessed constants (exact; provenance in comments).

# lean/FepSketches/active_inference.lean:731-734 — trueBiasedPolicyPrior
# (mass policy := if policy then 3 / 4 else 1 / 4), Bool order
# (false, true); equality Q(π) = prior proved at :816-826.
LEAN_Q_FALSE = 0.25
LEAN_Q_TRUE = 0.75

# lean/FepSketches/active_inference.lean:209-214 with :202-205, :762-773,
# :121-125, :745 — VFE on the initial belief collapses to -log P(o) with
# P(o) = 1/2 (fair law), i.e. log 2 (nats). Evaluated in float64 as the
# numerical witness of the proved closed form.
LEAN_VFE_INITIAL = math.log(2)

# lean/FepSketches/active_inference.lean:148-150 with :789-812 — Lean
# expectedFreeEnergy = risk + ambiguity = 0 + entropy(fairBoolLaw) = log 2.
LEAN_EFE = math.log(2)

PLANE_EXECUTION = "reported numerical values; execution provenance unverified"
PLANE_LEAN_COMPILATION = "referenced Lean statement (native receipt checked separately)"
PLANE_NUMERICAL = "numerical witness"


def _finite_number(value: object) -> bool:
    try:
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
        )
    except OverflowError:
        return False


def _within(value: float, expected: float, tolerance: float) -> bool:
    return abs(value - expected) <= tolerance


def _cert_entry(
    cid: str,
    passed: bool,
    lean_value: str,
    executed_value: str,
    delta: str,
    lean_plane: str,
    executed_plane: str,
    detail: str,
) -> dict[str, Any]:
    return {
        "certificate": cid,
        "passed": passed,
        "lean_value": lean_value,
        "executed_value": executed_value,
        "delta": delta,
        "lean_evidence_plane": lean_plane,
        "executed_evidence_plane": executed_plane,
        "detail": detail,
    }


def _compare_c1(
    results: dict[str, Any], tolerance: float
) -> tuple[dict[str, Any], bool]:
    q_posterior = results.get("policy_posterior")
    q0 = q_posterior[0] if isinstance(q_posterior, list) and q_posterior else None
    if isinstance(q0, list) and len(q0) == 2 and all(_finite_number(v) for v in q0):
        executed_q_false = float(q0[0])
        executed_q_true = float(q0[1])
        d_false = abs(executed_q_false - LEAN_Q_FALSE)
        d_true = abs(executed_q_true - LEAN_Q_TRUE)
        c1_pass = _within(executed_q_false, LEAN_Q_FALSE, tolerance) and _within(
            executed_q_true, LEAN_Q_TRUE, tolerance
        )
        entry = _cert_entry(
            "C1",
            c1_pass,
            f"Q = ({LEAN_Q_FALSE}, {LEAN_Q_TRUE}) exact",
            f"policy_posterior[0] = ({executed_q_false!r}, {executed_q_true!r})",
            f"|dfalse| = {d_false:.3e}, |dtrue| = {d_true:.3e}",
            PLANE_LEAN_COMPILATION + " + " + PLANE_NUMERICAL,
            PLANE_EXECUTION,
            "Lean equality Q(pi)=prior (:816-826) vs pymdp infer_policies"
            " posterior; argmax executed = "
            + ("true" if executed_q_true > executed_q_false else "false"),
        )
        return entry, c1_pass
    entry = _cert_entry(
        "C1",
        False,
        str((LEAN_Q_FALSE, LEAN_Q_TRUE)),
        "unstatable",
        "n/a",
        PLANE_LEAN_COMPILATION + " + " + PLANE_NUMERICAL,
        PLANE_EXECUTION,
        "policy_posterior missing or not a 2-vector in executed results",
    )
    return entry, False


def _compare_c2(
    results: dict[str, Any], tolerance: float
) -> tuple[dict[str, Any], bool]:
    vfe = results.get("variational_free_energy")
    executed_vfe = (
        float(vfe[0])
        if isinstance(vfe, list) and vfe and _finite_number(vfe[0])
        else None
    )
    if executed_vfe is not None:
        d_vfe = abs(executed_vfe - LEAN_VFE_INITIAL)
        c2_pass = _within(executed_vfe, LEAN_VFE_INITIAL, tolerance)
        entry = _cert_entry(
            "C2",
            c2_pass,
            f"VFE_initial = log 2 = {LEAN_VFE_INITIAL!r}",
            f"variational_free_energy[0] = {executed_vfe!r}",
            f"|d| = {d_vfe:.3e}",
            PLANE_LEAN_COMPILATION + " + " + PLANE_NUMERICAL,
            PLANE_EXECUTION,
            "Lean VFE on initial belief (closed form, README C2) vs pymdp"
            " infer_states VFE",
        )
        return entry, c2_pass
    entry = _cert_entry(
        "C2",
        False,
        str(LEAN_VFE_INITIAL),
        "unstatable",
        "n/a",
        PLANE_LEAN_COMPILATION + " + " + PLANE_NUMERICAL,
        PLANE_EXECUTION,
        "variational_free_energy missing from executed results",
    )
    return entry, False


def _observe_o1(results: dict[str, Any]) -> list[dict[str, str]]:
    observations: list[dict[str, str]] = []
    efe = results.get("expected_free_energy")
    if (
        isinstance(efe, list)
        and efe
        and isinstance(efe[0], list)
        and efe[0]
        and _finite_number(efe[0][0])
    ):
        executed_efe = float(efe[0][0])
        observations.append(
            {
                "id": "O1",
                "lean_value": f"expectedFreeEnergy = log 2 = {LEAN_EFE!r}"
                " (active_inference.lean:148-150, :789-812)",
                "executed_value": f"expected_free_energy[0] ="
                f" {executed_efe!r}"
                " (pymdp neg_efe, linear utility, pymdp/control.py:422-445)",
                "delta": f"{abs(executed_efe - LEAN_EFE):.6f}",
                "note": "different C conventions across the bridge surface;"
                " filed, not smoothed over (README O1)",
            }
        )
    return observations


def compare(
    results: dict[str, Any], tolerance: float
) -> tuple[list[dict[str, Any]], list[dict[str, str]], bool]:
    """Run C1/C2 comparisons; return (certificates, observations, ok)."""
    if not _finite_number(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    c1_entry, c1_pass = _compare_c1(results, tolerance)
    c2_entry, c2_pass = _compare_c2(results, tolerance)
    observations = _observe_o1(results)
    ok = c1_pass and c2_pass
    return [c1_entry, c2_entry], observations, ok


def render_markdown(
    certificates: list[dict[str, Any]],
    observations: list[dict[str, str]],
    results_path: Path,
    ok: bool,
) -> str:
    lines = [
        "# P3 certificates — FepLeanSymmetricBool",
        "",
        f"Identified result artifact: `{results_path.name}`.",
        "",
        "Numerical comparison only; execution provenance unverified.",
        "`execution_source_verified: false`; `native_claim_ready: false`.",
        "A passing comparison does not establish a current pipeline execution or Lean proof.",
        "",
        "| Certificate | Result | Lean value | Executed value | Delta |",
        "| --- | --- | --- | --- | --- |",
    ]
    for c in certificates:
        lines.append(
            f"| {c['certificate']} | {'PASS' if c['passed'] else 'FAIL'}"
            f" | {c['lean_value']} | {c['executed_value']} | {c['delta']} |"
        )
    lines += [
        "",
        "C3 (directional agreement) is a recorded boundary, not run: the",
        "instance is one-step and no Lean-witnessed decrease family exists",
        "for the Boolean carrier (README C3).",
        "",
        "## Evidence planes",
        "",
    ]
    for c in certificates:
        lines.append(
            f"- {c['certificate']}: Lean side = {c['lean_evidence_plane']};"
            f" executed side = {c['executed_evidence_plane']}."
        )
    if observations:
        lines += ["", "## Observations (findings, exact numbers)", ""]
        for o in observations:
            lines += [
                (
                    f"- {o['id']}: executed {o['executed_value']}; Lean"
                    f" {o['lean_value']}; delta = {o['delta']}."
                    f" {o['note']}"
                ),
            ]
    lines += [
        "",
        f"Gate: {'PASS' if ok else 'FAIL'} (C1 and C2 within tolerance).",
        "",
    ]
    return "\n".join(lines)
