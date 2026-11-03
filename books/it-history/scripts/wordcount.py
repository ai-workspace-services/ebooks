# 正文字数：序言 + 各章 chapter.md 正文（去掉 front matter、图片行、markdown 符号），按非空白字符计
import os,re,yaml,math
ROOT=os.path.dirname(os.path.abspath(__file__))+'/..'
def _clean(t):
    t=re.sub(r'^---\n.*?\n---\n','',t,flags=re.S)
    t='\n'.join(l for l in t.split('\n') if not l.strip().startswith('![') and not l.strip().startswith('[[img'))
    t=re.sub(r'[#*>`|_\-]','',t)
    return len(re.sub(r'\s','',t))
def count():
    b=yaml.safe_load(open(ROOT+'/book.yml'))
    n=_clean(open(ROOT+'/front/preface.md').read())
    for d in b['chapters']: n+=_clean(open(f'{ROOT}/chapters/{d}/chapter.md').read())
    return n
def wan(n): return '%.1f' % (math.floor(n/1000)/10)
if __name__=='__main__': n=count(); print(n, wan(n))
