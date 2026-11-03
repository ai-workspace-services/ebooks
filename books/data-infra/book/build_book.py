#!/usr/bin/env python3
"""Build 《数据基础设施 · AI 时代》合订本 PDF (v4: book-style chapters).
Rerunnable & idempotent; reads all inputs fresh each run, no hardcoded counts.
Usage: python3 build_book.py [--md CHAPTERS.md] [--topics XHS.md] [--img DIR] [--out DIR] [--name NAME] [--no-subheads-in-toc]
"""
import argparse, re, sys, glob, os, datetime, shutil
import pymupdf as fitz
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument('--md', default=os.path.join(BASE, 'book-chapters.md'), help='chapter source: "## NN 标题" per chapter, "### " subheads, optional "## 前言"')
ap.add_argument('--topics', default=os.path.join(BASE, 'xhs-copy-series.md'), help='optional: series topic labels ("系列 NN/12 · 主题") for image TOC entries')
ap.add_argument('--img', default=os.path.join(BASE, 'xhs'))
ap.add_argument('--out', default=HERE)
ap.add_argument('--name', default='趣谈数据基础设施-AI时代-合订本')
ap.add_argument('--version', default='v5')
ap.add_argument('--no-subheads-in-toc', action='store_true')
a = ap.parse_args()

# ---------------- configuration ----------------
TITLE = '《趣谈数据基础设施 · AI 时代》'
BYLINE1 = 'Haitao Pan | XWork Technologies LLC 服务支持'
BYLINE2 = 'xworktech.com 开源平台方案'
PROMO_SITE = 'xworktech.com'                       # clickable part
PROMO_URL = 'https://xworktech.com/'
PROMO = f'{PROMO_SITE} · XWork Technologies LLC 提供开源平台方案'
BYLINE = PROMO                                     # cover, back cover, metadata
OLD_BYLINES = ['Haitao Pan · XWork Technologies LLC 服务支持']  # replaced inside chapter text
BACK_COVER = True
PREFACE_TITLE = '前言'
W, H = 621, 828                                    # 3:4 points
MARGIN_X, BODY_SIZE, BODY_LEAD, PARA_GAP = 58, 11.5, 20.5, 7
SUB_SIZE, SUB_GAP_ABOVE, SUB_GAP_BELOW = 14, 16, 8
TOP_FIRST, TOP_CONT, BOTTOM = 135, 78, 52          # y from top
INDENT = 2                                         # first-line indent in em
NO_LINE_START = set('，。、；：？！）」』》”’…·%,.;:?!)]')
NO_LINE_END = set('（「『《“‘([')

FR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FB = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
if not os.path.exists(FB): FB = FR
if not os.path.exists(FR): sys.exit('Noto Sans CJK not found (apt install fonts-noto-cjk)')
FONT = {'R': fitz.Font(fontfile=FR), 'B': fitz.Font(fontfile=FB)}
today = datetime.date.today().isoformat()
def tw(s, f, size): return FONT[f].text_length(s, fontsize=size)

def clean(s):
    s = re.sub(r'(\d)\ufe0f?\u20e3', r'\1. ', s)          # keycap digits
    s = s.replace('\U0001F4CC', '▶ ')
    s = re.sub(r'[\U0001F000-\U0001FFFF\u2600-\u27BF\ufe0f]', '', s)
    for ob in OLD_BYLINES: s = s.replace(ob, BYLINE)
    return s

# ---------------- inputs ----------------
text = clean(open(a.md, encoding='utf-8').read())
chapters = []   # (num or None, title, body)
for m in re.finditer(r'^## (.+?)\n(.*?)(?=^## |\Z)', text, re.S | re.M):
    head, body = m.group(1).strip(), m.group(2).strip()
    mm = re.match(r'(\d+)\s+(.+)', head)
    chapters.append((mm.group(1), mm.group(2), body) if mm else (None, head, body))
if not any(c[0] for c in chapters): sys.exit(f'no "## NN 标题" chapters parsed from {a.md}')

topics = {}
if a.topics and os.path.exists(a.topics):
    for m in re.finditer(r'系列\s*(\d+)/\d+\s*·\s*(.+)', open(a.topics, encoding='utf-8').read()):
        topics[m.group(1)] = m.group(2).strip()

