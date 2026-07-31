#!/usr/bin/env python3
"""Verify one topic through the canonical command-line interface."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cli import main

if __name__ == "__main__":
    arguments = sys.argv[1:] or ["fep-008"]
    if arguments and not arguments[0].startswith("-"):
        arguments = ["topic", *arguments]
    else:
        arguments = ["topic", "fep-008", *arguments]
    raise SystemExit(main(arguments))
