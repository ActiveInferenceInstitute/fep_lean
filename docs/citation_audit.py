#!/usr/bin/env python3
"""Audit manuscript citation coverage, index parity, and corrected key records."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = PROJECT_ROOT / "manuscript"
_ENTRY_RE = re.compile(
    r"^@(?P<kind>[A-Za-z]+)\{(?P<key>[^,\s]+),(?P<body>.*?)(?=^@[A-Za-z]+\{|\Z)",
    re.MULTILINE | re.DOTALL,
)
_FIELD_RE = re.compile(
    r"^\s*(?P<name>[A-Za-z]+)\s*=\s*\{(?P<value>.*?)\}\s*,?\s*$",
    re.MULTILINE,
)
_CITATION_BLOCK_RE = re.compile(r"\[[^\]]*?@[^\]]+\]")
_CITATION_KEY_RE = re.compile(r"@([A-Za-z][A-Za-z0-9_:.+-]*)")
_INDEX_KEY_RE = re.compile(r"^    ([A-Za-z][A-Za-z0-9_:.+-]+)\s+—", re.MULTILINE)
_AUTHORING_EXCLUDES = frozenset(
    {
        "07_references.md",
        "09z_unified_formalism_catalogue.md",
        "AGENTS.md",
        "README.md",
    }
)


@dataclass(frozen=True)
class BibEntry:
    """Minimal parsed BibTeX record used by the project-local audit."""

    kind: str
    key: str
    fields: dict[str, str]


def parse_bibliography(path: Path) -> tuple[BibEntry, ...]:
    """Parse entry keys and braced fields without accepting duplicate keys."""
    text = Path(path).read_text(encoding="utf-8")
    entries: list[BibEntry] = []
    for match in _ENTRY_RE.finditer(text):
        fields = {
            field.group("name").lower(): " ".join(field.group("value").split())
            for field in _FIELD_RE.finditer(match.group("body"))
        }
        entries.append(
            BibEntry(
                kind=match.group("kind").lower(),
                key=match.group("key"),
                fields=fields,
            )
        )
    return tuple(entries)


def cited_keys(manuscript_dir: Path) -> set[str]:
    """Return Pandoc citation keys from authored manuscript chapters."""
    keys: set[str] = set()
    for path in sorted(Path(manuscript_dir).glob("*.md")):
        if path.name in _AUTHORING_EXCLUDES:
            continue
        text = path.read_text(encoding="utf-8")
        for block in _CITATION_BLOCK_RE.findall(text):
            keys.update(_CITATION_KEY_RE.findall(block))
    return keys


def audit_citations(project_root: Path = PROJECT_ROOT) -> tuple[str, ...]:
    """Return deterministic citation-contract violations."""
    root = Path(project_root)
    manuscript = root / "manuscript"
    entries = parse_bibliography(manuscript / "references.bib")
    errors: list[str] = []
    keys = [entry.key for entry in entries]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        errors.append("duplicate bibliography keys: " + ", ".join(duplicates))
    key_set = set(keys)
    citations = cited_keys(manuscript)
    undefined = sorted(citations - key_set)
    uncited = sorted(key_set - citations)
    if undefined:
        errors.append("undefined citation keys: " + ", ".join(undefined))
    if uncited:
        errors.append("uncited bibliography entries: " + ", ".join(uncited))

    index_text = (manuscript / "07_references.md").read_text(encoding="utf-8")
    index_keys = set(_INDEX_KEY_RE.findall(index_text))
    if missing := sorted(key_set - index_keys):
        errors.append(
            "bibliography keys missing from human index: " + ", ".join(missing)
        )
    if extra := sorted(index_keys - key_set):
        errors.append("human-index keys missing from bibliography: " + ", ".join(extra))

    by_key = {entry.key: entry for entry in entries}
    for banned in ("maheu2026reframing", "lean_slt2026"):
        if banned in by_key:
            errors.append(f"unverified or obsolete bibliography key remains: {banned}")
    expected = {
        "champion2026reframing": {
            "title": "Reframing the Expected Free Energy: Four Formulations and a Unification",
            "doi": "10.1162/NECO.a.1491",
        },
        "millidge2021whence": {
            "title": "Whence the Expected Free Energy?",
            "doi": "10.1162/neco_a_01354",
        },
    }
    for key, fields in expected.items():
        entry = by_key.get(key)
        if entry is None:
            errors.append(f"required verified bibliography key is missing: {key}")
            continue
        for field, value in fields.items():
            if entry.fields.get(field) != value:
                errors.append(
                    f"{key}: {field} must be {value!r}, found {entry.fields.get(field)!r}"
                )
    errors.extend(audit_citation_cff_version(root))
    return tuple(errors)


def audit_citation_cff_version(project_root: Path) -> tuple[str, ...]:
    """Fail when CITATION.cff version drifts from pyproject metadata."""
    try:
        import tomllib
    except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
        return ()

    metadata = tomllib.loads(
        (Path(project_root) / "pyproject.toml").read_text(encoding="utf-8")
    )
    package_version = str(metadata["project"]["version"])
    cff_text = (Path(project_root) / "CITATION.cff").read_text(encoding="utf-8")
    match = re.search(r'(?m)^version:\s*"?(?P<version>[^"\s]+)"?\s*$', cff_text)
    if match is None:
        return ("CITATION.cff does not declare a version",)
    if match.group("version") != package_version:
        message = (
            f"CITATION.cff version {match.group('version')!r} "
            f"!= pyproject version {package_version!r}"
        )
        return (message,)
    return ()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    args = parser.parse_args(argv)
    errors = audit_citations(args.root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    entries = parse_bibliography(args.root / "manuscript" / "references.bib")
    print(f"OK: {len(entries)} bibliography entries are defined, indexed, and cited")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
