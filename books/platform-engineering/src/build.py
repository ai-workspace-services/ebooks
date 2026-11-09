#!/usr/bin/env python3
"""《图解平台工程 · 云中立实践》 builder: book.md + figs.py -> HTML -> Chrome PDF -> PyMuPDF (footer, page no., TOC numbers, bookmarks)."""
import re, os, sys, html, json, subprocess, base64, datetime
import pymupdf as fitz
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sys.path.insert(0,HERE); from figs import FIGS
from quickstart import QS, PLAN, cmds, REAL, REALTAG
from outline import O
from figs_xhs import X as _X
[FIGS.update({f'fig{c}{i+1}':_X[c][i] for i in range(3)}) for c in ['1','2','3','4','7','8','9','10','11']]

import base64 as _b64
def _png(n): return '<img style="width:100%;height:auto" src="data:image/png;base64,'+_b64.b64encode(open(os.path.join(os.path.dirname(HERE),'assets','ch6',n),'rb').read()).decode()+'">'
FIGS['figX1']=('图 6-10 四个维度交叉：多环境、多分支、滚动发布、特性泳道，一次变更按需选组合',_png('dims.jpg'))
FIGS['figX2']=('图 6-11 一个需求一条泳道：PR 拉起 SIT 泳道，合并 main 进 UAT，签发 Release 后受控进 PROD',_png('feature-lane-pipeline-1080-final.jpg'))
FIGS['figX3']=('图 6-12 SIT / UAT / PROD 多环境分层与生命周期矩阵',_png('matrix.jpg'))

VERSION=os.environ.get('BOOK_VERSION',open(os.path.join(ROOT,'VERSION')).read().strip())
TITLE='图解平台工程 · 云中立实践'; AUTHOR='Haitao Pan'
FOOT1='Haitao Pan | XWork Technologies LLC 服务支持'; FOOT2='xworktech.com 开源平台方案'
PROMO='XWork Technologies LLC 服务支持 / xworktech.com 开源平台方案'
OUT=os.path.join(ROOT,'dist',f'图解平台工程-云中立实践-{VERSION}.pdf')
CHAPTERS=[('1','从自由软件到平台工程',['1.1 自由软件','1.2 开源社区','1.3 开源商业：Red Hat 与 SUSE','1.4 社区发行版：Debian','1.5 从中台到平台工程']),
('2','Git 与 CI：一切从 commit 开始',[]),('3','资源即代码：环境 apply 就出来',[]),('4','交付引擎：幂等地把软件装上去',[]),
('5','安全与身份：没有共享账号，没有固定密码',None),('6','环境治理：SIT → UAT → PROD',[]),('7','云中立：一套配置，任意部署',[]),
('8','可观测：平台的眼睛和手',[]),('9','能恢复才算稳定',[]),('10','七层拧成 Open Platform',[]),('11','AI 接入平台：模型也是基础设施',[]),
 *[(k,v[0],[]) for k,v in __import__('outline').SK.items()]]
SAMPLES=[str(i) for i in range(1,18)]
PART1='上篇 经典平台工程：七层云中立实践'; PART2='下篇 现代平台工程：AI 时代与平台工程'; INTRO2='下篇导言：从经典回路到现代闭环'; PART3='实践篇 最佳实践参考'
import outline; SAMPLE='5'
md=open(os.path.join(HERE,'book.md'),encoding='utf-8').read()
def inline(s):
    s=html.escape(s); s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s); s=re.sub(r'`(.+?)`',r'<code>\1</code>',s); return s
def plain(s): return re.sub(r'[*`]','',s)
# ---- word count (CJK chars + latin words) over body text ----
def wc(s):
    s=re.sub(r'\[\[fig\w+\]\]|:::\w*','',s); s=plain(s)
    return len(re.findall(r'[\u4e00-\u9fff]',s))+len(re.findall(r'[A-Za-z0-9][A-Za-z0-9._/+#-]*',s))
