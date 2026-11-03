#!/usr/bin/env bash
# Emit the book matrix as JSON to $GITHUB_OUTPUT.
# tag <slug>-v<ver> -> that book only (VERSION must match); tag v* or non-tag -> all books.
set -euo pipefail
ref="${GITHUB_REF_NAME:-}"; type="${GITHUB_REF_TYPE:-branch}"
all=$(cd books && ls -d */ | tr -d / )
sel="$all"
if [[ "$type" == tag && "$ref" != v* ]]; then
  slug="${ref%-v*}"; ver="${ref##*-v}"
  [[ -f "books/$slug/VERSION" ]] || { echo "::error::tag $ref: no book '$slug'"; exit 1; }
  have=$(tr -d '[:space:]' < "books/$slug/VERSION")
  [[ "$have" == "$ver" ]] || { echo "::error::tag $ref: books/$slug/VERSION is $have"; exit 1; }
  sel="$slug"
fi
json=$(printf '%s\n' $sel | python3 -c 'import sys,json;print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')
echo "books=$json" >> "$GITHUB_OUTPUT"; echo "matrix: $json"
