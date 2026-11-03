#!/usr/bin/env bash
# Pick the versioned PDF, optionally shrink it with Ghostscript (kept only if >=10% smaller
# and the page count is unchanged), then zip -9 it to dist/<slug>-<version>.zip.
set -euo pipefail
slug="$1"; dir="books/$slug"; ver="$(tr -d '[:space:]' < "$dir/VERSION")"
pdf=""
for f in "$dir"/dist/*.pdf; do [[ "$f" == *"-$ver.pdf" ]] && { pdf="$f"; break; }; done
[[ -n "$pdf" ]] || pdf="$(ls -S "$dir"/dist/*.pdf | head -1)"
before=$(stat -c %s "$pdf"); pages=$(pdfinfo "$pdf" | awk '/^Pages/{print $2}')
note="kept original"
if command -v gs >/dev/null; then
  tmp="$(mktemp --suffix=.pdf)"
  if gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pdfwrite -dCompatibilityLevel=1.7 \
       -dPDFSETTINGS=/printer -dDetectDuplicateImages=true -dCompressFonts=true -dSubsetFonts=true \
       -dDownsampleColorImages=true -dColorImageResolution=200 -dColorImageDownsampleThreshold=1.5 \
       -dDownsampleGrayImages=true -dGrayImageResolution=200 -dGrayImageDownsampleThreshold=1.5 \
       -dPreserveAnnots=true -dPrinted=false -sOutputFile="$tmp" "$pdf" 2>/dev/null; then
    after=$(stat -c %s "$tmp"); p2=$(pdfinfo "$tmp" 2>/dev/null | awk '/^Pages/{print $2}')
    if [[ "$p2" == "$pages" && $((after * 100)) -le $((before * 90)) ]]; then
      mv "$tmp" "$pdf"; note="gs optimized"
    else
      note="gs result $after B not kept"; rm -f "$tmp"
    fi
  fi
fi
size=$(stat -c %s "$pdf")
zipf="$dir/dist/$slug-$ver.zip"; rm -f "$zipf"
zip -9 -j -q "$zipf" "$pdf"
z=$(stat -c %s "$zipf")
echo "| $slug | $(basename "$pdf") | $pages | $before | $size | $z | $note |" >> "$GITHUB_STEP_SUMMARY"
echo "zip=$zipf" >> "$GITHUB_OUTPUT"
echo "$slug: pdf $before -> $size ($note), zip $z"