fig_text=' '.join(t for t,_ in FIGS.values())
import quickstart as _q
WORDS=wc(md)+wc(fig_text)+wc(' '.join(a+' '+' '.join(b)+' '+c for k,(a,b,c) in __import__('outline').O.items() if k not in SAMPLES))+wc(' '.join(str(x) for q in _q.QS for x in q))
pre_md,ch_md=md.split('\n## ',1); ch_md='## '+ch_md
CHSECS={}
from xhs_cover import cover as _cov, MAP as _MAP
_MAP.update({'12':['center','sec'],'13':['title','git','chain'],'14':['iac','auto','sec','identity'],'15':['obs','observable','ops','recov'],'16':['title','center','chain'],'17':['iac','sec','chain'],'X10':list(_MAP['11']),'X11':list(_MAP['10'])}); _MAP['10']=_MAP['X10']; _MAP['11']=_MAP['X11']
for _k,(_c,_v) in list(FIGS.items()):
    if re.match(r'fig1[01]\d$',_k): FIGS[_k]=(re.sub(r'^图 1([01])-',lambda m:'图 1'+('1' if m.group(1)=='0' else '0')+'-',_c),_v)
def chimg(n):
    d=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'dist','_cov'); os.makedirs(d,exist_ok=True)
    p=os.path.join(d,f'ch{n}.png')
    if n in ('11','12','13','14','15','16','17'): import openers; openers.render(n,p)
    else: _cov(n,p)
    return f'<img class="chov" src="file://{p}">'
def render_body(src):
    out=[]; secs=[]
    for blk in re.split(r'\n\s*\n',src.strip()):
        b=blk.strip()
        if b.startswith('# '): out.append(f'<h1 class="pre">{inline(b[2:].replace("序 ",""))}</h1>')
        elif b.startswith('## '):
            n,t=b[3:].split(' ',1); out.append(f'<div class="chopen"><div class="chno">第 {n} 章</div><h1 id="ch{n}">{inline(t)}</h1></div>'+chimg(n))
        elif b.startswith('### '): secs.append(b[4:]); CHSECS.setdefault(b[4:].split('.')[0],[]).append(b[4:]); out.append(f'<h2>{inline(b[4:])}</h2>')
        elif re.fullmatch(r'\[\[(fig\w+)\]\]',b):
            k=b[2:-2]
            if k=='fig0': continue
            cap,svg=FIGS[k]; out.append(f'<figure>{svg}<figcaption>{html.escape(cap)}</figcaption></figure>')
        elif b.startswith(':::table'):
            rows=[l.split('|') for l in b.split('\n')[1:] if l.strip() and not l.startswith(':::')]
            out.append('<table class="cmp"><tr>'+''.join(f'<th>{inline(c)}</th>' for c in rows[0])+'</tr>'+''.join('<tr>'+''.join(f'<td>{inline(c)}</td>' for c in r)+'</tr>' for r in rows[1:])+'</table>')
        elif b.startswith(':::code'):
            body='\n'.join(l for l in b.split('\n')[1:] if not l.startswith(':::'))
            out.append(f'<pre class="code">{html.escape(body)}</pre>')
        elif b.startswith(':::practice'):
            items=[inline(l) for l in b.split('\n')[1:] if l.strip() and not l.startswith(':::')]
            out.append('<div class="practice"><div class="ptag">实践：ai-workspace-infra</div>'+''.join(f'<p>{i}</p>' for i in items)+'</div>')
        elif b.startswith('- '): out.append('<ul class="rl">'+''.join(f'<li>{inline(l[2:])}</li>' for l in b.split('\n'))+'</ul>')
        else: out.append(f'<p>{inline(b)}</p>')
    return '\n'.join(out),secs
pre_html,_=render_body(pre_md); SECS=[]; CHHTML={}
for part in ch_md.split('\n## '):
    part=part if part.startswith('## ') else '## '+part
    n=part[3:].split(' ',1)[0]; h_,ss=render_body(part); CHHTML[n]=h_; SECS+=ss
