#!/usr/bin/env python3
"""《人民币 ⇄ 海外卡 · 三条路线攻略》 builder: book.md + figs -> HTML -> Chrome PDF -> PyMuPDF footer/page no./bookmarks."""
import re,os,html,subprocess,json
import pymupdf as fitz
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
V=os.environ.get('BOOK_VERSION','v0.1')
TITLE='人民币 ⇄ 海外卡'; SUB='三条路线攻略'; AUTHOR='Haitao Pan'; SUPPORT='XWork Technologies LLC 服务支持'
OUT=os.path.join(ROOT,'dist',f'人民币海外卡三条路线攻略-{V}.pdf')
F="font-family:'Noto Sans CJK SC',sans-serif"
PAN='#e8f0fb'; PRI='#0058bd'; ACC='#4b43e8'; TT='#101c44'
def box(x,y,w,h,t,sub='',hi=False):
    fill='url(#g)' if hi else PAN; tc='#fff' if hi else TT; sc='#e8f0fb' if hi else '#46506e'
    cy=y+h/2+(-5 if sub else 5)
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{PRI}" stroke-width="1.5"/>'
    s+=f'<text x="{x+w/2}" y="{cy}" text-anchor="middle" font-size="14" font-weight="700" fill="{tc}" style="{F}">{html.escape(t)}</text>'
    if sub: s+=f'<text x="{x+w/2}" y="{cy+18}" text-anchor="middle" font-size="11" fill="{sc}" style="{F}">{html.escape(sub)}</text>'
    return s
def arr(x1,y1,x2,y2,l=''):
    s=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ACC}" stroke-width="2" marker-end="url(#ah)"/>'
    if l: s+=f'<text x="{(x1+x2)/2+6}" y="{(y1+y2)/2+4}" font-size="10.5" fill="{ACC}" style="{F}">{l}</text>'
    return s
def svg(w,h,b):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{ACC}"/></marker>'
            f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#075ecc"/><stop offset="1" stop-color="#4338ca"/></linearGradient></defs><rect width="{w}" height="{h}" rx="14" fill="#f8f9fa"/>{b}</svg>')
def vflow(steps,hi=()):
    h=len(steps)*62+20; b=''
    for i,(t,s) in enumerate(steps):
        y=14+i*62; b+=box(110,y,280,46,t,s,i in hi)
        if i: b+=arr(250,y-16,250,y-2)
    return svg(500,h,b)
def hflow(steps,hi=()):
    n=len(steps); w=(500-20-(n-1)*22)/n; b=''
    for i,(t,s) in enumerate(steps):
        x=10+i*(w+22); b+=box(x,20,w,64,t,s,i in hi)
        if i: b+=arr(x-20,52,x-3,52)
    return svg(500,104,b)
def branch(top,items,bottom=None):
    n=len(items); w=(480-(n-1)*14)/n; b=box(150,14,200,48,*top,hi=True); h=210 if bottom else 150
    for i,(t,s) in enumerate(items):
        x=10+i*(w+14); b+=box(x,96,w,56,t,s); b+=arr(250,62,x+w/2,94)
        if bottom: b+=arr(x+w/2,152,250,166)
    if bottom: b+=box(150,168,200,36,*bottom)
    return svg(500,h,b)
FIGS={
'overview':('图 01-1 三条路线与各自的前提',branch(('人民币 ⇄ 海外卡',''),[('香港','前提：本人赴港'),('菲律宾 Maya','前提：短信 eSIM'),('美国 Mercury','前提：海外 LLC')],('分工组合，而非互相替代',''))),
'ph':('图 03-1 DITO eSIM + Maya',hflow([('DITO eSIM','短信收码'),('Maya 注册','本人 KYC'),('中转入金','香港 / Wise'),('虚拟 Visa','小额订阅')],hi=(0,))),
'us':('图 04-1 Mercury 的前提链路',hflow([('美国 LLC','成立文件'),('EIN','147C'),('Mercury','材料审核'),('入金','本人香港户')],hi=(0,))),
'combo':('图 05-1 推荐组合：资金怎么走',vflow([('内地本人银行卡','年度购汇额度 · 如实申报'),('本人香港个人户','人民币枢纽'),('LLC Mercury 账户','成员出资 ⇄ 分红 · 美元营收'),('Maya 虚拟 Visa','经香港 / Wise 小额入金 · AI 订阅')],hi=(1,))),
}
def inl(s):
    s=html.escape(s); s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s); return re.sub(r'`(.+?)`',r'<code>\1</code>',s)
