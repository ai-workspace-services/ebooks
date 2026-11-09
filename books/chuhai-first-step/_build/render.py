import os
#!/usr/bin/env python3
"""合集版渲染：HTML -> headless Chrome PDF -> pypdf 书签 -> PNG。复用 _build/render.py 的管线思路。"""
import html, re, subprocess, sys, pathlib, shutil
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import *

OUT = pathlib.Path('/workspace/xhs-notes/collection')
BUILD = OUT / '_build'
NAVY = '#20384a'
CHD = {c['key']: c for c in CH}
NEXT = {'llc': 'ein', 'ein': 'mercury', 'mercury': 'ms', 'ms': 'apple', 'apple': 'gp', 'gp': 'fx', 'fx': 'final'}

def md(s):
    s = html.escape(s)
    s = s.replace('D-U-N-S', '<span style="white-space:nowrap">D-U-N-S</span>')
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)

# ---------- icons (48x48, stroke) ----------
IC = {
 'building': '<path d="M6 18 L24 8 L42 18 Z"/><path d="M11 18v17M19 18v17M29 18v17M37 18v17M6 38h36"/>',
 'bank': '<path d="M6 16 L24 7 L42 16 Z"/><path d="M9 20h30M12 20v14M20 20v14M28 20v14M36 20v14M7 38h34"/>',
 'doc': '<path d="M13 6h16l8 8v28H13z"/><path d="M29 6v8h8M18 22h14M18 28h14M18 34h9"/>',
 'check': '<circle cx="24" cy="24" r="17"/><path d="M16 24l6 6 11-12"/>',
 'upload': '<path d="M24 31V10M16 18l8-8 8 8M10 32v7h28v-7"/>',
 'clock': '<circle cx="24" cy="24" r="17"/><path d="M24 14v10l7 5"/>',
 'mail': '<path d="M7 12h34v24H7z"/><path d="M7 12l17 14 17-14"/>',
 'globe': '<circle cx="24" cy="24" r="17"/><path d="M7 24h34M24 7c-8 9-8 25 0 34M24 7c8 9 8 25 0 34"/>',
 'search': '<circle cx="21" cy="21" r="12"/><path d="M30 30l10 10"/>',
 'id': '<path d="M6 11h36v26H6z"/><circle cx="17" cy="22" r="4"/><path d="M11 31c2-4 10-4 12 0M28 20h9M28 26h9M28 32h5"/>',
 'phone': '<rect x="13" y="5" width="22" height="38" rx="4"/><path d="M21 37h6"/>',
 'monitor': '<path d="M6 9h36v24H6z"/><path d="M18 41h12M24 33v8"/>',
}
def icon(name, color, size=52):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" stroke="{color}" stroke-width="2.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{IC[name]}</svg>')
def svg_check(color='#fff', size=30, w=5):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{w*0.6}" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
def svg_x(color='#fff', size=26):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'
def svg_arrow(color, w=90):
    return f'<svg width="{w}" height="20" viewBox="0 0 {w} 20" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M2 10H{w-4}M{w-12} 3l8 7-8 7"/></svg>'

