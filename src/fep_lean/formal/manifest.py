"""Single explicit roster for maintained formal Lean resources."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath


class FormalModuleRole(str, Enum):
    """How a maintained Lean module participates in formal evidence."""

    FOUNDATION = "foundation"
    COMPOSITION = "composition"
    AGGREGATE = "aggregate"


@dataclass(frozen=True)
class FormalModule:
    """One packaged Lean resource and its workspace module address."""

    resource: str
    lean_module: str
    role: FormalModuleRole

    def __post_init__(self) -> None:
        resource = PurePosixPath(self.resource)
        if (
            not self.resource
            or "\\" in self.resource
            or resource.is_absolute()
            or resource.suffix != ".lean"
            or any(part in {"", ".", ".."} for part in resource.parts)
        ):
            raise ValueError(
                "formal resource must be a safe relative POSIX path ending in .lean: "
                f"{self.resource!r}"
            )
        expected_module = "FepSketches." + ".".join(resource.with_suffix("").parts)
        if self.lean_module != expected_module:
            raise ValueError(
                "formal Lean module must exactly match its resource path: "
                f"expected {expected_module!r}, got {self.lean_module!r}"
            )


FORMAL_MODULES: tuple[FormalModule, ...] = (
    FormalModule(
        resource="finite_probability.lean",
        lean_module="FepSketches.finite_probability",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="finite_information.lean",
        lean_module="FepSketches.finite_information",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="active_inference.lean",
        lean_module="FepSketches.active_inference",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="markov_blanket.lean",
        lean_module="FepSketches.markov_blanket",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="information_geometry.lean",
        lean_module="FepSketches.information_geometry",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="statistical_convergence.lean",
        lean_module="FepSketches.statistical_convergence",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="measure_bayes.lean",
        lean_module="FepSketches.measure_bayes",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="variational_duality.lean",
        lean_module="FepSketches.variational_duality",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="controlled_markov.lean",
        lean_module="FepSketches.controlled_markov",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="temporal_inference.lean",
        lean_module="FepSketches.temporal_inference",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="finite_markov_dynamics.lean",
        lean_module="FepSketches.finite_markov_dynamics",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="causal_dynamics.lean",
        lean_module="FepSketches.causal_dynamics",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="predictive_coding.lean",
        lean_module="FepSketches.predictive_coding",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="ness_flow.lean",
        lean_module="FepSketches.ness_flow",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="path_thermodynamics.lean",
    FormalModule(
        resource="path_thermodynamics.lean",
        lean_module="FepSketches.path_thermodynamics",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="geometric_optimization.lean",
        lean_module="FepSketches.geometric_optimization",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="collective_inference.lean",
        lean_module="FepSketches.collective_inference",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="learning_theory.lean",
        lean_module="FepSketches.learning_theory",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="empirical_risk.lean",
        lean_module="FepSketches.empirical_risk",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="policy_tree.lean",
        lean_module="FepSketches.policy_tree",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="native_blanket.lean",
        lean_module="FepSketches.native_blanket",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="exponential_family.lean",
        lean_module="FepSketches.exponential_family",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="continuous_time_markov.lean",
        lean_module="FepSketches.continuous_time_markov",
        role=FormalModuleRole.FOUNDATION,
    ),
    FormalModule(
        resource="compositions/core.lean",
        lean_module="FepSketches.compositions.core",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/measure_variational.lean",
        lean_module="FepSketches.compositions.measure_variational",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/control_temporal.lean",
        lean_module="FepSketches.compositions.control_temporal",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/causal_predictive.lean",
        lean_module="FepSketches.compositions.causal_predictive",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/thermo_geometry.lean",
        lean_module="FepSketches.compositions.thermo_geometry",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/collective_learning.lean",
        lean_module="FepSketches.compositions.collective_learning",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/risk_calibration.lean",
        lean_module="FepSketches.compositions.risk_calibration",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/policy_trees.lean",
        lean_module="FepSketches.compositions.policy_trees",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/native_blanket_transfer.lean",
        lean_module="FepSketches.compositions.native_blanket_transfer",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/exponential_family.lean",
        lean_module="FepSketches.compositions.exponential_family",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="compositions/continuous_time.lean",
        lean_module="FepSketches.compositions.continuous_time",
        role=FormalModuleRole.COMPOSITION,
    ),
    FormalModule(
        resource="composed.lean",
        lean_module="FepSketches.composed",
        role=FormalModuleRole.AGGREGATE,
    ),
)


def _selected(role: FormalModuleRole | None) -> tuple[FormalModule, ...]:
    modules = (
        FORMAL_MODULES
        if role is None
        else tuple(module for module in FORMAL_MODULES if module.role is role)
    )
    resources = tuple(module.resource for module in modules)
    lean_modules = tuple(module.lean_module for module in modules)
    if len(set(resources)) != len(resources):
        raise ValueError("formal resource manifest contains duplicate resources")
    if len(set(lean_modules)) != len(lean_modules):
        raise ValueError("formal resource manifest contains duplicate Lean modules")
    return modules


def formal_resource_paths(
    role: FormalModuleRole | None = None,
    *,
    project_root: Path | None = None,
) -> tuple[Path, ...]:
    """Return canonical resources from an explicit package or checkout origin.

    Omitting ``project_root`` discovers installed package data. Checkout-bound
    generation and audits pass it explicitly so a wheel cannot silently
    substitute its own formal bytes for the checkout being validated.
    """
    resource_dir = (
        Path(project_root) / "src" / "fep_lean" / "formal"
        if project_root is not None
        else Path(__file__).resolve().parent
    )
    return tuple(resource_dir / module.resource for module in _selected(role))


def formal_resource_relative_paths(
    role: FormalModuleRole | None = None,
) -> tuple[Path, ...]:
    """Return repository-relative canonical resource paths in manifest order."""
    base = Path("src") / "fep_lean" / "formal"
    return tuple(base / module.resource for module in _selected(role))


def formal_resource_manifest_drift(project_root: Path) -> tuple[Path, ...]:
    """Return missing manifested resources and unlisted canonical Lean files."""
    resource_dir = Path(project_root) / "src" / "fep_lean" / "formal"
    manifested = {resource_dir / module.resource for module in FORMAL_MODULES}
    present = set(resource_dir.rglob("*.lean")) if resource_dir.is_dir() else set()
    return tuple(sorted(manifested ^ present, key=lambda path: path.as_posix()))


def formal_module_imports(
    role: FormalModuleRole | None = None,
) -> tuple[str, ...]:
    """Return workspace Lean imports in manifest order."""
    return tuple(module.lean_module for module in _selected(role))
