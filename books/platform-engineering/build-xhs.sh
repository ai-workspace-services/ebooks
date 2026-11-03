#!/usr/bin/env bash
# Rebuild all XHS chapter packs: ./build-xhs.sh  -> xhs/chNN/, xhs/封面总览.png, xhs/文案汇总.md, dist/xhs-分章.zip
set -euo pipefail; cd "$(dirname "$0")"
python3 src/build_xhs.py
mkdir -p xhs/covers; for d in xhs/ch[0-9][0-9]; do cp "$d/01-首页.png" "xhs/covers/$(basename $d)-封面.png"; done
python3 -c "import shutil;shutil.make_archive('dist/xhs-分章','zip','xhs')"; echo "zip: dist/xhs-分章.zip"
