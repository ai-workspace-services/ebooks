# 书名唯一来源：book.yml 的 title（及可选 xhs_title）。生成书稿 md 与 XHS 文案。
import yaml,re,sys,os
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
b=yaml.safe_load(open('book.yml')); N=b['title']; V=b['version']; T=b.get('xhs_title') or N
fn=re.sub(r'[：:，,、]+','-',N.replace(' ','')).strip('-')+('-'+b['edition_label'] if b.get('edition_label') else '')
LB=b.get('edition_label') or ''
s=f'# 《{N}》{LB} {V} 书稿（章节合订）\n\n'+re.sub(r'^---.*?---\n','',open('front/preface.md').read(),flags=re.S).replace('{book_title}',N).replace('{edition_label}',LB)+'\n'
for dd in b['chapters']:
  t=open(f'chapters/{dd}/chapter.md').read(); m=re.match(r'^---\n(.*?)\n---\n',t,re.S); fm=yaml.safe_load(m.group(1))
  s+=f"\n## {fm['label']}　{fm['title']}\n\n> {fm['intro']}\n\n"+t[m.end():].replace('](images/',f'](chapters/{dd}/images/')
open(f'dist/{fn}-{V}-书稿.md','w').write(s)
sys.path.insert(0,'scripts'); import wordcount as _w; WW=_w.wan(_w.count())
body=f'''散落在公众号和小红书上的图文，这次攒成了一本书：《{N}》{LB}。

从大型机到云、再到 AI，复杂度一路上涨，人们用虚拟化、容器、K8s、平台工程一层层盖控制面。收录图解 402 张 · 正文约 {WW} 万字，图穿插在文字旁，茶水间也能读完。看懂今天的系统，为什么长成这样。

适合想补 IT 全景、又不想啃砖头文档的人。

xworktech.com · 开源平台方案'''
open(f'/workspace/it-history/xhs-sell-copy-{V}.md','w').write(f'# 小红书种草文案 · {V}\n\n## 标题（≤20 字）\n\n{T}\n\n## 正文（≤200 字）\n\n{body}\n')
L=lambda x:len(re.sub(r'\s','',x))
print('pdf name:',f'{fn}-{V}.pdf'); print('xhs title',T,L(T),'body',L(body)); print('banned:',[w for w in ['简史','帝国'] if w in T+body])
