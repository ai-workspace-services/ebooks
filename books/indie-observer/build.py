#!/usr/bin/env python3
"""Build HTML from book/ (toc.json, intro.md, reading-notes.md) + src/content articles."""
import json,os,re,markdown,datetime
V=os.environ.get('BOOK_VERSION','v0.1'); D=os.environ.get('BOOK_DATE',datetime.date.today().isoformat())
B=json.load(open('book/toc.json',encoding='utf-8'))
S='src/content/03-observability/guance-data-ai/series-v4'
U='https://github.com/ai-workspace-services/knowledge/blob/main/'+S[len('src/content/')-0:].replace('src/','') if False else 'https://github.com/ai-workspace-services/knowledge/blob/main/content/03-observability/guance-data-ai/series-v4/'
M=lambda s:markdown.markdown(s,extensions=['tables','fenced_code'])
def md(p,d):
    t=open(p,encoding='utf-8').read()
    t=re.sub(r'^---\n.*?\n---\n','',t,flags=re.S)
    t=re.sub(r'(!\[[^\]]*\]\()(?!http)([^)]+)\)',lambda m:m.group(1)+os.path.relpath(os.path.join(d,m.group(2)),'.')+')',t)
    t=re.sub(r'^(#+)',lambda m:'#'*min(6,len(m.group(1))+2),t,flags=re.M)
    return M(t)
core,subs=B['core'],B['subs']
toc=''
for arc in B['arcs']:
    n=[c['arc'] for c in core].index(arc)+1
    toc+=f'<h3>{arc}</h3><ol start="{n}">'+''.join(f'<li>{c["title"]}</li>' for c in core if c['arc']==arc)+'</ol>'
toc+='<h3>替补（不另加篇）</h3><ul>'+''.join(f'<li>{s["id"]} {s["title"]}</li>' for s in subs)+'</ul>'
# cover is its own page; title+TOC start directly on page 2 (no spacer page)
o=[f'<section class="cover front"><div class="cover-title">{B["title"]}</div><img src="cover-front.png"></section>',
f'<section class="toc"><h1>{B["title"]}</h1><p class="ver">{V} · {D} · {B["subtitle"]}</p><h2>目录</h2>{toc}</section>',
M(open('book/intro.md',encoding='utf-8').read()),
'<h2>核心 12 篇</h2><table><tr><th>#</th><th>标题</th><th>小红书标题</th><th>模板</th><th>阶段</th><th>状态</th><th>公众号字</th><th>小红书字</th><th>动图</th></tr>']
for c in core: o.append('<tr>'+''.join(f'<td>{c[k]}</td>' for k in ['id','title','xhs_title','template','arc','status','wechat_chars','xhs_chars','gifs'])+'</tr>')
o.append('</table><h2>替补选题</h2><table><tr><th>#</th><th>标题</th><th>模板</th><th>用途</th><th>状态</th><th>大纲字数</th></tr>')
for s in subs: o.append('<tr>'+''.join(f'<td>{s[k]}</td>' for k in ['id','title','template','use','status','outline_chars'])+'</tr>')
o.append('</table>'+M(open('book/reading-notes.md',encoding='utf-8').read()))
for c in core:
    d=f'{S}/{c["dir"]}'
    o.append(f'<h2 class="art">#{c["id"]} {c["title"]}</h2><p class="meta">{c["arc"]} · {c["template"]} · {c["status"]} · 源：{U}{c["dir"]}/</p>')
    if c['status']=='全文稿': o.append('<h3>公众号稿</h3>'+md(f'{d}/wechat.md',d)+'<h3>小红书稿</h3>'+md(f'{d}/xhs.md',d))
    else:
        f='outline.md' if os.path.exists(f'{d}/outline.md') else 'wechat.md'
        o.append('<p class="note">大纲稿：仅收大纲，待实测后成稿。</p>'+md(f'{d}/{f}',d))
for s in subs:
    d=f'{S}/{s["dir"]}'
    o.append(f'<h2 class="art">{s["id"]} {s["title"]}（替补）</h2><p class="meta">{s["use"]} · {s["template"]} · {s["status"]}</p><p class="note">替补大纲：仅收大纲。</p>'+md(f'{d}/{s["file"]}',d))
A='src/content/03-observability/guance-data-ai/articles'
import glob
arts=sorted(glob.glob(f'{A}/[0-9][0-9]-*/article_draft.md'))
if arts:
    o.append('<h2 class="art">第一季成稿（knowledge #294 合并正文）</h2>')
    for f in arts:
        d=os.path.dirname(f); o.append(f'<h2 class="art">{os.path.basename(d)}</h2>'+md(f,d))
o.append(f'<section class="colophon"><p>版本 {V} · {D}<br>Haitao Pan / XWork Technologies LLC 服务支持<br>内容源：github.com/ai-workspace-services/knowledge（series-v4 + articles）<br>许可：CC BY-SA 4.0 · 署名 Haitao Pan / XWork Technologies LLC</p></section><section class="cover last"><img src="cover-back.png"></section>')
css=open('book/style.css').read()
open('dist/book.html','w').write(f'<html><head><meta charset="utf-8"><base href="../"><style>{css}</style></head><body>{"".join(o)}</body></html>')
print('dist/book.html',V)
