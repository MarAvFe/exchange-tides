#!/usr/bin/env bash
# Copies the README screenshots taken by the self-test (tools/selftest.sh) into docs/screenshots.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${HOME}/.config/ExchangeTides"
mkdir -p "$ROOT/docs/screenshots"
for n in town market captains battle map; do
	cp "$SRC/shot_readme_$n.png" "$ROOT/docs/screenshots/$n.png"
done
echo "copied to docs/screenshots"
