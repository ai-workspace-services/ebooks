#!/usr/bin/env bash
# One-command rebuild: ./build.sh   |  BOOK_VERSION=v0.2 ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
export BOOK_VERSION="${BOOK_VERSION:-$(cat VERSION)}"
mkdir -p dist preview
python3 build.py
PDF="dist/独立开发观察者计划-AI×可观测SaaS首季-${BOOK_VERSION}.pdf"
google-chrome --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PDF" "file://$PWD/dist/book.html" 2>/dev/null
pdfinfo "$PDF" | grep Pages
# guard: page 2 must contain the TOC (no blank page after cover)
pdftotext -f 2 -l 2 "$PDF" - | grep -q 目录 || { echo "ERROR: page 2 has no TOC"; exit 1; }
pdftoppm -png -r 80 -f 1 -l 1 -singlefile "$PDF" preview/cover
pdftoppm -png -r 80 -f 2 -l 2 -singlefile "$PDF" preview/toc
echo "built $PDF"
