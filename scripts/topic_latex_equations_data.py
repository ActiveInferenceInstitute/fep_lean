# ruff: noqa: RUF001
"""Backward-compatible re-export of ``THEOREM_LATEX``.

The authoritative data are built in ``theorem_latex_signatures`` from
``catalogue_sketches.SKETCHES``; see that module and ``THEOREM_LATEX`` in
``catalogue_sketches`` for the display-math layout (``aligned`` blocks with
``variable`` context, binders, and goal). Import ``THEOREM_LATEX`` from
``catalogue_sketches`` in new code to avoid the extra indirection.
"""

from __future__ import annotations

from catalogue_sketches import THEOREM_LATEX

__all__ = ["THEOREM_LATEX"]
