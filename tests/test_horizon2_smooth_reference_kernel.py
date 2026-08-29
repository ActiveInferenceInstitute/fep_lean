"""H2.7 connected scalar and separate Fin4 terminal contracts."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

from tests._support.lean_runner import run_lean_probe

from fep_lean.formal.manifest import FORMAL_MODULES, FormalModuleRole


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEAN_ROOT = PROJECT_ROOT / "lean"
SOURCE = (
    PROJECT_ROOT
    / "src"
    / "fep_lean"
    / "formal"
    / "compositions"
    / "smooth_reference_kernel.lean"
)
PROJECTION = LEAN_ROOT / "FepSketches" / "compositions" / SOURCE.name
AGGREGATE = PROJECT_ROOT / "src" / "fep_lean" / "formal" / "composed.lean"
WORKSPACE_AGGREGATE = LEAN_ROOT / "FepSketches" / "composed.lean"
R0_RECEIPT = (
    PROJECT_ROOT
    / "specs"
    / "horizon-2-smooth-stochastic"
    / "readiness"
    / "repairs"
    / "07-gaussian-vfe-natural-gradient.json"
)

pytestmark = pytest.mark.serial_lean

NAMESPACE = "FEPComposed.SmoothReferenceKernel"
EXACT_IMPORTS = (
    "FepSketches.gaussian_information_geometry",
    "FepSketches.smooth_information_geometry",
    "FepSketches.posterior_convergence",
    "FepSketches.markov_semigroup",
    "FepSketches.scalar_gaussian_semigroup",
    "FepSketches.fin4_gaussian_semigroup",
    "FepSketches.gaussian_precision_conditioning",
    "FepSketches.compositions.gaussian_filter",
    "FepSketches.compositions.gaussian_control",
    "FepSketches.compositions.gaussian_grid_path",
)
PUBLIC_DEFINITIONS = (
    "selectedDynamics",
    "alternativeDynamics",
    "selectedPrior",
    "selectedFilter",
    "selectedControl",
    "selectedUnitGrid",
    "evidenceSurprisal",
    "gaussianVariationalFreeEnergy",
    "meanNaturalGradient",
    "naturalGradientFlow",
)
PUBLIC_THEOREMS = (
    "selectedDynamics_stationaryVariance",
    "selectedStationaryLaw_eq_learningObservationFalse",
    "selectedTransition_eq_gaussianLocation",
    "selectedObservationKernel_eq_learningObservationLaw",
    "selectedPredictionBelief_eq_prior",
    "selectedPosterior_mean",
    "selectedPosterior_variance",
    "evidenceLaw_eq_volume_withDensity",
    "evidenceDensity_ne_top",
    "gaussianVariationalFreeEnergy_eq_meanSquare_add_surprisal",
    "gaussianVariationalFreeEnergy_sub_surprisal_eq_nativeKL",
    "gaussianVariationalFreeEnergy_eq_surprisal_iff",
    "gaussianVariationalFreeEnergy_hasDerivAt",
    "meanNaturalGradient_eq_displacement",
    "meanNaturalGradient_metric_dual",
    "naturalGradientFlow_zero",
    "gaussianVariationalFreeEnergy_naturalGradientFlow_hasDerivAt",
    "gaussianVariationalFreeEnergy_naturalGradientFlow_deriv_neg",
    "continuousGaussianVFE_naturalGradient",
    "selectedControl_false_dynamics",
    "selectedControl_false_risk",
    "selectedControl_true_risk",
    "selectedControl_false_strictlyBetter",
    "selectedControl_selectedAction",
    "selectedControl_actionTransition_eq_selectedTransition",
    "selectedControl_actionTransitions_ne",
    "selectedUnitGrid_stepDuration",
    "selectedUnitGrid_stepKernel",
    "smoothReferenceKernel_terminal",
    "fin4ReferenceKernel_terminal",
)
PUBLIC_ENVIRONMENT = frozenset((*PUBLIC_DEFINITIONS, *PUBLIC_THEOREMS))
ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})


def _lake_executable() -> str:
    lake = shutil.which("lake")
    if lake is None:
        candidate = Path.home() / ".elan" / "bin" / "lake"
        if candidate.is_file():
            lake = str(candidate)
    if lake is None:
        raise RuntimeError("lake is required for H2.7 native validation")
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


def _run_lean(source_text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix="lean_probe_") as temp_dir:
        probe = Path(temp_dir) / "LeanProbe.lean"
        probe.write_text(source_text, encoding="utf-8")
        return run_lean_probe(
            probe,
            import_root=PROJECT_ROOT / "src" / "fep_lean" / "formal",
            cwd=LEAN_ROOT,
            timeout_s=300,
        )
def _parse_axioms(block: str) -> frozenset[str]:
    return frozenset(
        token.strip().strip("'")
        for token in block.replace("\n", " ").split(",")
        if token.strip().strip("'")
    )


def _axiom_reports(output: str) -> dict[str, frozenset[str]]:
    reports: dict[str, frozenset[str]] = {}
    for name in PUBLIC_THEOREMS:
        qualified = f"{NAMESPACE}.{name}"
        report = re.search(
            rf"'{re.escape(qualified)}' "
            r"(?:depends on axioms: \[(?P<axioms>.*?)\]"
            r"|does not depend on any axioms)",
            output,
            re.DOTALL,
        )
        assert report is not None, f"missing axiom report for {qualified}\n{output}"
        if report.group("axioms") is None:
            reports[name] = frozenset()
        else:
            parsed = _parse_axioms(report.group("axioms"))
            assert parsed, f"empty axiom report for {qualified}"
            reports[name] = parsed
    return reports


def _namespace_names(output: str) -> frozenset[str]:
    prefix = re.escape(f"{NAMESPACE}.")
    return frozenset(
        re.findall(rf"(?m)^{prefix}([A-Za-z_][A-Za-z0-9_']*)\b", output)
    )


def test_h2_7_owns_one_terminal_composition_leaf() -> None:
    assert SOURCE.is_file()
    source = SOURCE.read_text(encoding="utf-8")
    assert tuple(re.findall(r"(?m)^import (\S+)$", source)) == EXACT_IMPORTS
    assert f"namespace {NAMESPACE}\n" in source
    assert source.rstrip().endswith(f"end {NAMESPACE}")


def test_h2_7_public_surface_is_exact_and_has_no_stored_certificate() -> None:
    source = _without_lean_comments(SOURCE.read_text(encoding="utf-8"))
    definitions = tuple(
        re.findall(
            r"(?m)^(?:noncomputable )?def ([A-Za-z_][A-Za-z0-9_']*)\b", source
        )
    )
    theorems = tuple(
        re.findall(r"(?m)^theorem ([A-Za-z_][A-Za-z0-9_']*)\b", source)
    )
    assert definitions == PUBLIC_DEFINITIONS
    assert theorems == PUBLIC_THEOREMS
    assert not re.search(
        r"(?m)^(?:@\[[^\n]*\]\s*)*(?:private|protected|local)\s+"
        r"(?:noncomputable\s+)?(?:def|theorem|lemma|structure|class|abbrev|instance)\b",
        source,
    )
    assert not re.search(
        r"(?m)^(?:@\[[^\n]*\]\s*)*(?:structure|class|abbrev|lemma|instance)\b",
        source,
    )
    assert not re.search(
        r"\b(?:sorry|admit|axiom|opaque)\b|unsafe\s+(?:def|theorem)|:\s*True\b",
        source,
    )


def test_h2_7_scalar_carrier_bridges_are_source_visible_and_fail_closed() -> None:
    source = _without_lean_comments(SOURCE.read_text(encoding="utf-8"))
    assert "rate := 1" in source
    assert "diffusionVarianceRate := 2" in source
    assert "dynamics := selectedDynamics" in source
    assert "observationNoise := selectedGaussianFamily" in source
    assert "if action then alternativeDynamics else selectedDynamics" in source
    assert re.search(
        r"klDiv\s+\(\(posteriorFamily model prior\)\.law recognitionMean\)\s+"
        r"\(\(posteriorBelief model prior observation\)\.law\)",
        source,
    )
    assert "selectedObservationKernel_eq_learningObservationLaw" in source
    assert "selectedControl_actionTransition_eq_selectedTransition" in source
    assert "selectedUnitGrid_stepKernel" in source
    assert "posteriorProbability_consistent_ae" in source
    assert "posteriorDecisionRisk_tendsto_zero_ae" in source
    assert "ouKL_to_stationary_nonincrease" in source
    assert "endpointCondDistrib_ae_eq_product" in source
    assert "precisionZero_covarianceNonzero_condIndep" in source
    assert "perturbedEndpoint_external_not_indep_internal" in source
    assert "FEPProbe" not in source
    assert not re.search(
        r"\b(?:FiniteLaw|GenerativeModel|expectedFreeEnergy|reward|"
        r"HamiltonJacobi|FokkerPlanck|Girsanov|SDE|Ito)\b",
        source,
    )


def test_h2_7_compiles_warning_free() -> None:
    result = subprocess.run(
        [
            _lake_executable(),
            "env",
            "lean",
            "-R",
            str(PROJECT_ROOT / "src" / "fep_lean" / "formal"),
            str(SOURCE),
        ],
        cwd=LEAN_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=300,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert output == ""


def test_h2_7_environment_and_all_theorems_use_only_standard_axioms() -> None:
    suffix = "\n" + "\n".join(
        f"#print axioms {NAMESPACE}.{name}" for name in PUBLIC_THEOREMS
    )
    suffix += f"\n#print prefix {NAMESPACE}\n"
    result = _run_lean(SOURCE.read_text(encoding="utf-8") + suffix)
    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert "warning:" not in output
    assert "sorryAx" not in output
    reports = _axiom_reports(output)
    assert set(reports) == set(PUBLIC_THEOREMS)
    assert all(axioms <= ALLOWED_AXIOMS for axioms in reports.values())
    actual = _namespace_names(output)
    assert actual == PUBLIC_ENVIRONMENT, (
        f"missing={sorted(PUBLIC_ENVIRONMENT - actual)}; "
        f"extra={sorted(actual - PUBLIC_ENVIRONMENT)}"
    )


def test_h2_7_is_manifested_projected_and_aggregated_exactly_once() -> None:
    owners = [
        module
        for module in FORMAL_MODULES
        if module.resource == "compositions/smooth_reference_kernel.lean"
    ]
    assert len(owners) == 1
    owner = owners[0]
    assert owner.lean_module == "FepSketches.compositions.smooth_reference_kernel"
    assert owner.role is FormalModuleRole.COMPOSITION
    assert owner.declaration_namespace == NAMESPACE
    assert PROJECTION.read_bytes() == SOURCE.read_bytes()
    expected_import = "import FepSketches.compositions.smooth_reference_kernel"
    assert AGGREGATE.read_text(encoding="utf-8").splitlines().count(expected_import) == 1
    assert WORKSPACE_AGGREGATE.read_bytes() == AGGREGATE.read_bytes()


def test_h2_7_consumes_only_an_accepted_source_bound_r0_decision() -> None:
    receipt = json.loads(R0_RECEIPT.read_text(encoding="utf-8"))
    assert receipt["gate"] == "H2.7-R0"
    assert receipt["decision"] == "go"
    assert receipt["decision_scope"] == "open_H2.7_implementation_only"
    assert receipt["review"] == {
        **receipt["review"],
        "independent_lean_api": "approved_no_api_or_proof_blocker",
        "independent_information_geometry": "approved_no_scientific_blocker",
        "independent_skeptical_claim_scope": "approved_fail_closed_source_bound_contract",
    }
    assert receipt["downstream"]["opened"] == ["H2.7 maintained implementation"]
    assert receipt["downstream"]["remains_closed"] == [
        "H3.G0 pending accepted H2.7 terminal certificate",
        "all H3 implementation",
    ]
