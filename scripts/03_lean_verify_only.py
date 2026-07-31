#!/usr/bin/env python3
"""Run the complete strict verification command for selected topics."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cli import main


if __name__ == "__main__":
    raise SystemExit(main(["verify", *sys.argv[1:]]))
