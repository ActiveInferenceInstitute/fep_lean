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

TOOLCHAIN="$(tr -d '[:space:]' < "$LEAN_DIR/lean-toolchain")"
export ELAN_HOME="${ELAN_HOME:-$HOME/.elan}"

ELAN_EXE="${FEP_LEAN_ELAN_EXE:-}"
if [[ -z "$ELAN_EXE" ]]; then
  ELAN_EXE="$(command -v elan || true)"
fi
if [[ -z "$ELAN_EXE" && -x "$ELAN_HOME/bin/elan" ]]; then
  ELAN_EXE="$ELAN_HOME/bin/elan"
fi
if [[ -z "$ELAN_EXE" || ! -x "$ELAN_EXE" ]]; then
  echo "error: elan is unavailable; install elan or set FEP_LEAN_ELAN_EXE" >&2
  exit 1
fi

TOOLCHAIN_NAME="${TOOLCHAIN//\//--}"
TOOLCHAIN_NAME="${TOOLCHAIN_NAME//:/---}"
TOOLCHAIN_BIN="$ELAN_HOME/toolchains/$TOOLCHAIN_NAME/bin"

echo "[fep_lean bootstrap] Installing toolchain: $TOOLCHAIN"
if [[ ! -x "$TOOLCHAIN_BIN/lean" ]]; then
  "$ELAN_EXE" toolchain install "$TOOLCHAIN"
fi

if [[ ! -x "$TOOLCHAIN_BIN/lake" ]]; then
  echo "error: pinned Lake binary is missing at $TOOLCHAIN_BIN/lake" >&2
  exit 1
fi
LAKE_EXE="$TOOLCHAIN_BIN/lake"
export PATH="$TOOLCHAIN_BIN:$ELAN_HOME/bin:$PATH"

cd "$LEAN_DIR"
echo "[fep_lean bootstrap] lake update (refresh manifest)"
"$LAKE_EXE" update

echo "[fep_lean bootstrap] lake build cache (cache CLI on this toolchain)"
"$LAKE_EXE" build cache || echo "[fep_lean bootstrap] lake build cache target unavailable; continuing"

echo "[fep_lean bootstrap] lake exe cache get (Mathlib oleans; may take several minutes)"
"$LAKE_EXE" exe cache get

echo "[fep_lean bootstrap] lake build FepSketches"
"$LAKE_EXE" build FepSketches

MATHLIB_REV=""
if [[ -f "$LEAN_DIR/.lake/packages/mathlib/.git/HEAD" ]]; then
  MATHLIB_REV="$(git -C "$LEAN_DIR/.lake/packages/mathlib" rev-parse --short HEAD 2>/dev/null || true)"
fi
LEAN_VER="$("$LAKE_EXE" env lean --version 2>/dev/null | head -1 || echo unknown)"
echo "[fep_lean bootstrap] OK | lean: $LEAN_VER | mathlib: ${MATHLIB_REV:-n/a}"
