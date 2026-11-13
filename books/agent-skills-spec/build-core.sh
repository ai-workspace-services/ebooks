#!/usr/bin/env bash
# HTML → Chrome PDF (two-pass TOC page numbers) → optional pypdf bookmarks.
# CI (.github/workflows/build.yml) provides: fonts-noto-cjk, poppler-utils,
# google-chrome, and pip packages pypdf, pymupdf, markdown.
set -euo pipefail
cd "$(dirname "$0")"
V=${V:-v0.1}
OUT="XWorkspace-Agent-Skills工程规范-开放方案-$V"
python3 - "$V" "$OUT" <<'PY'
import html as htmlmod
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

VERSION, OUT = sys.argv[1], sys.argv[2]
ROOT = Path('.').resolve()
BOOK_MD = ROOT / 'book.md'
HTML_PATH = ROOT / 'book.html'
PDF_PATH = ROOT / f'{OUT}.pdf'
INFO_PATH = ROOT / 'build-info.json'


def slugify(text, used):
    text = htmlmod.unescape(re.sub(r'<[^>]+>', '', text))
    s = re.sub(r'[^\w\u4e00-\u9fff]+', '-', text, flags=re.UNICODE).strip('-').lower()
    s = s or 'section'
    base, n = s, 2
    while s in used:
        s = f'{base}-{n}'
        n += 1
    used.add(s)
    return s


def add_heading_ids(body):
    used = {'toc', 'cover'}
    entries = []

    def repl(m):
        level = int(m.group(1))
        inner = m.group(2)
        if level not in (1, 2):
            return m.group(0)
        title = htmlmod.unescape(re.sub(r'<[^>]+>', '', inner)).strip()
        hid = slugify(title, used)
        entries.append({'level': level, 'title': title, 'id': hid})
        return f'<h{level} id="{hid}">{inner}</h{level}>'

    body = re.sub(r'<h([1-6])>(.*?)</h\1>', repl, body, flags=re.S)
    return body, entries


def mark_appendix_tables(body):
    """Give appendix tables a tighter, fixed layout without changing chapter tables."""
    parts = re.split(r'(<h1\b[^>]*>.*?</h1>)', body, flags=re.S)
    out = []
    in_app = False
    for part in parts:
        if part.startswith('<h1'):
            in_app = '附录' in part
            out.append(part)
        else:
            if in_app:
                part = part.replace('<table>', '<table class="idx">')
            out.append(part)
    return ''.join(out)


def toc_html(entries, pages):
    rows = []
    for e in entries:
        page = pages.get(e['id'])
        # Fixed-width placeholder keeps two-pass layout stable (p.00 vs p.12).
        label = f'p.{page}' if page else 'p.00'
        rows.append(
            f'<div class="t{e["level"]}">'
            f'<a href="#{e["id"]}">{htmlmod.escape(e["title"])}</a>'
            f'<span class="dots" aria-hidden="true"></span>'
            f'<span class="pg">{label}</span>'
            f'</div>'
        )
    return (
        '<section class="toc" id="toc">'
        '<h1 class="pre">目录</h1>'
        + ''.join(rows)
        + '</section>'
    )


