"""Canonical declaration inventory and manuscript reference audit."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from pathlib import Path

from fep_lean.lean_source import lean_code_without_comments

from .registry import BODIES

_DECLARATION_RE = re.compile(
    r"^\s*(?:noncomputable\s+)?(?:theorem|lemma|def|abbrev|structure|inductive)\s+"
    r"([A-Za-z][A-Za-z0-9_]*)",
    re.MULTILINE,
)
_REFERENCE_RE = re.compile(r"\bfep\d{3}_[A-Za-z0-9_]+\b")
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_EXCLUDED_MANUSCRIPT_FILES = frozenset(
    {
        "AGENTS.md",
        "README.md",
        "09z_unified_formalism_catalogue.md",
        "09z_appendix_b_lean_catalogue.md",
        "09zc_appendix_c_lean_equations.md",
    }
)


def declaration_names(bodies: Mapping[str, str] = BODIES) -> frozenset[str]:
    """Return every named declaration in the canonical topic bodies."""
    return frozenset(
        name
        for body in bodies.values()
        for name in _DECLARATION_RE.findall(lean_code_without_comments(body))
    )


def unresolved_manuscript_references(
    manuscript_dir: Path, *, additional_declarations: Iterable[str] = ()
) -> tuple[str, ...]:
    """Return locations whose ``fepNNN_*`` name is not in a canonical surface."""
    known = declaration_names() | frozenset(additional_declarations)
    failures: list[str] = []
    for path in sorted(Path(manuscript_dir).glob("*.md")):
        if path.name in _EXCLUDED_MANUSCRIPT_FILES:
            continue
        text = _FENCE_RE.sub("", path.read_text(encoding="utf-8"))
        for line_number, line in enumerate(text.splitlines(), 1):
            for reference in _REFERENCE_RE.findall(line):
                if reference not in known:
                    failures.append(f"{path.name}:{line_number}: {reference}")
    return tuple(failures)
