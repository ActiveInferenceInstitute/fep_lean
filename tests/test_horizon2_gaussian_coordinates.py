"""H2.1b coordinate-qualified Gaussian score, Fisher, and Bregman contracts."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEAN_ROOT = PROJECT_ROOT / "lean"
FOUNDATION = (
    PROJECT_ROOT / "src" / "fep_lean" / "formal" / "gaussian_information_geometry.lean"
)
PROJECTION = LEAN_ROOT / "FepSketches" / "gaussian_information_geometry.lean"

pytestmark = pytest.mark.serial_lean

EXACT_IMPORTS = (
    "Mathlib.Analysis.Calculus.Deriv.Mul",
    "Mathlib.InformationTheory.KullbackLeibler.Basic",
    "Mathlib.Probability.Distributions.Gaussian.Real",
)
COORDINATE_DEFINITIONS = (
    "meanToNatural",
    "naturalToMean",
    "naturalLogPartition",
    "naturalScore",
    "meanScore",
    "naturalFisher",
    "meanFisher",
    "naturalBregman",
)
BASE_THEOREMS = (
    "law_eq_gaussianReal",
    "density_support",
    "law_eq_withDensity",
    "density_lintegral_eq_one",
    "law_univ",
    "law_rnDeriv_volume",
    "law_mutuallyAbsolutelyContinuous",
    "klDiv_law_eq_meanSquare",
    "klDiv_law_self",
    "klDiv_law_pos_of_ne",
    "zero_variance_excluded",
)
COORDINATE_THEOREMS = (
    "meanToNatural_naturalToMean",
    "naturalToMean_meanToNatural",
    "meanToNatural_hasDerivAt",
    "naturalLogPartition_hasDerivAt",
    "naturalLogPartitionGradient_hasDerivAt",
    "naturalLogDensityRatio_eq",
    "naturalScore_is_logDensityRatio_derivative",
    "meanLogDensityRatio_eq",
    "meanScore_is_logDensityRatio_derivative",
    "naturalScore_centered",
    "meanScore_centered",
    "law_variance_eq_fixed",
    "naturalFisher_eq_variance",
    "naturalFisher_eq_covariance",
    "meanFisher_eq_inv_variance",
    "meanFisher_eq_naturalFisher_pullback",
    "naturalBregman_eq_meanSquare",
    "klDiv_law_eq_naturalBregman",
    "naturalToMean_injective",
    "law_injective",
)


def _lake_executable() -> str:
    lake = shutil.which("lake")
    if lake is None:
        candidate = Path.home() / ".elan" / "bin" / "lake"
        if candidate.is_file():
            lake = str(candidate)
    if lake is None:
        raise RuntimeError("lake is required for H2.1b native acceptance")
    return lake


def _without_lean_comments(source: str) -> str:
    result: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline == -1 else newline
        else:
            result.append(source[index])
            index += 1
    return "".join(result)


def test_h2_1b_extends_the_single_owner_with_exact_imports() -> None:
    source = FOUNDATION.read_text(encoding="utf-8")
    uncommented = _without_lean_comments(source)

    assert tuple(re.findall(r"(?m)^import (\S+)$", source)) == EXACT_IMPORTS
    assert (
        tuple(
            name
            for name in re.findall(r"(?m)^noncomputable def (\w+)\b", uncommented)
            if name in COORDINATE_DEFINITIONS
        )
        == COORDINATE_DEFINITIONS
    )
    assert tuple(re.findall(r"(?m)^theorem (\w+)\b", uncommented)) == (
        *BASE_THEOREMS,
        *COORDINATE_THEOREMS,
    )
    assert PROJECTION.read_bytes() == FOUNDATION.read_bytes()


def test_h2_1b_coordinate_labels_and_scientific_boundaries_are_visible() -> None:
    source = _without_lean_comments(FOUNDATION.read_text(encoding="utf-8"))

    assert "family.naturalToMean natural" in source
    assert "family.meanToNatural mean" in source
    assert "family.naturalScore natural x" in source
    assert "family.meanScore mean x" in source
    assert "family.naturalFisher natural = (family.variance : ℝ)" in source
    assert "family.meanFisher mean = ((family.variance : ℝ)⁻¹)" in source
    assert "family.naturalFisher (family.meanToNatural mean)" in source
    assert "InformationTheory.klDiv" in source
    assert "family.naturalBregman sourceNatural referenceNatural" in source
    assert "gaussianPDFReal" in source
    assert "integral" in source
    covariance_theorems = re.findall(
        r"(?m)^theorem (\w*[Ff]isher\w*[Cc]ovariance\w*)\b", source
    )
    assert covariance_theorems == ["naturalFisher_eq_covariance"]
    for forbidden in (
        "multivariateGaussian",
        "FokkerPlanck",
        "StochasticIntegral",
        "RiemannianMetric",
    ):
        assert forbidden not in source


def test_h2_1b_exact_formula_diagnostics_are_nonproof_regressions() -> None:
    """Check readable exact values; native Lean theorems remain the evidence."""
    variance = Fraction(2)
    source_natural = Fraction(3, 2)
    reference_natural = Fraction(-1, 2)
    source_mean = variance * source_natural
    reference_mean = variance * reference_natural

    natural_fisher = variance
    mean_fisher = 1 / variance
    natural_bregman = variance * (source_natural - reference_natural) ** 2 / 2
    mean_square_kl = (source_mean - reference_mean) ** 2 / (2 * variance)

    assert natural_fisher == 2
    assert mean_fisher == Fraction(1, 2)
    assert natural_bregman == 4
    assert mean_square_kl == natural_bregman


def test_h2_1b_foundation_compiles_warning_free() -> None:
    with tempfile.TemporaryDirectory(prefix="fep-h2-1b-") as output_dir:
        output_path = Path(output_dir) / "gaussian_information_geometry.olean"
        result = subprocess.run(
            [
                _lake_executable(),
                "env",
                "lean",
                "-R",
                str(PROJECT_ROOT / "src" / "fep_lean" / "formal"),
                "-o",
                str(output_path),
                str(FOUNDATION),
            ],
            cwd=LEAN_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
        assert output_path.is_file(), result.stdout + result.stderr

    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert "warning:" not in output.lower()


def test_h2_1b_coordinate_theorems_use_only_standard_axioms(tmp_path: Path) -> None:
    probe = tmp_path / "GaussianCoordinateAxioms.lean"
    source = FOUNDATION.read_text(encoding="utf-8")
    prints = "\n".join(
        f"#print axioms FEP.GaussianInformationGeometry.FixedVarianceGaussian.{name}"
        for name in COORDINATE_THEOREMS
    )
    probe.write_text(f"{source}\n{prints}\n", encoding="utf-8")
    result = subprocess.run(
        [
            _lake_executable(),
            "env",
            "lean",
            "-R",
            str(PROJECT_ROOT / "src" / "fep_lean" / "formal"),
            str(probe),
        ],
        cwd=LEAN_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=300,
    )

    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert "sorryAx" not in output
    assert "warning:" not in output.lower()
    axiom_blocks = re.findall(r"depends on axioms: \[(.*?)\]", output, flags=re.DOTALL)
    assert len(axiom_blocks) == len(COORDINATE_THEOREMS), output
    for block in axiom_blocks:
        axioms = set(re.findall(r"'([^']+)'", block))
        assert axioms <= {"propext", "Classical.choice", "Quot.sound"}