md=open(os.path.join(HERE,'book.md'),encoding='utf-8').read()
body=[]; toc=[]
for blk in re.split(r'\n\s*\n',md.strip()):
    b=blk.strip()
    if b.startswith(':::table'):
        rows=[[c.strip() for c in l.split('|')] for l in b.split('\n')[1:-1]]
        t='<table><tr>'+''.join(f'<th>{inl(c)}</th>' for c in rows[0])+'</tr>'+''.join('<tr>'+''.join(f'<td>{inl(c)}</td>' for c in r)+'</tr>' for r in rows[1:])+'</table>'; body.append(t)
    elif b.startswith(':::'):
        hd=b.split('\n')[0][3:].split(' ',1); kind=hd[0]; ttl=hd[1] if len(hd)>1 else ('注意' if kind=='warn' else '提示')
        inner=' '.join(b.split('\n')[1:-1]); body.append(f'<div class="call {kind}"><b>{inl(ttl)}</b><p>{inl(inner)}</p></div>')
    elif b.startswith('# '):
        t=b[2:]; i=len(toc); toc.append((1,t,f'p{i}'))
        if t=='前言': body.append(f'<h1 class="pre" id="p{i}">前言</h1>')
        else:
            p,_,n=t.partition(' '); body.append(f'<div class="part" id="p{i}"><div class="pk">{inl(p)}</div><div class="pn">{inl(n)}</div></div>')
    elif b.startswith('## '):
        t=b[3:]; i=len(toc); toc.append((2,t,f'p{i}')); n,_,tt=t.partition(' ')
        body.append(f'<div class="chopen" id="p{i}"><div class="chno">{"附录" if n=="附录" else "第 "+n+" 章"}</div><h1>{inl(tt)}</h1></div>')
    elif b.startswith('### '): body.append(f'<h2>{inl(b[4:])}</h2>')
    elif re.fullmatch(r'\[\[fig:(\w+)\]\]',b):
        c,s=FIGS[b[6:-2]]; body.append(f'<figure>{s}<figcaption>{html.escape(c)}</figcaption></figure>')
    elif re.match(r'\d+\. ',b): body.append('<ol>'+''.join(f'<li>{inl(re.sub(r"^\d+\. ","",l))}</li>' for l in b.split('\n'))+'</ol>')
    elif b.startswith('- '): body.append('<ul>'+''.join(f'<li>{inl(l[2:])}</li>' for l in b.split('\n'))+'</ul>')
    else: body.append(f'<p>{inl(b)}</p>')
cover=f'''<section class="cover"><div class="band"></div><div class="ctag">图解攻略 · 第六本</div><div class="ct">{TITLE}</div><div class="cs">{SUB}</div>
<div class="cdesc">香港 · 菲律宾 DITO eSIM + Maya · 美国 LLC + Mercury · 购汇额度 · 出资与回流</div>
<div class="cfig">{FIGS['overview'][1] if False else hflow([('人民币','内地本人卡'),('香港','枢纽'),('Mercury','美元营收'),('Maya','小额订阅')],hi=(1,))}</div>
<div class="cby">{AUTHOR}</div><div class="csup">{SUPPORT}</div><div class="cver">{V}</div></section>'''
_cv=os.path.join(ROOT,'assets','cover.png')
if os.path.exists(_cv):  # designed cover from Drive assets (assets.manifest.json); falls back to the HTML cover
    cover=f'<section class="imgcover"><img src="file://{_cv}"></section>'
