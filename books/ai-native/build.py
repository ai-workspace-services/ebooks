#!/usr/bin/env python3
"""一键重建《AI-Native 超级个体 · 新时代游戏》: python3 build.py [--version v0.1]
_build/content.py -> HTML -> headless Chrome PDF -> pypdf 书签 -> dist/"""
import argparse, base64, html, pathlib, re, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '_build'))
import content as C, ws as W
ap = argparse.ArgumentParser(); ap.add_argument('--version', default=(ROOT / 'VERSION').read_text().strip()); a = ap.parse_args()
V = a.version; E = html.escape
def img(n): return 'data:image/jpeg;base64,' + base64.b64encode((ROOT / 'assets' / 'jpg' / f'0{n}.jpg').read_bytes()).decode()

pages = []   # (bookmark title or None, html inner, label)
TIGHT={'03 装备库 · 3.6 作者推荐':.86,'03 装备库 · 3.5 全家桶':.82,'03 装备库 · 对照表':.86,'目录（续）':.84,'02 主城 · 作者实战经验':.8,'1.4 关卡插画 · 2026-10 装备版':.86,**{f'03 装备库 · 3.{i}':.8 for i in (1,2,3,4,6)},'02 架构':.9,'03 Google AI · 2026-02-06 版':.92,'附录 B':.92,'02 主城 AI Workspace · 攻略':.93}
def add(inner, label='', bm=None, cls=''):
    if label in TIGHT: inner=f'<div style="zoom:{TIGHT[label]}">{inner}</div>'
    pages.append(dict(inner=inner, label=label, bm=bm, cls=cls))

# 封面
add(f'''<div class="gcv"><img src="{ROOT/'assets'/'jpg'/'cover-v07.jpg'}">
<div class="gtt"><div class="ck">AI-NATIVE SUPER INDIVIDUAL · {V}</div><h1 class="ct">AI-Native 超级个体<br>· 新时代游戏 ·</h1><div class="cs">{E(C.SUB)}</div></div>
<div class="gwel">欢迎来到 AI-Native 超级个体新手村</div>
<div class="gstart">▶ 开始游戏　·　进入新手村</div>
<div class="gau"><b>Haitao Pan</b>　·　XWork Technologies LLC 解决方案支持</div></div>''', bm='封面', cls='nofoot')
MAP_IDX=len(pages); add('', '世界地图', bm='AI-Native 世界地图', cls='nofoot')
add('', '目录', bm='目录')  # TOC 占位，稍后填
add('', '目录（续）')
TOC_IDX = next(i for i,p in enumerate(pages) if p['label']=='目录')
GL=[('新手村','01 章 1.1–1.2：看清世界地图与版本更新'),('职业 / 天赋','1.3、1.5：五层能力与转型路线'),('技能树 · 装备栏','1.4 五大模块；03 章工具与最新模型'),('主城基地','02 章：AI Workspace 架构'),('主线任务 · Boss 门','04 章：W0–W6 任务卡与 G0–G6 阶段门'),('副本 / 关卡','05 章：作者的 4 条 AI 工作流'),('经验值 · 存档','1.6 资产复利；2.6 三级记忆；06 章开局存档；版本号 v0.x'),('通关条件 · 道具鉴定','4.2 十项验收；4.3 E0–E5 证据等级')]
add(f'''<div class="kicker">GAME MANUAL · 游戏说明书</div><h1>开局前先读：玩法说明</h1>
<p>这是一本<b>攻略书</b>：从新手村出发，选职业、点技能树、配装备，建好主城，再去刷主线和副本。路线：<b>01 新手村</b>（1.1–1.6）→ <b>02 主城 AI Workspace</b> → <b>03 装备库</b> → <b>04 主线任务</b> → <b>05 副本：我的 AI 工作流</b> → <b>06 开局存档</b>。</p>
{''.join(f'<div class="it"><b>{E(a)}</b><span>{E(b)}</span></div>' for a,b in GL)}
<p>01、06 章以《AI-Native 超级个体成长计划》图文为骨架；02、04 章与附录精简自{E(W.WP)}（v0.2-plan，2026-10-23 评审稿）；03 章按厂商整理各阵营能力，摘自官方文档（信息截至 2026-10-23）；05 章副本来自作者「我的 AI 工作流」4 集泳道图视频底稿。</p>
<div class="note"><b>道具鉴定（证据等级）</b>：E0 = 规划，E4 = 已合并到主干。书中凡未标 E4 的架构内容均为规划（E0）。<br><b>信息截至</b>：模型与产品信息截至 {C.MODEL_DATE}；第 03 章只写官方文档可查的能力，价格与额度以官方页面为准。</div>
''', '游戏说明书', bm='游戏说明书')

