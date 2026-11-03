#!/usr/bin/env python3
"""《AI 工具出海通关 · 注册与订阅全流程》 builder: book.md + figs -> HTML -> Chrome PDF -> PyMuPDF footer/page no./bookmarks."""
import re,os,html,subprocess,json
import pymupdf as fitz
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
V=os.environ.get('BOOK_VERSION','v0.1')
TITLE='AI 工具出海通关'; SUB='注册与订阅全流程'; AUTHOR='Haitao Pan'; SUPPORT='XWork Technologies LLC 服务支持'
OUT=os.path.join(ROOT,'dist',f'AI工具出海通关-注册与订阅全流程-{V}.pdf')
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
'overview':('图 01-1 全书链路：每一层依赖上一层',vflow([('网络环境','XConnect · 三端'),('海外手机号','实体卡 / eSIM / 虚拟号'),('Gmail + 恢复邮箱','核心恢复入口'),('ChatGPT · Claude · Grok · Gemini','网页 / App / 桌面端'),('支付：官网直接填卡','Maya 虚拟 Visa（作者实测）'),('可选：应用内订阅','App Store · Google Play'),('开发工具（可选）','Codex / Claude Code / Cursor / Antigravity'),('订阅 · 续费 · 取消 · 恢复','')],hi=(0,7))),
'xconnect':('图 02-1 XConnect 上手流程',hflow([('下载','按设备选择'),('注册控制台','邮箱验证码'),('配置连接器','端点 · 账号'),('开始连接','iOS/Android/桌面'),('验证可达','Google·AI 服务')],hi=(4,))),
'phone':('图 03-1 手机号怎么选：可靠性从高到低',branch(('需要海外手机号','收验证码 · 账号恢复'),[('① 实体卡','首选 · 长期账号'),('② 短信 eSIM','次选 · 如 DITO'),('③ 虚拟号','仅临时 · 尽快替换')],('绑定后定期续费保号',''))),
'recovery':('图 04-1 恢复资料互相兜底',branch(('重要账号','Gmail · AI · 商店 · 支付'),[('恢复邮箱','独立链路'),('长期手机号','可续费'),('双因素 + 恢复码','密码管理器保存')])),
'gmail':('图 05-1 Gmail 注册与检查',hflow([('稳定网络','打开注册页'),('真实资料','独立密码'),('手机验证','长期号码'),('恢复邮箱','收发测试'),('2FA+恢复码','换设备登录')])),
'chatgpt':('图 06-1 ChatGPT：注册与三条订阅路径',branch(('Google 账号登录','必要时手机验证'),[('网页订阅','网页账单管理'),('iOS 订阅','App Store 管理'),('Android 订阅','Google Play 管理')])),
'claude':('图 07-1 Claude：注册与订阅',branch(('Gmail / Google 登录','邮箱 + 支持地区手机号'),[('网页/桌面','Billing 页面'),('iOS','App Store'),('Android','Google Play')],('扣款前 24 小时以上取消',''))),
'grok':('图 08-1 Grok 经由 X 账号进入',hflow([('X 账号','真实资料'),('邮箱/短信验证','长期可控'),('进入 Grok','网页 / App / 桌面端'),('确认订阅平台','记录扣款处')])),
'gemini':('图 09-1 一个 Google 账号，两类用法',branch(('本人 Google 账号','2FA · 恢复资料'),[('Gemini','网页 / App / 桌面端'),('Antigravity','Gemini 的开发工具 · IDE / CLI / SDK')],('分别核对计费路径',''))),
'payroutes':('图 10-1 三种可选支付方式',branch(('让订阅自动扣费',''),[('① Maya 虚拟 Visa','网页直接支付 · 主路线'),('② Apple Pay / Play','绑定 Visa · App 内订阅'),('③ 非大陆银行卡','含港澳')],('同一服务只保留一条路径',''))),
'combo':('图 11-1 DITO eSIM + Maya 的分工',hflow([('DITO eSIM','短信 · 收验证码'),('Maya 开户','本人实名验证'),('开虚拟 Visa','充值'),('官网直接填卡','作者实测'),('订阅','记录账单归属')],hi=(0,3))),
'apple':('图 12-1 可选：App Store 应用内订阅',hflow([('Apple ID','地区=实际'),('双因素','认证'),('添加 Visa','3-D Secure'),('App 内订阅','确认方案'),('设置→订阅','核对续费')])),
'play':('图 13-1 可选：Google Play 应用内订阅',hflow([('登录 Play','本人 Gmail'),('核对地区','所在地一致'),('付款方式','Visa / Maya'),('App 内订阅','核对账号'),('付款和订阅','保存订单号')])),
'trouble':('图 附-1 先定位是哪一段出了问题',branch(('出问题了','先记录报错与时间'),[('打不开','网络 / DNS / 代理'),('收不到码','号码 / 短信 / 频率'),('登录报错','账号 / 组织策略'),('付款失败','地区 / 卡 / 重复订阅')])),
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
<div class="cdesc">网络 · 手机号 · Gmail · ChatGPT · Claude · Grok · Gemini · Codex · Claude Code · Cursor · Antigravity · App Store · Google Play</div>
<div class="cfig">{FIGS['overview'][1] if False else hflow([('网络','XConnect'),('手机号','eSIM'),('账号','Gmail'),('注册','AI 服务'),('支付','官网填卡')],hi=(4,))}</div>
<div class="cby">{AUTHOR}</div><div class="csup">{SUPPORT}</div><div class="cver">{V}</div></section>'''
tochtml='<section class="toc"><h1 class="pre">目录</h1>'+''.join(f'<div class="t{l}"><a href="#{a}">{inl(t)}</a><span class="pg" data-a="{a}"></span></div>' for l,t,a in toc)+'</section>'
CSS='''@page{size:A5;margin:16mm 14mm 18mm}body{font-family:'Noto Sans CJK SC',sans-serif;color:#1b2340;font-size:10pt;line-height:1.7}
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
