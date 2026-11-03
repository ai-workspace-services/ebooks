#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exec python3 ../../tools/fetch_assets.py assets.manifest.json
