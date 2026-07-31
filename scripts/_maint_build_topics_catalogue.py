#!/usr/bin/env python3
"""Regenerate config/topics.yaml with all 50 catalogue rows.

Run manually after editing METADATA below (or recover real sketches):
  uv run python scripts/_maint_build_topics_catalogue.py

Paths are resolved from the project root (parent of scripts/).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from catalogue_sketches import LATEX_EQUATIONS, SKETCHES, assert_complete

# Distribution: FEP 14, ActiveInference 11, BayesianMechanics 10, InfoGeometry 8, Thermodynamics 7
# Fifth field is mathlib_status (real/partial/aspirational); all rows currently use "real".
METADATA: list[tuple[str, str, str, str, str]] = [
    # id, title, area, mathlib hint, mathlib_status
    ("fep-001", "Variational Free Energy Bound", "FEP", "MeasureTheory.Measure.MeasureSpace", "real"),
    ("fep-002", "Gibbs Free Energy as Marginal Likelihood", "FEP", "MeasureTheory.Measure.MeasureSpace", "real"),
    ("fep-003", "Expected Free Energy Decomposition", "ActiveInference", "Algebra.BigOperators.Group.Finset", "real"),
    ("fep-004", "Fisher Information Metric", "InfoGeometry", "Analysis.InnerProductSpace.Basic", "real"),
    ("fep-005", "Markov Blanket Partition", "BayesianMechanics", "Data.Finset.Basic", "real"),
    ("fep-006", "Generalized State and Flow", "FEP", "MeasureTheory.Measure.MeasureSpace", "real"),
    ("fep-007", "Belief Propagation on Factor Graphs", "ActiveInference", "Algebra.BigOperators.Group.Finset", "real"),
    ("fep-008", "Active Inference Optimal Policy", "ActiveInference", "Data.Finset.Basic, Order.Bounds.Basic", "real"),
    ("fep-009", "Generative Model Likelihood", "BayesianMechanics", "MeasureTheory.Measure.MeasureSpace", "real"),
    ("fep-010", "Fluctuation Theorem Sketch", "BayesianMechanics", "Analysis.SpecialFunctions.Exp", "real"),
    ("fep-011", "Surprise and Self-Information", "FEP", "Analysis.SpecialFunctions.Log.Basic", "real"),
    ("fep-012", "Policy Entropy Regularizer", "FEP", "Analysis.SpecialFunctions.Exp", "real"),
    ("fep-013", "Helmholtz Free Energy Bridge", "Thermodynamics", "Analysis.SpecialFunctions.Log.Basic", "real"),
    ("fep-014", "KL Divergence: Non-Negativity, Chain Rule, Data Processing", "InfoGeometry", "MeasureTheory.Measure.MeasureSpace", "real"),
    ("fep-015", "Measurability of Variational Objectives", "FEP", "MeasureTheory.MeasurableSpace.Basic", "real"),
    ("fep-016", "Laplace Approximation", "FEP", "Analysis.SpecialFunctions.Pow.Real", "real"),
    ("fep-017", "Conditional Expectation in Bayesian Updates", "InfoGeometry", "Algebra.BigOperators.Group.Finset", "real"),
    ("fep-018", "Statistical Manifold Geodesics", "InfoGeometry", "Topology.MetricSpace.Basic", "real"),
    ("fep-019", "Prior Predictive Density", "BayesianMechanics", "Algebra.BigOperators.Group.Finset", "real"),
    ("fep-020", "Langevin Sampling View", "ActiveInference", "Analysis.SpecialFunctions.Pow.Real", "real"),
    ("fep-021", "EFE Equivalence Forms", "ActiveInference", "Order.Basic", "real"),
    ("fep-022", "Posterior Predictive Checks", "BayesianMechanics", "MeasureTheory.Measure.MeasureSpace", "real"),
    ("fep-023", "Affordance: Reachable Distributions", "ActiveInference", "Data.Finset.Basic, Data.Set.Basic", "real"),
    ("fep-024", "KL Regularization in Objectives", "InfoGeometry", "Analysis.SpecialFunctions.Log.Basic", "real"),
    ("fep-025", "NESS Solenoidal Flow", "Thermodynamics", "LinearAlgebra.Matrix.Transpose", "real"),
    ("fep-026", "Complexity Penalty in FEP", "FEP", "Analysis.SpecialFunctions.Log.Basic", "real"),
    ("fep-027", "Hierarchical Generative Models", "BayesianMechanics", "MeasureTheory.Measure.Prod", "real"),
    ("fep-028", "Softmax Policy Selection", "ActiveInference", "Data.Finset.Basic, Analysis.SpecialFunctions.Exp", "real"),
    ("fep-029", "Bregman Divergences", "InfoGeometry", "Analysis.Convex.Basic", "real"),
    ("fep-030", "Maximum Entropy Principle", "Thermodynamics", "Analysis.SpecialFunctions.Log.Basic", "real"),
    ("fep-031", "Boltzmann–Gibbs Measure", "Thermodynamics", "Analysis.SpecialFunctions.Exp", "real"),
    ("fep-032", "Gradient Flows on Beliefs", "FEP", "Analysis.SpecialFunctions.Pow.Real", "real"),
    ("fep-033", "Planning Horizon in Active Inference", "ActiveInference", "Algebra.BigOperators.Group.Finset", "real"),
    ("fep-034", "Discrete Belief Update (Categorical)", "ActiveInference", "Algebra.BigOperators.Group.Finset", "real"),
    ("fep-035", "Jensen's Inequality for Log", "FEP", "Analysis.SpecialFunctions.Log.Basic", "real"),
    ("fep-036", "Empirical Bayes Coupling", "BayesianMechanics", "MeasureTheory.Measure.MeasureSpace", "real"),
    ("fep-037", "Fluctuation–Dissipation Link", "Thermodynamics", "Analysis.SpecialFunctions.Exp", "real"),
    ("fep-038", "Natural Gradient Step", "InfoGeometry", "Analysis.InnerProductSpace.Basic", "real"),
    ("fep-039", "Global vs Local Free Energy", "FEP", "Algebra.BigOperators.Group.Finset", "real"),
    ("fep-040", "Gaussian Entropy and Heat Capacity", "BayesianMechanics", "Analysis.SpecialFunctions.Log.Basic", "real"),
    ("fep-041", "Exploration Bonus from Information Gain", "ActiveInference", "Algebra.BigOperators.Group.Finset", "real"),
    ("fep-042", "Sufficient Statistics Factorization", "BayesianMechanics", "MeasureTheory.MeasurableSpace.Basic", "real"),
    ("fep-043", "Critical Points of Free Energy", "FEP", "Analysis.Calculus.Deriv.Basic", "real"),
    ("fep-044", "α-Divergence Family", "InfoGeometry", "Analysis.SpecialFunctions.Pow.Real", "real"),
    ("fep-045", "Conjugate Prior Update", "FEP", "Data.List.Basic", "real"),
    ("fep-046", "Stick-Breaking Priors", "BayesianMechanics", "Algebra.Order.Field.Basic", "real"),
    ("fep-047", "Active Inference Message Passing", "ActiveInference", "Algebra.BigOperators.Group.Finset", "real"),
    ("fep-048", "Sync vs Async Policy Updates", "FEP", "Order.Monotone.Basic", "real"),
    ("fep-049", "Entropy Production Rate", "Thermodynamics", "Algebra.Order.Ring.Lemmas", "real"),
    ("fep-050", "Landauer Bound and Information Thermodynamics", "Thermodynamics", "Analysis.SpecialFunctions.Log.Basic", "real"),
]


def _nl_for(meta: tuple[str, str, str, str, str]) -> str:
    tid, title, area, _, status = meta
    return (
        f"{title} ({area}). Catalogue row {tid}; maturity `{status}` in config/topics.yaml. "
        f"Natural-language anchor for OpenGauss / Hermes sessions and `lake env lean` checks.\n"
    )


def build_topics() -> dict[str, Any]:
    assert_complete()
    rows: list[dict[str, Any]] = []
    for meta in METADATA:
        tid, title, area, mathlib, status = meta
        sketch = SKETCHES[tid]
        rows.append(
            {
                "id": tid,
                "title": title,
                "area": area,
                "mathlib": mathlib,
                "mathlib_status": status,
                "nl": _nl_for(meta),
                "lean_sketch": sketch,
                "latex_equations": LATEX_EQUATIONS[tid],
            }
        )
    return {"topics": rows}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "config" / "topics.yaml"
    data = build_topics()
    header = (
        "# FEP / Active Inference / Bayesian Mechanics — 50-topic Lean4 catalogue\n"
        "# Each topic maps to one OpenGauss session when workflows are enabled.\n"
        "# Regenerate: uv run python scripts/_maint_build_topics_catalogue.py\n"
        "# Fields: id, title, area, mathlib, mathlib_status (real|partial|aspirational), nl, lean_sketch, latex_equations\n\n"
    )
    out.write_text(header + yaml.dump(data, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    print(f"Wrote {len(data['topics'])} topics to {out}")


if __name__ == "__main__":
    main()
