"""Packaged cross-topic Lean has one owner and deterministic projections."""

from __future__ import annotations

from pathlib import Path

import pytest

from fep_lean.formal import (
    FORMAL_MODULES,
    FormalModule,
    FormalModuleRole,
    formal_aggregate_drift,
    formal_projection_drift,
    formal_projection_pairs,
    formal_resource_manifest_drift,
    formal_resource_paths,
    render_formal_aggregate,
    write_formal_aggregate,
    write_formal_projections,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_formal_module_accepts_safe_nested_resources_with_exact_module_path() -> None:
    module = FormalModule(
        resource="compositions/measure_variational.lean",
        lean_module="FepSketches.compositions.measure_variational",
        role=FormalModuleRole.COMPOSITION,
    )

    assert module.resource == "compositions/measure_variational.lean"


@pytest.mark.parametrize(
    ("resource", "lean_module"),
    [
        ("../escape.lean", "FepSketches.escape"),
        ("/tmp/escape.lean", "FepSketches.escape"),
        ("compositions/family.lean", "FepSketches.wrong.family"),
    ],
)
def test_formal_module_rejects_unsafe_or_mismatched_resource_paths(
    resource: str, lean_module: str
) -> None:
    with pytest.raises(ValueError):
        FormalModule(
            resource=resource,
            lean_module=lean_module,
            role=FormalModuleRole.COMPOSITION,
        )


def test_formal_module_manifest_is_the_single_explicit_resource_roster() -> None:
    foundation_resources = (
        "finite_probability.lean",
        "finite_information.lean",
        "active_inference.lean",
        "markov_blanket.lean",
        "information_geometry.lean",
        "statistical_convergence.lean",
        "measure_bayes.lean",
        "variational_duality.lean",
        "controlled_markov.lean",
        "temporal_inference.lean",
        "finite_markov_dynamics.lean",
        "causal_dynamics.lean",
        "predictive_coding.lean",
        "path_thermodynamics.lean",
        "geometric_optimization.lean",
        "collective_inference.lean",
        "learning_theory.lean",
        "empirical_risk.lean",
        "policy_tree.lean",
        "native_blanket.lean",
        "exponential_family.lean",
        "continuous_time_markov.lean",
    )
    composition_resources = (
        "compositions/core.lean",
        "compositions/measure_variational.lean",
        "compositions/control_temporal.lean",
        "compositions/causal_predictive.lean",
        "compositions/thermo_geometry.lean",
        "compositions/collective_learning.lean",
        "compositions/risk_calibration.lean",
        "compositions/policy_trees.lean",
        "compositions/native_blanket_transfer.lean",
        "compositions/exponential_family.lean",
        "compositions/continuous_time.lean",
    )
    aggregate_resources = ("composed.lean",)
    resources = (
        *foundation_resources,
        *composition_resources,
        *aggregate_resources,
    )
    modules = tuple(
        "FepSketches." + resource.removesuffix(".lean").replace("/", ".")
        for resource in resources
    )
    assert tuple(module.resource for module in FORMAL_MODULES) == resources
    assert tuple(module.lean_module for module in FORMAL_MODULES) == modules
    expected_resources_by_role = {
        FormalModuleRole.FOUNDATION: foundation_resources,
        FormalModuleRole.COMPOSITION: composition_resources,
        FormalModuleRole.AGGREGATE: aggregate_resources,
    }
    assert {
        role: tuple(module.resource for module in FORMAL_MODULES if module.role is role)
        for role in FormalModuleRole
    } == expected_resources_by_role
    assert formal_resource_paths() == tuple(
        PROJECT_ROOT / "src" / "fep_lean" / "formal" / resource
        for resource in resources
    )
    assert formal_resource_paths(project_root=PROJECT_ROOT) == tuple(
        PROJECT_ROOT / "src" / "fep_lean" / "formal" / resource
        for resource in resources
    )


def test_checkout_resource_origin_is_explicit_and_not_site_package_derived(
    tmp_path: Path,
) -> None:
    assert formal_resource_paths(project_root=tmp_path) == tuple(
        tmp_path / "src" / "fep_lean" / "formal" / module.resource
        for module in FORMAL_MODULES
    )


def test_formal_resource_manifest_rejects_missing_and_unlisted_lean_files(
    tmp_path: Path,
) -> None:
    formal_root = tmp_path / "src" / "fep_lean" / "formal"
    for module in FORMAL_MODULES:
        path = formal_root / module.resource
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("/- manifested fixture -/\n", encoding="utf-8")

    rogue = formal_root / "unmanifested.lean"
    rogue.write_text("theorem escapedAudit : True := by trivial\n", encoding="utf-8")
    assert formal_resource_manifest_drift(tmp_path) == (rogue,)

    rogue.unlink()
    missing = formal_root / FORMAL_MODULES[0].resource
    missing.unlink()
    assert formal_resource_manifest_drift(tmp_path) == (missing,)


def test_core_composition_leaf_names_cross_topic_witnesses() -> None:
    source, projection = next(
        pair
        for module, pair in zip(
            FORMAL_MODULES,
            formal_projection_pairs(PROJECT_ROOT),
            strict=True,
        )
        if module.resource == "compositions/core.lean"
    )
    text = source.read_text(encoding="utf-8")
    assert "theorem fep002_vfe_compProd_chain_rule" in text
    assert "theorem fep031_zeroBeta_binary_maxEntropy" in text
    assert "theorem fep034_filter_is_fep017_posterior" in text
    assert "theorem fep027_priorPredictive_is_fep019" in text
    assert "theorem fep022_predictive_is_hierarchical_marginal" in text
    assert "theorem fep036_empiricalPosterior_closed" in text
    assert "theorem fep038_fisherRao_separation" in text
    assert "theorem fep041_informationGain_is_fep014_kl" in text
    assert "theorem fep025_current_dissipation_nonneg" in text
    assert "theorem fep037_autocorrelation_tracks_fep020" in text
    assert "theorem fep021_informationGain_balance" in text
    assert "theorem fep003_pragmaticCost_efe_balance" in text
    assert "theorem fep024_regularizer_is_fep014_kl" in text
    assert "zero inverse temperature" in text
    assert "zero temperature" not in text.lower()
    assert "sorry" not in text
    assert projection == (
        PROJECT_ROOT / "lean" / "FepSketches" / "compositions" / "core.lean"
    )


def test_formal_projection_writer_and_drift_are_byte_exact(tmp_path: Path) -> None:
    assert formal_projection_drift(tmp_path)
    for module in FORMAL_MODULES:
        canonical = tmp_path / "src" / "fep_lean" / "formal" / module.resource
        canonical.parent.mkdir(parents=True, exist_ok=True)
        canonical.write_bytes(
            (
                PROJECT_ROOT / "src" / "fep_lean" / "formal" / module.resource
            ).read_bytes()
        )
    written = write_formal_projections(tmp_path)
    assert written == tuple(
        tmp_path / "lean" / "FepSketches" / module.resource for module in FORMAL_MODULES
    )
    assert formal_projection_drift(tmp_path) == ()

    written[0].write_text("tampered\n", encoding="utf-8")
    assert formal_projection_drift(tmp_path) == (written[0],)


def test_public_composition_aggregate_is_manifest_generated(tmp_path: Path) -> None:
    aggregate = tmp_path / "src" / "fep_lean" / "formal" / "composed.lean"
    assert formal_aggregate_drift(tmp_path) == (aggregate,)
    assert write_formal_aggregate(tmp_path) == aggregate
    assert aggregate.read_text(encoding="utf-8") == render_formal_aggregate()
    assert "theorem " not in aggregate.read_text(encoding="utf-8")
    assert formal_aggregate_drift(tmp_path) == ()

    aggregate.write_text("import FepSketches.compositions.core\n", encoding="utf-8")
    assert formal_aggregate_drift(tmp_path) == (aggregate,)


def test_checkout_formal_projection_is_current() -> None:
    assert formal_aggregate_drift(PROJECT_ROOT) == ()
    assert formal_projection_drift(PROJECT_ROOT) == ()