CSS = """
@page { size: A5; margin: 16mm 14mm; }
@page:first { margin: 0; }
.imgcover { height: 210mm; width: 148mm; display: flex; align-items: center;
  background: linear-gradient(#e2f6f0, #f8fafc); page-break-after: always; overflow: hidden; }
.imgcover img { width: 148mm; display: block; }
body { font-family: 'Noto Serif CJK SC', serif; font-size: 10.5pt; line-height: 1.7; color: #222; }
h1 { font-family: 'Noto Sans CJK SC', sans-serif; color: #1e3a8a; border-bottom: 2px solid #1e3a8a;
  padding-bottom: 4px; font-size: 16pt; page-break-after: avoid; break-after: avoid;
  word-break: keep-all; overflow-wrap: break-word; line-break: strict; }
h1.pre { page-break-after: avoid; }
h2 { font-family: 'Noto Sans CJK SC', sans-serif; color: #1e40af; font-size: 12pt;
  margin-top: 12px; page-break-after: avoid; break-after: avoid;
  word-break: keep-all; overflow-wrap: break-word; line-break: strict; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 8px 0; }
td, th { border: 1px solid #cbd5e1; padding: 3px 4px; vertical-align: top; overflow-wrap: break-word; }
th { background: #e0e7ff; text-align: left; }
tr { page-break-inside: avoid; break-inside: avoid; }
table.idx { table-layout: fixed; font-size: 8pt; }
table.idx td:first-child { width: 32%; }
table.idx td:last-child { width: 22%; }
pre { background: #f1f5f9; padding: 8px; font-size: 8pt; white-space: pre-wrap; border-radius: 4px; }
code { font-size: 8.5pt; }
blockquote { border-left: 4px solid #6366f1; margin: 8px 0; padding: 4px 10px; background: #eef2ff; }
.mermaid { background: #fff; text-align: center; }
.cover { height: 178mm; display: flex; flex-direction: column; justify-content: center; text-align: center;
  background: linear-gradient(160deg, #0f172a, #1e3a8a); color: #fff; margin: -16mm -14mm; padding: 20mm;
  page-break-after: always; }
.cover h1 { color: #fff; border: none; font-size: 22pt; }
.toc { page-break-after: always; }
.toc a { color: #1e3a8a; text-decoration: none; }
.toc .t1, .toc .t2 { display: flex; align-items: baseline; gap: 4px; line-height: 1.45; }
.toc .t1 { font-weight: 700; margin-top: 3px; font-size: 10.2pt; color: #1e3a8a; }
.toc .t2 { padding-left: 1.1em; font-size: 9pt; }
.toc .dots { flex: 1 1 auto; border-bottom: 1px dotted #94a3b8; margin: 0 6px 3px; min-width: 8px; }
.toc .pg { font-variant-numeric: tabular-nums; font-feature-settings: 'tnum';
  font-weight: 700; color: #1e40af; white-space: nowrap; min-width: 2.6em; text-align: right;
  font-family: 'Noto Sans CJK SC', sans-serif; }
"""


def cover_html(version):
    cv = (ROOT / 'assets' / 'cover.png').resolve()
    if cv.is_file():
        return f'<section class="imgcover" id="cover"><img src="file://{cv}"></section>'
    return (
        '<div class="cover" id="cover"><div style="font-size:11pt;opacity:.8">XWorkspace Core Skills</div>'
        '<h1>XWorkspace Agent Skills<br>工程规范 · 开放方案</h1>'
        '<div style="font-size:12pt">代码开源 · 文档开源 · 开放方案</div>'
        f'<div style="margin-top:30mm;font-size:10pt">{version} · 2026-11-13 · skills@07c6e772<br>'
        'Haitao Pan<br>XWork Technologies LLC 服务支持</div></div>'
    )


def write_html(body, entries, pages, version):
    doc = (
        '<html><head><meta charset="utf-8"><style>' + CSS + '</style>'
        '<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>'
        '<script>mermaid.initialize({startOnLoad:true})</script></head><body>'
        + cover_html(version) + toc_html(entries, pages) + body
        + '</body></html>'
    )
    HTML_PATH.write_text(doc, encoding='utf-8')


