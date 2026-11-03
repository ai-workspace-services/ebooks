#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
V="${BOOK_VERSION:-$(cat VERSION)}"; export BOOK_VERSION="$V"
[ -x ./fetch-assets.sh ] && ./fetch-assets.sh
python3 scripts/build.py --version "$V" --out "dist/图解IT简史-合集-$V.pdf"