# 07.jpg 已裁去含价格字样的上半部分（v0.3）
import game as GM
def tips3(pit, egg, tip):
    return (f'<div class="gbox pit"><b>⚠ 踩坑提示</b>{pit}</div><div class="gbox egg"><b>★ 隐藏彩蛋</b>{egg}</div>'
            f'<div class="gbox win"><b>✔ 通关小贴士</b>{tip}</div>')
def entry(k, num, title, quote):
    add(f'''<div class="gcv"><img src="{ROOT/'assets'/'jpg'/f'entry-{k}.jpg'}"><div class="ebx"><div class="enum">CHAPTER {num} · 第 {num} 章</div><h1 class="eti">{E(title)}</h1><div class="eq">「{E(quote)}」</div></div></div>''',
        f'{num} 入口页', bm=f'{num} {title}', cls='nofoot')
def chapter(i, n):
    t, items, side, concl = C.MAPS[i]
    z, gt, lead, paras, pit, egg, tip = GM.CH[i]
    sec = f'1.{n}' if i < 6 else ''
    kk = f'第 01 章 · {sec} {E(z)}' if sec else f'第 06 章 · {E(z)}'
    add(f'<div class="kicker">{kk}</div><h1>{E(gt)}</h1><div class="lead">{lead}</div>' + ''.join(f'<p>{x}</p>' for x in paras),
        f'{sec or "06"} {z}', bm=(f'　{sec} {gt}' if sec else None))
    mp = ''.join(f'<div class="mi">{E(x)}</div>' for x in items)
    add(f'<div class="kicker">{kk} · 攻略卡</div><h1>{E(z)}攻略卡</h1>'
        + f'<div class="map"><div class="mt">要点图 · {E(t)}</div>{mp}' + (f'<div class="ms">{E(side)}</div>' if side else '')
        + f'<div class="mc">{E(concl)}</div></div>' + tips3(pit, egg, tip), f'{sec or "06"} 攻略卡')
    if i == 3:
        exec(open(ROOT / '_build' / 'tools_card.py').read()); return
    if i == 6:
        exec(open(ROOT / '_build' / 'ch06_art.py').read()); return
    add(f'<div class="full"><img src="{img(i+1)}"></div>', f'{sec or "06"} 原图 · 关卡插画')