def images_for(num):
    if num is None: return []
    pat = 'data-infra-overview-*.jpg' if int(num) == 0 else f'series-{int(num):02d}-*.jpg'
    return sorted(glob.glob(os.path.join(a.img, pat)))
missing = [c[0] for c in chapters if c[0] and not images_for(c[0])]
for n in missing: print(f'WARNING: no images for chapter {n}', file=sys.stderr)

# ---------------- CJK typesetting ----------------
def wrap(s, fnt, size, maxw, indent=0.0):
    """greedy char wrap with simple kinsoku (no closing punct at line start / opening at line end)."""
    lines, cur, w0 = [], '', indent
    i = 0
    while i < len(s):
        ch = s[i]
        lim = maxw - (w0 if not lines else 0)
        if cur and tw(cur + ch, fnt, size) > lim:
            if ch in NO_LINE_START:                 # hang punctuation on current line
                cur += ch; i += 1
                if i < len(s) and s[i] in NO_LINE_START: continue
            elif cur[-1] in NO_LINE_END:
                ch0 = cur[-1]; cur = cur[:-1]; lines.append(cur); cur = ch0; continue
            lines.append(cur); cur = ''
            continue
        cur += ch; i += 1
    if cur: lines.append(cur)
    return lines or ['']

def layout(body):
    """-> pages: list of [ (kind, text, y_top, x) ], subs: [(subhead, page_index)]"""
    maxw = W - 2 * MARGIN_X
    blocks = []
    for raw in re.split(r'\n\s*\n', body):
        raw = raw.strip()
        if not raw: continue
        for part in raw.split('\n'):
            part = part.strip()
            if not part: continue
            if part.startswith('### '): blocks.append(('h', part[4:].strip()))
            elif part.startswith('#') and not part.startswith('##'): blocks.append(('tag', part))
            else: blocks.append(('p', part))
    pages, cur, y, subs = [], [], TOP_FIRST, []
    def newpage():
        nonlocal cur, y
        pages.append(cur); cur = []; y = TOP_CONT
    for bi, (k, t) in enumerate(blocks):
        if k == 'h':
            need = SUB_GAP_ABOVE + SUB_SIZE + SUB_GAP_BELOW + 3 * BODY_LEAD   # keep with next
            if cur and y + need > H - BOTTOM: newpage()
            if cur: y += SUB_GAP_ABOVE
            y += SUB_SIZE
            cur.append(('h', t, y, MARGIN_X)); subs.append((t, len(pages)))
            y += SUB_GAP_BELOW
            continue
        ind = INDENT * BODY_SIZE if k == 'p' and not re.match(r'^(\d+\.|▶|[-•])', t) else 0
        ls = wrap(t, 'R', BODY_SIZE, maxw, ind)
        for li, l in enumerate(ls):
            if y + BODY_LEAD > H - BOTTOM:
                # avoid a single orphan line at page bottom
                newpage()
            y += BODY_LEAD
            cur.append((k, l, y, MARGIN_X + (ind if li == 0 else 0)))
        y += PARA_GAP
    pages.append(cur)
    return pages, subs

# ---------------- plan ----------------
content, entries = [], []   # entries: (level, label, content_index, group)
for num, title, body in chapters:
    pages, subs = layout(body)
    imgs = images_for(num); topic = topics.get(num, '') if num else ''
    head = f'{num}  {title}' if num else title
    start = len(content)
    entries.append((1, head, start, 'pre' if num is None else 'main'))
    if not a.no_subheads_in_toc:
        for s, pi in subs: entries.append((2, s, start + pi, None))
    for i, p in enumerate(pages): content.append(('text', (num, title, p, i, len(pages))))
    for k, im in enumerate(imgs, 1):
        entries.append((2, f'图 {k}/{len(imgs)}' + (f' · {topic}' if topic else ''), len(content), 'img'))
        content.append(('img', (num, im)))

