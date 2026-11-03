#!/usr/bin/env python3
"""一键重建《出海第一步 · 一人公司合规全流程》。
用法: python3 build.py [--version v1.1] [--checked 2026-10-21] [--png] [--no-verify]
流程: _build/content.py -> _build/render.py(HTML) -> headless Chrome PDF -> pypdf 书签 -> dist/
页数、P n/总页、目录页码、书签全部由 render.py 按 PLAN 自动重算。不改动原 collection.pdf / png/。"""
import argparse, pathlib, re, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '_build'))
ap = argparse.ArgumentParser()
ap.add_argument('--version', default=(ROOT / 'VERSION').read_text().strip())
ap.add_argument('--checked', help='核对日期，默认用 content.py 的 CHECKED')
ap.add_argument('--png', action='store_true', help='同时导出 XHS 逐页 PNG')
ap.add_argument('--no-verify', action='store_true')
a = ap.parse_args()
import render  # noqa
if a.checked: render.CHECKED = a.checked
DIST = ROOT / 'dist'; WORK = DIST / f'_work-{a.version}'
if WORK.exists(): shutil.rmtree(WORK)
WORK.mkdir(parents=True)
render.OUT = WORK; render.BUILD = WORK
render.build()  # 写 WORK/collection.html, collection.raw.pdf, collection.pdf, png/
pdf = DIST / f'出海第一步-一人公司合规全流程-{a.version}.pdf'
shutil.move(str(WORK / 'collection.pdf'), pdf)
if a.png:
    pd = DIST / f'png-{a.version}'
    if pd.exists(): shutil.rmtree(pd)
    shutil.move(str(WORK / 'png'), pd); print('PNG ->', pd)
else: shutil.rmtree(WORK / 'png', ignore_errors=True)
print('PDF ->', pdf)
if not a.no_verify:
    info = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True).stdout
    pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    assert pages == render.TOTAL, f'页数 {pages} != PLAN {render.TOTAL}'
    txt = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True, text=True).stdout
    bad = [p for p in re.findall(r'P(\d+)\s*/\s*(\d+)', txt) if p[1] != str(pages)]
    assert not bad, f'页脚总页数不一致: {bad[:5]}'
    # 敏感信息粗检：EIN 格式 / 邮箱
    leak = re.findall(r'\b\d{2}-\d{7}\b|[\w.+-]+@[\w-]+\.[\w.]+', txt)
    assert not leak, f'疑似敏感信息: {leak}'
    subprocess.run(['pdftoppm', '-png', '-r', '72', '-f', '1', '-l', '1', '-singlefile', str(pdf), str(DIST / f'preview-p1-{a.version}')], check=True)
    print(f'OK: {pages} 页，页脚 P n/{pages} 一致，无 EIN/邮箱格式文本，预览 dist/preview-p1-{a.version}.png')
