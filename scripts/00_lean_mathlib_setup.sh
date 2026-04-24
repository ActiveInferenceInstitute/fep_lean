#!/usr/bin/env bash
# Thin wrapper — canonical bootstrap is _maint_bootstrap_lean_toolchain.sh (same directory).
# Kept so older paths and muscle memory for this filename still work.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/_maint_bootstrap_lean_toolchain.sh" "$@"
