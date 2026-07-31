#!/usr/bin/env python3
"""Audit toolchain and model pins across project markdown for drift.

Canonical sources of truth (read at every invocation, never the docs):

- ``lean/lean-toolchain``                     -> Lean toolchain string
                                                  (e.g. ``leanprover/lean4:v4.29.0``)
- ``lean/lakefile.lean``                      -> Mathlib4 git tag
                                                  (e.g. ``v4.29.0``)
- ``config/settings.yaml::hermes.model``      -> Hermes primary model
                                                  (e.g. ``moonshotai/kimi-k2.6``)
- ``config/settings.yaml::gauss.default_model`` -> sanity cross-check;
                                                    must equal ``hermes.model``.

The script then walks every ``*.md`` under ``projects/fep_lean/``
(excluding ``manuscript/`` which uses ``{{...}}`` placeholders rendered from
``manuscript_vars.yaml``, and ``docs/_generated/`` which is build output) and
flags any *literal* pin that does not match the canonical value.

Patterns checked
----------------

- ``leanprover/lean4:v\\d+\\.\\d+\\.\\d+``  (compared to canonical Lean toolchain)
- ``Lean ?4? v\\d+\\.\\d+\\.\\d+``          (informal mentions in prose)
- ``Mathlib ?4? v\\d+\\.\\d+\\.\\d+``       (compared to canonical Mathlib tag)
- ``moonshotai/kimi-k2\\.\\d+``             (compared to canonical primary model)

Fallback-chain entries other than the primary (``z-ai/glm-5.1``,
``moonshotai/kimi-k2-thinking``, ``qwen/qwen3-next-80b-a3b-instruct:free``,
etc.) are intentional narrative content and are NOT flagged. Sentinel codepaths
inside fenced code blocks are still inspected because pins matter just as much
in shell snippets as in prose.

Exit codes
----------

- ``0`` -- no drift.
- ``1`` -- at least one drifted pin (CI-friendly).

Usage
-----

.. code-block:: bash

    uv run python pin_audit.py            # default
    uv run python pin_audit.py --verbose  # also print every confirming sighting
    uv run python pin_audit.py --json     # machine-readable summary
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCS_DIR.parent

EXCLUDED_DIRS = (
    PROJECT_ROOT / "manuscript",
    PROJECT_ROOT / "docs" / "_generated",
)

# Path *fragments* (matched anywhere in the resolved path) to skip. Covers
# Lake's ``.lake/packages/`` tree which mirrors third-party RELEASE notes that
# legitimately mention older Lean toolchain pins, plus build/cache dirs that
# could be created by Python tooling.
EXCLUDED_PATH_FRAGMENTS = (
    "/.lake/",
    "/__pycache__/",
    "/.pytest_cache/",
    "/output/",
)

_RE_LEAN_TOOLCHAIN = re.compile(r"leanprover/lean4:v(\d+\.\d+\.\d+)")
_RE_LEAN_PROSE = re.compile(r"\bLean\s?4?\s+v(\d+\.\d+\.\d+)\b")
_RE_MATHLIB = re.compile(r"\bMathlib\s?4?\s+v(\d+\.\d+\.\d+)\b")
_RE_KIMI = re.compile(r"moonshotai/kimi-k2\.\d+")
_RE_LAKEFILE_MATHLIB = re.compile(r"mathlib4\.git\"\s*@\s*\"(v\d+\.\d+\.\d+)\"")


@dataclass
class CanonicalPins:
    lean_toolchain: str
    lean_version: str
    mathlib_tag: str
    primary_model: str
    sources: dict[str, str] = field(default_factory=dict)


@dataclass
class Drift:
    path: Path
    line: int
    found: str
    expected: str
    pin_kind: str

    def format(self, root: Path) -> str:
        rel = self.path.relative_to(root)
        return (
            f"{rel}:{self.line}: {self.pin_kind} drift -- "
            f"found {self.found!r}, expected {self.expected!r}"
        )


def _read_lean_toolchain(root: Path) -> str:
    pin = (root / "lean" / "lean-toolchain").read_text(encoding="utf-8").strip()
    if not _RE_LEAN_TOOLCHAIN.fullmatch(pin):
        raise SystemExit(f"lean/lean-toolchain has unexpected format: {pin!r}")
    return pin


def _read_mathlib_tag(root: Path) -> str:
    text = (root / "lean" / "lakefile.lean").read_text(encoding="utf-8")
    m = _RE_LAKEFILE_MATHLIB.search(text)
    if not m:
        raise SystemExit(
            'lean/lakefile.lean: could not find a `mathlib4.git "@" "vX.Y.Z"` pin'
        )
    return m.group(1)


def _read_settings(root: Path) -> tuple[str, str]:
    """Return ``(hermes.model, gauss.default_model)`` from ``config/settings.yaml``.

    We parse a tiny subset of YAML by hand to avoid pulling pyyaml as a runtime
    dep for what is otherwise a small audit script. The two keys we care about
    are top-level ``hermes:`` -> ``model:`` and ``gauss:`` -> ``default_model:``.
    """
    text = (root / "config" / "settings.yaml").read_text(encoding="utf-8")
    hermes_model = None
    gauss_model = None
    section = None
    for raw in text.splitlines():
        if raw.startswith(("hermes:", "gauss:")):
            section = raw.split(":", 1)[0]
            continue
        if not raw.startswith((" ", "\t")) and raw.strip() and not raw.startswith("#"):
            section = None
            continue
        line = raw.split("#", 1)[0].rstrip()
        m = re.match(r"\s+(\w+)\s*:\s*\"?([^\"]+?)\"?\s*$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2)
        if section == "hermes" and key == "model":
            hermes_model = value
        elif section == "gauss" and key == "default_model":
            gauss_model = value
    if hermes_model is None:
        raise SystemExit("config/settings.yaml: hermes.model not found")
    if gauss_model is None:
        raise SystemExit("config/settings.yaml: gauss.default_model not found")
    return hermes_model, gauss_model


def load_canonical(root: Path) -> CanonicalPins:
    lean_toolchain = _read_lean_toolchain(root)
    lean_version = _RE_LEAN_TOOLCHAIN.fullmatch(lean_toolchain).group(1)  # type: ignore[union-attr]
    mathlib_tag = _read_mathlib_tag(root)
    hermes_model, gauss_model = _read_settings(root)
    if hermes_model != gauss_model:
        raise SystemExit(
            "config/settings.yaml: hermes.model "
            f"({hermes_model!r}) != gauss.default_model ({gauss_model!r}); "
            "fix the source of truth before running the audit."
        )
    if lean_version != mathlib_tag.lstrip("v"):
        # Not strictly an error -- Mathlib can be pinned to a different tag than
        # the toolchain -- but worth surfacing so the human notices.
        print(
            f"note: Lean toolchain ({lean_version}) and Mathlib tag "
            f"({mathlib_tag}) differ; both will be enforced separately."
        )
    return CanonicalPins(
        lean_toolchain=lean_toolchain,
        lean_version=lean_version,
        mathlib_tag=mathlib_tag,
        primary_model=hermes_model,
        sources={
            "lean_toolchain": "lean/lean-toolchain",
            "mathlib_tag": "lean/lakefile.lean",
            "primary_model": "config/settings.yaml::hermes.model",
        },
    )


def _scan_file(path: Path, pins: CanonicalPins) -> list[Drift]:
    drifts: list[Drift] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [Drift(path, 0, str(exc), "", "io")]
    for i, line in enumerate(text.splitlines(), start=1):
        for m in _RE_LEAN_TOOLCHAIN.finditer(line):
            found = m.group(0)
            if found != pins.lean_toolchain:
                drifts.append(
                    Drift(path, i, found, pins.lean_toolchain, "lean_toolchain")
                )
        for m in _RE_LEAN_PROSE.finditer(line):
            found_version = m.group(1)
            if found_version != pins.lean_version:
                drifts.append(
                    Drift(
                        path,
                        i,
                        m.group(0),
                        f"Lean 4 v{pins.lean_version}",
                        "lean_prose",
                    )
                )
        for m in _RE_MATHLIB.finditer(line):
            found_version = "v" + m.group(1)
            if found_version != pins.mathlib_tag:
                drifts.append(
                    Drift(
                        path,
                        i,
                        m.group(0),
                        f"Mathlib4 {pins.mathlib_tag}",
                        "mathlib_tag",
                    )
                )
        for m in _RE_KIMI.finditer(line):
            found = m.group(0)
            if found != pins.primary_model:
                drifts.append(
                    Drift(path, i, found, pins.primary_model, "primary_model")
                )
    return drifts


def _gather_files(root: Path) -> list[Path]:
    excluded = tuple(p.resolve() for p in EXCLUDED_DIRS)
    files: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        rp = path.resolve()
        rp_str = str(rp)
        if any(rp_str.startswith(str(ex) + "/") or rp == ex for ex in excluded):
            continue
        if any(frag in rp_str for frag in EXCLUDED_PATH_FRAGMENTS):
            continue
        files.append(path)
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print every confirming pin sighting (not only drift).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a machine-readable JSON summary instead of human text.",
    )
    args = parser.parse_args(argv)

    pins = load_canonical(PROJECT_ROOT)
    files = _gather_files(PROJECT_ROOT)

    all_drifts: list[Drift] = []
    confirmed = 0
    for path in files:
        drifts = _scan_file(path, pins)
        if drifts:
            all_drifts.extend(drifts)
        if args.verbose:
            text = path.read_text(encoding="utf-8")
            for pattern in (_RE_LEAN_TOOLCHAIN, _RE_LEAN_PROSE, _RE_MATHLIB, _RE_KIMI):
                confirmed += sum(1 for _ in pattern.finditer(text))

    if args.json:
        out = {
            "canonical": {
                "lean_toolchain": pins.lean_toolchain,
                "lean_version": pins.lean_version,
                "mathlib_tag": pins.mathlib_tag,
                "primary_model": pins.primary_model,
                "sources": pins.sources,
            },
            "files_scanned": len(files),
            "drift_count": len(all_drifts),
            "drifts": [
                {
                    "path": str(d.path.relative_to(PROJECT_ROOT)),
                    "line": d.line,
                    "found": d.found,
                    "expected": d.expected,
                    "kind": d.pin_kind,
                }
                for d in all_drifts
            ],
        }
        json.dump(out, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1 if all_drifts else 0

    print("Canonical pins:")
    print(
        f"  lean_toolchain : {pins.lean_toolchain}  (from {pins.sources['lean_toolchain']})"
    )
    print(
        f"  mathlib_tag    : {pins.mathlib_tag}  (from {pins.sources['mathlib_tag']})"
    )
    print(
        f"  primary_model  : {pins.primary_model}  (from {pins.sources['primary_model']})"
    )
    print()

    if all_drifts:
        for d in all_drifts:
            print(d.format(PROJECT_ROOT))
        print()
        print(f"FAIL: {len(all_drifts)} drift(s) across {len(files)} file(s)")
        return 1

    if args.verbose:
        print(
            f"OK: {len(files)} file(s) scanned, {confirmed} pin sighting(s) — no drift."
        )
    else:
        print(f"OK: {len(files)} file(s) scanned — no drift.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