def chrome_print(pdf_path):
    cmd = [
        'google-chrome', '--headless', '--no-sandbox', '--disable-gpu',
        '--virtual-time-budget=8000', '--no-pdf-header-footer',
        f'--print-to-pdf={pdf_path}', str(HTML_PATH),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def pdftotext_pages(pdf_path):
    """Split pdftotext output on form feeds. CI and local both have poppler-utils."""
    proc = subprocess.run(
        ['pdftotext', '-layout', str(pdf_path), '-'],
        check=True, capture_output=True,
    )
    text = proc.stdout.decode('utf-8', errors='replace')
    parts = text.split('\f')
    if parts and not parts[-1].strip():
        parts = parts[:-1]
    return parts


def first_line(page_text):
    for ln in page_text.splitlines():
        s = ln.strip()
        if s:
            return s
    return ''


def normalize(s):
    return re.sub(r'\s+', '', s)


def heading_line_match(title, line):
    s = line.strip()
    if not s:
        return False
    compact_title = normalize(title)
    compact_line = normalize(s)
    # Short titles (e.g. 许可) also appear in the preface table — require an exact line.
    if len(compact_title) <= 4:
        return compact_line == compact_title
    if s == title or s.startswith(title):
        return True
    # Long titles may wrap: accept a first-line prefix of the heading.
    if len(compact_line) >= 10 and compact_title.startswith(compact_line) and len(compact_line) >= int(0.5 * len(compact_title)):
        return True
    return False


def locate_pages(entries, pdf_path):
    pages_text = pdftotext_pages(pdf_path)
    n = len(pages_text)
    toc_end = 1
    for i, t in enumerate(pages_text, start=1):
        fl = first_line(t)
        if i == 1:
            continue
        if '目录' in fl or fl.startswith('目录'):
            toc_end = i
            continue
        break
    if toc_end == 1 and n >= 2:
        toc_end = 2
        for i in range(3, n + 1):
            fl = first_line(pages_text[i - 1])
            if fl.startswith('序章'):
                break
            if '目录' in pages_text[i - 1] or sum(1 for e in entries if e['title'] in pages_text[i - 1]) >= 8:
                toc_end = i
            else:
                break

    found = {}
    # Prefer pymupdf named destinations when Chrome preserves HTML ids (not guaranteed).
    try:
        import pymupdf
        doc = pymupdf.open(pdf_path)
        names = {}
        try:
            names = doc.resolve_names() or {}
        except Exception:
            names = {}
        for e in entries:
            info = names.get(e['id'])
            if isinstance(info, dict) and 'page' in info:
                page = int(info['page']) + 1
                if page > toc_end:
                    found[e['id']] = page
        doc.close()
    except Exception:
        pass

    # Line-accurate search from the first body page onward (skip cover + TOC).
    start = toc_end
    for e in entries:
        hit = None
        for i in range(start, n):
            for ln in pages_text[i].splitlines():
                if heading_line_match(e['title'], ln):
                    hit = i + 1
                    break
            if hit:
                break
        if hit:
            found[e['id']] = hit

    return found, n, toc_end


def add_bookmarks(pdf_path, entries, pages, total):
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print('note: pypdf not installed; skipping PDF outline bookmarks', file=sys.stderr)
        return False
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)
    writer.add_outline_item('封面', 0)
    toc_page = max(1, min(total, 2)) - 1
    writer.add_outline_item('目录', toc_page)
    parent = None
    for e in entries:
        p = pages.get(e['id'])
        if not p:
            continue
        idx = max(0, min(total, p) - 1)
        title = e['title']
        if e['level'] == 1:
            parent = writer.add_outline_item(title, idx)
        else:
            writer.add_outline_item(title, idx, parent=parent)
    tmp = pdf_path.with_suffix('.bookmarked.pdf')
    with open(tmp, 'wb') as f:
        writer.write(f)
    tmp.replace(pdf_path)
    return True


def main():
    raw = BOOK_MD.read_text(encoding='utf-8')
    body = markdown.markdown(raw, extensions=['tables', 'fenced_code'])
    body = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        lambda m: '<pre class="mermaid">' + m.group(1) + '</pre>',
        body,
        flags=re.S,
    )
    body, entries = add_heading_ids(body)
    body = mark_appendix_tables(body)
    if not entries:
        sys.exit('no headings found in book.md')

    write_html(body, entries, pages={}, version=VERSION)
    chrome_print(PDF_PATH)
    pages, total, toc_end = locate_pages(entries, PDF_PATH)
    missing = [e['title'] for e in entries if e['id'] not in pages]
    if missing:
        print('warning: first pass missing page numbers for: ' + '; '.join(missing), file=sys.stderr)

    write_html(body, entries, pages=pages, version=VERSION)
    chrome_print(PDF_PATH)
    pages2, total2, toc_end2 = locate_pages(entries, PDF_PATH)
    if pages2 != pages or total2 != total:
        pages, total, toc_end = pages2, total2, toc_end2
        still = [e['title'] for e in entries if e['id'] not in pages]
        if still:
            print('warning: second pass missing page numbers for: ' + '; '.join(still), file=sys.stderr)
        write_html(body, entries, pages=pages, version=VERSION)
        chrome_print(PDF_PATH)
        pages, total, toc_end = locate_pages(entries, PDF_PATH)

    bookmarked = add_bookmarks(PDF_PATH, entries, pages, total)
    info = {
        'pages': total,
        'toc_end': toc_end,
        'bookmarked': bookmarked,
        'version': VERSION,
        'entries': [
            {'level': e['level'], 'title': e['title'], 'id': e['id'], 'page': pages.get(e['id'])}
            for e in entries
        ],
    }
    INFO_PATH.write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    shutil.copyfile(BOOK_MD, ROOT / f'{OUT}.md')
    print(PDF_PATH.name)


if __name__ == '__main__':
    main()
PY
