#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
V="${BOOK_VERSION:-$(cat VERSION)}"; export BOOK_VERSION="$V"
[ -x ./fetch-assets.sh ] && ./fetch-assets.sh
python3 book/build_book.py --md book-chapters.md --version "$V" --img ./xhs --out dist
