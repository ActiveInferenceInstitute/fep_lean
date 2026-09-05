"""Explicit bridge emission and read-only source/artifact verification."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from types import ModuleType
from typing import Any

from fep_lean.bridge.certificates import TOLERANCE, compare, render_markdown
from fep_lean.bridge.custody import (
    FRESH,
    binding_digest,
    contained_file,
    fingerprint,
    refresh_signature,
    valid_commit,
    validate_binding,
    write_json,
    write_text,
)

PIN = "specs/gnn-bridge-w2-source-custody/source-pin.json"
EMITTERS = {
    "finite": "specs/gnn-bridge-p1-finite-spike/projection.py",
    "continuous": "specs/gnn-bridge-p4b-continuous-emission/projection_continuous.py",
}
DOCUMENTS = {
    "finite": "specs/gnn-bridge-p1-finite-spike/gnn-input/FepLeanSymmetricBool.md",
    "continuous": "specs/gnn-bridge-p4b-continuous-emission/gnn-input/FepLeanContinuousOU.md",
}
CONTRACT = "docs/design/gnn-bridge/bridge-contract.md"
MIRROR = "doc/other/fep_lean/bridge-contract.md"
SYNTAX_PIN = "specs/gnn-bridge-w1-bridge-operations/syntax-pin.json"
SYNTAX_FILES = ("doc/gnn/gnn_syntax.md", "src/pipeline/step_registry.py")


def owner_roster(root: Path, repository: str) -> list[str]:
    """Discover relevant owners; validation also rejects additions/deletions."""
    patterns: tuple[str, ...]
    if repository == "fep_lean":
        fixed = [
            "pyproject.toml",
            "uv.lock",
            "lean/lean-toolchain",
            "lean/lakefile.lean",
            "lean/lake-manifest.json",
            CONTRACT,
            *EMITTERS.values(),
        ]
        patterns = ("src/fep_lean/**/*.py", "src/fep_lean/formal/**/*.lean")
    elif repository == "gnn":
        fixed = ["pyproject.toml", "uv.lock", "src/main.py", MIRROR, *SYNTAX_FILES]
        patterns = tuple(
            f"src/{folder}/**/*.py"
            for folder in ("gnn", "render", "execute", "pipeline", "utils", "ontology")
        )
    else:
        raise ValueError("unknown repository")
    return sorted(
        set(fixed)
        | {
            p.relative_to(root).as_posix()
            for pattern in patterns
            for p in root.glob(pattern)
        }
    )


def _head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result.stdout.strip()


def _read_object(path: Path) -> dict[str, Any]:
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise TypeError(f"JSON root must be an object: {path.name}")
    return result


def pin_sources(root: Path, gnn: Path) -> dict[str, Any]:
    """Explicitly seal current owner bytes. Does not bless any existing receipt."""
    pin: dict[str, Any] = {"schema_version": 1}
    for key, checkout in (("fep_lean", root), ("gnn", gnn)):
        pin[key] = {
            "commit": _head(checkout),
            "owners": fingerprint(checkout, owner_roster(checkout, key)),
        }
    write_json(root / PIN, pin)
    return pin


def check_sources(root: Path, gnn: Path, pin: dict[str, Any]) -> list[str]:
    errors = []
    if pin.get("schema_version") != 1:
        errors.append("unsupported source pin schema")
    for key, checkout in (("fep_lean", root), ("gnn", gnn)):
        entry = pin.get(key)
        if (
            not isinstance(entry, dict)
            or not valid_commit(entry.get("commit"))
            or not isinstance(entry.get("owners"), dict)
        ):
            errors.append(f"malformed {key} source binding")
            continue
        errors.extend(
            f"{key}: {error}"
            for error in validate_binding(
                checkout, entry["owners"], owner_roster(checkout, key)
            )
        )
    return errors


def _emitter(root: Path, model: str, expected_digest: str) -> ModuleType:
    path = contained_file(root, EMITTERS[model])
    source = path.read_bytes()
    if hashlib.sha256(source).hexdigest() != expected_digest:
        raise ValueError("emitter source changed after custody validation")
    # Execute exactly the verified source, never timestamp-valid cached bytecode.
    module = ModuleType(f"bridge_{model}_emitter")
    module.__file__ = str(path)
    exec(compile(source, str(path), "exec"), module.__dict__)  # noqa: S102 -- pinned local emitter source
    return module


def projected_document(root: Path, model: str, pin: dict[str, Any]) -> str:
    if model not in EMITTERS:
        raise ValueError("unknown bridge model")
    module = _emitter(root, model, pin["fep_lean"]["owners"][EMITTERS[model]])
    document = str(
        module.build_document(pin["fep_lean"]["commit"], pin["gnn"]["commit"])
    )
    return document + (
        f"source_owners_sha256: {binding_digest(pin['fep_lean']['owners'])}\n"
        f"pipeline_owners_sha256: {binding_digest(pin['gnn']['owners'])}\n"
    )


def emit(
    root: Path, gnn: Path, model: str, *, check: bool = False, refresh: bool = False
) -> bool:
    pin = _read_object(root / PIN)
    errors = check_sources(root, gnn, pin)
    if errors:
        raise ValueError("source pin is stale: " + "; ".join(errors))
    document = projected_document(root, model, pin)
    path = root / DOCUMENTS[model]
    if check:
        return path.is_file() and path.read_text(encoding="utf-8") == document
    if refresh:
        refresh_signature(path, document)
    else:
        write_text(path, document)
    return True


def _contract_body(text: str) -> str:
    return "\n".join(
        line
        for line in text.splitlines()
        if not line.startswith(("| Canonical copy |", "| Mirror copy |"))
    )


def status(root: Path, gnn: Path) -> dict[str, Any]:
    """Inspect both models and all owners. Never invoke an emitting subprocess."""
    checks: dict[str, dict[str, Any]] = {}
    try:
        pin = _read_object(root / PIN)
        errors = check_sources(root, gnn, pin)
        checks["source_binding"] = {"passed": not errors, "errors": errors}
        for model in DOCUMENTS:
            fresh = emit(root, gnn, model, check=True) if not errors else False
            checks[f"{model}_freshness"] = {
                "passed": fresh,
                "status": FRESH if fresh else "STALE",
            }
    except (ValueError, OSError, KeyError, TypeError) as exc:
        checks["source_binding"] = {"passed": False, "errors": [str(exc)]}
    try:
        syntax_pin = _read_object(root / SYNTAX_PIN)
        actual = fingerprint(gnn, SYNTAX_FILES)
        checks["syntax_surface"] = {
            "passed": all(actual[name] == syntax_pin.get(name) for name in SYNTAX_FILES)
        }
        checks["contract_mirror"] = {
            "passed": _contract_body((root / CONTRACT).read_text())
            == _contract_body((gnn / MIRROR).read_text())
        }
        from fep_lean.formal.manifest import FORMAL_MODULES

        drift = [
            m.resource
            for m in FORMAL_MODULES
            if (root / "src/fep_lean/formal" / m.resource).read_bytes()
            != (root / "lean/FepSketches" / m.resource).read_bytes()
        ]
        checks["formal_projection"] = {"passed": not drift, "drift": drift}
    except (ValueError, OSError, KeyError, TypeError) as exc:
        checks["contracts"] = {"passed": False, "errors": [str(exc)]}
    passed = all(check["passed"] for check in checks.values())
    return {
        "schema_version": 1,
        "status": "ok" if passed else "error",
        "checks": checks,
        "evidence_plane": "bridge source and artifact custody",
        "native_claim_ready": False,
    }


def certificate_receipt(
    root: Path, gnn: Path, results: Path, *, tolerance: float = TOLERANCE
) -> dict[str, Any]:
    """Evaluate one explicit result artifact; records agreement, never a proof."""
    pin = _read_object(root / PIN)
    errors = check_sources(root, gnn, pin)
    if errors:
        raise ValueError("stale source pin: " + "; ".join(errors))
    if not emit(root, gnn, "finite", check=True):
        raise ValueError("finite document is stale")
    relative = results.resolve().relative_to(root.resolve()).as_posix()
    artifacts = fingerprint(root, [relative, DOCUMENTS["finite"]])
    payload = _read_object(results)
    certificates, observations, ok = compare(payload, tolerance)
    if fingerprint(root, artifacts) != artifacts or check_sources(root, gnn, pin):
        raise ValueError("sources or artifacts changed during comparison")
    return {
        "schema_version": 1,
        "source_pin": pin,
        "artifacts": artifacts,
        "results_path": relative,
        "tolerance": tolerance,
        "policy_match": tolerance == TOLERANCE,
        "all_certificates_pass": ok,
        "certificates": certificates,
        "observations": observations,
        "evidence_plane": "numerical comparison of an identified artifact",
        "native_claim_ready": False,
        "execution_source_verified": False,
    }


def validate_certificate(root: Path, gnn: Path, receipt: dict[str, Any]) -> list[str]:
    """Recompute the whole comparison and binding; never trust a passed flag."""
    try:
        pin = _read_object(root / PIN)
        if receipt.get("source_pin") != pin:
            return ["certificate source pin mismatch"]
        results = root / receipt["results_path"]
        expected = certificate_receipt(
            root, gnn, results, tolerance=receipt["tolerance"]
        )
        if (
            expected != receipt
            or not expected["all_certificates_pass"]
            or not expected["policy_match"]
        ):
            return ["certificate content, numeric result, or tolerance policy mismatch"]
        return []
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [str(exc)]


def emit_certificate(path: Path, receipt: dict[str, Any]) -> None:
    write_json(path, receipt)
    write_text(
        path.with_suffix(".md"),
        render_markdown(
            receipt["certificates"],
            receipt["observations"],
            Path(receipt["results_path"]),
            receipt["all_certificates_pass"],
        ),
    )
