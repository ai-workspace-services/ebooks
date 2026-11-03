#!/usr/bin/env python3
"""v4：把 v4src/<章>.md（含 [[img 1,2]] 占位）与原 chapter.md 的图片列表合成新的 chapters/<章>/chapter.md。
原图片列表来自 v4src/_orig/<章>.md（v3.1 的 chapter.md 快照），保证每张图恰好引用一次。可反复运行。"""
import os, re, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, read_md, IMG_RE
SRC = os.path.join(ROOT, 'v4src'); ORIG = os.path.join(SRC, '_orig')
RENAME = yaml.safe_load(open(os.path.join(SRC, 'renames.yml'), encoding='utf-8')) or {}
def main():
    for f in sorted(os.listdir(SRC)):
        if not f.endswith('.md'): continue
        d = f[:-3]; ofm, obody = read_md(os.path.join(ORIG, f)); nfm, nbody = read_md(os.path.join(SRC, f))
        imgs = []
        for ln in obody.split('\n'):
            m = IMG_RE.match(ln.strip())
            if m:
                cap, rel = m.group(1), m.group(2)
                r = RENAME.get(d, {}).get(os.path.basename(rel))
                if r: rel = 'images/' + r; cap = os.path.splitext(r)[0].split('-', 1)[1]
                imgs.append('![%s](%s)' % (cap, rel))
        used = []
        def sub(m):
            out = []
            for x in m.group(1).split(','):
                i = int(x); used.append(i); out.append(imgs[i - 1])
            return '\n\n'.join(out)
        body = re.sub(r'\[\[img ([\d, ]+)\]\]', sub, nbody)
        miss = sorted(set(range(1, len(imgs) + 1)) - set(used)); dup = sorted({i for i in used if used.count(i) > 1})
        if miss or dup: raise SystemExit('%s 缺图 %s 重复 %s' % (d, miss, dup))
        fm = dict(ofm); fm.update(nfm); fm.pop('note', None) if d.startswith('07x') else None
        out = '---\n' + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=1000) + '---\n\n' + body.strip() + '\n'
        open(os.path.join(ROOT, 'chapters', d, 'chapter.md'), 'w', encoding='utf-8').write(out)
        print('%-32s 图 %3d  正文 %5d 字' % (d, len(imgs), len(re.sub(r'!\[[^\]]*\]\([^)]*\)|\s', '', body))))
if __name__ == '__main__': main()