logo=open(os.path.join(ROOT,'assets','xwork-logo-mark.svg')).read().replace('width="22" height="22"','width="40" height="40"')
fig0=base64.b64encode(open(os.path.join(ROOT,'assets','fig0-open-platform-toolkit.jpg'),'rb').read()).decode()
def toc_html(pages):
    P=lambda k:str(pages.get(k,'')) 
    rows=[('序 工具拼在一起 ≠ 平台','pre',0),('图 0 Open Platform Toolkit 总图','fig0',1),('目录','toc',0),('快速开始手册：一个域名，一台机器，一行脚本','qsall',0)]
    h='<p class="tlegend">✅ 已写 ｜ 🚀 = 该章快速开始页</p>'
    for k,lbl,lvl in [(r[1],r[0],r[2]) for r in rows]:
        h+=f'<div class="tr l{lvl}"><span>{html.escape(lbl)}</span><i></i><span>{P(k)}</span></div>'
    parts={'2':'七层搭建','9':'运维与收束'}
    for n,t,subs in CHAPTERS:
        if n=='1': h+=f'<div class="tpart big">{PART1}</div><div class="tr l0"><span>上篇扉页</span><i></i><span>{P("part1")}</span></div>'
        if n=='11': h+=f'<div class="tpart big">{PART2}</div><div class="tr l0"><span>下篇扉页</span><i></i><span>{P("part2")}</span></div><div class="tr l0 on"><span>{INTRO2}</span><i></i><span>✅ {P("intro2")}</span></div>'
        if n=='17': h+=f'<div class="tpart big">{PART3}</div><div class="tr l0"><span>实践篇扉页</span><i></i><span>{P("part3")}</span></div>'
        if n in parts: h+=f'<div class="tpart">{parts[n]}</div>'
        S=n in SAMPLES; st='<em>规划中</em>'
        subs=CHSECS.get(n) if S else O[n][1]
        h+=f'<div class="tr l0{" on" if S else ""}"><span>第 {n} 章 {html.escape(t)}</span><i></i><span>{"✅ " if S else st+" "}{P("ch"+n)}</span></div>'
        for s in subs:
            h+=f'<div class="tr l1"><span>{html.escape(plain(s))}</span><i></i><span>{P("s:"+plain(s)) if S else ""}</span></div>'
        if any(q[0]==n for q in QS): h+=f'<div class="tr l1 qsr"><span>🚀 快速开始</span><i></i><span>{P("qs"+n)}</span></div>'
    h+=f'<div class="tr l0"><span>尾页</span><i></i><span>{P("end")}</span></div>'
    return h

PILLAR={'11':'AI & Runtime','2':'CI/CD Engine','3':'IaC & GitOps','4':'IaC & GitOps','5':'Zero-Trust','6':'IaC & GitOps','7':'IaC & GitOps','8':'AI & Runtime（可观测）','9':'CI/CD Engine','10':'AI & Runtime'}
REPOS={'11':'ai-aggregator、Infrastructure-MCP-Server、diagram-generator','2':'.github（Reusable Workflows）、Platform-Orchestrator、gitops','3':'iac_modules、Platform-Orchestrator','4':'playbooks、artifacts','5':'.github（OIDC + Vault 基线）、Platform-Orchestrator、playbooks','6':'gitops、Platform-Orchestrator（serverless / selfhost orchestrator）','7':'iac_modules、postgresql.example.com、Platform-Orchestrator','8':'observability、postgresql.example.com','9':'artifacts（Daily 快照）、postgresql.example.com','10':'ai-aggregator、Infrastructure-MCP-Server、diagram-generator'}
def qs_html():
    e=html.escape
    h='<section class="flow qs"><div class="chopen"><div class="chno">快速开始手册</div><h1 id="qsall">一个域名，一台机器，一行脚本</h1></div>'
    h+='<p>第 2–9 章与第 11 章各配一页快速开始：同一种形态、同一套约定。四大支柱（IaC &amp; GitOps、CI/CD Engine、Zero-Trust、AI &amp; Runtime）对应 ai-workspace-infra 组织主页；组合式交付链是 Daily Main Snapshot（不可变快照 tag <code>uat-daily-build-YYYY.MM.DD[-rN]</code>）→ 仅在 UAT 快照完整成功时解析 tag → serverless-orchestrator（deploy+migrate）与 selfhost-orchestrator（deploy 后注册到 web-saas）。</p>'
    h+=f'<div class="practice"><div class="ptag">{e(PLAN)}</div><p>本手册的命令均已在 ai-workspace-infra 各仓库 main 分支提供，与脚本 --help 中的 Printed Book Commands 一致。建议先加 --dry-run 预检；每页另列官方上游来源。</p></div></section>'
    return h+'</section>' if False else h
