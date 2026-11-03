#!/usr/bin/env python3
"""《图解 IT 简史》PDF 生成器：book.yml + front/*.md + chapters/*/chapter.md + images -> dist/*.pdf
用法：python3 scripts/build.py [--chapters 03,05] [--dpi 180] [--quality 85] [--version v3] [--out 路径] [--placeholder-images]
--placeholder-images（或环境变量 BOOK_PLACEHOLDER_IMAGES=1）：缺图时用灰色占位页，供 CI 在无图仓库里做冒烟构建；默认缺图直接报错。
"""
import os, re, sys, argparse, hashlib
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image
import pymupdf as fitz
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, read_md, load_book, load_chapter, placeholder_mode
import fonts as F
Image.MAX_IMAGE_PIXELS = None
W, H = 595.28, 841.89; ML = MR = 56; MT = 60; MB = 56; CW = W - ML - MR
IMGH = H - MT - MB - 34
NAVY = (0.05, 0.2, 0.45); TXT = (0.12, 0.12, 0.12)
CACHE = os.path.join(ROOT, 'dist', '.cache'); os.makedirs(os.path.join(CACHE, 'jpg'), exist_ok=True)

def placeholder(rel):
    """缺图占位：浅灰 1600×1000 PNG（含 ASCII 文件名哈希），缓存在 dist/.cache/placeholder/"""
    d = os.path.join(CACHE, 'placeholder'); os.makedirs(d, exist_ok=True)
    out = os.path.join(d, hashlib.md5(rel.encode()).hexdigest()[:16] + '.png')
    if not os.path.exists(out):
        from PIL import ImageDraw
        im = Image.new('RGB', (1600, 1000), (222, 222, 222)); dr = ImageDraw.Draw(im)
        dr.rectangle((20, 20, 1579, 979), outline=(160, 160, 160), width=6)
        dr.line((20, 20, 1579, 979), fill=(190, 190, 190), width=4); dr.line((20, 979, 1579, 20), fill=(190, 190, 190), width=4)
        dr.text((60, 60), 'PLACEHOLDER  missing image  ' + os.path.basename(out)[:16], fill=(90, 90, 90))
        im.save(out)
    return out

# ---------------- text utils ----------------
def clean(s):
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s); return s.replace('**', '').replace('`', '').strip()
NO_START = set('，。、；：？！）」』》”’…·%,.;:?!)]')
NO_END = set('（「『《“‘([')
def wrap(t, font, size, width, first=0.0):
    """CJK 换行：避头尾（标点不出现在行首、开括号不留行尾）；first 为首行缩进（pt）"""
    out = []
    for para in t.split('\n'):
        line = ''; w = width - first
        for c in para:
            if font.text_length(line + c, size) > w and line:
                if c in NO_START: line += c; out.append(line); line = ''; w = width; continue
                if line[-1] in NO_END: out.append(line[:-1]); line = line[-1]; w = width
                else: out.append(line); line = ''; w = width
            line += c
        out.append(line)
    return out
def md_blocks(md):
    bl = []
    for raw in md.split('\n'):
        l = raw.rstrip()
        if not l.strip(): bl.append(('gap',)); continue
        if l.lstrip().startswith('|') and set(l.replace('|', '').replace('-', '').replace(':', '').strip()) == set(): continue
        if l.startswith('#'):
            bl.append(('h', clean(l.lstrip('#').strip()), len(l) - len(l.lstrip('#')))); continue
        if l.lstrip().startswith('|'):
            bl.append(('p', '｜'.join(clean(c) for c in l.strip().strip('|').split('|')), 1)); continue
        ind = (len(l) - len(l.lstrip())) // 2; t = l.strip()
        if t.startswith('> '): bl.append(('q', clean(t[2:]))); continue
        if t.startswith('- '): bl.append(('p', '• ' + clean(t[2:]), 1 + ind)); continue
        bl.append(('p', clean(t), ind))
    return bl