tochtml='<section class="toc"><h1 class="pre">目录</h1>'+''.join(f'<div class="t{l}"><a href="#{a}">{inl(t)}</a><span class="pg" data-a="{a}"></span></div>' for l,t,a in toc)+'</section>'
CSS='''@page{size:A5;margin:16mm 14mm 18mm}@page:first{margin:0}.imgcover{height:210mm;width:148mm;display:flex;align-items:center;background:linear-gradient(#fbe3e9,#f8fafc);page-break-after:always;overflow:hidden}.imgcover img{width:148mm;display:block}body{font-family:'Noto Sans CJK SC',sans-serif;color:#1b2340;font-size:10pt;line-height:1.7}
.cover{page-break-after:always;height:170mm;position:relative;overflow:hidden;text-align:center}.band{height:10mm;background:linear-gradient(90deg,#075ecc,#4338ca);border-radius:6px}
.ctag{margin-top:14mm;color:#4b43e8;font-weight:700;letter-spacing:3px}.ct{font-size:30pt;font-weight:900;color:#101c44;margin-top:6mm}.cs{font-size:16pt;color:#0058bd;font-weight:700;margin-top:2mm}
h2,h3{break-after:avoid;page-break-after:avoid}.cdesc{font-size:8.5pt;color:#46506e;margin:8mm 6mm}.cfig svg{width:100%}.cby{margin-top:14mm;font-size:13pt;font-weight:700}.csup{color:#46506e;font-size:9pt}.cver{position:absolute;bottom:0;width:100%;color:#888;font-size:8pt}
h1.pre{color:#101c44;border-bottom:3px solid #4b43e8;padding-bottom:2mm}.toc{page-break-after:always}.toc a{color:#1b2340;text-decoration:none}.t1{font-weight:900;margin-top:3mm;color:#0058bd}.t2{padding-left:6mm;display:flex}.t2 a{flex:1}
.part{page-break-before:always;page-break-after:always;padding-top:55mm;text-align:center}.pk{font-size:26pt;font-weight:900;color:#4b43e8}.pn{font-size:20pt;font-weight:700;color:#101c44}
.chopen{page-break-before:always;border-left:6px solid #4b43e8;padding-left:4mm;margin-bottom:5mm}.chno{color:#4b43e8;font-weight:700}.chopen h1{margin:0;font-size:18pt;color:#101c44}
h2{color:#0058bd;font-size:12pt;margin:5mm 0 2mm}figure{margin:3mm 0;page-break-inside:avoid;text-align:center}figure svg{width:100%}figcaption{font-size:8pt;color:#46506e}
table{border-collapse:collapse;width:100%;font-size:8.3pt;margin:3mm 0;page-break-inside:avoid}th{background:#0058bd;color:#fff}th,td{border:1px solid #c9d6ee;padding:1.5mm;vertical-align:top}tr:nth-child(odd) td{background:#f3f7fd}
.call{border-radius:8px;padding:2mm 4mm;margin:3mm 0;page-break-inside:avoid}.call p{margin:1mm 0}.warn{background:#fff4e5;border-left:4px solid #e8890c}.tip{background:#e8f0fb;border-left:4px solid #0058bd}code{background:#eef;padding:0 2px}'''
doc=f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{cover}{tochtml}{"".join(body)}</body></html>'
os.makedirs(os.path.join(ROOT,'dist'),exist_ok=True); hp=os.path.join(ROOT,'dist','book.html'); open(hp,'w').write(doc)
tmp=OUT+'.tmp.pdf'
subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--no-pdf-header-footer',f'--print-to-pdf={tmp}','file://'+hp],check=True,capture_output=True)
d=fitz.open(tmp)
# locate anchors via Chrome named destinations
nm=d.resolve_names(); pages={a:nm[a]['page'] for _,_,a in toc if a in nm}
from fontTools import subset as _ss
FR=os.path.join(ROOT,'dist','_foot.otf'); _t=''.join(t for _,t,_ in toc)+AUTHOR+SUPPORT+'0123456789 |'
_o=_ss.Options(); _o.font_number=2; _f=_ss.load_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',_o); _s=_ss.Subsetter(_o); _s.populate(text=_t); _s.subset(_f); _f.save(FR)
Fo=fitz.Font(fontfile=FR)
for l,t,a in toc:
    if a in pages and l==2:
      for tocp in (d[1],d[2]):
        hits=tocp.search_for(t.partition(' ')[2][:12]) if tocp.number<pages['p0'] else []
        if hits: r=hits[0]; tocp.insert_font(fontname='cjk',fontfile=FR); s=str(pages[a]+1); tocp.insert_text((tocp.rect.width-40-Fo.text_length(s,fontsize=9),r.y1-2),s,fontname='cjk',fontsize=9,color=(0,.345,.741))
for i,p in enumerate(d):
    if i==0: continue
    r=p.rect; p.insert_font(fontname='cjk',fontfile=FR); g=(.29,.33,.45); ft=f'{AUTHOR} | {SUPPORT}'
    p.insert_text(((r.width-Fo.text_length(ft,fontsize=7))/2,r.height-20),ft,fontname='cjk',fontsize=7,color=g)
    n=str(i+1); p.insert_text((r.width-36-Fo.text_length(n,fontsize=8.5),r.height-20),n,fontname='cjk',fontsize=8.5,color=(0,.345,.741))
d.set_toc([[1,'封面',1],[1,'目录',2]]+[[l,t,pages[a]+1] for l,t,a in toc if a in pages])
d.save(OUT,garbage=4,deflate=True); os.remove(tmp)
json.dump({'pages':len(d),'anchors':{a:pages.get(a,0)+1 for _,_,a in toc}},open(os.path.join(ROOT,'dist','build-info.json'),'w'),ensure_ascii=False)
print(OUT,len(d))
