#!/usr/bin/env bash
# Idempotent Lean/Mathlib bootstrap for fep_lean (run from repo root or this script's directory).
# Provenance footer: Lean version, Mathlib rev, FepSketches build OK.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEAN_DIR="${FEP_LEAN_DIR:-$SCRIPT_DIR/../lean}"
# projects/fep_lean/scripts -> ../../.. -> repository root
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if [[ ! -f "$LEAN_DIR/lean-toolchain" ]]; then
  echo "error: expected $LEAN_DIR/lean-toolchain" >&2
  exit 1
fi

TOOLCHAIN="$(cut -d: -f2 "$LEAN_DIR/lean-toolchain" | tr -d '[:space:]')"
export ELAN_HOME="${ELAN_HOME:-$HOME/.elan}"

echo "[fep_lean bootstrap] Installing toolchain: $TOOLCHAIN"
elan toolchain install "$TOOLCHAIN" || true

cd "$LEAN_DIR"
echo "[fep_lean bootstrap] lake update (refresh manifest)"
lake update

echo "[fep_lean bootstrap] lake build cache (cache CLI on this toolchain)"
lake build cache || true

echo "[fep_lean bootstrap] lake exe cache get (Mathlib oleans; may take several minutes)"
lake exe cache get

echo "[fep_lean bootstrap] lake build FepSketches"
lake build FepSketches

MATHLIB_REV=""
if [[ -f "$LEAN_DIR/.lake/packages/mathlib/.git/HEAD" ]]; then
  MATHLIB_REV="$(git -C "$LEAN_DIR/.lake/packages/mathlib" rev-parse --short HEAD 2>/dev/null || true)"
fi
LEAN_VER="$(lake env lean --version 2>/dev/null | head -1 || echo unknown)"
echo "[fep_lean bootstrap] OK | lean: $LEAN_VER | mathlib: ${MATHLIB_REV:-n/a}"
