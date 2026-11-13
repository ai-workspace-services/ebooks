import html as htmlmod
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

import diagrams

VERSION, OUT = sys.argv[1], sys.argv[2]
ROOT = Path('.').resolve()
BOOK_MD = ROOT / 'book.md'
HTML_PATH = ROOT / 'book.html'
PDF_PATH = ROOT / f'{OUT}.pdf'
INFO_PATH = ROOT / 'build-info.json'
INDEX_PATH = ROOT / 'index.md'


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
            in_app = ('附录' in part) or ('许可' in part)
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
body { font-family: 'Noto Serif CJK SC', serif; font-size: 10.5pt; line-height: 1.7; color: #222; }
h1 { font-family: 'Noto Sans CJK SC', sans-serif; color: #115e59; border-bottom: 2px solid #0f766e;
  padding-bottom: 4px; font-size: 15.5pt; page-break-after: avoid; break-after: avoid;
  word-break: keep-all; overflow-wrap: break-word; line-break: strict; }
h1.pre { page-break-after: avoid; }
h2 { font-family: 'Noto Sans CJK SC', sans-serif; color: #0f766e; font-size: 12pt;
  margin-top: 12px; page-break-after: avoid; break-after: avoid;
  word-break: keep-all; overflow-wrap: break-word; line-break: strict; }
table { border-collapse: collapse; width: 100%; font-size: 8.6pt; margin: 8px 0; table-layout: fixed; }
td, th { border: 1px solid #cbd5e1; padding: 3px 5px; vertical-align: top; overflow-wrap: break-word; word-break: break-word; }
th { background: #ccfbf1; text-align: left; font-family: 'Noto Sans CJK SC', sans-serif; color: #115e59; }
tr { page-break-inside: avoid; break-inside: avoid; }
table.idx { table-layout: fixed; font-size: 8pt; }
table.idx td:first-child { width: 34%; }
table.idx td:last-child { width: 42%; }
pre { background: #f1f5f9; padding: 8px 8px 8px 10px; font-size: 7.6pt; line-height: 1.45;
  white-space: pre-wrap; word-break: break-word; overflow-wrap: anywhere; border-radius: 4px;
  border-left: 3px solid #0f766e; page-break-inside: avoid; break-inside: avoid; }
code { font-size: 8.2pt; font-family: 'Noto Sans Mono CJK SC', ui-monospace, monospace; }
blockquote { border-left: 4px solid #0f766e; margin: 8px 0; padding: 4px 10px; background: #f0fdfa; }
.cover { height: 210mm; width: 148mm; display: flex; flex-direction: column; justify-content: center;
  text-align: center; background: linear-gradient(165deg, #042f2e 0%, #0f766e 55%, #115e59 100%);
  color: #fff; margin: 0; padding: 18mm 14mm; page-break-after: always; box-sizing: border-box; }
.cover .eyebrow { font-family: 'Noto Sans CJK SC', sans-serif; font-size: 10pt; letter-spacing: .18em;
  opacity: .82; }
.cover h1 { color: #fff; border: none; font-size: 22pt; line-height: 1.35; margin: 16px 0 10px; }
.cover .sub { font-family: 'Noto Sans CJK SC', sans-serif; font-size: 11.5pt; opacity: .92; }
.cover .stack { font-family: 'Noto Sans CJK SC', sans-serif; font-size: 9.5pt; opacity: .84; margin-top: 8mm; }
.cover .by { margin-top: 28mm; font-size: 10pt; line-height: 1.7; opacity: .95; }
.toc { page-break-after: always; }
.toc a { color: #115e59; text-decoration: none; }
.toc .t1, .toc .t2 { display: flex; align-items: baseline; gap: 4px; line-height: 1.38; }
.toc .t1 { font-weight: 700; margin-top: 2px; font-size: 10pt; color: #115e59; }
.toc .t2 { padding-left: 1.05em; font-size: 8.5pt; }
.toc .dots { flex: 1 1 auto; border-bottom: 1px dotted #94a3b8; margin: 0 6px 3px; min-width: 8px; }
.toc .pg { font-variant-numeric: tabular-nums; font-feature-settings: 'tnum';
  font-weight: 700; color: #0f766e; white-space: nowrap; min-width: 2.6em; text-align: right;
  font-family: 'Noto Sans CJK SC', sans-serif; }
.diagram { margin: 8px 0 12px; page-break-inside: avoid; break-inside: avoid; }
.diagram svg { width: 100%; height: auto; display: block; }
.diagram figcaption { font-family: 'Noto Sans CJK SC', sans-serif; font-size: 8.4pt;
  color: #334155; margin: 5px 2px 0; line-height: 1.45; }
"""


def cover_html(version):
    return (
        '<section class="cover" id="cover">'
        '<div class="eyebrow">DESIGN PATTERNS  ·  AI ERA</div>'
        '<h1>图解经典设计模式<br>遇到 AI 时代</h1>'
        '<div class="sub">先找变化点，再落回原语</div>'
        '<div class="stack">Linux 容器原生  ·  Next.js Portal  ·  Go / Gin  ·  PostgreSQL</div>'
        f'<div class="by">{version}  ·  2026-11-13<br>'
        'Haitao Pan<br>XWork Technologies LLC 服务支持<br>'
        '内容 CC BY-SA 4.0  ·  示例代码 MIT</div>'
        '</section>'
    )


def write_html(body, entries, pages, version):
    doc = (
        '<html><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>'
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
    # Short titles (e.g. 许可) also appear in body text — require an exact line.
    if len(compact_title) <= 4:
        return compact_line == compact_title
    # Table rows often start with the pattern name but continue with other cells.
    if s == title or s.startswith(title):
        if len(compact_line) > len(compact_title) + 8:
            return False
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
            if fl.startswith('序章') or fl.startswith('第') or fl.startswith('许可'):
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

    def search_title(title, start_page, end_page):
        # start_page / end_page are 1-based inclusive.
        lo = max(toc_end, start_page) - 1
        hi = min(n, end_page)
        for i in range(lo, hi):
            for ln in pages_text[i].splitlines():
                if heading_line_match(title, ln):
                    return i + 1
        return None

    # Locate h1 first, searching forward so earlier chapters do not steal later titles.
    cursor = toc_end + 1
    for e in entries:
        if e['level'] != 1:
            continue
        hit = search_title(e['title'], cursor, n)
        if hit:
            found[e['id']] = hit
            cursor = hit

    # h2 only within the parent chapter page range, so the overview table cannot match.
    parent_id = None
    for idx, e in enumerate(entries):
        if e['level'] == 1:
            parent_id = e['id']
            continue
        start_page = found.get(parent_id, toc_end + 1) if parent_id else (toc_end + 1)
        end_page = n
        for later in entries[idx + 1:]:
            if later['level'] == 1 and later['id'] in found:
                end_page = found[later['id']]  # inclusive: last h2 may share the next h1 page
                break
        if end_page < start_page:
            end_page = start_page
        hit = search_title(e['title'], start_page, end_page)
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


PATTERN_KEYS = (
    'Strategy', 'Adapter', 'Facade', 'Factory', 'Builder', 'Decorator',
    'Chain of Responsibility', 'Template Method', 'Command', 'State',
    'Observer', 'Composite', 'Proxy', 'Iterator', 'Repository',
    'Unit of Work', 'Transactional Outbox', 'Ports and Adapters',
)


def write_index(entries, pages, total, version):
    lines = [
        f'# 图解经典设计模式 · 遇到 AI 时代 · {version}',
        '',
        f'PDF 共 **{total}** 页（A5）。页码与目录、书签一致，来自本次构建的两遍渲染结果。',
        '',
        '## 章节',
        '',
        '| 章节 | 页码 |',
        '| --- | ---: |',
    ]
    for e in entries:
        if e['level'] != 1:
            continue
        p = pages.get(e['id'])
        lines.append(f"| {e['title']} | {p if p else '—'} |")
    lines += [
        '',
        '## 十八个模式速查',
        '',
        '| 模式 | 所在章节 | 页码 |',
        '| --- | --- | ---: |',
    ]
    parent = None
    for e in entries:
        if e['level'] == 1:
            parent = e['title']
            continue
        title = e['title']
        if any(title.startswith(k) or title == k for k in PATTERN_KEYS):
            p = pages.get(e['id'])
            lines.append(f"| {title} | {parent or ''} | {p if p else '—'} |")
    lines += [
        '',
        '## 图解',
        '',
        '本书六张图解由 `diagrams.py` 在构建时生成内联 SVG，不入库。',
        '',
        '1. AI 代码通胀对比（整整齐齐的屎山 vs 先找变化点再落原语）',
        '2. 十八个模式按四大变化点分类全景',
        '3. Portal → Gin → Adapter / Ports → PostgreSQL 分层边界',
        '4. Gin 鉴权责任链与订阅状态机（条件更新）',
        '5. 订阅原子写入与 Transactional Outbox + 幂等 Worker',
        '6. GitHub Actions 与 HCL / Playbook 组合边界',
        '',
        '许可：内容 CC BY-SA 4.0，署名 Haitao Pan / XWork Technologies LLC；构建脚本与示例代码 MIT。',
        '',
    ]
    INDEX_PATH.write_text('\n'.join(lines), encoding='utf-8')


def main():
    raw = BOOK_MD.read_text(encoding='utf-8')
    body = markdown.markdown(raw, extensions=['tables', 'fenced_code'])
    body = diagrams.inject(body)
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
    write_index(entries, pages, total, VERSION)
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