def qs_page(q):
    e=html.escape; h=''
    if True:
        ch,t,tools,repo,path,dom,inst,env,extra,note,refs=q; url,s1,t2=cmds(q)
        h+=f'<section class="flow qs"><h2 class="qsh">🚀 快速开始 · 第 {ch} 章 {e(t)}</h2><p class="qst"><b>{e(tools)}</b> ｜ 支柱：{e(PILLAR[ch])} ｜ 仓库：{e(REPOS[ch])}</p>'
        h+=(f'<p class="plan ok">{e(REALTAG)} · ai-workspace-infra/observability：setup-observability-server.sh（中心端）/ setup-observability-agent.sh（探针）</p>' if ch in REAL else f'<p class="plan ok">{e(PLAN)} · 脚本：ai-workspace-infra/{e(repo)}/{e(path)}</p>')
        h+=f'<h3>1. 准备域名</h3><p>将节点域名（如 <code>{dom}</code>）的 A 记录指向 VPS 公网 IP，放行 80/443。在 Debian/Ubuntu VPS 上以 root 执行。</p>'
        h+=f'<h3>{"2. 中心服务" if ch in REAL else "2. 独立节点"}</h3><pre>{e(s1)}</pre>'
        h+=f'<h3>{"3. 接入探针（每台主机）" if ch in REAL else "3. 托管、共享或团队节点"}</h3><p>先由 Vault/Secret Manager 注入环境变量，再执行安装；不要把真实值放进命令行历史：</p><pre>{e(t2)}</pre>'
        h+=f'<p class="note">安装内容：{e(inst)}。{e(note)}</p><p class="ref">现在可用的上游/仓库来源：{e("；".join(refs))}</p></section>'
    return h
QSN={q[0]:q for q in QS}
def opener(n,t):
    e=html.escape; summ,subs,repos=O[n]
    if n in outline.SK: return skel(n,t)
    h=f'<section class="flow ch op"><div class="chopen"><div class="chno">第 {n} 章</div><h1 id="ch{n}">{e(t)}</h1></div>{chimg(n)}<div class="badge">规划中 · 章首页，正文待写</div><p>{e(summ)}</p><h2>本章小节</h2><ol class="secl">'+''.join(f'<li>{e(x)}</li>' for x in subs)+'</ol>'
    h+=f'<div class="practice"><div class="ptag">实践：ai-workspace-infra</div><p>{e(repos)}</p></div>'
    if n in QSN: h+=f'<p class="qslink">🚀 本章快速开始：{e(QSN[n][2])}，见下一页。</p>'
    return h+'</section>'
def skel(n,t):
    e=html.escape; _,summ,secs=outline.SK[n]
    h=f'<section class="flow ch op"><div class="chopen"><div class="chno">第 {n} 章</div><h1 id="ch{n}">{e(t)}</h1></div>{chimg(n)}<div class="badge">骨架 · 小节标题与要点已定，正文待写</div><p>{e(summ)}</p><h2>本章小节</h2>'
    h+=''.join(f'<div class="sk"><div class="skt">{e(a)}<span class="dai">待写</span></div><p>{e(b)}</p></div>' for a,b in secs)
    return h+'</section>'
def divider(k,title,sub,chs):
    e=html.escape; a,b=title.split(' ',1)
    return f'<section class="partdiv"><div class="pk">{ {"part1":"PART I","part2":"PART II"}.get(k,"PART III") } · {e(a)}</div><h1 id="{k}">{e(b)}</h1><p class="ps">{e(sub)}</p><ol class="pl2">'+''.join(f'<li><b>{n}</b>{e(t)}</li>' for n,t,_ in CHAPTERS if n in chs)+'</ol></section>'
INTRO_MD=open(os.path.join(HERE,'part2-intro.md'),encoding='utf-8').read()
def intro2():
    b,_=render_body(INTRO_MD)
    return f'<section class="flow ch"><div class="chopen"><div class="chno">下篇导言</div><h1 id="intro2">{INTRO2}</h1></div>{b}</section>'
def chapters_html():
    D={'1':divider('part1',PART1,'用开源软件与开放标准，把平台的每一层写成代码：入口、资源、交付、安全、环境、云中立、可观测、可恢复，最后拧成一个 Open Platform。',[str(i) for i in range(1,11)]),
       '11':divider('part2',PART2,'上篇把平台写成了代码；再加上向量化，平台状态变得可观测、可检索。下篇讨论在规范与安全边界之内，让 AI 参与平台的控制闭环。',[str(i) for i in range(11,17)])+intro2(),
       '17':divider('part3',PART3,'上下两篇讲原则；实践篇记录同一套平台此刻真实推进到哪一步。案例摘要与完整草案按主题并排保留，区分 ✅ 已合并与 ⏳ 待验收，不宣称任何生产部署已完成。',['17'])}
    return ''.join(D.get(n,'')+(f'<section class="flow ch">{CHHTML[n]}</section>' if n in CHHTML else opener(n,t))+(qs_page(QSN[n]) if n in QSN else '') for n,t,_ in CHAPTERS)
