#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
V=${V:-v0.1}
OUT="XWorkspace-Agent-Skills工程规范-开放方案-$V"
python3 - "$V" <<'PY'
import markdown,sys,re
v=sys.argv[1]
body=markdown.markdown(open('book.md').read(),extensions=['tables','fenced_code'])
body=re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',lambda m:'<pre class="mermaid">'+m.group(1)+'</pre>',body,flags=re.S)
css="""@page{size:A5;margin:16mm 14mm}@page:first{margin:0}.imgcover{height:210mm;width:148mm;display:flex;align-items:center;background:linear-gradient(#e2f6f0,#f8fafc);page-break-after:always;overflow:hidden}.imgcover img{width:148mm;display:block}body{font-family:'Noto Serif CJK SC',serif;font-size:10.5pt;line-height:1.7;color:#222}
h1{font-family:'Noto Sans CJK SC',sans-serif;color:#1e3a8a;border-bottom:2px solid #1e3a8a;padding-bottom:4px;font-size:17pt}
h2{color:#1e40af;font-size:13pt}table{border-collapse:collapse;width:100%;font-size:9pt;margin:8px 0}td,th{border:1px solid #cbd5e1;padding:4px}th{background:#e0e7ff}
pre{background:#f1f5f9;padding:8px;font-size:8pt;white-space:pre-wrap;border-radius:4px}code{font-size:8.5pt}blockquote{border-left:4px solid #6366f1;margin:8px 0;padding:4px 10px;background:#eef2ff}
.pb{page-break-after:always}.cover{height:178mm;display:flex;flex-direction:column;justify-content:center;text-align:center;background:linear-gradient(160deg,#0f172a,#1e3a8a);color:#fff;margin:-16mm -14mm;padding:20mm;page-break-after:always}
.cover h1{color:#fff;border:none;font-size:22pt}.mermaid{background:#fff;text-align:center}"""
cover=f"""<div class="cover"><div style="font-size:11pt;opacity:.8">XWorkspace Core Skills</div><h1>XWorkspace Agent Skills<br>工程规范 · 开放方案</h1>
<div style="font-size:12pt">代码开源 · 文档开源 · 开放方案</div><div style="margin-top:30mm;font-size:10pt">{v} · 2026-11-13 · skills@07c6e772<br>Haitao Pan<br>XWork Technologies LLC 服务支持</div></div>"""
import os
cv=os.path.abspath('assets/cover.png')
if os.path.exists(cv):  # designed cover from Drive assets (assets.manifest.json)
    cover=f'<section class="imgcover"><img src="file://{cv}"></section>'
toc="<h1>目录</h1><ul>"+"".join(f"<li>{t}</li>" for t in re.findall(r'<h1>(.*?)</h1>',body))+"</ul><div class='pb'></div>"
open('book.html','w').write(f"<html><head><meta charset=utf-8><style>{css}</style><script src='https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'></script><script>mermaid.initialize({{startOnLoad:true}})</script></head><body>{cover}{toc}{body}</body></html>")
PY
google-chrome --headless --no-sandbox --disable-gpu --virtual-time-budget=8000 --no-pdf-header-footer --print-to-pdf="$OUT.pdf" book.html 2>/dev/null
cp book.md "$OUT.md"
echo "$OUT.pdf"