entry(1, '01', '新手村', '从世界地图到战利品：先看清版本、选好职业、点亮技能树。')
for i in range(6): chapter(i, i + 1)
exec(open(ROOT / '_build' / 'chapters.py').read())
add(f'''<div class="kicker">COPYRIGHT & LICENSE</div><h1>版权与许可</h1>
<p><b>《{E(C.TITLE)}》{V}</b>　作者 Haitao Pan　·　XWork Technologies LLC 解决方案支持</p>
<p>正文文字采用 <b>CC BY-SA 4.0</b>（署名-相同方式共享 4.0 国际）许可；书中代码与构建脚本采用 <b>Apache License 2.0</b>。</p>
<h2>说明</h2>
<div class="it"><b>内容</b><span>全书文字、图解与攻略内容均为 Haitao Pan 原创整理，XWork Technologies LLC 解决方案支持；含《AI-Native 超级个体成长计划》、AI Workspace 白皮书规划 v0.2-plan 与「我的 AI 工作流」4 集泳道图视频底稿。</span></div>
<div class="it"><b>模型来源</b><span>第 03 章各厂商官方文档、价格页与更新日志（OpenAI、Anthropic、xAI、Google、DeepSeek、Qwen、Kimi、智谱、MiniMax、Meta、Mistral；核实于 2026-10-23，清单见源码包 sources 目录）。</span></div>
<div class="it"><b>商标</b><span>Google、Gemini、OpenAI、Claude、Grok、DeepSeek 等为其各自权利人的商标，本书与相关公司无关联。</span></div>
<div class="note">模型信息截至 {C.MODEL_DATE}；产品功能与额度以官方页面为准。本书不构成任何投资或职业承诺。</div>''', '版权与许可', bm='版权与许可')
TOTAL = len(pages)
def lv2(b): return b.startswith('　') or b.startswith('副本') or b.startswith('W5') or b.startswith('3.1')
PG={p['bm'].strip('　'):i+1 for i,p in enumerate(pages) if p['bm']}
ents=[(p['bm'].strip('　'),i+1,lv2(p['bm'])) for i,p in enumerate(pages) if p['bm'] and p['bm'] not in ('封面','目录','AI-Native 世界地图')]
def row(t,n,l2): return f'<div class="tr {"t2" if l2 else "t1"}"><span class="tt">{E(t)}</span><span class="dl"></span><span class="tn">P{n}</span></div>'
SPLIT=next(k for k,e in enumerate(ents) if e[0].startswith('03'))
pages[TOC_IDX]['inner'] = '<div class="kicker">CONTENTS</div><h1>目录</h1><div class="toc1">'+''.join(row(*e) for e in ents[:SPLIT])+'</div>'
pages[TOC_IDX+1]['inner'] = '<div class="kicker">CONTENTS · 续</div><h1>目录（续）</h1><style>.tc2 .tr.t1{padding:6px 0 3px}.tc2 .tr.t2{padding:2px 0 2px 48px}</style><div class="toc1 tc2">'+''.join(row(*e) for e in ents[SPLIT:])+'</div>'
def pr(a,b=None): return f'P{PG[a]}' if not b else f'P{PG[a]}–{PG[b]-1}'
ch=lambda k: next(t for t in PG if t.startswith(k))
RG=[('新手村','01 章 · 1.1–1.6',pr(ch('01 ')),60,1215),('主城 AI Workspace','02 章',pr(ch('02 ')),700,915),('装备库','03 章',pr(ch('03 ')),50,830),
('主线 Boss 门','04 章 · W0–W6 / G0–G6',pr(ch('04 ')),690,500),('副本 1–4','05 章 · 我的 AI 工作流',pr(ch('05 ')),330,455),('开局存档','06 章',pr(ch('06 ')),560,40)]
mk=''.join(f'<div class="mlab" style="left:{x}px;top:{y}px"><b>{a}</b><span>{b} · {c}</span></div>' for a,b,c,x,y in RG)
pages[MAP_IDX]['inner']=f'''<div class="gcv"><img src="{ROOT/'assets'/'jpg'/'map-v07.jpg'}">{mk}
<div class="mroute">路线：新手村 → 主城 → 装备库 → Boss 门 → 副本 → 开局存档</div></div>'''
CSS = '''@page{size:1080px 1440px;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'Noto Sans CJK SC',sans-serif;color:#24323c;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:1080px;height:1440px;position:relative;overflow:hidden;page-break-after:always;padding:80px 80px 150px;background:#fbfcfd}
.kicker{color:#2f6df6;font-weight:800;letter-spacing:3px;font-size:22px}h1{font-size:54px;margin:10px 0 22px;color:#132a3e}h2{font-size:34px;color:#1d4fd8;margin:26px 0 6px}
p{font-size:27px;line-height:1.75;margin:0 0 16px}.lead{font-size:30px;font-weight:700;color:#1d4fd8;border-left:8px solid #2f6df6;padding:6px 0 6px 20px;margin-bottom:26px}
.map{margin-top:22px;background:#eef4ff;border-radius:22px;padding:24px 30px}.mt{font-weight:800;color:#2f6df6;font-size:24px;margin-bottom:10px}.mi{font-size:25px;padding:6px 0;border-bottom:1px dashed #c6d5f5}.ms{font-size:22px;color:#55657a;margin-top:10px}.mc{font-size:27px;font-weight:800;color:#132a3e;margin-top:12px}
.note{background:#fff7e6;border-left:8px solid #f0a020;padding:18px 24px;font-size:24px;line-height:1.6;border-radius:10px;margin:22px 0}.quote{font-size:36px;font-weight:800;text-align:center;color:#1d4fd8;margin-top:60px}
.src{font-size:20px;color:#7c8a93;margin-bottom:8px}.it{display:flex;gap:18px;font-size:24px;line-height:1.6;padding:10px 0;border-bottom:1px solid #e6eaec}.it b{flex:0 0 230px;color:#132a3e}
table.lm{width:100%;border-collapse:collapse;font-size:26px;margin-top:10px}table.lm td,table.lm th{border:1px solid #d5dde6;padding:14px 18px;text-align:left}table.lm th{background:#2f6df6;color:#fff}
.toc1 .tr{align-items:baseline;white-space:nowrap}.tr .dl{flex:1;border-bottom:3px dotted #b8c4cc;margin:0 14px}.tr.t1{font-size:29px;font-weight:800;color:#132a3e;padding:13px 0 9px;border:0}.tr.t2{font-size:24px;padding:7px 0 7px 48px;color:#3a4b58;border:0}.tr .tt{overflow:hidden;text-overflow:clip}.tr{display:flex;justify-content:space-between;font-size:28px;padding:13px 0;border-bottom:1px dotted #b8c4cc}
.full{position:absolute;left:0;right:0;top:40px;bottom:130px;display:flex;justify-content:center}.full img{height:100%;border-radius:18px;box-shadow:0 6px 24px rgba(0,0,0,.12)}
.gcv{position:absolute;inset:0;overflow:hidden}.gcv>img{width:100%;height:100%;object-fit:cover;display:block}.gtt{position:absolute;left:150px;right:150px;top:200px;text-align:center;background:rgba(255,255,255,.84);border-radius:28px;padding:18px 30px 26px;box-shadow:0 8px 30px rgba(0,0,0,.18)}.gtt .ct{font-size:72px;margin:8px 0;color:#0f2d4a}.gtt .cs{font-size:27px;color:#2c4a63}.gwel{position:absolute;left:0;right:0;top:610px;margin:auto;width:660px;text-align:center;background:linear-gradient(90deg,#f6b73c,#f08a24);color:#fff;font-size:34px;font-weight:800;padding:14px 0;border-radius:40px;box-shadow:0 6px 18px rgba(0,0,0,.25)}.gstart{position:absolute;left:0;right:0;bottom:170px;margin:auto;width:600px;text-align:center;background:#1fa37a;color:#fff;font-size:36px;font-weight:800;padding:16px 0;border-radius:18px;border:4px solid #fff;box-shadow:0 6px 18px rgba(0,0,0,.3)}.gau{position:absolute;left:0;right:0;bottom:0;padding:30px 0;text-align:center;font-size:30px;color:#fff;background:rgba(15,45,74,.8)}.mlab{position:absolute;background:rgba(255,255,255,.9);border:3px solid #c99a3b;border-radius:16px;padding:8px 18px;box-shadow:0 4px 12px rgba(0,0,0,.2)}.mlab b{display:block;font-size:30px;color:#0f2d4a}.mlab span{font-size:21px;color:#7a5a1c}.mroute{position:absolute;left:40px;right:40px;bottom:30px;text-align:center;background:rgba(15,45,74,.82);color:#fff;font-size:25px;padding:12px;border-radius:14px}.ebx{position:absolute;left:70px;right:70px;top:110px;text-align:center;background:rgba(255,255,255,.86);border-radius:28px;padding:26px 36px 30px;box-shadow:0 8px 30px rgba(0,0,0,.18)}.enum{color:#2f6df6;font-weight:800;letter-spacing:6px;font-size:24px}.eti{white-space:nowrap;font-size:42px;line-height:1.25;margin:10px 0 14px;color:#0f2d4a}.eq{font-size:28px;color:#7a5a1c;font-weight:700}.cover{text-align:center}.ck{color:#2f6df6;font-weight:800;letter-spacing:4px;font-size:22px;margin-top:10px}.ct{font-size:76px;line-height:1.2;margin:18px 0}.cs{font-size:28px;color:#55657a}.tbd{display:inline-block;margin-top:14px;background:#fff0f0;color:#c0392b;font-size:20px;padding:4px 14px;border-radius:20px}
.cimg{height:820px;margin-top:26px;border-radius:18px;box-shadow:0 6px 24px rgba(0,0,0,.15)}.ca{font-size:28px;margin-top:30px}
.gbox{border-radius:14px;padding:16px 22px;margin:14px 0;font-size:23px;line-height:1.6}.gbox b{display:block;font-size:22px;margin-bottom:4px}.pit{background:#fff0ef;border-left:8px solid #d9534f}.egg{background:#f4efff;border-left:8px solid #7b5cd6}.win{background:#eafaf0;border-left:8px solid #2e9e5b}.gp p{font-size:25px}.tocw{column-count:2;column-gap:40px}.tocw .tr{padding:6px 0!important;font-size:19px!important;break-inside:avoid}.mt2 td,.mt2 th{font-size:19px!important;padding:7px 10px!important}.chip{display:inline-block;background:#e8f0ff;color:#1d4fd8;font-size:20px;padding:4px 14px;border-radius:20px;vertical-align:middle;margin:4px}.chip.big{font-size:22px}table.lm td{font-size:23px}.footer{position:absolute;left:60px;right:60px;bottom:34px;border-top:2px solid #e6eaec;padding-top:14px;display:flex;justify-content:space-between;font-size:22px;color:#7c8a93}.footer .by{font-size:19px;color:#4f5f69}.footer .by2{font-size:17px;color:#9aa9b3}'''
def foot(n, lab): return (f'<div class="footer"><span>{E(C.TITLE)}{(" · " + E(lab)) if lab else ""}<br><span class="by">Haitao Pan | XWork Technologies LLC 解决方案支持</span>'
                          f'<br><span class="by2">xworktech.com 开源平台方案</span></span><span>{V}　P{n} / {TOTAL}</span></div>')
