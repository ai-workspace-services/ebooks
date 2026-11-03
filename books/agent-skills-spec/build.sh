#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
V="${BOOK_VERSION:-$(cat VERSION)}"; export BOOK_VERSION="$V"
[ -x ./fetch-assets.sh ] && ./fetch-assets.sh
cp "XWorkspace-Agent-Skills工程规范-开放方案-v0.2.md" book.md; V="$V" ./build-core.sh; mkdir -p dist; rm -f XWorkspace-Agent-Skills工程规范-开放方案-"$V".md book.html; mv -f XWorkspace-Agent-Skills工程规范-开放方案-"$V".pdf dist/ 2>/dev/null || true
