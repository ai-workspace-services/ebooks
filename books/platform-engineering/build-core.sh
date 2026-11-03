#!/usr/bin/env bash
# One-command rebuild: ./build.sh  (BOOK_VERSION=v0.2 ./build.sh for a new version)
set -euo pipefail
cd "$(dirname "$0")"
python3 src/quickstart.py
python3 src/build.py
V="${BOOK_VERSION:-v0.9.18}"; PDF="dist/图解平台工程-云中立实践-${V}.pdf"
mkdir -p preview
pdftoppm -png -r 110 -f 1 -l 1 -singlefile "$PDF" preview/cover
P=$(python3 -c "import json;print(json.load(open('dist/build-info.json'))['anchors']['ch5'])")
pdftoppm -png -r 110 -f "$P" -l "$P" -singlefile "$PDF" preview/sample-ch5-p1
echo "preview: preview/cover.png preview/sample-ch5-p1.png"
Q=$(python3 -c "import json;print(json.load(open(\"dist/build-info.json\"))[\"anchors\"][\"qs2\"])"); pdftoppm -png -r 110 -f "$Q" -l "$Q" -singlefile "$PDF" preview/quickstart-ch2; pdftoppm -png -r 110 -f $(python3 -c "import json;print(json.load(open(\"dist/build-info.json\"))[\"anchors\"][\"toc\"])") -l $(python3 -c "import json;print(json.load(open(\"dist/build-info.json\"))[\"anchors\"][\"toc\"])") -singlefile "$PDF" preview/toc
C=$(python3 -c "import json;print(json.load(open(\"dist/build-info.json\"))[\"anchors\"][\"ch6\"])"); pdftoppm -png -r 110 -f "$C" -l "$C" -singlefile "$PDF" preview/sample-ch6-p1