# ---------------- images ----------------
def slices(it):
    w, h = it['w'], it['h']; sc = CW / w
    if h * sc <= IMGH or IMGH / h * w >= 0.7 * CW: return [(0, h)]
    im = np.asarray(Image.open(it['src']).convert('L').resize((max(1, w // 4), max(1, h // 4))), dtype=np.int16)
    var = im.std(axis=1); lim = int(IMGH / sc); cuts = [0]; y = 0
    while h - y > lim:
        lo = int((y + lim * 0.75) / 4); hi = int((y + lim) / 4); seg = var[lo:hi]
        c = (lo + int(np.argmin(seg))) * 4 if len(seg) else y + lim
        cuts.append(c); y = c
    cuts.append(h); return list(zip(cuts[:-1], cuts[1:]))
def prep(args):
    out, src, box, dispw, dpi, q = args
    if os.path.exists(out): return out
    im = Image.open(src)
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[-1]); im = bg
    else: im = im.convert('RGB')
    im = im.crop(box); tw = int(dispw / 72 * dpi)
    if im.width > tw: im = im.resize((tw, int(im.height * tw / im.width)), Image.LANCZOS)
    im.save(out, 'JPEG', quality=q, optimize=True, progressive=True); return out

class Book:
    def __init__(s, args):
        s.cfg = load_book(); s.a = args
        s.dpi = args.dpi or s.cfg['image']['dpi']; s.q = args.quality or s.cfg['image']['jpeg_quality']
        s.version = args.version or s.cfg['version']
        s.chdirs = s.cfg['chapters']
        if args.chapters:
            want = [c.strip() for c in args.chapters.split(',')]
            s.chdirs = [d for d in s.chdirs if d.split('-')[0] in want]
            if not s.chdirs: raise SystemExit('--chapters 没有匹配到任何章')
        s.chs = [load_chapter(d) for d in s.cfg['chapters']]          # 全部章（图号/页码口径一致）
        s.sel = [c for c in s.chs if c['meta']['dir'] in s.chdirs]
        s.front = {k: read_md(os.path.join(ROOT, 'front', k + '.md')) for k in ['cover', 'about', 'preface', 'back-cover']}
        s.appx = [read_md(os.path.join(ROOT, 'appendix', k + '.md')) for k in ['errata', 'gaps']]
        import yaml
        ex = os.path.join(ROOT, 'appendix', 'excluded.yml')
        s.excluded = (yaml.safe_load(open(ex, encoding='utf-8')) or {}).get('excluded_files', []) if os.path.exists(ex) else []
        s.items = []; s.n_placeholder = 0
        ph = getattr(args, 'placeholder_images', False) or placeholder_mode()
        for c in s.chs:
            m = c['meta']; ch = m['ch']; pre = str(m.get('fig_prefix') or (int(ch) if ch.isdigit() else ch)); n = 0
            for b in c['blocks']:
                if b[0] != 'img': continue
                n += 1; src = b[2]
                if ph and not os.path.exists(src): src = placeholder(m['dir'] + '/' + b[3]); s.n_placeholder += 1
                w, h = Image.open(src).size
                s.items.append(dict(ch=ch, cap=b[1], src=src, fig='%s-%d' % (pre, n), w=w, h=h))
        _lb = s.cfg.get('edition_label') or ''
        s.cfg['display_title'] = '《%s》%s' % (s.cfg['title'], _lb) if _lb else s.cfg['title']
        import importlib.util as _iu; _sp=_iu.spec_from_file_location('wc', os.path.join(ROOT,'scripts','wordcount.py')); _wc=_iu.module_from_spec(_sp); _sp.loader.exec_module(_wc); _n=_wc.count()
        s.fmt = dict(word_count=_n, word_wan=_wc.wan(_n), book_title=s.cfg['title'], edition_label=_lb, image_count=len(s.items), dpi=s.dpi, quality=s.q)
    def label(s, m): return m.get('label') or m['ch']
    def chtitle(s, m): return '%s　%s' % (s.label(m), m['title'])
    # ----- fonts -----
    def setup_fonts(s, text):
        r = F.sc_face(F.find('regular', s.cfg.get('fonts', {}).get('regular')), CACHE)
        b = F.sc_face(F.find('bold', s.cfg.get('fonts', {}).get('bold')), CACHE)
        s.fr = fitz.Font(fontfile=r); s.fb = fitz.Font(fontfile=b)
        s.sub_r = F.subset(r, text, CACHE); s.sub_b = F.subset(b, text, CACHE)
    def all_text(s):
        import json
        t = json.dumps(s.cfg, ensure_ascii=False)
        for fm, body in list(s.front.values()) + s.appx: t += json.dumps(fm, ensure_ascii=False, default=str) + body
        for c in s.chs: t += json.dumps(c['meta'], ensure_ascii=False, default=str) + ''.join(b[1] for b in c['blocks'])
        t += ''.join(str(x) for x in s.excluded) + '图注目录附录索引页第章续未收录的非图片文件以下仍在因不是无法以图版张份封面封底总序言关于出品方服务支持作者产品页联系邮箱版权信息主站版本（）导读关键时间线本章篇目小节收录图解清单见'
        return t.replace('κέρας', 'keras')
    # ----- page helpers -----
    def newpage(s, doc, title):
        p = doc.new_page(width=W, height=H)
        p.insert_font(fontname='R', fontfile=s.sub_r); p.insert_font(fontname='B', fontfile=s.sub_b)
        if title is not None: s.decorate(p, title, len(doc))
        return p
    def decorate(s, page, title, pno):
        g = (.5, .5, .5)
        page.insert_text((ML, 36), s.cfg['display_title'], fontname='R', fontsize=8, color=g)
        page.insert_text((W - MR - s.fr.text_length(title, 8), 36), title, fontname='R', fontsize=8, color=g)
        page.draw_line((ML, 42), (W - MR, 42), color=(.8, .8, .8), width=.5)
        sl, pr = s.cfg.get('site_label'), s.cfg.get('support_line')
        if pr:
            page.insert_text((ML, H - 12), pr, fontname='R', fontsize=6.5, color=(.6, .6, .6))
            if sl and pr.startswith(sl) and s.cfg.get('site_url'):
                page.insert_link({'kind': fitz.LINK_URI, 'uri': s.cfg['site_url'], 'from': fitz.Rect(ML, H - 19, ML + s.fr.text_length(sl, 6.5), H - 9)})
        n = str(pno); page.insert_text(((W - s.fr.text_length(n, 9)) / 2, H - 28), n, fontname='R', fontsize=9, color=(.4, .4, .4))
    # ----- plan -----
    def plan(s):
        pages, jobs = [], []
        for c in s.sel:
            m = c['meta']; its = [i for i in s.items if i['ch'] == m['ch']]; k = 0
            pages.append(dict(kind='div', c=c)); pend = None
            for b in c['blocks']:
                if b[0] == 'text': pages.append(dict(kind='text', c=c, md=b[1])); pend = None; continue
                it = its[k]; k += 1; sl = slices(it); land = it['h'] / it['w'] < 0.75 and len(sl) == 1
                for j, (a, z) in enumerate(sl):
                    ar = (z - a) / it['w']; dw = CW if (CW * ar <= IMGH or land) else IMGH / ar
                    key = hashlib.md5(('%s|%s|%s|%s|%s|%s' % (it['src'], os.path.getmtime(it['src']), a, z, s.dpi, s.q)).encode()).hexdigest()
                    jp = os.path.join(CACHE, 'jpg', key + '.jpg'); jobs.append((jp, it['src'], (0, a, it['w'], z), dw, s.dpi, s.q))
                    part = dict(it=it, jpg=jp, j=j, nj=len(sl), ar=ar)
                    if land:
                        if pend is not None and len(pend['parts']) == 1 and (pend['parts'][0]['ar'] + ar) * CW <= IMGH - 40:
                            pend['parts'].append(part); pend = None; continue
                        pg = dict(kind='img', c=c, parts=[part]); pages.append(pg); pend = pg
                    else:
                        pages.append(dict(kind='img', c=c, parts=[part])); pend = None
        return pages, jobs
    # ----- flow text -----
    def flow(s, doc, title, md, dry, head=None, fm=None):
        st = dict(pages=0, y=H, page=None)
        def np_():
            st['pages'] += 1; st['y'] = MT + 6
            if not dry: st['page'] = s.newpage(doc, title)
        def line(t, font, size, x=ML, color=TXT):
            lh = size * 1.65
            if st['y'] + lh > H - MB: np_()
            if not dry and t: st['page'].insert_text((x, st['y'] + size), t, fontname='B' if font is s.fb else 'R', fontsize=size, color=color)
            st['y'] += lh
        def para(t, font, size, indent=0, color=TXT, first=0):
            for k, ln in enumerate(wrap(t, font, size, CW - indent, first)): line(ln, font, size, ML + indent + (first if k == 0 else 0), color)
        st['line'] = line; st['para'] = para; np_(); s.heads = []
        if head: para(head, s.fb, 20, color=NAVY); st['y'] += 10
        for b in md_blocks(md.replace('κέρας', 'keras')):
            if b[0] == 'gap': st['y'] += 4
            elif b[0] == 'h':
                sz = {1: 16, 2: 14, 3: 12, 4: 11}.get(b[2], 11); st['y'] += 6
                if st['y'] + sz * 3 > H - MB: np_()
                s.heads.append((b[2], b[1], st['pages'] - 1))
                para(b[1], s.fb, sz, color=NAVY)
            elif b[0] == 'q': para(b[1], s.fr, 9, 12, (0.35, 0.35, 0.35))
            elif b[2] == 0 and not b[1].startswith('•'): para(b[1], s.fr, 10, 0, first=20)
            else: para(b[1], s.fr, 9.5, b[2] * 12)
        s.last_y = st['y']; s.last_page = st['page']
        return st['pages']
    def divider(s, doc, c, dry):
        m = c['meta']; st = {}
        pages = [0]; y = [0]; cur = [None]
        def np_():
            pages[0] += 1; y[0] = MT + 6
            if not dry: cur[0] = s.newpage(doc, s.chtitle(m))
        def para(t, font, size, indent=0, color=TXT):
            for ln in wrap(t, font, size, CW - indent):
                lh = size * 1.65
                if y[0] + lh > H - MB: np_()
                if not dry and ln: cur[0].insert_text((ML + indent, y[0] + size), ln, fontname='B' if font is s.fb else 'R', fontsize=size, color=color)
                y[0] += lh
        np_(); y[0] = MT + 60
        para(s.label(m), s.fr, 14, color=(0.3, 0.45, 0.7)); y[0] += 6
        para(m['title'], s.fb, 28, color=NAVY)
        if m.get('subtitle'): para(m['subtitle'], s.fr, 11, color=(0.45, 0.45, 0.45))
        if not dry: cur[0].draw_line((ML, y[0] + 6), (ML + 120, y[0] + 6), color=NAVY, width=2)
        y[0] += 22
        if m.get('intro'): para('导读', s.fb, 12, color=NAVY); para(m['intro'], s.fr, 10.5); y[0] += 8
        if m.get('timeline'):
            para('关键时间线', s.fb, 12, color=NAVY)
            for t in m['timeline']: para('•  ' + str(t), s.fr, 10, 8)
            y[0] += 8
        if m.get('note'): para(m['note'], s.fr, 9.5, 0, (0.35, 0.35, 0.35)); y[0] += 8
        its = [i for i in s.items if i['ch'] == m['ch']]
        hs = [b[1] for blk in c['blocks'] if blk[0] == 'text' for b in md_blocks(blk[1]) if b[0] == 'h']
        if hs:
            para('本章小节', s.fb, 12, color=NAVY)
            for k, h in enumerate(hs, 1): para('%d　%s' % (k, h), s.fr, 10, 8)
            y[0] += 8
        para('本章收录图解 %d 张，图片清单见附录 C。' % len(its), s.fr, 9.5, 0, (0.35, 0.35, 0.35))
        return pages[0]
    def img_h(s, part): return min(CW * part['ar'], IMGH)
    def imgpage(s, doc, pg, page=None, y0=None):
        p = page or s.newpage(doc, s.chtitle(pg['c']['meta'])); y = MT if y0 is None else y0; parts = pg['parts']; gap = 24
        for part in parts:
            it = part['it']; ar = part['ar']
            hh = min(CW * ar, IMGH if len(parts) == 1 else (IMGH - gap) / 2)
            if y0 is not None: hh = min(hh, H - MB - 34 - y)
            ww = hh / ar; x = ML + (CW - ww) / 2
            p.insert_image(fitz.Rect(x, y, x + ww, y + hh), filename=part['jpg'])
            c = '图 %s　%s' % (it['fig'], it['cap']) + ('（%d/%d）' % (part['j'] + 1, part['nj']) if part['nj'] > 1 else '')
            yy = y + hh + 14
            for ln in wrap(c, s.fr, 9, CW - 20)[:2]:
                p.insert_text(((W - s.fr.text_length(ln, 9)) / 2, yy), ln, fontname='R', fontsize=9, color=(.3, .3, .3)); yy += 13
            y = yy + gap - 10
    # ----- toc -----
    def toc_layout(s, entries):
        pages = [[]]; y = MT + 50
        for e in entries:
            lh = 26 if e[0] == 1 else 14.5
            if y + lh > H - MB: pages.append([]); y = MT + 10
            pages[-1].append((e, y)); y += lh
        return pages
    def render_toc(s, doc, entries, links):
        for pi, pl in enumerate(s.toc_layout(entries)):
            p = s.newpage(doc, '总目录')
            if pi == 0: p.insert_text((ML, MT + 26), '总目录', fontname='B', fontsize=22, color=NAVY)
            for (lv, t, pg), y in pl:
                fn, font, sz, x = ('B', s.fb, 11.5, ML) if lv == 1 else ('R', s.fr, 9, ML + 16)
                num = str(pg); nw = font.text_length(num, sz); maxw = W - MR - nw - x - 24
                while font.text_length(t, sz) > maxw: t = t[:-2] + '…'
                p.insert_text((x, y + sz), t, fontname=fn, fontsize=sz, color=(0.1, 0.1, 0.1) if lv == 1 else (0.25, 0.25, 0.25))
                tw = font.text_length(t, sz); dots = '.' * int((W - MR - nw - x - tw - 12) / s.fr.text_length('.', sz))
                p.insert_text((x + tw + 6, y + sz), dots, fontname='R', fontsize=sz, color=(.7, .7, .7))
                p.insert_text((W - MR - nw, y + sz), num, fontname=fn, fontsize=sz, color=(0.1, 0.1, 0.1))
                links.append((len(doc) - 1, pg - 1, fitz.Rect(x, y, W - MR, y + sz + 4)))
    # ----- special pages -----
    def cover(s, doc):
        fm, body = s.front['cover']; cfg = s.cfg
        p = doc.new_page(width=W, height=H); p.insert_font(fontname='R', fontfile=s.sub_r); p.insert_font(fontname='B', fontfile=s.sub_b)
        hx = lambda h: tuple(int(h[k:k+2],16)/255 for k in (1,3,5)); BG, PANEL, HEAD, ACC, PRI, TXT, MUT = hx('#f8f9fa'), hx('#e8f0fb'), hx('#101c44'), hx('#4b43e8'), hx('#0058bd'), hx('#1c1b1f'), hx('#667085')  # www.xworktech.com palette
        p.draw_rect(fitz.Rect(0, 0, W, H), color=None, fill=BG)
        p.draw_rect(fitz.Rect(0, H * 0.62, W, H), color=None, fill=PANEL)
        _lb = cfg.get('edition_label'); _ct = fm.get('title') or ('《%s》' % cfg['title'] if _lb else cfg['title']); _cs = 48
        while _cs > 22 and s.fb.text_length(_ct, _cs) > CW: _cs -= 1
        p.insert_text((ML, 190), _ct, fontname='B', fontsize=_cs, color=HEAD)
        dy = 0
        if _lb: p.insert_text((ML, 232), _lb, fontname='B', fontsize=24, color=ACC); dy = 40
        p.insert_text((ML, 232 + dy), fm.get('subtitle', cfg['subtitle']), fontname='R', fontsize=18, color=PRI)
        g0, g1 = hx('#075ecc'), hx('#4338ca')
        for k in range(40): t = k / 39; p.draw_rect(fitz.Rect(ML + k*4, 254.5 + dy, ML + k*4 + 4.2, 257.5 + dy), color=None, fill=tuple(g0[q]*(1-t) + g1[q]*t for q in range(3)))
        y = 300 + dy
        for ln in [l[2:].format(**s.fmt) for l in body.split('\n') if l.startswith('- ')]:
            p.insert_text((ML, y), ln, fontname='R', fontsize=12.5, color=TXT); y += 24
        y = H * 0.62 + 40
        for i, c in enumerate(s.chs):
            x = ML + (i % 2) * (CW / 2); yy = y + (i // 2) * 24
            p.insert_text((x, yy), '%s　%s' % (s.label(c['meta']), c['meta']['title'].split('：')[0]), fontname='R', fontsize=10.5, color=HEAD)
        # 品牌标（无 URL、无推广语）：www.xworktech.com 页头 .xds-logo-mark + 文字标
        _lp = fitz.open('pdf', fitz.open(os.path.join(ROOT, 'scripts', 'xwork-logo-mark.svg')).convert_to_pdf())
        _wm, _sz, _ms, _gx = 'XWork Technologies', 11, 16, 7; _yt = H - 62 - 12
        p.show_pdf_page(fitz.Rect(ML, _yt, ML + _ms, _yt + _ms), _lp, 0)
        p.insert_text((ML + _ms + _gx, _yt + 12.2), _wm, fontname='B', fontsize=_sz, color=HEAD)
    def about(s, doc):
        fm, body = s.front['about']; p = s.newpage(doc, '关于出品方'); y = [MT + 30]
        def para(t, font, sz, x=ML, col=TXT):
            for ln in wrap(t, font, sz, W - MR - x):
                p.insert_text((x, y[0] + sz), ln, fontname='B' if font is s.fb else 'R', fontsize=sz, color=col); y[0] += sz * 1.75
        para(fm.get('title', '关于出品方'), s.fb, 22, col=NAVY); y[0] += 14
        for blk in [b.strip() for b in body.split('\n\n') if b.strip()]:
            if blk.startswith('**'): para(clean(blk), s.fb, 11.5); y[0] += 2
            elif blk.startswith('- '):
                for li in blk.split('\n'):
                    p.insert_text((ML + 8, y[0] + 11), '•', fontname='R', fontsize=11); para(clean(li[2:]), s.fr, 11, ML + 22); y[0] += 4
                y[0] += 6
            else: para(clean(blk), s.fr, 11); y[0] += 8
        yb = H - MB - 150; p.draw_line((ML, yb), (W - MR, yb), color=(.75, .75, .75), width=.6); yb += 20
        for lab, val, uri in [('产品页', fm.get('product_url'), fm.get('product_url')), ('联系邮箱', fm.get('email'), 'mailto:%s' % fm.get('email')), ('主站', s.cfg.get('site_label'), s.cfg.get('site_url')), ('版本', '%s（%s）' % (s.cfg.get('edition') or s.version, s.cfg.get('date')), None), ('版权信息', fm.get('copyright'), None)]:
            if not val: continue
            p.insert_text((ML, yb + 10), lab, fontname='B', fontsize=10, color=(.3, .3, .3))
            p.insert_text((ML + 70, yb + 10), val, fontname='R', fontsize=10, color=(0.05, 0.3, 0.7) if uri else (.2, .2, .2))
            if uri: p.insert_link({'kind': fitz.LINK_URI, 'uri': uri, 'from': fitz.Rect(ML + 70, yb - 2, ML + 70 + s.fr.text_length(val, 10), yb + 14)})
            yb += 24
    def backcover(s, doc):
        fm, body = s.front['back-cover']; org = (0.95, 0.65, 0.2); cfg = s.cfg
        p = doc.new_page(width=W, height=H); p.insert_font(fontname='R', fontfile=s.sub_r); p.insert_font(fontname='B', fontfile=s.sub_b)
        p.draw_rect(fitz.Rect(0, 0, W, H), color=None, fill=(0.04, 0.11, 0.24))
        _bt = cfg['display_title']; _bs = 34
        while _bs > 18 and s.fb.text_length(_bt, _bs) > CW: _bs -= 1
        p.insert_text((ML, 300), _bt, fontname='B', fontsize=_bs, color=(1, 1, 1))
        p.insert_text((ML, 334), cfg['subtitle'], fontname='R', fontsize=13, color=(0.75, 0.85, 1))
        p.draw_line((ML, 352), (ML + 120, 352), color=org, width=3)
        if fm.get('next_series'): p.insert_text((ML, 400), fm['next_series'], fontname='R', fontsize=13, color=(0.95, 0.8, 0.55))
        pr, sl = cfg.get('support_line'), cfg.get('site_label')
        if pr:
            p.insert_text((ML, H - 12), pr, fontname='R', fontsize=6.5, color=(0.62, 0.7, 0.82))
            if sl and pr.startswith(sl): p.insert_link({'kind': fitz.LINK_URI, 'uri': cfg['site_url'], 'from': fitz.Rect(ML, H - 19, ML + s.fr.text_length(sl, 6.5), H - 9)})
    def index_md(s):
        out = ''
        for c in s.sel:
            m = c['meta']; out += '\n## %s\n' % s.chtitle(m)
            for it in s.items:
                if it['ch'] == m['ch']: out += '- 图 %s　%s　……　第 %d 页\n' % (it['fig'], it['cap'], it.get('page', 0))
        if s.excluded:
            out += '\n## 未收录的非图片文件（%d 份）\n> 以下文件仍在 Drive 整理版对应章节，因不是图片无法以图版收录。\n' % len(s.excluded)
            for x in s.excluded: out += '- [%s] %s（%s）\n' % (x['chapter'], x['name'], x['mime'])
        return out
    # ----- build -----
    def build(s, out):
        pages, jobs = s.plan()
        todo = [j for j in jobs if not os.path.exists(j[0])]
        if todo:
            with ProcessPoolExecutor(min(6, os.cpu_count() or 2)) as ex: list(ex.map(prep, todo, chunksize=4))
        s.setup_fonts(s.all_text())
        pref_fm, pref = s.front['preface']; pref = pref.format(**s.fmt)
        apx = [(fm.get('title', ''), body) for fm, body in s.appx]
        idx_title = '附录 C　图片索引'
        d = fitz.open()
        n_pref = s.flow(d, '序言', pref, True, pref_fm.get('title', '序言'))
        n_div = {c['meta']['dir']: s.divider(d, c, True) for c in s.sel}
        n_apx = [s.flow(d, t, b, True, t) for t, b in apx]
        for it in s.items: it['page'] = 999
        n_idx = s.flow(d, idx_title, s.index_md(), True, idx_title)
        n_txt = {}; heads = {}
        for i, pg in enumerate(pages):
            if pg['kind'] == 'text':
                n_txt[i] = s.flow(d, s.chtitle(pg['c']['meta']), pg['md'], True); heads[i] = list(s.heads)
                nx = pages[i + 1] if i + 1 < len(pages) else None
                if nx and nx['kind'] == 'img' and len(nx['parts']) == 1 and nx['parts'][0]['nj'] == 1:
                    need = min(CW * nx['parts'][0]['ar'], IMGH) * 0.6 + 40
                    if H - MB - 34 - (s.last_y + 10) >= need: nx['inline'] = s.last_y + 10
        for pg in pages:
            if pg.get('inline') is not None: pg['n'] = 0
        ent = [(1, '序言', 0)]
        for i, pg in enumerate(pages):
            if pg['kind'] == 'div': ent.append((1, 'x', 0))
            elif pg['kind'] == 'text': ent += [(2, 'x', 0) for _ in heads[i]]
        ent += [(1, '附录', 0)] + [(2, t, 0) for t, _ in apx] + [(2, idx_title, 0)]
        n_toc = len(s.toc_layout(ent))
        pno = 2; pref_p = pno; pno += n_pref; toc_p = pno; pno += n_toc; chp = {}
        for i, pg in enumerate(pages):
            if pg['kind'] == 'div': chp[pg['c']['meta']['dir']] = pno; pno += n_div[pg['c']['meta']['dir']]
            elif pg['kind'] == 'text':
                for lv, h, off in heads[i]: pg.setdefault('h', []).append((lv, h, pno + off))
                pno += n_txt[i]
            else:
                inl = pg.get('inline') is not None
                for part in pg['parts']:
                    if part['j'] == 0: part['it']['page'] = pno - 1 if inl else pno
                if not inl: pno += 1
        app_p = []
        for n in n_apx: app_p.append(pno); pno += n
        idx_p = pno; pno += n_idx
        E = [(1, '序言', pref_p)]; BM = []
        for c in s.sel:
            d0 = c['meta']['dir']; E.append((1, s.chtitle(c['meta']), chp[d0])); BM.append([1, s.chtitle(c['meta']), chp[d0]])
            for pg in pages:
                if pg['c'] is not c: continue
                if pg['kind'] == 'text':
                    for lv, h, pp in pg.get('h', []): E.append((2, h, pp)); BM.append([2, h, pp])
                elif pg['kind'] == 'img':
                    for part in pg['parts']:
                        if part['j'] == 0:
                            it = part['it']; BM.append([3 if BM[-1][0] >= 2 else 2, '图 %s　%s' % (it['fig'], it['cap']), it['page']])
        E += [(1, '附录', app_p[0])] + [(2, t, p) for (t, _), p in zip(apx, app_p)] + [(2, idx_title, idx_p)]
        doc = fitz.open(); links = []
        s.cover(doc)
        s.flow(doc, '序言', pref, False, pref_fm.get('title', '序言'))
        s.render_toc(doc, E, links)
        for pg in pages:
            if pg['kind'] == 'div': assert len(doc) + 1 == chp[pg['c']['meta']['dir']]; s.divider(doc, pg['c'], False)
            elif pg['kind'] == 'text': s.flow(doc, s.chtitle(pg['c']['meta']), pg['md'], False)
            elif pg.get('inline') is not None: s.imgpage(doc, pg, s.last_page, s.last_y + 10)
            else: s.imgpage(doc, pg)
        for (t, b) in apx: s.flow(doc, t, b, False, t)
        s.flow(doc, idx_title, s.index_md(), False, idx_title)
        s.backcover(doc); pno += 1
        assert len(doc) == pno - 1, (len(doc), pno)
        for a, b, r in links: doc[a].insert_link({'kind': fitz.LINK_GOTO, 'page': b, 'from': r, 'to': fitz.Point(0, 0)})
        toc = [[1, '封面', 1], [1, '序言', pref_p], [1, '总目录', toc_p]] + BM + [list(e) for e in E if e[1] == '附录' or (e[0] == 2 and e[2] >= app_p[0])] + [[1, '封底', len(doc)]]
        doc.set_toc(toc)
        doc.set_metadata({'title': s.cfg['display_title'] + ' ' + s.version, 'author': s.cfg.get('author') or s.cfg.get('publisher', ''),
                          'subject': s.cfg['subtitle'], 'creator': 'book-src/scripts/build.py'})
        os.makedirs(os.path.dirname(out), exist_ok=True)
        doc.save(out, garbage=3, deflate=True)
        return len(doc)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--chapters', help='只生成这些章（章号逗号分隔，如 03,05），用于预览')
    ap.add_argument('--dpi', type=int); ap.add_argument('--quality', type=int)
    ap.add_argument('--version'); ap.add_argument('--out')
    ap.add_argument('--placeholder-images', action='store_true', help='缺图用灰色占位页（CI 冒烟构建）')
    a = ap.parse_args(); bk = Book(a)
    if a.out: out = a.out
    elif a.chapters: out = os.path.join(ROOT, 'dist', 'preview-%s.pdf' % a.chapters.replace(',', '_'))
    else: out = os.path.join(ROOT, 'dist', bk.cfg['output'].format(version=bk.version))
    n = bk.build(out); mb = os.path.getsize(out) / 1e6
    print('生成：%s\n页数：%d　大小：%.1f MB　dpi=%d　quality=%d' % (out, n, mb, bk.dpi, bk.q))
    if bk.n_placeholder: print('占位页：%d 张图片缺失，已用灰色占位（仅供冒烟检查，勿发布）' % bk.n_placeholder)
    lim = bk.cfg.get('max_size_mb')
    if lim and not a.chapters and mb > lim:
        print('警告：超过大小上限 %s MB，可用 --dpi 130 等降低压缩参数' % lim); sys.exit(2)
if __name__ == '__main__': main()
