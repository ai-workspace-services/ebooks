#!/usr/bin/env bash
# HTML → Chrome PDF (two-pass TOC page numbers) → optional pypdf bookmarks.
# Diagrams are injected as inline SVG by diagrams.py (no Drive binaries).
# CI (.github/workflows/build.yml) provides: fonts-noto-cjk, poppler-utils,
# google-chrome, and pip packages pypdf, pymupdf, markdown.
set -euo pipefail
cd "$(dirname "$0")"
V=${V:-v0.1}
OUT="图解经典设计模式-遇到AI时代-$V"
python3 build-core.py "$V" "$OUT"
