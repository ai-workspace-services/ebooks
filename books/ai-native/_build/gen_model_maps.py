#!/usr/bin/env python3
"""Generate light-theme model-family maps (HTML → PNG) for AI-Native ch.03.

Editable sources of truth: this generator + sibling *.html files.
*.svg files are optional index stubs only — NOT editable vector artwork.

Verified-only facts; evidence: sources/model-maps-evidence-20261120.md
User-supplied dark infographics are reference layout only.
"""
from __future__ import annotations
import html, json, subprocess, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'model-maps'
OUT.mkdir(parents=True, exist_ok=True)

BG = '#FFFEFA'
INK = '#1A2332'
MUTED = '#3D4A5C'
CARD = '#FFFFFF'
BORDER = '#D8DEE8'
WIDTH = 1400
FOOTER_GAP = 40  # reserved space above footer band
BOTTOM_PAD = 48

# --- family data (same verified content) ---
FAMILIES = [
  {
    'id': 'openai', 'file': 'map-openai-gpt', 'accent': '#10A37F',
    'title': 'OpenAI · GPT 模型族谱（核实版）',
    'subtitle': '模型族 ≠ ChatGPT 订阅档 / App；以 API 模型目录为准',
    'cols': [
      ('旗舰推理', [('GPT-6.2 Astra', 'gpt-6.2-astra', '1.05M 上下文 · 128K 输出', '复杂推理 / 编码 / 电脑操作')]),
      ('均衡主力', [('GPT-6.2 Sol', 'gpt-6.2-sol', '1.05M 上下文 · 128K 输出', '日常编码与 Agent 规模化')]),
      ('高效批量', [('GPT-6 Luna', 'gpt-6-luna', '1.05M 上下文 · 128K 输出', '高吞吐 / 可关 reasoning')]),
    ],
    'extra': [('专用 / 多媒体（目录另列）', 'GPT-Image-2.6 Sunburst / Flare；GPT-Live-1.1；Daybreak / GPT-6 Cyber（需审批，未在本书展开）')],
    'notes': [
      '官方选型页建议：最难项目用 Astra；日常用 Sol；成本敏感用 Luna。',
      'Astra / Sol 拒绝 reasoning.effort=none；Luna 支持 none。',
      '产品计划（ChatGPT Free/Plus/Pro）≠ 模型族 ID，勿混为一谈。',
    ],
    'sources': 'developers.openai.com/api/docs/models · 访问 2026-11-20',
  },
  {
    'id': 'anthropic', 'file': 'map-anthropic-claude', 'accent': '#D97706',
    'title': 'Anthropic · Claude 模型族谱（核实版）',
    'subtitle': 'Claude API / 云平台模型 ID；产品 App 另计',
    'cols': [
      ('最新旗舰线', [
        ('Claude Fable 5.2', 'claude-fable-5-2', '1M · 128K 输出', '高难推理与长程 Agent'),
        ('Claude Opus 5.5', 'claude-opus-5-5', '1M · 128K 输出', '官方建议多数负载由此起步'),
        ('Claude Sonnet 5.5', 'claude-sonnet-5-5', '1M · 128K 输出', '速度与智能平衡'),
        ('Claude Haiku 5.5', 'claude-haiku-5-5', '1M · 128K 输出', '高吞吐 / 低延迟'),
      ]),
    ],
    'extra': [
      ('仍列于官方「All models」', 'Fable 5.1 / Fable 5；Opus 5 / 4.8 / 4.7 / 4.6；Sonnet 5 / 4.6 等 — 优先用最新线'),
      ('有限供应', 'Claude Mythos 5.2 / 5.1 / 5（需验证计划；本书不展开）'),
      ('已标注 retired（部分云平台仍可）', 'Opus 4.1、Opus 4、Sonnet 4 — 详见 Model deprecations，勿自行臆测下线日'),
    ],
    'notes': [
      '先用 Opus 5.5 评测；不够再升 Fable 5.2；子 Agent 用 Haiku 5.5。',
      '全系当前线均为 1M 上下文 / 128K 同步输出上限。',
      '退休承诺以 Anthropic 运营平台为准；合作云平台自定日期。',
    ],
    'sources': 'platform.claude.com/docs/en/models/overview · 访问 2026-11-20',
  },
  {
    'id': 'xai', 'file': 'map-xai-grok', 'accent': '#2563EB',
    'title': 'xAI · Grok 模型族谱（核实版）',
    'subtitle': '文本 API 定价表所列 ID；Imagine / Voice 为专用模态',
    'cols': [
      ('文本旗舰', [
        ('Grok 4.7', 'grok-4.7', '500k 上下文', '官方推荐代码与通用任务'),
        ('Grok 4.6', 'grok-4.6', '500k 上下文', '同代次前一档'),
        ('Grok 4.5', 'grok-4.5', '500k 上下文', '同代次'),
      ]),
      ('长上下文档', [
        ('Grok 4.3', 'grok-4.3', '1M 上下文', '更长上下文定价档'),
        ('Grok 4.20 系列', 'grok-4.20-*-0309', '1M 上下文', 'reasoning / non-reasoning / multi-agent'),
      ]),
    ],
    'extra': [
      ('图像 / 视频', 'grok-imagine-image · grok-imagine-image-2.0 · grok-imagine-video · video-1.5 / 1.5-lite'),
      ('语音', 'grok-voice-3.0（STS）；Voice 2.0 文档标注 Deprecated'),
    ],
    'notes': [
      '选型页：Code / Chat → Grok 4.7；图像 → Image 2.0；视频 → Video 1.5；语音 → Voice API。',
      '未开 Web/X Search 时无训练截止后的实时事件（知识截止：Grok 4.7 为 2026-05）。',
      'Grok 产品 App / SuperGrok 订阅 ≠ API 模型 ID。',
    ],
    'sources': 'docs.x.ai/developers/models · 访问 2026-11-20',
  },
  {
    'id': 'google', 'file': 'map-google-gemini', 'accent': '#4285F4',
    'title': 'Google · Gemini 模型族谱（核实版）',
    'subtitle': 'Gemini API / AI Studio 模型码；≠ Google AI Plus/Pro 订阅档',
    'cols': [
      ('Gemini 4', [
        ('Carbon', 'gemini-4-carbon', '1M · 最长输出 64K/1M', '最强推理 / Agent 编码'),
        ('Neon', 'gemini-4-neon', '1M · 64K/1M', '前沿智能 + 较快完成'),
        ('Hydrogen', 'gemini-4-hydrogen', '1M · 64K/1M', '日常编码与 Agent 效率'),
        ('Argon', 'gemini-4-argon', '1M · 64K/1M', '相对 Carbon 更省 token 的前沿推理'),
      ]),
      ('Gemini 3 Flash / Live', [
        ('3.8 Flash', 'gemini-3.8-flash', 'Flash 档', '长程工程与自主 Agent'),
        ('3.8 Live', 'gemini-3.8-live', '实时语音', '低延迟语音 Agent'),
        ('3.6 Flash', 'gemini-3.6-flash', 'Flash 档', '速度与多模态平衡'),
        ('3.5 Flash-Lite', 'gemini-3.5-flash-lite', '高吞吐', '低成本子 Agent'),
      ]),
    ],
    'extra': [
      ('生成媒体（摘录）', 'Nano Banana 2.1 / 2 / Pro；Gemini Omni Flash；Genie 4；Lyria；TTS / Transcribe 等 — 见官方 models 页'),
      ('已弃用并路由（changelog）', 'gemini-3.7-flash → 3.8-flash；gemini-3.5-flash → 3.6-flash — 请改模型字符串'),
    ],
    'notes': [
      '官方「Latest」页以 Carbon 为最强推理；Argon 为更高效的前沿推理档。',
      '稳定版示例：gemini-3.6-flash；preview / latest / experimental 命名约定见文档。',
      'Antigravity / Jules / Deep Research 是产品或 Agent，不是模型族 ID。',
    ],
    'sources': 'aistudio.google.com/docs/models · changelog · 访问 2026-11-20',
  },
  {
    'id': 'open-weights', 'file': 'map-open-weights', 'accent': '#7C3AED',
    'title': '开放权重阵营 · 核实摘录（非穷尽）',
    'subtitle': '开放权重 ≠ OSI 开源许可；商用前必读各家许可证',
    'cols': [
      ('已核 API / 文档', [
        ('DeepSeek V4.1 Flash', 'deepseek-flash', '1M · 视觉✓', 'V4 Pro：1M · 无视觉'),
        ('Mistral Large 4', 'mistral-large-4', '开放权重多模态', 'Ecosystem Open Weight License'),
        ('Mistral Small 4', 'mistral-small-4', 'Apache 2.0', 'instruct / reasoning / coding'),
        ('GLM 5.3 / Flash', '见 Z.ai / Mistral 目录', '1M 上下文', 'Flash 多模态；5.3 文本'),
      ]),
    ],
    'extra': [
      ('仍以旧证据文件为准、本次仅交叉抽查', 'Qwen3.8-Max、Kimi K3、MiniMax M3、Meta Muse Spark Open — 细节见 ch03-sources；变更以各厂商页为准'),
      ('弃用提示（Mistral 目录）', 'Mistral Medium 3.5：文档标 Deprecation 2026-10-31 / Retirement 2027-04-30 — 替代：Large 4；勿当作「已下线」除非官方确认不可用'),
    ],
    'notes': [
      '自托管看许可证与硬件；云 API 看模型 ID 与地区合规。',
      '编程工具作者统一推荐 OpenCode + 网关切后端；厂商官方工具另注。',
      '本图不穷尽所有开放权重模型；未核名称一律不写。',
    ],
    'sources': 'api-docs.deepseek.com · docs.mistral.ai · docs.z.ai · 访问 2026-11-20',
  },
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render_html(fam: dict) -> str:
    accent = fam['accent']
    cards = []
    for col_title, items in fam['cols']:
        cells = []
        for name, mid, meta, use in items:
            cells.append(f'''
            <div class="card">
              <div class="name">{esc(name)}</div>
              <div class="id"><code>{esc(mid)}</code></div>
              <div class="meta">{esc(meta)}</div>
              <div class="use">{esc(use)}</div>
            </div>''')
        cards.append(f'<div class="col"><div class="col-h">{esc(col_title)}</div>{"".join(cells)}</div>')
    extras = ''.join(f'<div class="extra"><b>{esc(t)}</b> — {esc(b)}</div>' for t, b in fam.get('extra', []))
    notes = ''.join(f'<li>{esc(n)}</li>' for n in fam['notes'])
    return f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<style>
  @font-face {{ font-family: 'NotoSansSC'; src: local('Noto Sans CJK SC'), local('Noto Sans SC'); }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: {BG}; }}
  body {{
    width: {WIDTH}px; min-height: 100px; height: auto; overflow: visible;
    color: {INK};
    font-family: 'NotoSansSC', 'Noto Sans CJK SC', 'Source Han Sans SC', sans-serif;
    padding: 36px 40px {BOTTOM_PAD}px; position: relative;
  }}
  .wrap {{ display: flex; flex-direction: column; gap: 0; }}
  .banner {{
    display: flex; align-items: flex-start; justify-content: space-between;
    border-bottom: 4px solid {accent}; padding-bottom: 16px; margin-bottom: 20px;
  }}
  .banner h1 {{ font-size: 32px; font-weight: 800; letter-spacing: 0.5px; color: {INK}; line-height: 1.25; }}
  .banner .sub {{ font-size: 15px; color: {MUTED}; margin-top: 8px; font-weight: 600; }}
  .badge {{
    background: {accent}; color: #fff; font-size: 13px; font-weight: 800;
    padding: 8px 14px; border-radius: 999px; white-space: nowrap; margin-left: 16px; flex: 0 0 auto;
  }}
  .grid {{ display: flex; gap: 16px; align-items: flex-start; }}
  .col {{ flex: 1; min-width: 0; }}
  .col-h {{
    font-size: 15px; font-weight: 800; color: {accent};
    margin-bottom: 10px; letter-spacing: 0.5px;
  }}
  .card {{
    background: {CARD}; border: 1.5px solid {BORDER}; border-left: 5px solid {accent};
    border-radius: 12px; padding: 12px 14px; margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(26,35,50,0.06);
  }}
  .name {{ font-size: 18px; font-weight: 800; color: {INK}; }}
  .id {{ font-size: 13px; color: {MUTED}; margin-top: 4px; }}
  .id code {{ background: #F1F4F9; padding: 2px 6px; border-radius: 4px; font-size: 12px; }}
  .meta {{ font-size: 13px; color: {MUTED}; margin-top: 5px; font-weight: 600; }}
  .use {{ font-size: 14px; color: {INK}; margin-top: 5px; font-weight: 600; }}
  .extras {{ margin-top: 12px; }}
  .extra {{
    background: #F7F9FC; border: 1px solid {BORDER}; border-radius: 10px;
    padding: 10px 14px; margin-bottom: 8px; font-size: 13px; color: {INK}; line-height: 1.45;
  }}
  .extra b {{ color: {accent}; }}
  .notes {{
    margin-top: 10px; background: #FFF; border: 1.5px solid {BORDER}; border-radius: 12px;
    padding: 12px 18px 12px 32px; font-size: 13px; color: {INK}; line-height: 1.5;
  }}
  .notes li {{ margin: 4px 0; }}
  /* Footer in document flow — never overlaps content */
  .foot {{
    margin-top: {FOOTER_GAP}px; padding-top: 14px;
    border-top: 1px solid {BORDER};
    display: flex; justify-content: space-between; gap: 16px;
    font-size: 12px; color: {MUTED}; font-weight: 600; line-height: 1.4;
  }}
  .foot span {{ max-width: 48%; }}
  .foot .right {{ text-align: right; }}
</style></head><body>
  <div class="wrap">
  <div class="banner">
    <div>
      <h1>{esc(fam['title'])}</h1>
      <div class="sub">{esc(fam['subtitle'])}</div>
    </div>
    <div class="badge">核实 · 2026-11-20</div>
  </div>
  <div class="grid">{''.join(cards)}</div>
  <div class="extras">{extras}</div>
  <ul class="notes">{notes}</ul>
  <div class="foot">
    <span>整理/重绘 · 参考用户暗色族谱图版式 · 事实仅取官方目录 · 可编辑源：本 HTML + gen_model_maps.py</span>
    <span class="right">{esc(fam['sources'])}</span>
  </div>
  </div>
</body></html>'''


def _cdp(port: int, method: str, params: dict | None = None, session_id: str | None = None):
    # Use HTTP /json/protocol via websocket is hard without deps; instead use chrome --dump
    raise NotImplementedError


def measure_and_screenshot(html_path: Path, png_path: Path, width: int = WIDTH) -> tuple[int, int]:
    """Launch Chrome with remote debugging, get document height, screenshot full page, crop."""
    import socket
    # pick free port
    s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
    user_data = Path('/tmp') / f'chrome-map-{port}'
    user_data.mkdir(exist_ok=True)
    url = html_path.resolve().as_uri()
    proc = subprocess.Popen([
        'google-chrome', f'--remote-debugging-port={port}', '--headless=new',
        '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
        f'--user-data-dir={user_data}',
        f'--window-size={width},1200',
        url,
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        # wait for debugger
        ws_url = None
        for _ in range(50):
            try:
                with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list', timeout=1) as r:
                    tabs = json.loads(r.read().decode())
                for tab in tabs:
                    if tab.get('type') == 'page' and tab.get('webSocketDebuggerUrl'):
                        ws_url = tab['webSocketDebuggerUrl']
                        break
                if ws_url:
                    break
            except Exception:
                time.sleep(0.1)
        if not ws_url:
            raise RuntimeError('Chrome CDP not ready')

        # Prefer websocket; fallback if websocket-client missing
        try:
            import websocket  # type: ignore
        except ImportError:
            subprocess.check_call(['pip', 'install', '--break-system-packages', '-q', 'websocket-client'])
            import websocket  # type: ignore

        ws = websocket.create_connection(ws_url, timeout=15)
        msg_id = 0

        def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            payload = {'id': msg_id, 'method': method}
            if params:
                payload['params'] = params
            ws.send(json.dumps(payload))
            while True:
                raw = ws.recv()
                data = json.loads(raw)
                if data.get('id') == msg_id:
                    if 'error' in data:
                        raise RuntimeError(data['error'])
                    return data.get('result', {})

        call('Page.enable')
        # wait for load
        time.sleep(0.4)
        metrics = call('Page.getLayoutMetrics')
        content = metrics.get('cssContentSize') or metrics.get('contentSize') or {}
        h = int(content.get('height', 1000)) + 8
        w = int(content.get('width', width))
        # clamp
        h = max(h, 700)
        h = min(h, 2400)
        # set device metrics then capture
        call('Emulation.setDeviceMetricsOverride', {
            'width': width, 'height': h, 'deviceScaleFactor': 1, 'mobile': False,
        })
        time.sleep(0.15)
        shot = call('Page.captureScreenshot', {'format': 'png', 'fromSurface': True, 'captureBeyondViewport': True})
        import base64
        png_path.write_bytes(base64.b64decode(shot['data']))
        ws.close()
        return w, h
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()



def crop_whitespace(png_path: Path, bottom_pad: int = 40, top_pad: int = 0, side_pad: int = 0, thresh: int = 250):
    """Trim excess ivory/white below content while keeping bottom_pad."""
    from PIL import Image
    im = Image.open(png_path).convert('RGB')
    w, h = im.size
    px = im.load()
    def row_has_ink(y):
        dark = 0
        for x in range(0, w, 3):
            r, g, b = px[x, y]
            if r < thresh or g < thresh or b < thresh:
                dark += 1
                if dark > 2:
                    return True
        return False
    top = 0
    for y in range(h):
        if row_has_ink(y):
            top = max(0, y - top_pad)
            break
    bottom = h - 1
    for y in range(h - 1, -1, -1):
        if row_has_ink(y):
            bottom = min(h - 1, y + bottom_pad)
            break
    if bottom <= top:
        return im.size
    cropped = im.crop((0, top, w, bottom + 1))
    cropped.save(png_path)
    return cropped.size


def write_index_svg(fam: dict, svg_path: Path, h: int):
    """Non-editable index stub pointing at HTML — do not treat as vector artwork."""
    svg_path.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{min(h, 200)}" viewBox="0 0 {WIDTH} {min(h, 200)}">
  <desc>INDEX ONLY — not editable vector art. Edit {fam['file']}.html or _build/gen_model_maps.py then re-run generator.</desc>
  <rect width="100%" height="100%" fill="{BG}"/>
  <text x="40" y="56" font-size="22" font-family="Noto Sans CJK SC, sans-serif" fill="{INK}">{esc(fam['title'])}</text>
  <text x="40" y="96" font-size="14" font-family="Noto Sans CJK SC, sans-serif" fill="{MUTED}">Editable sources: {fam['file']}.html + gen_model_maps.py → PNG. This SVG is an index stub only.</text>
</svg>
''',
        encoding='utf-8',
    )


def main():
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        subprocess.check_call(['pip', 'install', '-q', 'pillow'])

    sizes = []
    for fam in FAMILIES:
        html_str = render_html(fam)
        html_path = OUT / f"{fam['file']}.html"
        png_path = OUT / f"{fam['file']}.png"
        svg_path = OUT / f"{fam['file']}.svg"
        html_path.write_text(html_str, encoding='utf-8')
        w, h = measure_and_screenshot(html_path, png_path)
        cw, ch = crop_whitespace(png_path, bottom_pad=72)
        w, h = cw, ch
        write_index_svg(fam, svg_path, h)
        sizes.append((fam['file'], w, h, png_path.stat().st_size))
        print(f"wrote {png_path.name} {w}x{h} {png_path.stat().st_size}B")

    (OUT / 'README.md').write_text(
        '# Model-family maps (light theme)\n\n'
        '**Editable sources of truth:** `_build/gen_model_maps.py` and `*.html` in this folder.\n'
        '**Print/raster:** `*.png` (regenerated by the generator).\n'
        '**`*.svg`:** index stubs only — **not** editable vector graphics.\n\n'
        'Redrawn from user-supplied dark references; facts from official catalogs only '
        '(see `sources/model-maps-evidence-20261120.md`).\n',
        encoding='utf-8',
    )
    print('sizes:', sizes)


if __name__ == '__main__':
    main()