CSS=open(os.path.join(HERE,'style.css'),encoding='utf-8').read()
def doc(pages):
    left=CHAPTERS[:10]; right=CHAPTERS[10:]
    col=lambda L:''.join(f'<li><b>{n}</b>{html.escape(t.split("：")[0])}</li>' for n,t,_ in L)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<section class="cover"><div class="ver">{VERSION} 预览版 · 活的书，持续更新</div>
<div class="kicker">图解 · OPEN PLATFORM</div><h1 class="ct">图解平台工程<br><span>云中立实践</span></h1>
<div class="theme">工具拼在一起 ≠ 平台：用开源软件、开放标准，搭一个不被任何云锁定的 Open Platform</div>
<div class="keys"><span>Git 为入口</span><span>OpenTofu 资源引擎</span><span>Ansible 交付引擎</span><span>Vault 安全边界</span></div>
<div class="prev"><div class="ph">上篇 经典平台工程 · 10 章 ｜ 下篇 现代平台工程 · 6 章 ｜ 实践篇 · 1 章</div><div class="cols"><ol>{col(left)}</ol><ol>{col(right)}</ol></div></div>
<div class="promo">能自建的都自建 · Gitea 与 GitHub Actions 对等讲 · 每章配 ai-workspace-infra 真实实践</div>
<div class="author">{AUTHOR}</div><div class="brand">{logo}<span>XWork Technologies</span></div></section>
<section class="flow lic"><h1 class="lich" id="lic">版权与许可</h1>
<p>Copyright © 2026 Haitao Pan / XWork Technologies LLC</p>
<h2>正文与图解：CC BY-SA 4.0</h2><p>本书的文字与图解以 Creative Commons 署名-相同方式共享 4.0 国际许可协议（CC BY-SA 4.0）发布：<br>以 Creative Commons 官方发布的 CC BY-SA 4.0 文本为准</p>
<p>在遵守协议的前提下，你可以自由地分享（复制、分发）和演绎（改编、转换、二次创作），包括商业用途；须给出适当署名、提供许可协议链接，并标明是否作了修改。</p>
<h2>代码片段与脚本：Apache License 2.0</h2><p>书中的代码片段、命令与脚本以 Apache License, Version 2.0 发布：<br>以 Apache 软件基金会官方发布的 License 2.0 文本为准</p>
<h2>署名格式</h2><p class="attr">《图解平台工程 · 云中立实践》{VERSION}，Haitao Pan / XWork Technologies LLC，CC BY-SA 4.0</p>
<p>书中提到的第三方软件、商标与图标归各自权利人所有，并按其各自的许可协议使用。</p></section>
<section class="flow">{pre_html}</section>
<section class="figpage"><h2 class="fh">图 0 · Open Platform Toolkit 总图</h2><img src="data:image/png;base64,{fig0}"><p class="fc">起点图：中心是 Gitea、OpenTofu、Ansible、Vault 四个引擎，周围是身份、可观测、运维与可恢复能力，底部是从 Code &amp; PR 到 SIT/UAT/PROD 的交付链。此图由 ai-workspace-infra/diagram-generator 生成，后续版本按本书配色重绘。</p></section>
<section class="toc"><h1>目录</h1>{toc_html(pages)}</section>
{qs_html()}
{chapters_html()}
<section class="end"><div class="brand big">{logo}</div><h1>{TITLE}</h1><p>{VERSION} 预览版 · {datetime.date.today().isoformat()}</p>
<p>本版正文约 {WORDS:,} 字（自动统计：汉字 + 英文词）</p><p>这是一本活的书：跟着 ai-workspace-infra 的实践持续更新，每个版本由同一个 build.sh 重建。</p>
<p class="pl">作者 {AUTHOR}<br>{PROMO}</p></section></body></html>'''
def chrome(htmlstr,pdf):
    hp=os.path.join(ROOT,'dist','book.html'); open(hp,'w',encoding='utf-8').write(htmlstr)
    subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--no-pdf-header-footer',f'--print-to-pdf={pdf}',hp],check=True,capture_output=True)
def locate(pdf):
    d=fitz.open(pdf); pages={}; txt=[p.get_text().replace('\n','') for p in d]
    tocpages={i for i,t in enumerate(txt) if re.search(r'规划中\d|快速开始\d|✅ ?\d',t)}
    if tocpages: pages['toc']=min(tocpages)+1
    keys={'lic':'Copyright © 2026 Haitao Pan','pre':'工具拼在一起 ≠ 平台','fig0':'图 0 · Open Platform',**{'ch'+n:'第 '+n+' 章'+t for n,t,_ in CHAPTERS},'end':'本版正文约'}
    keys['qsall']='第 2–9 章与第 11 章各配一页快速开始'; keys['part1']='用开源软件与开放标准，把平台的每一层写成代码'; keys['part2']='上篇把平台写成了代码；再加上向量化，平台状态变得可观测'; keys['intro2']='下篇导言'+INTRO2; keys['part3']='实践篇记录同一套平台此刻真实推进到哪一步'
    for q in QS: keys['qs'+q[0]]=f'快速开始 · 第 {q[0]} 章'
    for x in SECS: keys['s:'+plain(x)]=plain(x)
    for k,v in keys.items():
        for i,t in enumerate(txt):
            if i==0 or i in tocpages: continue
            if v in t: pages[k]=i+1; break
    return pages
os.makedirs(os.path.dirname(OUT),exist_ok=True); tmp=OUT+'.tmp.pdf'
pages={}
for _ in range(3):
    chrome(doc(pages),tmp); np_=locate(tmp)
    if np_==pages: break
    pages=np_
d=fitz.open(tmp); FR='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
for i,p in enumerate(d):
    if i==0: continue
    r=p.rect; p.insert_font(fontname='cjk',fontfile=FR)
    g=(0.29,0.33,0.45); f=p.insert_font(fontname='cjk',fontfile=FR); F=fitz.Font(fontfile=FR)
    for y,t in ((r.height-30,FOOT1),(r.height-19,FOOT2)):
        p.insert_text(((r.width-F.text_length(t,fontsize=7))/2,y),t,fontname='cjk',fontsize=7,color=g)
    p.insert_text((40,r.height-19),'CC BY-SA 4.0',fontname='cjk',fontsize=7,color=g)
    n=str(i+1); p.insert_text((r.width-40-F.text_length(n,fontsize=8.5),r.height-19),n,fontname='cjk',fontsize=8.5,color=(0,0.345,0.741))
toc=[[1,'封面',1],[1,'版权与许可',pages.get('lic',2)],[1,'序',pages.get('pre',2)],[2,'图 0 总图',pages.get('fig0',3)],[1,'目录',pages.get('toc',4)],[1,'快速开始手册',pages.get('qsall',4)]]
for n,t,_ in CHAPTERS:
    if n=='1': toc.append([1,PART1,pages.get('part1',4)])
    if n=='11': toc+= [[1,PART2,pages.get('part2',4)],[2,INTRO2,pages.get('intro2',4)]]
    if n=='17': toc.append([1,PART3,pages.get('part3',4)])
    cp=pages.get('ch'+n,4); toc.append([1 if False else 2,f'第 {n} 章 {t}',cp])
    for x in (CHSECS.get(n) if n in CHHTML else O[n][1]): toc.append([3,plain(x),pages.get('s:'+plain(x),cp)])
    if n in QSN: toc.append([3,f'🚀 快速开始：{QSN[n][2]}',pages.get('qs'+n,cp)])
toc.append([1,'尾页',len(d)])
d.set_toc(toc); d.set_metadata({'title':TITLE+' '+VERSION,'author':AUTHOR,'subject':PROMO,'creator':'platform-book/build.sh'})
d.save(OUT,garbage=4,deflate=True); os.remove(tmp)
json.dump({'pdf':OUT,'pages':len(d),'words':WORDS,'anchors':pages},open(os.path.join(ROOT,'dist','build-info.json'),'w'),ensure_ascii=False,indent=1)
print(json.dumps({'pdf':OUT,'pages':len(d),'words':WORDS,'anchors':pages},ensure_ascii=False))