TOC_TOP, TOC_BOTTOM, TOC_LEAD, TOC_L1_GAP = 125, 50, 17.5, 6
def paginate_toc(entries):
    pages, cur, y = [], [], TOC_TOP
    for e in entries:
        add = TOC_LEAD + (TOC_L1_GAP if e[0] == 1 else 0)
        if cur and y + add > H - TOC_BOTTOM: pages.append(cur); cur, y = [], TOC_TOP
        y += add; cur.append((e, y))
    pages.append(cur); return pages
toc_pages = paginate_toc(entries)
front = 1 + len(toc_pages)
plan = [('cover', None)] + [('toc', (i, ch)) for i, ch in enumerate(toc_pages)] + content + [('license', None)] + ([('back', None)] if BACK_COVER else [])
pageno = lambda ci: front + ci + 1
n_imgs = sum(1 for k, _ in content if k == 'img')
n_ch = sum(1 for c in chapters if c[0])

# ---------------- render ----------------
os.makedirs(a.out, exist_ok=True)
doc = fitz.open(); total = len(plan); links = []
GRAY = lambda g: (g, g, g)
def put(pg, x, y, s, f='R', size=12, color=(0,0,0), align=0):
    """y measured from bottom (legacy) """
    if align: x = x - tw(s, f, size) * (0.5 if align == 1 else 1)
    pg.insert_text((x, H - y), s, fontname=f, fontfile=FR if f=='R' else FB, fontsize=size, color=color)
def puttop(pg, x, ytop, s, f='R', size=12, color=(0,0,0)):
    pg.insert_text((x, ytop), s, fontname=f, fontfile=FR if f=='R' else FB, fontsize=size, color=color)
