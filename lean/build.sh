#!/usr/bin/env bash
# Capped-parallelism build wrapper for the Lean/Mathlib FepSketches build.
# Prevents memory saturation: caps `lake build` at half the available cores,
# always warms the cache first, and runs at nice 10.
# Usage: ./build.sh [lake build args...]
set -u
CORES=$(sysctl -n hw.ncpu 2>/dev/null || nproc 2>/dev/null || echo 8)
BUILD_JOBS=$(( CORES / 2 ))
[ "$BUILD_JOBS" -lt 1 ] && BUILD_JOBS=1

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOGFILE="$SCRIPT_DIR/.lake/build.log"
mkdir -p "$(dirname "$LOGFILE")"

echo "=== build.sh $(date) ===" | tee -a "$LOGFILE"
echo "  cores=$CORES  build_jobs=$BUILD_JOBS  cwd=$PWD" | tee -a "$LOGFILE"

# Warm build cache (deterministic — pinned mathlib commit v4.33.1)
echo "  lake exe cache get..." | tee -a "$LOGFILE"
nice -n 10 lake exe cache get 2>&1 | tee -a "$LOGFILE"

# Build with capped parallelism at reduced priority
echo "  lake build -j$BUILD_JOBS $*" | tee -a "$LOGFILE"
nice -n 10 lake build -j "$BUILD_JOBS" "$@" 2>&1 | tee -a "$LOGFILE"
EXIT=$?

echo "  exit=$EXIT $(date)" | tee -a "$LOGFILE"
exit $EXIT
