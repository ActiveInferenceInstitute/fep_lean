"""Shared path resolution for the fep_lean project.

Provides ``project_root()`` so that any subpackage can locate the
project directory without depending on the pipeline layer.
"""

from __future__ import annotations

import os
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent  # src/


def project_root() -> Path:
    """Return the project root directory.

    Resolves to the directory containing ``src/``, ``config/``, ``lean/``.
    If the ``PROJECT_DIR`` environment variable is set, that path is used
    instead — useful for testing with tmp_path fixtures.
    """
    if env_dir := os.environ.get("PROJECT_DIR"):
        return Path(env_dir).resolve()
    return _THIS_DIR.parent
