#!/usr/bin/env bash
# Build one book. Books whose Drive assets are unavailable are reported as skipped (outcome=skipped), never as a silent pass.
set -uo pipefail
slug="$1"; dir="books/$slug"
if [[ -f "$dir/assets.manifest.json" ]]; then
  ( cd "$dir" && ./fetch-assets.sh ); rc=$?
  if [[ $rc == 78 ]]; then
    msg="$slug: Drive assets unavailable (set secret GDRIVE_SA_JSON or share the Drive files). Build skipped."
    echo "::warning title=assets missing::$msg"; echo "### ⚠️ $msg" >> "$GITHUB_STEP_SUMMARY"
    echo "outcome=skipped" >> "$GITHUB_OUTPUT"; exit 0
  fi
  [[ $rc == 0 ]] || exit $rc
fi
"$dir/build.sh" || exit $?
n=$(ls "$dir"/dist/*.pdf 2>/dev/null | wc -l)
[[ $n -ge 1 ]] || { echo "::error::$slug: build produced no PDF in $dir/dist"; exit 1; }
for f in "$dir"/dist/*.pdf; do echo "- \`$(basename "$f")\` $(pdfinfo "$f" | awk '/^Pages/{print $2}') pages" >> "$GITHUB_STEP_SUMMARY"; done
echo "outcome=built" >> "$GITHUB_OUTPUT"
