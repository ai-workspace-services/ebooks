#!/usr/bin/env python3
"""XHS free-teaser packs per chapter: covers, section list, 3 图解, short PDF, 文案.md."""
import os,re,sys,html,subprocess,base64
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); sys.path.insert(0,HERE)
from figs import FIGS; from figs_xhs import X; from outline import O; from xhs_copy import C
from quickstart import QS
from xhs_cover import cover
from PIL import Image
CH={'1':'从自由软件到平台工程','2':'Git 与 CI：一切从 commit 开始','3':'资源即代码：环境 apply 就出来','4':'交付引擎：幂等地把软件装上去','5':'安全与身份：没有共享账号，没有固定密码','6':'环境治理：SIT → UAT → PROD','7':'云中立：一套配置，任意部署','8':'可观测：平台的眼睛和手','9':'能恢复才算稳定','10':'AI 助手与 AI 接入平台'}
REUSE={'5':['fig1','fig2','fig4'],'6':['fig61','fig63','fig65']}
QSN={q[0]:q for q in QS}
DONE=os.environ.get('XHS_DONE','1,2,3,4,5,6').split(',')
md=open(os.path.join(HERE,'book.md'),encoding='utf-8').read()
def secs(n): return O[n][1] if n not in DONE else re.findall(r'^### ('+n+r'\.\d+ .+)$',md,re.M)
logo=open(os.path.join(ROOT,'assets','xwork-logo-mark.svg')).read().replace('width="22" height="22"','width="54" height="54"')
CSS='''@page{size:1080px 1440px;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'Noto Sans CJK SC',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:1080px;height:1440px;position:relative;overflow:hidden;background:#f8f9fa;padding:90px 84px;break-after:page}
.bk{font-size:30px;color:#0058bd;font-weight:700;letter-spacing:2px}.brand{position:absolute;left:84px;bottom:70px;display:flex;align-items:center;gap:16px;font-size:28px;color:#101c44;font-weight:700}
.pn{position:absolute;right:84px;bottom:80px;font-size:24px;color:#4b43e8}
.cv{background:#fbfcfe;color:#101c44}.cv .bk{color:#0058bd}.cv .brand{color:#101c44}.cv .tag{border-color:#4b43e8;color:#4b43e8}.cv .no{background:#4338ca;color:#fff}.cv .hook{border-left-color:#ff8a00;color:#33415c}.ov{display:block;width:912px;margin:34px 0 30px;border-radius:22px;box-shadow:0 8px 30px rgba(16,28,68,.12)}
.no{margin-top:70px;display:inline-block;background:#fff;color:#4338ca;font-size:40px;font-weight:700;padding:10px 34px;border-radius:40px}
.ct{font-size:68px;line-height:1.22;font-weight:900;margin:26px 0 0}.hook{font-size:34px;line-height:1.5;border-left:10px solid #fff;padding-left:28px;opacity:.95}
.tag{position:absolute;right:84px;top:90px;font-size:26px;border:2px solid #fff;border-radius:30px;padding:6px 24px}
h1{font-size:64px;color:#101c44;margin:30px 0 10px}.sub{font-size:30px;color:#4b43e8;margin-bottom:40px}
.it{font-size:36px;color:#101c44;padding:22px 30px;margin:14px 0;background:#e8f0fb;border-radius:18px;border-left:8px solid #0058bd}.it.q{border-color:#4b43e8;background:#fff;color:#4b43e8;font-weight:700}
.fg{margin-top:50px;background:#fff;border-radius:28px;padding:30px;box-shadow:0 6px 24px rgba(16,28,68,.08)}.fg svg{width:100%;height:auto;max-height:960px}
.fp{display:flex;flex-direction:column}.fp .fg{margin:auto 0 0}.fp .cap{margin:40px 0 auto;text-align:center}.cap{font-size:40px;color:#101c44;font-weight:700;margin-top:40px}'''
def figs_for(n): return [FIGS[k] for k in REUSE[n]] if n in REUSE else X[n]
NOLINK=lambda x:re.sub(r'postgresql\.svc\.plus','自建 PostgreSQL',x)
def pages(n):
    e=html.escape; done=n in DONE; t=CH[n]; nn=int(n)
    P=[f'<div class="pg cv"><div class="bk">图解平台工程 · 云中立实践</div><div class="tag">{"已写成" if done else "规划中 · 持续更新"}</div><div class="no">第 {n} 章</div><div class="ct">{e(t)}</div><img class="ov" src="{cover(n,os.path.join(ROOT,"xhs",f"ch{nn:02d}","_cov.png"))}"><div class="hook">{e(C[n]["hook"])}</div><div class="brand">{logo}Haitao Pan | XWork Technologies LLC 服务支持</div></div>']
    items=''.join(f'<div class="it">{e(s)}</div>' for s in secs(n))+(f'<div class="it q">🚀 快速开始：{e(QSN[n][2])}</div>' if n in QSN else '')
    P.append(f'<div class="pg"><div class="bk">图解平台工程 · 云中立实践</div><h1>第 {n} 章 目录</h1><div class="sub">{e(t)}</div>{items}<div class="pn">2 / 5</div></div>')
    for i,(cap,svg) in enumerate(figs_for(n)):
        P.append(f'<div class="pg fp"><div class="bk">图解平台工程 · 云中立实践 · 第 {n} 章</div><div class="fg">{svg}</div><div class="cap">{e(cap)}</div><div class="brand">{logo}Haitao Pan | XWork Technologies LLC 服务支持</div><div class="pn">{i+3} / 5</div></div>')
    return [NOLINK(p) for p in P]