# ---------- chapter illustration (user's style: circle + doc card + object + crosses) ----------
def illus(ch, width=560):
    c, a, l, lab = ch['c'], ch['a'], ch['l'], ch['label']
    fs = {1: 64, 2: 64, 3: 64, 4: 56}.get(len(lab), 42)
    x0, y0 = 110, 120
    doc = (f'<rect x="{x0+12}" y="{y0+12}" width="230" height="270" rx="18" fill="#dfe3dc"/>'
           f'<rect x="{x0}" y="{y0}" width="230" height="270" rx="18" fill="#fff" stroke="{NAVY}" stroke-width="5"/>'
           f'<rect x="{x0+24}" y="{y0+26}" width="182" height="13" rx="6.5" fill="{a}"/>'
           f'<text x="{x0+24}" y="{y0+112}" font-family="Noto Sans CJK SC" font-weight="800" font-size="{fs}" fill="{NAVY}">{html.escape(lab)}</text>'
           f'<rect x="{x0+24}" y="{y0+150}" width="176" height="5" rx="2.5" fill="#b9c9c9"/>'
           f'<rect x="{x0+24}" y="{y0+174}" width="120" height="4" rx="2" fill="#c9d1d3"/>'
           f'<rect x="{x0+24}" y="{y0+194}" width="150" height="4" rx="2" fill="#c9d1d3"/>'
           f'<circle cx="{x0+192}" cy="{y0+232}" r="22" fill="{l}"/>'
           f'<path d="M{x0+181} {y0+232}l8 8 14-15" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    s = ch['second']; ox = 400
    if s in ('building', 'bank'):
        obj = (f'<path d="M{ox} 210 L{ox+95} 160 L{ox+190} 210 Z" fill="{a}" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>'
               f'<rect x="{ox+12}" y="210" width="166" height="140" fill="#fff" stroke="{NAVY}" stroke-width="5"/>'
               + ''.join(f'<rect x="{ox+30+i*44}" y="230" width="22" height="100" fill="{l}" stroke="{NAVY}" stroke-width="4"/>' for i in range(4 if s == 'bank' else 3))
               + f'<rect x="{ox-6}" y="350" width="202" height="18" rx="6" fill="{a}" stroke="{NAVY}" stroke-width="5"/>')
    elif s == 'doc':
        obj = ''.join(f'<rect x="{ox+20+k*22}" y="{150+k*22}" width="150" height="200" rx="14" fill="#fff" stroke="{NAVY}" stroke-width="5"/>' for k in range(2))
        obj += ''.join(f'<rect x="{ox+64}" y="{220+i*26}" width="{90-i*12}" height="5" rx="2.5" fill="#b9c9c9"/>' for i in range(4))
        obj += f'<rect x="{ox+64}" y="196" width="100" height="10" rx="5" fill="{a}"/>'
    elif s == 'monitor':
        obj = (f'<rect x="{ox-10}" y="150" width="210" height="150" rx="12" fill="#fff" stroke="{NAVY}" stroke-width="5"/>'
               f'<rect x="{ox+6}" y="166" width="178" height="22" rx="4" fill="{a}"/>'
               + ''.join(f'<rect x="{ox+6}" y="{200+i*24}" width="{178 - i*30}" height="12" rx="4" fill="{l}"/>' for i in range(3))
               + f'<path d="M{ox+95} 300v36M{ox+55} 340h80" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>')
    else:
        obj = (f'<rect x="{ox+10}" y="120" width="170" height="290" rx="24" fill="{NAVY}"/>'
               f'<rect x="{ox+24}" y="142" width="142" height="236" rx="10" fill="{l}"/>'
               + ''.join(f'<rect x="{ox+40+(i%2)*66}" y="{164+(i//2)*62}" width="44" height="44" rx="10" fill="{a if i < 2 else "#fff"}"/>' for i in range(4))
               + f'<circle cx="{ox+95}" cy="394" r="5" fill="#9aa9b3"/>')
    arrow = f'<path d="M{x0+236} 260h52" stroke="{c}" stroke-width="5" stroke-linecap="round"/><path d="M{x0+282} 252l10 8-10 8z" fill="{c}"/>'
    cross = ''.join(f'<path d="M{x-14} {y}h28M{x} {y-14}v28" stroke="{a}" stroke-width="4" stroke-linecap="round"/>' for x, y in ((60, 80), (610, 360)))
    return (f'<svg width="{width}" viewBox="0 0 640 430" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="390" cy="230" r="180" fill="{l}" opacity=".9"/>{cross}{obj}{arrow}{doc}</svg>')

CSS = r"""
@page { size: 1080px 1440px; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1080px; }
body { font-family: 'Noto Sans CJK SC', sans-serif; color: #24323c; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: inherit; text-decoration: none; }
.page { width: 1080px; height: 1440px; position: relative; overflow: hidden; break-after: page; background: #fff;
  padding: 36px 60px 34px; display: flex; flex-direction: column; }
.page:last-child { break-after: auto; }
.nav { display: flex; align-items: center; gap: 12px; }
.pills { flex: 1; display: flex; gap: 8px; }
.pill { flex: 1; text-align: center; font-size: 21px; white-space: nowrap; font-weight: 700; color: #7c8a93; background: #f2f4f5; border-radius: 999px; padding: 8px 0; }
.pill.done { color: #4f5f69; }
.pill.on { background: var(--a); color: #fff; }
.home { font-size: 22px; font-weight: 800; color: #fff; background: #20384a; border-radius: 999px; padding: 8px 20px; white-space: nowrap; }
.prog { height: 6px; background: #eceff1; border-radius: 3px; margin: 14px 0 0; overflow: hidden; }
.prog div { height: 100%; background: var(--a); border-radius: 3px; }
.z { flex: 1; min-height: 0; display: flex; flex-direction: column; padding-top: 40px; overflow: hidden; }
.main { flex: 1; min-height: 0; overflow: hidden; display: flex; flex-direction: column; }
.kicker { font-size: 26px; font-weight: 700; color: var(--a); letter-spacing: 1px; margin-bottom: 14px; }
h1 { font-size: 58px; line-height: 1.22; font-weight: 800; color: #20384a; margin-bottom: 30px; }
h1 .sn { color: var(--a); margin-right: 18px; }
.para { font-size: 32px; line-height: 1.62; color: #33434d; margin: 4px 0 22px; }
.para b, .bl b, .st b, .cmp b { color: var(--c); font-weight: 800; }
.bl { list-style: none; margin-bottom: 22px; }
.bl li { font-size: 32px; line-height: 1.55; padding: 10px 0 10px 34px; position: relative; color: #2b3a44; }
.bl li::before { content: ''; position: absolute; left: 4px; top: 30px; width: 12px; height: 12px; border-radius: 50%; background: var(--a); }
.note { font-size: 25px; line-height: 1.55; color: #5d6c75; background: #f5f7f8; border-left: 7px solid var(--a); border-radius: 10px; padding: 14px 20px; margin: 4px 0 14px; }
.quote { font-size: 34px; font-weight: 800; color: var(--c); background: var(--l); border-radius: 22px; padding: 26px 34px; margin: 6px 0 22px; line-height: 1.45; }
.flow { background: var(--l); border-radius: 26px; padding: 30px 26px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 26px; }
.flow .nd { flex: 1; display: flex; flex-direction: column; align-items: center; text-align: center; }
.flow .nd .t { font-size: 30px; font-weight: 800; color: var(--c); margin-top: 10px; }
.flow .nd .s { font-size: 23px; color: #6b5a52; color: var(--c); opacity: .8; margin-top: 4px; }
.flow .ar { flex: 0 0 auto; padding-bottom: 50px; }
.pair { display: flex; gap: 22px; margin-bottom: 26px; }
.pair .bx { flex: 1; background: var(--l); border-radius: 24px; padding: 26px 26px; display: flex; gap: 20px; align-items: center; }
.pair .bx .t { font-size: 32px; font-weight: 800; color: var(--c); }
.pair .bx .s { font-size: 25px; color: var(--c); opacity: .85; margin-top: 4px; line-height: 1.4; }
.st { display: flex; gap: 22px; padding: 12px 0; align-items: flex-start; }
.st .n { flex: 0 0 54px; height: 54px; border-radius: 16px; background: var(--a); color: #fff; font-size: 28px; font-weight: 800; display: flex; align-items: center; justify-content: center; }
.st .t { font-size: 31px; line-height: 1.45; padding-top: 4px; }
.st .t small { display: block; font-size: 25px; color: #66757e; margin-top: 3px; }
.steps { margin-bottom: 22px; }
.cmp { display: flex; gap: 22px; margin-bottom: 24px; }
.cmp .col { flex: 1; background: #f5f7f8; border-radius: 24px; padding: 26px 26px; border: 3px solid transparent; }
.cmp .col.win { background: var(--l); border-color: var(--a); }
.cmp h3 { font-size: 34px; font-weight: 800; color: #20384a; margin-bottom: 10px; }
.cmp li { list-style: none; font-size: 27px; line-height: 1.45; padding: 7px 0 7px 22px; position: relative; }
.cmp li::before { content: ''; position: absolute; left: 0; top: 22px; width: 9px; height: 9px; border-radius: 50%; background: var(--a); }
.cmp .vd { font-size: 27px; font-weight: 800; color: var(--c); margin-top: 10px; }
.c3 .col h3 { font-size: 30px; }
.c3 .col li { font-size: 25px; }
.pits { margin-bottom: 22px; }
.pit { display: flex; gap: 20px; padding: 14px 0; border-bottom: 2px dashed #e3e7ea; }
.pit:last-child { border-bottom: none; }
.pit .x { flex: 0 0 46px; height: 46px; border-radius: 50%; background: #df654e; display: flex; align-items: center; justify-content: center; margin-top: 2px; }
.pit .bad { font-size: 30px; font-weight: 800; color: #20384a; line-height: 1.4; }
.pit .fix { font-size: 27px; color: #45555f; line-height: 1.5; margin-top: 4px; display: flex; gap: 8px; }
.pit .fix i { flex: 0 0 auto; margin-top: 5px; }
.chk { list-style: none; margin-bottom: 14px; }
.chk li { font-size: 27px; line-height: 1.38; padding: 7px 0 7px 58px; position: relative; color: #2b3a44; }
.chk li .bx { position: absolute; left: 0; top: 6px; width: 38px; height: 38px; border-radius: 11px; border: 4px solid var(--a); display: flex; align-items: center; justify-content: center; }
.chk li.done .bx { background: var(--a); }
.chk li.wip .bx::after { content: ''; width: 16px; height: 16px; border-radius: 4px; background: var(--a); }
.chk .grp { font-size: 24px; font-weight: 800; color: var(--a); margin: 10px 0 2px; letter-spacing: 1px; }
.hand { flex-shrink: 0; margin-top: 12px; margin-bottom: 4px; border: 3px dashed var(--a); border-radius: 24px; padding: 16px 20px; display: flex; align-items: center; gap: 14px; }
.hand .side { flex: 1; }
.hand .lb { font-size: 23px; font-weight: 800; color: #7c8a93; margin-bottom: 10px; }
.hand .lb a { color: var(--na); }
.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chips span { font-size: 23px; font-weight: 700; padding: 5px 14px; border-radius: 999px; }
.hand .o span { background: var(--l); color: var(--c); }
.hand .n span { background: var(--nl); color: var(--nc); }
.footer { flex-shrink: 0; margin-top: 18px; border-top: 2px solid #e6eaec; padding-top: 12px; display: flex; justify-content: space-between; font-size: 22px; color: #7c8a93; background: #fff; position: relative; z-index: 2; }
.footer b { color: #20384a; }
.footer .by { font-size: 19px; color: #4f5f69; } .footer .by2 { font-size: 17px; color: #9aa9b3; }
.fxm { display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px 18px; margin: 10px 0 16px; font-size: 24px; }
.fxm .bx { border-radius: 16px; padding: 16px; text-align:center; background: var(--l); color: var(--c); font-weight: 700; }
.fxm .bx small { display:block; font-weight:400; font-size: 20px; color:#4f5f69; }
.fxm .ar { grid-column: span 3; display:flex; align-items:center; gap:12px; font-size: 22px; padding: 6px 10px; border-radius: 12px; }
.fxm .ok { background:#e3f1e8; color:#1e5e51; } .fxm .wt { background:#fbf1dc; color:#8a5a1f; } .fxm .no { background:#fbe3e0; color:#9e3e2e; }
.fxm .st { margin-left:auto; font-weight:700; white-space:nowrap; }
.fxm .x { text-decoration: line-through; text-decoration-thickness: 3px; font-weight:700; }
.tbl { width:100%; border-collapse:separate; border-spacing:0; margin: 2px 0 14px; font-size:22px; line-height:1.4; }
.tbl th { background: var(--a); color:#fff; font-weight:800; text-align:left; padding:9px 12px; }
.tbl th:first-child { border-radius:14px 0 0 0; } .tbl th:last-child { border-radius:0 14px 0 0; }
.tbl td { padding:8px 12px; border-bottom:2px solid #e6eaec; vertical-align:top; color:#2b3a44; }
.tbl tr:nth-child(even) td { background:#f7f9fa; }
.tbl td:first-child { font-weight:800; color:var(--c); white-space:nowrap; width:22%; }
.tbl td:nth-child(2) { width:40%; } .tbl td:nth-child(3) { width:38%; color:#45555f; }
/* divider */
.dv .big { font-size: 150px; font-weight: 900; color: var(--l); line-height: 1; margin-top: 10px; }
.dv .cap { font-size: 26px; font-weight: 800; color: var(--a); letter-spacing: 6px; margin-top: -18px; }
.dv h1 { font-size: 66px; margin: 10px 0 12px; }
.dv .sub { font-size: 31px; color: #5d6c75; margin-bottom: 6px; }
.dv .ill { display: flex; justify-content: center; margin: 4px 0 6px; }
.mtoc { background: #f5f7f8; border-radius: 24px; padding: 16px 28px; }
.mtoc a { display: flex; justify-content: space-between; font-size: 28px; padding: 10px 0; border-bottom: 2px dashed #e1e5e8; color: #2b3a44; }
.mtoc a:last-child { border-bottom: none; }
.mtoc a span:first-child b { color: var(--a); margin-right: 14px; }
.mtoc a em { font-style: normal; color: var(--a); font-weight: 700; }
.src { margin-top: 18px; font-size: 22px; color: #7c8a93; line-height: 1.6; }
.src b { color: #4f5f69; }
.io { margin-top: 16px; display: flex; gap: 12px; font-size: 24px; align-items: center; color: #4f5f69; }
.io span.tag { background: var(--l); color: var(--c); font-weight: 800; padding: 5px 14px; border-radius: 999px; }
/* toc */
.toc a.row { display: flex; align-items: center; gap: 24px; background: #f5f7f8; border-radius: 22px; padding: 8px 26px 8px 12px; margin-bottom: 12px; }
.toc .mi { flex: 0 0 160px; }
.toc .tx { flex: 1; }
.toc .tx .t { font-size: 31px; font-weight: 800; }
.toc .tx .t b { margin-right: 12px; }
.toc .tx .s { font-size: 23px; color: #66757e; margin-top: 4px; }
.toc .pg { font-size: 28px; font-weight: 800; white-space: nowrap; }
/* cover */
.cv h1 { font-size: 84px; line-height: 1.16; margin-bottom: 16px; }
.cv .sub { font-size: 38px; color: #3b5a70; font-weight: 700; margin-bottom: 26px; }
.route { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 10px 0 26px; }
.route a { border-radius: 22px; padding: 20px 10px 16px; display: flex; flex-direction: column; align-items: center; }
.route .t { font-size: 27px; font-weight: 800; margin-top: 8px; }
.route .s { font-size: 21px; margin-top: 2px; opacity: .85; }
.tags { display: flex; flex-wrap: wrap; gap: 12px; margin-top: auto; }
.tags span { font-size: 24px; color: #3b5a70; background: #eef2f4; padding: 6px 18px; border-radius: 999px; font-weight: 700; }
.chip { display: inline-block; font-size: 24px; font-weight: 800; padding: 7px 20px; border-radius: 999px; margin-right: 10px; }
/* timeline */
.tl { position: relative; margin-bottom: 20px; }
.tl a { display: flex; gap: 24px; padding: 12px 0; position: relative; }
.tl .dt { flex: 0 0 150px; font-size: 28px; font-weight: 800; color: var(--c); padding-top: 6px; text-align: right; }
.tl .dot { flex: 0 0 44px; height: 44px; border-radius: 50%; border: 4px solid; display: flex; align-items: center; justify-content: center; background: #fff; position: relative; z-index: 1; }
.tl .tx .t { font-size: 31px; font-weight: 800; color: #20384a; }
.tl .tx .s { font-size: 25px; color: #5d6c75; margin-top: 2px; line-height: 1.45; }
.tl::before { content: ''; position: absolute; left: 195px; top: 30px; bottom: 30px; width: 4px; background: #e3e9ee; }
/* map */
.map a { display: flex; align-items: center; gap: 16px; padding: 15px 0; border-bottom: 2px dashed #e3e7ea; }
.map a:last-child { border-bottom: none; }
.map .sg { flex: 0 0 160px; text-align: center; font-size: 24px; font-weight: 800; padding: 8px 0; border-radius: 14px; }
.map .o { flex: 0 0 300px; font-size: 26px; font-weight: 700; color: #20384a; line-height: 1.4; }
.map .f { flex: 1; font-size: 25px; color: #45555f; line-height: 1.45; }
"""

FIT = '''<script>
document.querySelectorAll('.page').forEach(function(pg){
  var z = pg.querySelector('.z'); if (!z) return;
  var target = pg.querySelector('.main') || z;
  var avail = target.clientHeight, h = target.scrollHeight;
  if (h > avail + 8) { var r = avail / h; target.style.zoom = r; pg.setAttribute('data-zoom', r.toFixed(3)); }
});
</script>'''

# ---------- blocks ----------
def blk(b, ch):
    t, v = b[0], b[1]
    if t == 'para': return f'<p class="para">{md(v)}</p>'
    if t == 'note': return f'<div class="note">{md(v)}</div>'
    if t == 'quote': return f'<div class="quote">{md(v)}</div>'
    if t == 'bullets': return '<ul class="bl">' + ''.join(f'<li>{md(i)}</li>' for i in v) + '</ul>'
    if t == 'flow':
        parts = []
        for k, (ic, ti, su) in enumerate(v):
            if k: parts.append(f'<div class="ar">{svg_arrow(ch["c"], 70)}</div>')
            parts.append(f'<div class="nd">{icon(ic, ch["c"], 58)}<div class="t">{md(ti)}</div><div class="s">{md(su)}</div></div>')
        return '<div class="flow">' + ''.join(parts) + '</div>'
    if t == 'pair':
        return '<div class="pair">' + ''.join(f'<div class="bx">{icon(ic, ch["c"], 56)}<div><div class="t">{md(ti)}</div><div class="s">{md(su)}</div></div></div>' for ic, ti, su in v) + '</div>'
    if t == 'steps':
        rows = []
        for n, it in enumerate(v, 1):
            h, _, s = it.partition('|')
            rows.append(f'<div class="st"><div class="n">{n}</div><div class="t">{md(h)}' + (f'<small>{md(s)}</small>' if s else '') + '</div></div>')
        return '<div class="steps">' + ''.join(rows) + '</div>'
    if t == 'compare':
        return '<div class="cmp">' + ''.join(
            f'<div class="col{" win" if c.get("win") else ""}"><h3>{md(c["name"])}</h3><ul>' + ''.join(f'<li>{md(i)}</li>' for i in c['items']) + '</ul>'
            + (f'<div class="vd">{md(c["verdict"])}</div>' if c.get('verdict') else '') + '</div>' for c in v) + '</div>'
    if t == 'cols3':
        return '<div class="cmp c3">' + ''.join(
            f'<div class="col{" win" if w else ""}"><h3>{md(n)}</h3><ul>' + ''.join(f'<li>{md(i)}</li>' for i in its) + '</ul></div>' for n, its, w in v) + '</div>'
    if t == 'pits':
        return '<div class="pits">' + ''.join(
            f'<div class="pit"><div class="x">{svg_x()}</div><div><div class="bad">{md(bd)}</div><div class="fix"><i>{svg_check(ch["a"], 26)}</i><span>{md(fx)}</span></div></div></div>' for bd, fx in v) + '</div>'
    if t == 'check': return checklist(v)
    if t == 'fxmap': return FXMAP_XHS if os.environ.get('XHS') else FXMAP
    if t == 'handoff': return handoff(v)
    if t == 'table':
        headers = v.get('headers') or []
        rows = v.get('rows') or []
        thead = '<tr>' + ''.join(f'<th>{md(h)}</th>' for h in headers) + '</tr>'
        body = ''.join('<tr>' + ''.join(f'<td>{md(c)}</td>' for c in row) + '</tr>' for row in rows)
        return f'<table class="tbl"><thead>{thead}</thead><tbody>{body}</tbody></table>'
    raise ValueError(t)

def checklist(items):
    rows = []
    for it in items:
        if it.startswith('#'): rows.append(f'<div class="grp">{md(it[1:].strip())}</div>'); continue
        st, tx = it[:3], it[4:]
        cls = {'[x]': 'done', '[~]': 'wip', '[ ]': 'todo'}[st]
        inner = svg_check('#fff', 28) if cls == 'done' else ''
        rows.append(f'<li class="{cls}"><span class="bx">{inner}</span>{md(tx)}</li>')
    return '<ul class="chk">' + ''.join(rows) + '</ul>'

def handoff(key):
    h = HANDOFF[key]; ch = CHD[key]; nx = CHD[NEXT[key]]
    style = f'--na:{nx["a"]};--nl:{nx["l"]};--nc:{nx["c"]}'
    return (f'<div class="hand" style="{style}"><div class="side o"><div class="lb">本站产出</div><div class="chips">'
            + ''.join(f'<span>{md(x)}</span>' for x in h['out']) + f'</div></div>{svg_arrow(nx["c"], 60)}'
            f'<div class="side n" style="flex:1.6"><div class="lb"><a href="#p{ANCHOR[nx["key"]]}">下一站 · {md(h["nxt"])}（P{ANCHOR[nx["key"]]}）</a> 需要</div><div class="chips">'
            + ''.join(f'<span>{md(x)}</span>' for x in h['need']) + '</div></div></div>')

# ---------- page plan ----------
PLAN = []  # (kind, chkey, data)
PLAN.append(('cover', None, None)); PLAN.append(('toc', None, None))
for ch in [c for c in CH if c['key'] != 'final']:
    PLAN.append(('div', ch['key'], None))
    for i, c in enumerate(CARDS[ch['key']], 1): PLAN.append(('card', ch['key'], (i, c)))
PLAN += [('timeline', 'final', None), ('map', 'final', None), ('master', 'final', None), ('series', None, None), ('license', None, None)]
TOTAL = len(PLAN)
ANCHOR = {}
CHPAGES = {}
for n, (k, ck, _) in enumerate(PLAN, 1):
    if ck:
        CHPAGES.setdefault(ck, []).append(n)
        if ck not in ANCHOR: ANCHOR[ck] = n

def nav(cur, n):
    order = [c['key'] for c in CH]
    ci = order.index(cur) if cur in order else -1
    pills = ''.join(f'<a class="pill{" on" if c["key"] == cur else (" done" if i < ci else "")}" style="--a:{c["a"]}" href="#p{ANCHOR[c["key"]]}">{c["nav"]}</a>'
                    for i, c in enumerate(CH))
    a = CHD[cur]['a'] if cur in CHD else NAVY
    return (f'<div class="nav"><div class="pills">{pills}</div><a class="home" href="#p2">← 目录</a></div>'
            f'<div class="prog" style="--a:{a}"><div style="width:{n / TOTAL * 100:.1f}%"></div></div>')

def footer(n, label=''):
    return (f'<div class="footer"><span>{SERIES}{(" · " + label) if label else ""}<br><span class="by">Haitao Pan | XWork Technologies LLC 服务支持</span>'
            + ('' if os.environ.get('XHS') else '<br><span class="by2">xworktech.com 开源平台方案</span>') + '</span>'
            f'<span><b>P{n}</b> / {TOTAL}</span></div>')

def wrap(n, inner, ch=None, navkey=None, cls='', label=''):
    c = ch or CHD['final']
    style = f'--c:{c["c"]};--a:{c["a"]};--l:{c["l"]}'
    navh = nav(navkey, n) if navkey else ''
    return f'<section class="page {cls}" id="p{n}" style="{style}">{navh}<div class="z">{inner}</div>{footer(n, label)}</section>'

def chap_range(k):
    p = CHPAGES[k]; return f'P{p[0]}–P{p[-1]}'

def cover(n):
    nodes = []
    icons = {'llc': 'building', 'ein': 'doc', 'mercury': 'bank', 'ms': 'monitor', 'apple': 'phone', 'gp': 'phone', 'fx': 'bank', 'final': 'check'}
    subs = {'llc': '成立文件', 'ein': '税务身份', 'mercury': '企业账户', 'ms': '公司开发者号', 'apple': '组织号', 'gp': '组织号', 'fx': '合规 · 汇丰电汇', 'final': '时间线 · 总清单'}
    for i, c in enumerate(CH):
        nodes.append(f'<a href="#p{ANCHOR[c["key"]]}" style="background:{c["l"]};color:{c["c"]}">{icon(icons[c["key"]], c["c"], 56)}'
                     f'<div class="t">{c["no"]} {c["nav"]}</div><div class="s">{subs[c["key"]]}</div></a>')
    nodes.append(f'<a href="#p2" style="background:#20384a;color:#fff">{icon("search", "#fff", 56)}<div class="t">目录索引</div><div class="s">点击跳转 · P2</div></a>')
    inner = (f'<div><span class="chip" style="background:#df654e;color:#fff">合集版</span><span class="chip" style="background:#eef2f4;color:#3b5a70">核对日期：{CHECKED}</span><span class="chip" style="background:#eef2f4;color:#3b5a70">版本 {VERSION}</span></div>'
             f'<h1 style="margin-top:34px">出海第一步<br>一人公司合规全流程</h1><div class="sub">{SUBTITLE}</div>'
             f'<p class="para">一条真实走过的路：8 月 5 日成立公司，10 月 8 日拿到 147C，截至 10 月 10 日，Mercury 企业账户已建立；再把 Microsoft、Apple、Google 三家公司开发者账号的攻略模板接在后面；第 07 章补全汇丰香港「全球转账」操作步骤。按顺序看，每一站都写清楚“下一站需要什么”。</p>'
             f'<div class="route">{"".join(nodes)}</div>'
             f'<div class="note" style="--a:#3b5a70">个人经历分享 + 官方公开资料整理，不构成法律或税务意见；平台规则以官方页面为准。</div>'
             f'<div class="tags">' + ''.join(f'<span>#{t}</span>' for t in ['独立开发者', '出海', '美国LLC', 'EIN', 'Mercury', 'DUNS', '开发者账号']) + '</div>')
    return wrap(n, inner, CHD['final'], None, 'cv', '封面')

def toc(n):
    rows = []
    for c in CH:
        rows.append(f'<a class="row" href="#p{ANCHOR[c["key"]]}"><div class="mi">{illus(c, 160)}</div><div class="tx"><div class="t" style="color:{c["c"]}"><b>{c["no"]}</b>{md(c["name"])}</div>'
                    f'<div class="s">{md(c["toc_sub"])}</div></div><div class="pg" style="color:{c["a"]}">{chap_range(c["key"])}</div></a>')
    inner = (f'<div class="kicker" style="color:#3b5a70">INDEX · 共 {TOTAL} 页</div><h1 style="margin-bottom:10px">目录索引</h1>'
             f'<p class="para" style="font-size:26px;margin-bottom:18px">点任一章节直接跳转；每页顶部导航条可切换章节，“← 目录”随时回到这里。</p>'
             f'<div class="toc">{"".join(rows)}</div>'
             f'<div class="para" style="font-size:24px;margin-top:10px"><a href="#p{TOTAL-1}">系列攻略 · P{TOTAL-1}</a>　·　<a href="#p{TOTAL}">版权与许可 · P{TOTAL}</a></div>')
    return wrap(n, inner, CHD['final'], 'toc', '', '目录')

def divider(n, k):
    c = CHD[k]
    mt = ''.join(f'<a href="#p{p}"><span><b>{i:02d}</b>{md(cd["toc"])}</span><em>P{p}</em></a>' for i, (cd, p) in enumerate(zip(CARDS[k], CHPAGES[k][1:]), 1))
    src = ''.join(f'<div><b>{md(a)}</b> · {md(b)}</div>' for a, b in c['src'])
    nx = CHD[NEXT[k]]
    inner = (f'<div class="big">{c["no"]}</div><div class="cap">CHAPTER {c["no"]} / {CH[-1]["no"]}</div><h1>{md(c["name"])}</h1><div class="sub">{md(c["sub"])}</div>'
             f'<div class="ill">{illus(c, 600)}</div>'
             f'<div class="mtoc">{mt}</div>'
             f'<div class="io"><span class="tag">本章产出</span>{md(c["out"])}<span style="color:#9aa9b3">→</span><span class="tag">喂给</span>{md(c["feeds"])}</div>'
             f'<div class="src"><b>官方来源</b>{src}</div>')
    return wrap(n, inner, c, k, 'dv', f'{c["no"]} {c["nav"]}')

def card(n, k, i, cd):
    c = CHD[k]
    main_blocks, hand = [], None
    for b in cd['blocks']:
        if b[0] == 'handoff': hand = b
        else: main_blocks.append(b)
    body = ''.join(blk(b, c) for b in main_blocks)
    hand_html = blk(hand, c) if hand else ''
    inner = (f'<div class="main"><div class="kicker">第 {c["no"]} 章 · {md(c["name"])} · {i} / {len(CARDS[k])}</div>'
             f'<h1><span class="sn">{i}</span>{md(cd["title"])}</h1>{body}</div>{hand_html}')
    return wrap(n, inner, c, k, '', f'{c["no"]} {c["nav"]}')

def timeline(n):
    c = CHD['final']; rows = []
    for d, t, s, st, k in TIMELINE:
        cc = CHD[k]
        dot = {'done': f'<div class="dot" style="border-color:{cc["a"]};background:{cc["a"]}">{svg_check("#fff", 24)}</div>',
               'wip': f'<div class="dot" style="border-color:{cc["a"]}"><span style="width:16px;height:16px;border-radius:50%;background:{cc["a"]}"></span></div>',
               'todo': f'<div class="dot" style="border-color:#b9c4cb"></div>'}[st]
        rows.append(f'<a href="#p{ANCHOR[k]}" style="--c:{cc["c"]}"><div class="dt">{md(d)}</div>{dot}<div class="tx"><div class="t">{md(t)}</div><div class="s">{md(s)}</div></div></a>')
    inner = (f'<div class="kicker">第 {CH[-1]["no"]} 章 · 时间线 & 总清单 · 1 / 3</div><h1><span class="sn">1</span>全流程时间线</h1>'
             f'<div class="tl">{"".join(rows)}</div>'
             f'<div class="note">从公司成立到 147C 共 64 天，是我的实际经历，不代表统一办理时长。Mercury 进度更新至 10 月 10 日复盘；规则核对日期 {CHECKED}。三家商店为攻略模板，状态以各自后台为准。</div>')
    return wrap(n, inner, c, 'final', '', f'{CH[-1]["no"]} 清单')

def mapcard(n):
    rows = ''.join(f'<a href="#p{ANCHOR[k]}"><span class="sg" style="background:{CHD[k]["l"]};color:{CHD[k]["c"]}">{md(s)}</span><span class="o">{md(o)}</span>{svg_arrow(CHD[k]["a"], 44)}<span class="f">{md(f)}</span></a>' for k, s, o, f in MAP)
    inner = (f'<div class="kicker">第 {CH[-1]["no"]} 章 · 时间线 & 总清单 · 2 / 3</div><h1><span class="sn">2</span>每一站，喂给下一站</h1>'
             f'<p class="para">EIN 之后我把工作分成四条线：<b>资金账户、企业信息、应用分发、线上收单</b>。它们之间的依赖关系是这样的：</p>'
             f'<div class="map">{rows}</div>'
             f'<div class="note" style="margin-top:18px">成立公司和拿到 EIN，不会自动完成平台审核；注册验证通过，也不等于应用审核通过。每一站都单独验收。</div>')
    return wrap(n, inner, CHD['final'], 'final', '', f'{CH[-1]["no"]} 清单')

def master(n):
    inner = (f'<div class="kicker">第 {CH[-1]["no"]} 章 · 时间线 & 总清单 · 3 / 3</div><h1><span class="sn">3</span>出海基建总清单</h1>'
             + checklist(MASTER) +
             f'<div class="note">个人经历分享，具体税务问题请结合自身情况咨询专业人士。哪怕只是一只迎风扑腾的小鸟，找回属于自己的天空，也胜过一眼望到头的工位。</div>')
    return wrap(n, inner, CHD['final'], 'final', '', f'{CH[-1]["no"]} 清单')

FXMAP = ('<div class="fxm">'
  '<div class="bx">大陆个人账户<small>购汇 · 用途申报</small></div><div class="bx">本人香港个人账户<small>汇丰（HSBC）</small></div><div class="bx">LLC 海外公户<small>Mercury</small></div>'
  '<div class="ar no">✕ <span class="x">大陆个人账户 ⇄ 海外公户（LLC）</span><span class="st">禁止 · 双向</span></div>'
  '<div class="ar wt">① 大陆 → 香港：本人购汇 / 汇款，如实申报用途（外汇局规则已核对）<span class="st">按规则办理</span></div>'
  '<div class="ar wt">② 香港汇出端：汇丰网上理财「全球转账」操作步骤已整理（限额 / 费用仍待核实）<span class="st">步骤已整理</span></div>'
  '<div class="ar ok">③ 成员出资 → Mercury 收款端（书面答复）<span class="st">已确认</span></div>'
  '<div class="ar wt">④ 分红 / 利润分配 → 本人香港个人户<span class="st">待确认</span></div>'
  '<div class="ar wt">⑤ 税务处理（大陆 / 香港 / 美国）<span class="st">待确认</span></div>'
  '</div>')

FXMAP_XHS = ('<div class="fxm">'
  '<div class="bx">大陆个人账户<small>本册不涉及</small></div><div class="bx">本人香港个人账户<small>香港闭环</small></div><div class="bx">LLC 海外公户<small>美国闭环</small></div>'
  '<div class="ar no">✕ <span class="x">大陆个人账户 ⇄ 海外公户（LLC）</span><span class="st">禁止 · 双向</span></div>'
  '<div class="ar ok">渠道一：成员出资（本人香港个人账户 → LLC）· 收款端政策<span class="st">已确认</span></div>'
  '<div class="ar wt">渠道二：分红 / 利润分配（LLC → 本人香港个人账户）<span class="st">待确认</span></div>'
  '<div class="ar wt">香港银行侧核查要求<span class="st">待确认</span></div>'
  '<div class="ar wt">税务处理（大陆 / 香港 / 美国）<span class="st">待确认</span></div>'
  '</div>')

def series_page(n):
    xhs = bool(os.environ.get('XHS')); rows = []
    for t, v, d, u in SERIES_BOOKS:
        if u and not xhs: lk = f'<a href="{u}" style="color:#0058bd;text-decoration:underline">在 Google Drive 打开 PDF</a>'
        elif u: lk = ''
        else: lk = '<span style="color:#7c8a93">本书</span>'
        rows.append(f'<div class="note" style="--a:#3b5a70;margin-bottom:16px"><b style="font-size:30px">{t}</b> <span class="chip" style="background:#eef2f4;color:#3b5a70">{v}</span>'
                    f'<div style="margin-top:8px">{d}</div>' + (f'<div style="margin-top:8px;font-size:22px">{lk}</div>' if lk else '') + '</div>')
    inner = ('<div class="kicker" style="color:#3b5a70">SERIES</div><h1>系列攻略</h1>'
             '<p class="para">同一作者的四本图文书，可按兴趣挑着读：</p>' + ''.join(rows))
    return wrap(n, inner, CHD['final'], None, '', '系列攻略')

def license_page(n):
    inner = ('<div class="kicker" style="color:#3b5a70">COPYRIGHT & LICENSE</div><h1>版权与许可</h1>'
             f'<p class="para">《{TITLE}》</p>'
             '<p class="para"><b>文字与插图</b>：采用 CC BY-SA 4.0（署名-相同方式共享 4.0 国际）许可，转载、改编请注明作者与出处。</p>'
             '<p class="para"><b>代码与脚本</b>：采用 Apache License 2.0 许可。</p>'
             '<p class="para">作者：Haitao Pan</p>'
             '<div class="note" style="--a:#3b5a70">个人经历分享 + 官方公开资料整理，不构成法律或税务意见；平台与监管规则以官方页面为准。</div>')
    return wrap(n, inner, CHD['final'], None, '', '版权与许可')

def build():
    pages = []
    for n, (kind, k, d) in enumerate(PLAN, 1):
        if kind == 'cover': pages.append(cover(n))
        elif kind == 'toc': pages.append(toc(n))
        elif kind == 'div': pages.append(divider(n, k))
        elif kind == 'card': pages.append(card(n, k, *d))
        elif kind == 'timeline': pages.append(timeline(n))
        elif kind == 'map': pages.append(mapcard(n))
        elif kind == 'master': pages.append(master(n))
        elif kind == 'series': pages.append(series_page(n))
        elif kind == 'license': pages.append(license_page(n))
    doc = f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{TITLE}</title><style>{CSS}</style></head><body>{"".join(pages)}{FIT}</body></html>'
    hp = BUILD / 'collection.html'; hp.write_text(doc, encoding='utf-8')
    raw = BUILD / 'collection.raw.pdf'
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    '--virtual-time-budget=5000', f'--print-to-pdf={raw}', hp.as_uri()], check=True, capture_output=True)
    dom = subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--window-size=1080,1440',
                          '--virtual-time-budget=5000', '--dump-dom', hp.as_uri()], capture_output=True, text=True).stdout
    zooms = re.findall(r'id="p(\d+)"[^>]*data-zoom="([0-9.]+)"|data-zoom="([0-9.]+)"[^>]*id="p(\d+)"', dom)
    print('zoomed:', zooms)
    add_outline(raw, OUT / 'collection.pdf')
    pngdir = OUT / 'png'
    if pngdir.exists(): shutil.rmtree(pngdir)
    pngdir.mkdir()
    subprocess.run(['pdftoppm', '-png', '-r', '96', str(OUT / 'collection.pdf'), str(pngdir / 'p')], check=True)
    for f in sorted(pngdir.glob('p-*.png')):
        num = int(f.stem.split('-')[1]); f.rename(pngdir / f'{num:02d}.png')
    print('pages', TOTAL)

