#!/usr/bin/env python3
"""Generate light-theme model-family maps (SVG + PNG) for AI-Native ch.03.

Verified-only facts; evidence: sources/model-maps-evidence-20261120.md
User-supplied dark infographics are reference layout only — redrawn, not claimed as original authorship.
"""
from __future__ import annotations
import html, os, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'model-maps'
OUT.mkdir(parents=True, exist_ok=True)

# Shared light theme
BG = '#FFFEFA'  # ivory
INK = '#1A2332'
MUTED = '#3D4A5C'  # dark enough for print — not low-contrast grey
CARD = '#FFFFFF'
BORDER = '#D8DEE8'

FAMILIES = [
  {
    'id': 'openai',
    'file': 'map-openai-gpt',
    'accent': '#10A37F',
    'title': 'OpenAI · GPT 模型族谱（核实版）',
    'subtitle': '模型族 ≠ ChatGPT 订阅档 / App；以 API 模型目录为准',
    'cols': [
      ('旗舰推理', [
        ('GPT-6.2 Astra', 'gpt-6.2-astra', '1.05M 上下文 · 128K 输出', '复杂推理 / 编码 / 电脑操作'),
      ]),
      ('均衡主力', [
        ('GPT-6.2 Sol', 'gpt-6.2-sol', '1.05M 上下文 · 128K 输出', '日常编码与 Agent 规模化'),
      ]),
      ('高效批量', [
        ('GPT-6 Luna', 'gpt-6-luna', '1.05M 上下文 · 128K 输出', '高吞吐 / 可关 reasoning'),
      ]),
    ],
    'extra': [
      ('专用 / 多媒体（目录另列）', 'GPT-Image-2.6 Sunburst / Flare；GPT-Live-1.1；Daybreak / GPT-6 Cyber（需审批，未在本书展开）'),
    ],
    'notes': [
      '官方选型页建议：最难项目用 Astra；日常用 Sol；成本敏感用 Luna。',
      'Astra / Sol 拒绝 reasoning.effort=none；Luna 支持 none。',
      '产品计划（ChatGPT Free/Plus/Pro）≠ 模型族 ID，勿混为一谈。',
    ],
    'sources': 'developers.openai.com/api/docs/models · 访问 2026-11-20',
  },
  {
    'id': 'anthropic',
    'file': 'map-anthropic-claude',
    'accent': '#D97706',
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
    'id': 'xai',
    'file': 'map-xai-grok',
    'accent': '#2563EB',
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
    'id': 'google',
    'file': 'map-google-gemini',
    'accent': '#4285F4',
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
    'id': 'open-weights',
    'file': 'map-open-weights',
    'accent': '#7C3AED',
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
  body {{
    width: 1400px; height: 900px; background: {BG}; color: {INK};
    font-family: 'NotoSansSC', 'Noto Sans CJK SC', 'Source Han Sans SC', sans-serif;
    padding: 36px 40px 28px; position: relative;
  }}
  .banner {{
    display: flex; align-items: flex-start; justify-content: space-between;
    border-bottom: 4px solid {accent}; padding-bottom: 16px; margin-bottom: 22px;
  }}
  .banner h1 {{ font-size: 34px; font-weight: 800; letter-spacing: 0.5px; color: {INK}; }}
  .banner .sub {{ font-size: 16px; color: {MUTED}; margin-top: 8px; font-weight: 600; }}
  .badge {{
    background: {accent}; color: #fff; font-size: 13px; font-weight: 800;
    padding: 8px 14px; border-radius: 999px; white-space: nowrap; margin-left: 16px;
  }}
  .grid {{ display: flex; gap: 18px; align-items: stretch; }}
  .col {{ flex: 1; min-width: 0; }}
  .col-h {{
    font-size: 15px; font-weight: 800; color: {accent}; text-transform: none;
    margin-bottom: 10px; letter-spacing: 0.5px;
  }}
  .card {{
    background: {CARD}; border: 1.5px solid {BORDER}; border-left: 5px solid {accent};
    border-radius: 12px; padding: 14px 16px; margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(26,35,50,0.06);
  }}
  .name {{ font-size: 20px; font-weight: 800; color: {INK}; }}
  .id {{ font-size: 13px; color: {MUTED}; margin-top: 4px; }}
  .id code {{ background: #F1F4F9; padding: 2px 6px; border-radius: 4px; font-size: 12px; }}
  .meta {{ font-size: 14px; color: {MUTED}; margin-top: 6px; font-weight: 600; }}
  .use {{ font-size: 15px; color: {INK}; margin-top: 6px; font-weight: 600; }}
  .extras {{ margin-top: 14px; }}
  .extra {{
    background: #F7F9FC; border: 1px solid {BORDER}; border-radius: 10px;
    padding: 10px 14px; margin-bottom: 8px; font-size: 14px; color: {INK}; line-height: 1.45;
  }}
  .extra b {{ color: {accent}; }}
  .notes {{
    margin-top: 12px; background: #FFF; border: 1.5px solid {BORDER}; border-radius: 12px;
    padding: 12px 18px 12px 32px; font-size: 14px; color: {INK}; line-height: 1.5;
  }}
  .notes li {{ margin: 4px 0; }}
  .foot {{
    position: absolute; left: 40px; right: 40px; bottom: 18px;
    display: flex; justify-content: space-between; font-size: 12px; color: {MUTED}; font-weight: 600;
  }}
</style></head><body>
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
    <span>整理/重绘 · 参考用户提供的暗色族谱图版式 · 事实仅取官方目录</span>
    <span>{esc(fam['sources'])}</span>
  </div>
</body></html>'''


def html_to_png(html_path: Path, png_path: Path, w=1400, h=900):
    url = html_path.resolve().as_uri()
    cmd = [
        'google-chrome', '--headless=new', '--disable-gpu', '--no-sandbox',
        '--hide-scrollbars', f'--window-size={w},{h}',
        f'--screenshot={png_path}', url,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def html_to_svg_wrapper(html_str: str, svg_path: Path, w=1400, h=900):
    """Store editable source as foreignObject SVG for print/edit pipelines."""
    # Escape for embedding: keep as CDATA-ish by using xhtml namespace
    inner = html_str.replace('<!DOCTYPE html>', '').replace('<html lang="zh-CN">', '').replace('</html>', '')
    # Simpler: save the HTML alongside and a minimal SVG that points conceptually
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <title>Editable source companion — see sibling .html</title>
  <rect width="100%" height="100%" fill="{BG}"/>
  <text x="40" y="48" font-family="Noto Sans CJK SC, sans-serif" font-size="22" fill="{INK}">
    可编辑源：同目录 .html（Chrome 渲染出 PNG）。本 SVG 为占位索引。
  </text>
</svg>
'''
    # Better: actually embed foreignObject with the body content
    # For editability, the .html IS the source of truth.
    svg_path.write_text(svg, encoding='utf-8')


def main():
    for fam in FAMILIES:
        html_str = render_html(fam)
        html_path = OUT / f"{fam['file']}.html"
        png_path = OUT / f"{fam['file']}.png"
        svg_path = OUT / f"{fam['file']}.svg"
        html_path.write_text(html_str, encoding='utf-8')
        html_to_png(html_path, png_path)
        # Also write a self-contained SVG via foreignObject for vector edit
        fo = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xhtml="http://www.w3.org/1999/xhtml"
     width="1400" height="900" viewBox="0 0 1400 900">
  <foreignObject width="1400" height="900">
    <xhtml:div xmlns="http://www.w3.org/1999/xhtml">{html_str.split('<body>',1)[1].rsplit('</body>',1)[0] if '<body>' in html_str else ''}</xhtml:div>
  </foreignObject>
</svg>
'''
        # Keep editable HTML as primary; SVG index points to it
        svg_path.write_text(
            f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900">
  <desc>Primary editable source: {fam['file']}.html · Generated PNG: {fam['file']}.png · Accent {fam['accent']}</desc>
  <rect width="1400" height="900" fill="{BG}"/>
  <text x="48" y="80" font-size="28" font-family="Noto Sans CJK SC, sans-serif" fill="{INK}">{esc(fam['title'])}</text>
  <text x="48" y="120" font-size="16" font-family="Noto Sans CJK SC, sans-serif" fill="{MUTED}">See sibling .html for full editable layout; render with Chrome → PNG.</text>
</svg>
''',
            encoding='utf-8',
        )
        print('wrote', png_path, png_path.stat().st_size)
    # manifest for chapters
    (OUT / 'README.md').write_text(
        '# Model-family maps (light theme)\n\n'
        'Generated by `_build/gen_model_maps.py`. Editable: `*.html`. Print: `*.png`.\n'
        'Redrawn from user-supplied dark references; facts from official catalogs only '
        '(see `sources/model-maps-evidence-20261120.md`).\n',
        encoding='utf-8',
    )


if __name__ == '__main__':
    main()