NAMES=['01-首页','02-目录','03-图解1','04-图解2','05-图解3']
def chrome(args): subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars']+args,check=True,capture_output=True)
def build(n):
    d=os.path.join(ROOT,'xhs',f'ch{int(n):02d}'); os.makedirs(d,exist_ok=True)
    P=pages(n); wrap=lambda b:f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{b}</body></html>'
    for nm,p in zip(NAMES,P):
        hp=os.path.join(d,'_p.html'); open(hp,'w',encoding='utf-8').write(wrap(p))
        chrome(['--window-size=1080,1440',f'--screenshot={os.path.join(d,nm+".png")}',hp])
    hp=os.path.join(d,'_all.html'); open(hp,'w',encoding='utf-8').write(wrap(''.join(P)))
    chrome(['--no-pdf-header-footer',f'--print-to-pdf={os.path.join(d,f"ch{int(n):02d}-分章.pdf")}',hp])
    for f in ('_p.html','_all.html','_cov.png'): os.remove(os.path.join(d,f))
    c=C[n]; body=c['body']; cnt=len(re.sub(r'\s','',body))
    open(os.path.join(d,'文案.md'),'w').write(f'# {c["title"]}\n\n{body}\n\n{" ".join(c["tags"])}\n\n<!-- 标题 {len(c["title"])} 字；正文 {cnt} 字（不含空白） -->\n')
    return d,c['title'],cnt
if __name__=='__main__':
    out=[build(n) for n in CH]
    ims=[Image.open(os.path.join(d,'01-首页.png')).resize((270,360)) for d,_,_ in out]
    sheet=Image.new('RGB',(5*270+60,2*360+30),'#f8f9fa')
    for i,im in enumerate(ims): sheet.paste(im,(10+(i%5)*280,10+(i//5)*370))
    sheet.save(os.path.join(ROOT,'xhs','封面总览.png'))
    with open(os.path.join(ROOT,'xhs','文案汇总.md'),'w') as f:
        f.write('# 《图解平台工程 · 云中立实践》XHS 分章文案汇总\n\n')
        for (d,t,cnt),n in zip(out,CH): f.write(f'---\n\n## 第 {n} 章 · 标题 {len(t)} 字 · 正文 {cnt} 字\n\n'+open(os.path.join(d,'文案.md')).read().split('<!--')[0]+'\n')
    for d,t,cnt in out: print(os.path.basename(d),t,len(t),cnt)