H = '<!doctype html><html><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>' + ''.join(
    f'<section class="page">{p["inner"]}{"" if p["cls"]=="nofoot" else foot(i+1, p["label"])}</section>' for i, p in enumerate(pages)) + '</body></html>'
DIST = ROOT / 'dist'; WORK = DIST / '_work'; shutil.rmtree(WORK, ignore_errors=True); WORK.mkdir(parents=True)
(WORK / 'book.html').write_text(H)
subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={WORK/"raw.pdf"}', (WORK / 'book.html').as_uri()], check=True, capture_output=True)
from pypdf import PdfReader, PdfWriter
w = PdfWriter(clone_from=str(WORK / 'raw.pdf'))
par = None
for i, p in enumerate(pages):
    if p['bm']:
        if lv2(p['bm']) and par is not None: w.add_outline_item(p['bm'].strip('　'), i, parent=par)
        else: par = w.add_outline_item(p['bm'].strip('　'), i)
w.add_metadata({'/Title': C.TITLE + ' ' + V, '/Author': 'Haitao Pan'})
out = DIST / f'AI-Native超级个体-新时代游戏-{V}.pdf'; w.write(str(out))
info = subprocess.run(['pdfinfo', str(out)], capture_output=True, text=True).stdout
n = int(re.search(r'Pages:\s+(\d+)', info).group(1)); assert n == TOTAL, (n, TOTAL)
txt = subprocess.run(['pdftotext', str(out), '-'], capture_output=True, text=True).stdout
assert not re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+|svc\.plus|行者深蓝|/home/|/workspace', txt), 'leak'
print(f'OK {out} {n} pages')