def leaders(pg, x0, x1, ytop, size):
    dot = tw('. ', 'R', size*0.8); nd = int((x1 - x0 - 10) // dot)
    if nd > 0: pg.insert_text((x0 + 6, ytop), '. ' * nd, fontname='R', fontfile=FR, fontsize=size*0.8, color=GRAY(.7))
def promo(pg, y, size, color, n):
    x = W/2 - tw(PROMO, 'R', size)/2
    put(pg, x, y, PROMO, 'R', size, color)
    i = PROMO.find(PROMO_SITE)
    if i >= 0:
        x0 = x + tw(PROMO[:i], 'R', size); x1 = x0 + tw(PROMO_SITE, 'R', size)
        pg.draw_line((x0, H-y+2), (x1, H-y+2), color=color, width=0.5)
        links.append((n-1, {'kind': fitz.LINK_URI, 'uri': PROMO_URL, 'from': fitz.Rect(x0, H-y-size, x1, H-y+4)}))
ACCENT = (0.85, 0.2, 0.25)
# cover lines, taken from the book's own 前言 (book-chapters.md)
COVER_THEME = '老的没有退场，新的一层一层叠在一起'
COVER_PATH = '存储 → 采集 → 计算 → 仓湖与 BI → 治理 → AI 数据层'
COVER_VALUE = '文字负责讲故事，图负责查资料'
def _wc(t):
    t = '\n'.join(l for l in t.split('\n') if not l.strip().startswith('!['))
    return len(re.sub(r'\s', '', re.sub(r'[#*>`|_\-]', '', t)))
N_WORDS = sum(_wc(c[2]) for c in chapters)
import math; WAN = '%.1f' % (math.floor(N_WORDS/1000)/10)
for n, (kind, d) in enumerate(plan, 1):
    pg = doc.new_page(width=W, height=H)
    pg.insert_font(fontname='R', fontfile=FR)
    if kind != 'img': pg.insert_font(fontname='B', fontfile=FB)
    if kind == 'cover':
        # palette from https://www.xworktech.com/ (see report): bg --color-background, panel --color-primary-muted,
        # heading .hero-title, accent .hero-title-accent, primary --color-primary, muted --color-text-muted
        hx = lambda h: tuple(int(h[k:k+2], 16)/255 for k in (1, 3, 5))
        BG, PANEL, HEAD, ACC, PRI, MUT, TXT = hx('#f8f9fa'), hx('#e8f0fb'), hx('#101c44'), hx('#4b43e8'), hx('#0058bd'), hx('#667085'), hx('#1c1b1f')
        ML = 56; CWc = W - 2*ML
        pg.draw_rect(pg.rect, color=None, fill=BG)
        pg.draw_rect(fitz.Rect(0, H*0.62, W, H), color=None, fill=PANEL)
        cs = 44
        while cs > 22 and tw(TITLE, 'B', cs) > CWc: cs -= 1
        puttop(pg, ML, 190, TITLE, 'B', cs, HEAD)
        puttop(pg, ML, 232, '合订本', 'B', 24, ACC)
        puttop(pg, ML, 272, COVER_THEME, 'R', 17, PRI)
        g0, g1 = hx('#075ecc'), hx('#4338ca')   # site gradient from-[#075ecc] to-[#4338ca]
        for k in range(40):
            t = k/39; c = tuple(g0[q]*(1-t)+g1[q]*t for q in range(3))
            pg.draw_rect(fitz.Rect(ML+k*4, 293, ML+k*4+4.2, 296), color=None, fill=c)
        y = 336
        for ln in [COVER_PATH, f'{n_ch} 章', f'收录竖图 {n_imgs} 张 · 正文约 {WAN} 万字', COVER_VALUE]:
            puttop(pg, ML, y, ln, 'R', 12.5, TXT); y += 24
        y = H*0.62 + 40
        chs = [c for c in chapters if c[0]]
        for k, c in enumerate(chs):
            x = ML + (k % 2)*(CWc/2); yy = y + (k//2)*24
            puttop(pg, x, yy, f'第 {c[0]} 章　{c[1]}', 'R', 10, HEAD)
        # brand mark (no URL / no promo): header logo mark from www.xworktech.com (.xds-logo-mark) + wordmark
        _svg = fitz.open(os.path.join(HERE, 'xwork-logo-mark.svg')); _lp = fitz.open('pdf', _svg.convert_to_pdf())
        _wm = 'XWork Technologies'; _sz = 11; _ms = 16; _gx = 7
        _x0 = W/2 - (_ms + _gx + tw(_wm, 'B', _sz))/2; _yt = H - 76
        pg.show_pdf_page(fitz.Rect(_x0, _yt, _x0 + _ms, _yt + _ms), _lp, 0)
        puttop(pg, _x0 + _ms + _gx, _yt + 12.2, _wm, 'B', _sz, HEAD)
        put(pg, W/2, 40, f'版本 {a.version} · {today}', 'R', 9, MUT, 1)
    elif kind == 'toc':
        ti, chunk = d
        puttop(pg, MARGIN_X, 82, '目录' + (f'（续 {ti+1}/{len(toc_pages)}）' if ti else ''), 'B', 22)
        for (lvl, label, ci, grp), y in chunk:
            p = pageno(ci)
            if lvl == 1: f, size, x, col = 'B', 11.5, MARGIN_X, (0,0,0)
            elif grp == 'img': f, size, x, col = 'R', 9.5, MARGIN_X + 26, GRAY(.45)
            else: f, size, x, col = 'R', 10, MARGIN_X + 26, GRAY(.2)
            if lvl == 1: pg.draw_rect(fitz.Rect(MARGIN_X - 8, y - size + 1, MARGIN_X - 5, y + 1), color=None, fill=ACCENT)
            puttop(pg, x, y, label, f, size, col)
            ps = str(p); pw = tw(ps, f, size)
            leaders(pg, x + tw(label, f, size), W - MARGIN_X - pw, y, size)
            puttop(pg, W - MARGIN_X - pw, y, ps, f, size, col)
            links.append((n-1, {'kind': fitz.LINK_GOTO, 'page': p-1, 'from': fitz.Rect(x-2, y-size-2, W-MARGIN_X+2, y+4)}))
    elif kind == 'text':
        num, title, items, i, npg = d
        head = f'{num}  {title}' if num else title
        if i == 0:
            if num:
                puttop(pg, MARGIN_X, 62, f'第 {num} 章', 'R', 10, ACCENT)
            pg.draw_rect(fitz.Rect(MARGIN_X, 74, MARGIN_X + 4, 102), color=None, fill=ACCENT)
            puttop(pg, MARGIN_X + 13, 96, title, 'B', 20)
            pg.draw_line((MARGIN_X, 114), (W - MARGIN_X, 114), color=GRAY(.85), width=0.6)
        else:
            puttop(pg, MARGIN_X, 46, f'{head}（续 {i+1}/{npg}）', 'R', 8.5, GRAY(.55))
            pg.draw_line((MARGIN_X, 54), (W - MARGIN_X, 54), color=GRAY(.88), width=0.5)
        for k, t, y, x in items:
            if k == 'h':
                pg.draw_rect(fitz.Rect(MARGIN_X, y - SUB_SIZE + 2, MARGIN_X + 3, y + 1), color=None, fill=ACCENT)
                puttop(pg, MARGIN_X + 9, y, t, 'B', SUB_SIZE, (0.1, 0.12, 0.2))
            else:
                puttop(pg, x, y, t, 'R', BODY_SIZE, (0.2,0.4,0.7) if k == 'tag' else GRAY(.12))
    elif kind == 'img':
        pg.insert_image(pg.rect, filename=d[1])
    elif kind == 'back':
        pg.draw_rect(pg.rect, color=None, fill=(0.07, 0.1, 0.18))
        put(pg, W/2, H*0.55, TITLE + ' 合订本', 'B', 18, (1,1,1), 1)
        put(pg, W/2, H*0.55-34, '感谢阅读', 'R', 12, GRAY(.75), 1)
        put(pg, W/2, H*0.55-80, BYLINE1, 'R', 12, (1,1,1), 1)
        put(pg, W/2, H*0.55-100, BYLINE2, 'R', 10, GRAY(.75), 1)
    elif kind == 'license':
        puttop(pg, MARGIN_X, 96, '版权与许可', 'B', 22)
        y = 150
        for ln in [TITLE + f' 合订本 · {a.version}', '', '文字与插图：采用 CC BY-SA 4.0（署名-相同方式共享 4.0 国际）许可，', '转载、改编请注明作者与出处。', '',
                   '代码与脚本：采用 Apache License 2.0 许可。', '', '作者：Haitao Pan', '']:
            puttop(pg, MARGIN_X, y, ln, 'R', 12, GRAY(.15)); y += 24
        put(pg, W/2, 60, BYLINE1, 'R', 10, GRAY(.35), 1)
        put(pg, W/2, 44, BYLINE2, 'R', 9, GRAY(.5), 1)
    # page numbers
    if kind == 'img':   # top-right margin, clear of the image's own footer
        put(pg, W - 12, H - 14, f'{n} / {total}', 'R', 7, GRAY(.55), 2)
    elif kind in ('toc', 'text'):
        put(pg, W/2, 22, f'{n} / {total}', 'R', 8.5, GRAY(.5), 1)

# ---------------- bookmarks ----------------
outline = [[1, '卷首', 1], [2, '封面', 1], [2, '目录', 2]]
main_started = False
for lvl, label, ci, grp in entries:
    if grp == 'pre': outline.append([2, label, pageno(ci)]); continue
    if grp == 'main' and not main_started:
        outline.append([1, '正文', pageno(ci)]); main_started = True
    if not main_started:   # subheads under preface
        outline.append([3, label, pageno(ci)]); continue
    outline.append([lvl + 1, label.replace('  ', ' '), pageno(ci)])
outline.append([1, '版权与许可', total - (1 if BACK_COVER else 0)])
if BACK_COVER: outline.append([1, '封底', total])
for pi, l in links: doc[pi].insert_link(l)
doc.set_toc(outline)
doc.set_metadata({'title': TITLE + ' 合订本', 'author': BYLINE1})
tmp = os.path.join(a.out, f'.{a.name}.tmp.pdf')
doc.save(tmp, garbage=3, deflate=True, deflate_fonts=True); doc.close()
for f in [os.path.join(a.out, a.name + '.pdf'), os.path.join(a.out, f'{a.name}-{a.version}.pdf')]:
    shutil.copy(tmp, f)
os.remove(tmp)
tp = sum(1 for k, _ in content if k == 'text')
print(f'OK: {total} pages ({len(toc_pages)} TOC, {tp} text, {n_imgs} images), {n_ch} chapters'
      f'{" + 前言" if any(c[0] is None for c in chapters) else ""}, missing={missing or "none"}')
print(os.path.join(a.out, a.name + '.pdf'))
