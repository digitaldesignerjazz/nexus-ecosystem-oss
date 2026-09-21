#!/usr/bin/env bash
# Local sovereign mesh control plane. No vendor login servers, no keys in logs.
# Usage: ./start_nexus_independent_mesh.sh status|prepare|up|down|pulse
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
export NEXUS_ROOT="${NEXUS_ROOT:-$HOME/nexus}"
PY="$DIR/independent_mesh.py"
mkdir -p "$NEXUS_ROOT/logs" "$NEXUS_ROOT/mesh" "$NEXUS_ROOT/config"
if [[ ! -f "$PY" ]]; then
  echo "independent_mesh.py missing beside this script"
  exit 2
fi
exec python3 "$PY" "$@"
