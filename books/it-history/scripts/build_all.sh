#!/bin/bash
# 一键：按 book.yml 的 title 生成 PDF、校验、书稿 md、XHS 文案、封面预览
set -e; cd "$(dirname "$0")/.."
FN=$(python3 -c "import yaml,re;b=yaml.safe_load(open('book.yml'));print(re.sub(r'[：:，,、]+','-',b['title'].replace(' ','')).strip('-')+('-'+b['edition_label'] if b.get('edition_label') else '')+'-'+b['version'])")
python3 scripts/v4_assemble.py >/dev/null
python3 scripts/build.py --out "dist/$FN.pdf" | tail -1
python3 scripts/check.py --pdf "dist/$FN.pdf" | tail -1
for d in chapters/*/; do grep -o '](images/[^)]*)' $d/chapter.md; done | sort | diff -q - /tmp/imgs-v4.2.txt && echo "images: SAME 402"
python3 scripts/make_bundle_xhs.py
python3 -c "import pymupdf as f,sys;d=f.open('dist/$FN.pdf');d[0].get_pixmap(dpi=90,alpha=False).save('../v4.6-preview.png');print(len(d),'pages |',d.metadata['title']);print(d[0].get_text()[:150]);print('HDR:',d[5].get_text()[:30].replace(chr(10),' '));print('BACK:',d[-1].get_text().replace(chr(10),' | '))"
