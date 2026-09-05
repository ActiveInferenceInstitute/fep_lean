"""The presentation join conserves the two canonical evidence sources."""

from __future__ import annotations

import shutil
from collections import Counter
from collections.abc import MutableMapping
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import cast

import pytest

from fep_lean.catalogue.coverage import build_formalism_coverage
from fep_lean.output.formalism_presentation import (
    build_formalism_presentation,
    humanize_formalism_identifier,
)
from fep_lean.verification.numerical_witnesses import (
    NON_PROOF_EVIDENCE,
    evaluate_numerical_witnesses,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_scientific_acronyms_survive_human_readable_labels() -> None:
    assert (
        humanize_formalism_identifier("closed-loop-policy-trees-and-efe")
        == "Closed Loop Policy Trees And EFE"
    )
    assert humanize_formalism_identifier("finite-kl-cmi") == "Finite KL CMI"


def test_presentation_join_conserves_canonical_sources_and_is_immutable() -> None:
    coverage = build_formalism_coverage(PROJECT_ROOT)
    evaluated = evaluate_numerical_witnesses(scope="catalogue")
    presentation = build_formalism_presentation(PROJECT_ROOT)

    assert tuple(topic.id for topic in presentation.topics) == tuple(
        row["id"] for row in coverage["topics"]
    )
    assert tuple(
        (relation.source, relation.kind, relation.target, relation.witness)
        for relation in presentation.relations
    ) == tuple(
        (row["source"], row["kind"], row["target"], row["witness"])
        for row in coverage["relations"]
    )
    assert presentation.witnesses == evaluated
    assert presentation.metrics == coverage["metrics"]
    assert len(presentation.topics) == 155
    assert len(presentation.areas) == 5
    assert len(presentation.families) == 20
    assert len(presentation.witnesses) == 15
    assert presentation.unmatched_witness_families == ()
    assert all(
        witness.evidence_kind == NON_PROOF_EVIDENCE
        for witness in presentation.witnesses
    )
    assert all(witness.accepted for witness in presentation.witnesses)

    review_date_field = "review_date"
    with pytest.raises(FrozenInstanceError):
        setattr(presentation, review_date_field, "mutable")
    mutable_metrics = cast(MutableMapping[str, int], presentation.metrics)
    with pytest.raises(TypeError):
        mutable_metrics["topics"] = 0


def test_renderers_depend_only_on_the_shared_presentation_join() -> None:
    output_root = PROJECT_ROOT / "src" / "fep_lean" / "output"
    for name in ("formalism_atlas.py", "formal_kernel_dashboard.py"):
        source = (output_root / name).read_text(encoding="utf-8")
        assert "build_formalism_coverage" not in source
        assert "evaluate_numerical_witnesses" not in source
        assert "build_formalism_presentation" in source


def test_family_summaries_conserve_witness_formal_alignment() -> None:
    presentation = build_formalism_presentation(PROJECT_ROOT)
    witnesses_by_family = {
        family.id: tuple(
            witness for witness in presentation.witnesses if witness.family == family.id
        )
        for family in presentation.families
    }

    for family in presentation.families:
        expected = Counter(
            witness.formal_alignment for witness in witnesses_by_family[family.id]
        )
        assert dict(family.formal_alignment_counts) == dict(sorted(expected.items()))

    learning_family = next(
        family
        for family in presentation.families
        if family.id == "learning-concentration-and-model-evidence"
    )
    assert dict(learning_family.formal_alignment_counts) == {"structural_analogue": 1}


def test_presentation_resolves_witnesses_against_the_supplied_checkout(
    tmp_path: Path,
) -> None:
    config = tmp_path / "config"
    config.mkdir()
    for name in (
        "catalogue_metadata.yaml",
        "theorem_maturity.yaml",
        "formalism_relations.yaml",
    ):
        shutil.copy2(PROJECT_ROOT / "config" / name, config / name)
    shutil.copytree(
        PROJECT_ROOT / "src" / "fep_lean" / "formal",
        tmp_path / "src" / "fep_lean" / "formal",
    )
    predictive = tmp_path / "src" / "fep_lean" / "formal" / "predictive_coding.lean"
    source = predictive.read_text(encoding="utf-8")
    source = source.replace(
        "theorem predictionError_update", "theorem predictionError_update_removed", 1
    )
    predictive.write_text(source, encoding="utf-8")

    with pytest.raises(
        ValueError,
        match=(
            "finite-jet-error-descent -> FEP.PredictiveCoding.predictionError_update"
        ),
    ):
        build_formalism_presentation(tmp_path)
