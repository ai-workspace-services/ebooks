#!/usr/bin/env bash
# Assemble release assets from out/*.zip: optional ebooks-all-<tag>.zip (v* tags), SHA256SUMS, notes.
set -euo pipefail
shopt -s nullglob
cd out
zips=(*.zip)
[[ ${#zips[@]} -gt 0 ]] || { echo "::error::no zips built for $TAG (assets missing?)"; exit 1; }
if [[ "$TAG" == v* ]]; then
  all="ebooks-all-$TAG.zip"
  zip -0 -q "$all" "${zips[@]}"   # members are already deflated
  zips+=("$all")
fi
sha256sum "${zips[@]}" > SHA256SUMS
{
  echo "电子书 PDF 构建 · $TAG"
  echo
  echo "| 书 | 版本 | 资产 | 大小 |"
  echo "|---|---|---|---|"
  for z in *.zip; do
    [[ "$z" == ebooks-all-* ]] && continue
    for d in ../books/*/; do
      slug=$(basename "$d"); ver=$(tr -d '[:space:]' < "$d/VERSION")
      if [[ "$z" == "$slug-$ver.zip" ]]; then
        title=$(head -1 "$d/README.md" | sed 's/^# *//')
        echo "| $title | \`$ver\` | \`$z\` | $(numfmt --to=iec --suffix=B "$(stat -c %s "$z")") |"
      fi
    done
  done
  [[ -n "${all:-}" ]] && echo && echo "全部打包：\`$all\`（内含以上各书 zip）。"
  echo
  echo "校验：\`sha256sum -c SHA256SUMS\`"
  echo
  echo "内容许可：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) · 署名 Haitao Pan / XWork Technologies LLC；构建脚本 MIT。"
} > ../notes.md
cat ../notes.md >> "$GITHUB_STEP_SUMMARY"
gh release view "$TAG" -R "$GITHUB_REPOSITORY" >/dev/null 2>&1 \
  || gh release create "$TAG" -R "$GITHUB_REPOSITORY" --title "$TAG" --notes-file ../notes.md
gh release edit "$TAG" -R "$GITHUB_REPOSITORY" --notes-file ../notes.md
gh release upload "$TAG" "${zips[@]}" SHA256SUMS -R "$GITHUB_REPOSITORY" --clobber
