#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
V="${BOOK_VERSION:-$(cat VERSION)}"; export BOOK_VERSION="$V"
OUT="XWorkspace-Agent-Skills工程规范-开放方案-$V"
[ -x ./fetch-assets.sh ] && ./fetch-assets.sh
cp agent-skills-spec.md book.md
V="$V" ./build-core.sh
mkdir -p dist
mv -f "$OUT.pdf" dist/
rm -f "$OUT.md" book.md book.html
