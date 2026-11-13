#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
V="${BOOK_VERSION:-$(cat VERSION)}"; export BOOK_VERSION="$V"
OUT="图解经典设计模式-遇到AI时代-$V"
cp design-patterns-ai.md book.md
V="$V" ./build-core.sh
mkdir -p dist
mv -f "$OUT.pdf" dist/
[ -f build-info.json ] && mv -f build-info.json dist/
rm -f "$OUT.md" book.md book.html