def add_outline(src, dst):
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter(clone_from=str(src))
    w.add_metadata({'/Title': f'{TITLE}：{SUBTITLE}', '/Author': 'Haitao Pan'})
    w.add_outline_item('封面', 0); w.add_outline_item('目录索引', 1)
    for c in CH:
        pg = CHPAGES[c['key']]
        par = w.add_outline_item(f'{c["no"]} {c["name"]}（{chap_range(c["key"])}）', pg[0] - 1, bold=True)
        if c['key'] == 'final':
            titles = ['全流程时间线', '每一站，喂给下一站', '出海基建总清单']
            for t, p in zip(titles, pg): w.add_outline_item(f'{t}（P{p}）', p - 1, parent=par)
        else:
            w.add_outline_item(f'章节页（P{pg[0]}）', pg[0] - 1, parent=par)
            for cd, p in zip(CARDS[c['key']], pg[1:]): w.add_outline_item(f'{cd["title"]}（P{p}）', p - 1, parent=par)
    w.add_outline_item(f'系列攻略（P{TOTAL-1}）', TOTAL - 2)
    w.add_outline_item(f'版权与许可（P{TOTAL}）', TOTAL - 1)
    w.page_mode = '/UseOutlines'
    with open(dst, 'wb') as f: w.write(f)

if __name__ == '__main__':
    build()
