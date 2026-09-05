#!/usr/bin/env python3
"""Generate/check the Q7 static coefficient probe; never run Lean or a runner."""

from __future__ import annotations

import argparse
import hashlib
import sys
import uuid
from pathlib import Path
from types import ModuleType

SLICE = Path(__file__).resolve().parent
ROOT = SLICE.parents[1]
PREFIX = "specs/gnn-bridge-q7-continuous-ou-proof"
EXTRACTOR = "src/fep_lean/verification/gnn_continuous_artifact_proof.py"
GENERATOR = f"{PREFIX}/generate_probe.py"
EXPECTED = f"{PREFIX}/expected.json"
FIXTURES = {"ou": f"{PREFIX}/fixtures/continuous_ou_jax.py"}
PROBES = {"ou": f"{PREFIX}/generated/probe.lean"}
MANIFEST = f"{PREFIX}/generated/artifact_proof_manifest.json"
TEMPLATE = f"{PREFIX}/probe.template.lean"
PROVENANCE = f"{PREFIX}/render_provenance.json"
INPUT = f"{PREFIX}/fixtures/FepLeanContinuousOU.md"
TARGETS = ("FepSketches.compositions.smooth_reference_kernel",)
EXTRA_FILES = (EXPECTED, TEMPLATE, INPUT, f"{PREFIX}/refresh_render.py")


def _extractor(root: Path) -> ModuleType:
    path = root / EXTRACTOR
    verified = globals().get("_VERIFIED_ARTIFACT_DIGESTS")
    expected_digest = (
        verified[EXTRACTOR]
        if verified is not None
        else hashlib.sha256(path.read_bytes()).hexdigest()
    )
    source_bytes = path.read_bytes()
    if hashlib.sha256(source_bytes).hexdigest() != expected_digest:
        raise ValueError("Q7 extractor changed before its exact buffer was executed")
    module = ModuleType("_q7_checked_extractor_" + uuid.uuid4().hex)
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    try:
        exec(compile(source_bytes, str(path), "exec"), module.__dict__)  # noqa: S102 - execute exactly the digest-verified owned source buffer
    finally:
        sys.modules.pop(module.__name__, None)
    return module


def regenerate(root: Path = ROOT) -> tuple[dict[str, str], dict[str, object]]:
    """Pure artifact regeneration hook for the parent's source-verified loader.

    Parent custody must fingerprint and verify extractor/generator buffers before
    executing either module and recheck after regeneration. This hook emits no
    success verdict and performs no native or runner execution.
    """
    root = root.resolve()
    api = _extractor(root)
    expected_bytes = (root / EXPECTED).read_bytes()
    expected = api.read_json_object(expected_bytes)
    artifact_bytes = (root / FIXTURES["ou"]).read_bytes()
    artifact = api.extract_continuous_artifact(artifact_bytes.decode(), expected)
    input_bytes = (root / INPUT).read_bytes()
    api.validate_input_document(input_bytes.decode(), artifact)
    provenance = api.read_json_object((root / PROVENANCE).read_bytes())
    # Local integrity check only; parent must independently supply current owners.
    api.validate_render_provenance(
        provenance,
        input_bytes=input_bytes,
        artifact_bytes=artifact_bytes,
        owners=provenance.get("owners_before", {}),
    )
    probe = api.render_lean_probe(artifact, (root / TEMPLATE).read_text()).encode()
    files = [
        EXTRACTOR,
        GENERATOR,
        EXPECTED,
        TEMPLATE,
        PROVENANCE,
        INPUT,
        FIXTURES["ou"],
        f"{PREFIX}/refresh_render.py",
    ]
    manifest = {
        "schema_version": 1,
        "evidence_plane": "static artifact certificate inputs",
        "native_evidence": "required separately; not supplied by generation",
        "artifact": artifact.to_dict(),
        "expected_contract_sha256": api.digest(expected_bytes),
        "inputs": {path: api.digest((root / path).read_bytes()) for path in files},
        "outputs": {PROBES["ou"]: api.digest(probe)},
        "receipt_contract": {
            "input_variant": "continuous",
            "canonical_variant": "ou",
            "fixtures": FIXTURES,
            "probes": PROBES,
            "targets": list(TARGETS),
            "theorems": {"ou": [f"{api.NAMESPACE}.{name}" for name in api.THEOREMS]},
            "render_route": api.RENDER_ROUTE,
            "extractor": EXTRACTOR,
            "extra_files": list(EXTRA_FILES),
            "allowed_axioms": ["propext", "Classical.choice", "Quot.sound"],
            "scope": "static binary64 coefficient approximation and real-arithmetic prediction bounds",
        },
    }
    return {
        "generated/probe.lean": probe.decode(),
        "generated/artifact_proof_manifest.json": api.canonical_json(manifest),
    }, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs, _manifest = regenerate()
    if args.check:
        changed = [
            path
            for path, data in outputs.items()
            if not (SLICE / path).is_file() or (SLICE / path).read_text() != data
        ]
        if changed:
            raise ValueError(f"Q7 generated artifacts differ: {changed}")
        print(
            "Q7 generated artifacts current; native evidence must be checked separately."
        )
    else:
        for path, data in outputs.items():
            (SLICE / path).parent.mkdir(parents=True, exist_ok=True)
            (SLICE / path).write_text(data)
        print("Generated Q7 probe and manifest; no native compilation performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
