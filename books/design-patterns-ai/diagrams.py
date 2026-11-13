#!/usr/bin/env python3
"""Deterministic inline SVG diagrams for 《图解经典设计模式 · 遇到 AI 时代》.

No binary assets. CI only needs Noto Sans CJK SC (already installed in build.yml).
Usage:
  python3 diagrams.py --list
  python3 diagrams.py diagram-ai-slop-vs-signal
  python3 diagrams.py --inject book.html
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from typing import Iterable

PORTAL, PORTAL_BG = "#0f766e", "#ccfbf1"
GIN, GIN_BG = "#b45309", "#fef3c7"
PG, PG_BG = "#1d4ed8", "#dbeafe"
AI, AI_BG = "#be123c", "#ffe4e6"
CLEAN, CLEAN_BG = "#15803d", "#dcfce7"
VIOLET, VIOLET_BG = "#5b21b6", "#ede9fe"
AMBER, AMBER_BG = "#b45309", "#ffedd5"
INK, MUTED, LINE = "#0f172a", "#334155", "#94a3b8"
CARD, PAGE, RULE = "#ffffff", "#f8fafc", "#cbd5e1"
FONT = "'Noto Sans CJK SC', 'Noto Sans CJK', 'Source Han Sans SC', sans-serif"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def text_width(s: str, size: float) -> float:
    w = 0.0
    for ch in s:
        cjk = ("\u4e00" <= ch <= "\u9fff") or ch in "，。、；：？！「」『』（）—…·《》￥"
        w += size * (1.02 if cjk else 0.58)
    return w


def wrap_text(text: str, max_width: float, size: float) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        buf = ""
        for ch in para:
            trial = buf + ch
            if buf and text_width(trial, size) > max_width:
                lines.append(buf)
                buf = ch
            else:
                buf = trial
        lines.append(buf)
    return lines or [""]


def tspans(x, y, lines: Iterable[str], size, fill, anchor="middle",
           weight="500", leading=None) -> str:
    leading = size * 1.35 if leading is None else leading
    parts = []
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else leading
        parts.append(f'<tspan x="{x:.1f}" dy="{dy:.1f}">{esc(line)}</tspan>')
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'font-family="{FONT}">{"".join(parts)}</text>'
    )


def rect(x, y, w, h, fill, stroke=None, sw=1.4, r=8) -> str:
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ' stroke="none"'
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{r}" ry="{r}" fill="{fill}"{s}/>'
    )


def box_label(x, y, w, h, fill, stroke, title, title_size=13, title_fill="#fff",
              r=8, weight="700") -> str:
    parts = [rect(x, y, w, h, fill, stroke, 1.5, r)]
    lines = wrap_text(title, w - 14, title_size)
    block = (len(lines) - 1) * title_size * 1.28
    ty = y + h / 2 + title_size * 0.35 - block / 2
    parts.append(tspans(x + w / 2, ty, lines, title_size, title_fill, weight=weight))
    return "".join(parts)


def defs() -> str:
    def marker(mid, color):
        return (
            f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7.5" markerHeight="7.5" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{color}"/></marker>'
        )
    return (
        "<defs>"
        + marker("arrow", "#334155")
        + marker("arrow-ai", AI)
        + marker("arrow-clean", CLEAN)
        + marker("arrow-pg", PG)
        + marker("arrow-gin", GIN)
        + marker("arrow-portal", PORTAL)
        + "</defs>"
    )


def svg(vid: str, w: int, h: int, title: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="100%" role="img" aria-labelledby="{vid}-title" '
        f'preserveAspectRatio="xMidYMid meet" font-family="{FONT}">'
        f'<title id="{vid}-title">{esc(title)}</title>'
        f'<rect width="{w}" height="{h}" rx="10" fill="{PAGE}" stroke="{RULE}" stroke-width="1"/>'
        + defs()
        + body
        + "</svg>"
    )


def vchevron(x, y, color) -> str:
    # small downward chevron between layers
    return (
        f'<polygon points="{x-8},{y} {x+8},{y} {x},{y+10}" fill="{color}"/>'
    )


# ---------------------------------------------------------------------------
# 1. AI slop vs signal
# ---------------------------------------------------------------------------
def diagram_ai_slop_vs_signal() -> str:
    w, h = 800, 430
    b = []
    b.append(tspans(400, 28, ["AI 能飞快写代码，也擅长飞快堆积一本正经的屎山"], 16, INK, weight="800"))
    b.append(tspans(400, 50, ["先判断变化点，再决定要不要模式；命名是沟通手段，实现落回原语"], 12, MUTED))

    b.append(rect(20, 68, 360, 340, AI_BG, AI, 2, 12))
    b.append(box_label(36, 84, 328, 38, AI, AI, "整整齐齐的屎山", title_size=15))
    left = [
        ("IXxxService + ServiceImpl", "只有一条路径，却先造接口家族"),
        ("GenericCRUDRepository", "按表生成通用增删改查，掩盖查询意图"),
        ("ManagerFacadeWrapper", "用模式名字当类型名，一层层空转"),
        ("看似结构工整，一改就碎", "多一层抽象，就多一处改动同步点"),
    ]
    y = 136
    for title, sub in left:
        b.append(rect(36, y, 328, 58, CARD, AI, 1.2, 8))
        b.append(tspans(52, y + 22, [title], 13, AI, anchor="start", weight="700"))
        b.append(tspans(52, y + 42, [sub], 11, MUTED, anchor="start"))
        y += 64

    b.append(rect(420, 68, 360, 340, CLEAN_BG, CLEAN, 2, 12))
    b.append(box_label(436, 84, 328, 38, CLEAN, CLEAN, "先找变化点，再落原语", title_size=15))
    right = [
        ("先定位变化点或一致性问题", "没有真实变化，就不要引入模式"),
        ("用信号和代价决定是否引入", "只有一种行为时直接调用"),
        ("函数、结构体、模块、框架原语", "Gin middleware、pgx 事务、条件更新"),
        ("名称表达业务，不表达模式身份", "用 startSubscription，不用 XxxFacade"),
    ]
    y = 136
    for title, sub in right:
        b.append(rect(436, y, 328, 58, CARD, CLEAN, 1.2, 8))
        b.append(tspans(452, y + 22, [title], 13, CLEAN, anchor="start", weight="700"))
        b.append(tspans(452, y + 42, [sub], 11, MUTED, anchor="start"))
        y += 64
    return svg("diagram-ai-slop-vs-signal", w, h,
               "AI 代码通胀对比：整整齐齐的屎山 vs 先找变化点再落原语", "".join(b))


# ---------------------------------------------------------------------------
# 2. 18 patterns map
# ---------------------------------------------------------------------------
def diagram_18_patterns_map() -> str:
    w, h = 800, 500
    b = []
    b.append(tspans(400, 26, ["十八个模式，按四个变化点归位"], 16, INK, weight="800"))
    b.append(tspans(400, 46, ["先找到问题属于哪一类，再看表里的信号与代价"], 12, MUTED))

    groups = [
        (PORTAL, PORTAL_BG, "入口与协议边界", "外部形状、协议入口、透明转发",
         ["Adapter 适配器", "Facade 外观", "Proxy 代理", "Ports & Adapters"], 1),
        (AMBER, AMBER_BG, "构造与组合", "依赖组合、分步约束、递归树形",
         ["Factory 工厂", "Builder 构建器", "Composite 组合"], 1),
        (VIOLET, VIOLET_BG, "请求链与行为控制", "选择、横切、顺序、状态与通知",
         ["Strategy 策略", "Decorator 装饰器", "责任链 CoR", "Template Method",
          "Command 命令", "State 状态", "Observer 观察者", "Iterator 迭代器"], 2),
        (PG, PG_BG, "数据一致性与可靠事件", "查询隔离、同事务提交、跨系统投递",
         ["Repository 仓储", "Unit of Work", "Transactional Outbox"], 1),
    ]
    y = 62
    for stroke, bg, title, sub, chips, rows in groups:
        bh = 92 if rows == 1 else 140
        b.append(rect(18, y, 764, bh, bg, stroke, 1.8, 10))
        b.append(rect(18, y, 7, bh, stroke, stroke, 0, 0))
        b.append(tspans(40, y + 20, [title], 14, stroke, anchor="start", weight="800"))
        b.append(tspans(40, y + 40, [sub], 11, MUTED, anchor="start"))
        gap = 8
        if rows == 1:
            n = len(chips)
            cw = (736 - gap * (n - 1)) / n
            cx, cy = 40, y + 50
            for chip in chips:
                b.append(box_label(cx, cy, cw, 32, CARD, stroke, chip,
                                   title_size=12, title_fill=stroke, r=6))
                cx += cw + gap
        else:
            cw = (736 - gap * 3) / 4
            for k, chip in enumerate(chips):
                cx = 40 + (k % 4) * (cw + gap)
                cy = y + 50 + (k // 4) * 40
                b.append(box_label(cx, cy, cw, 32, CARD, stroke, chip,
                                   title_size=12, title_fill=stroke, r=6))
        y += bh + 8
    return svg("diagram-18-patterns-map", w, h, "十八个模式按四大变化点分类全景图", "".join(b))


# ---------------------------------------------------------------------------
# 3. boundary layers
# ---------------------------------------------------------------------------
def diagram_boundary_layers() -> str:
    w, h = 800, 470
    b = []
    b.append(tspans(400, 24, ["分层边界：Portal 呈现，Gin 维护规则，端口隔离外部"], 15, INK, weight="800"))
    b.append(tspans(400, 44, ["资格规则不放在页面里；数据库用约束保护能表达的不变量"], 12, MUTED))

    layers = [
        (PORTAL, PORTAL_BG, "Portal  ·  Next.js",
         "交互与结果呈现。BFF 作为 Proxy：集中访问控制、超时与缓存身份，保持协议契约。",
         ["checkout 页面", "BFF 转发 /api", "错误与结果展示"]),
        (GIN, GIN_BG, "Gin  ·  服务入口与用例",
         "Facade 以业务动词命名。Middleware 责任链处理鉴权与限流。资格与计价规则留在用例里。",
         ["startSubscription", "鉴权 / 限流链", "qualify + quote"]),
        (VIOLET, VIOLET_BG, "Adapter  /  Ports",
         "外部协议与内部契约转换。同一用例可被 HTTP 与 CLI 适配，避免每个包先造接口。",
         ["账单事件适配", "用例端口契约", "CLI 调用同一用例"]),
        (PG, PG_BG, "PostgreSQL",
         "UNIQUE / CHECK 保护持久化不变量。条件更新防止非法转换。多步写入用显式事务，必要时再加 Outbox。",
         ["UNIQUE / CHECK", "UPDATE … WHERE", "同事务 outbox"]),
    ]
    y = 60
    for i, (stroke, bg, title, sub, chips) in enumerate(layers):
        b.append(rect(48, y, 704, 86, bg, stroke, 1.8, 10))
        b.append(tspans(64, y + 20, [title], 14, stroke, anchor="start", weight="800"))
        # sub may wrap
        sub_lines = wrap_text(sub, 672, 11)
        b.append(tspans(64, y + 38, sub_lines, 11, MUTED, anchor="start"))
        cx = 64
        cy = y + 58
        cw, ch, gap = 210, 22, 10
        for chip in chips:
            b.append(box_label(cx, cy, cw, ch, CARD, stroke, chip,
                               title_size=10.5, title_fill=stroke, r=4))
            cx += cw + gap
        if i < len(layers) - 1:
            b.append(vchevron(400, y + 86, stroke))
        y += 96
    return svg("diagram-boundary-layers", w, h,
               "Portal（Next.js BFF Proxy）→ Gin（Facade / Middleware / Usecase）→ Adapter / Ports 分层边界",
               "".join(b))


# ---------------------------------------------------------------------------
# 4. state machine + responsibility chain
# ---------------------------------------------------------------------------
def diagram_state_and_chain() -> str:
    w, h = 800, 430
    b = []
    b.append(tspans(400, 24, ["责任链把关请求，状态机把关转换"], 15, INK, weight="800"))
    b.append(tspans(400, 44, ["拒绝时后续步骤必须停止；非法转换用条件更新拒绝，而不是先改再补救"], 12, MUTED))

    # left: chain
    b.append(rect(16, 60, 368, 350, GIN_BG, GIN, 1.8, 12))
    b.append(tspans(200, 84, ["Gin 鉴权责任链"], 14, GIN, weight="800"))
    steps = [
        ("解析身份", "读出调用方，失败则 401"),
        ("校验权限", "不匹配则 403，链终止"),
        ("限流 / 配额", "超额则 429，不再进入用例"),
        ("进入用例", "startSubscription"),
    ]
    y = 104
    for i, (title, sub) in enumerate(steps):
        fill = GIN if i < 3 else CLEAN
        b.append(rect(44, y, 312, 44, CARD, fill, 1.5, 8))
        b.append(tspans(60, y + 18, [f"{i+1}.  {title}"], 13, fill, anchor="start", weight="700"))
        b.append(tspans(60, y + 36, [sub], 11, MUTED, anchor="start"))
        if i < len(steps) - 1:
            b.append(
                f'<line x1="200" y1="{y+44}" x2="200" y2="{y+56}" '
                f'stroke="{GIN}" stroke-width="2" marker-end="url(#arrow-gin)"/>'
            )
        y += 60
    b.append(tspans(200, 392, ["验证：拒绝之后，后续步骤不再执行"], 11, GIN, weight="700"))

    # right: state machine
    # pending (TL) --confirm--> active (TR)
    # pending (TL) --abort-->   canceled (BL)
    # active (TR)  --past due--> past_due (BR)
    # past_due (BR)--recover-->  active (TR)  (curve on the right)
    # past_due (BR)--cancel-->   canceled (BL)
    b.append(rect(416, 60, 368, 350, PG_BG, PG, 1.8, 12))
    b.append(tspans(600, 84, ["订阅状态机 + 条件更新"], 14, PG, weight="800"))

    nodes = [
        (508, 128, "pending", GIN),
        (692, 128, "active", CLEAN),
        (508, 236, "canceled", AI),
        (692, 236, "past_due", AMBER),
    ]
    for x, y, name, color in nodes:
        b.append(box_label(x - 58, y - 20, 116, 40, CARD, color, name, title_size=13, title_fill=color, r=20))

    def alabel(x, y, text, color):
        b.append(tspans(x, y, [text], 10, color, weight="700"))

    # confirm: pending → active
    b.append(f'<line x1="566" y1="128" x2="626" y2="128" stroke="{CLEAN}" stroke-width="2" marker-end="url(#arrow-clean)"/>')
    alabel(596, 116, "confirm", CLEAN)
    # abort: pending → canceled (down)
    b.append(f'<line x1="508" y1="148" x2="508" y2="208" stroke="{AI}" stroke-width="2" marker-end="url(#arrow-ai)"/>')
    alabel(472, 184, "abort", AI)
    # past due: active → past_due (down)
    b.append(f'<line x1="692" y1="148" x2="692" y2="208" stroke="{AMBER}" stroke-width="2" marker-end="url(#arrow)"/>')
    alabel(640, 184, "past due", AMBER)
    # cancel: past_due → canceled (left)
    b.append(f'<line x1="634" y1="236" x2="574" y2="236" stroke="{AI}" stroke-width="2" marker-end="url(#arrow-ai)"/>')
    alabel(604, 252, "cancel", AI)
    # recover: past_due → active, curve on the right so it does not overlap past due
    b.append(
        f'<path d="M744 236 C770 236 770 128 744 128" fill="none" '
        f'stroke="{CLEAN}" stroke-width="2" marker-end="url(#arrow-clean)"/>'
    )
    alabel(758, 186, "recover", CLEAN)

    b.append(rect(444, 300, 312, 90, CARD, PG, 1.2, 8))
    b.append(tspans(600, 322, ["UPDATE subscriptions"], 12, PG, weight="700"))
    b.append(tspans(600, 342, ["SET status = $next"], 11, MUTED))
    b.append(tspans(600, 360, ["WHERE id = $id AND status = $from"], 11, MUTED))
    b.append(tspans(600, 378, ["行数为 0：拒绝非法或并发转换"], 11, PG, weight="700"))

    return svg("diagram-state-and-chain", w, h,
               "Gin 鉴权责任链与订阅状态机（显式转换 + PostgreSQL 条件更新）", "".join(b))


def diagram_tx_outbox() -> str:
    w, h = 800, 460
    b = []
    b.append(tspans(400, 24, ["订阅原子写入与事务性发件箱"], 15, INK, weight="800"))
    b.append(tspans(400, 44, ["业务记录与 outbox 同一事务提交；Worker 投递，接收方按事件标识幂等"], 12, MUTED))

    # row 1: portal
    b.append(box_label(40, 64, 200, 56, PORTAL_BG, PORTAL, "Portal 确认支付", title_size=14, title_fill=PORTAL, r=10))
    b.append(f'<line x1="240" y1="92" x2="300" y2="92" stroke="{PORTAL}" stroke-width="2" marker-end="url(#arrow-portal)"/>')
    b.append(box_label(308, 64, 220, 56, GIN_BG, GIN, "Gin 用例开启事务", title_size=14, title_fill=GIN, r=10))
    b.append(f'<line x1="528" y1="92" x2="588" y2="92" stroke="{GIN}" stroke-width="2" marker-end="url(#arrow-gin)"/>')
    b.append(box_label(596, 64, 164, 56, PG_BG, PG, "BEGIN", title_size=14, title_fill=PG, r=10))

    # tx box
    b.append(rect(40, 148, 720, 150, "#eff6ff", PG, 1.8, 12))
    b.append(tspans(52, 170, ["同一 PostgreSQL 事务"], 13, PG, anchor="start", weight="800"))
    b.append(box_label(60, 188, 300, 88, CARD, PG, "", title_size=1, title_fill=PG, r=8))
    b.append(tspans(210, 218, ["写订阅行"], 14, PG, weight="800"))
    b.append(tspans(210, 240, ["约束与条件更新生效"], 12, MUTED))
    b.append(tspans(210, 258, ["资格规则已在用例内判定"], 11, MUTED))
    b.append(box_label(440, 188, 300, 88, CARD, PG, "", title_size=1, title_fill=PG, r=8))
    b.append(tspans(590, 218, ["写 outbox 事件"], 14, PG, weight="800"))
    b.append(tspans(590, 240, ["同一提交，同生同灭"], 12, MUTED))
    b.append(tspans(590, 258, ["带稳定的 event_id"], 11, MUTED))
    b.append(tspans(400, 286, ["COMMIT  ·  任一步失败则全部回滚"], 12, PG, weight="700"))

    # plus between the two boxes
    b.append(tspans(400, 236, ["＋"], 22, PG, weight="800"))

    # worker row
    b.append(f'<line x1="400" y1="298" x2="400" y2="328" stroke="{PG}" stroke-width="2" marker-end="url(#arrow-pg)"/>')
    b.append(box_label(70, 332, 240, 52, GIN_BG, GIN, "Worker 扫描未投递", title_size=13, title_fill=GIN, r=8))
    b.append(f'<line x1="310" y1="358" x2="360" y2="358" stroke="{GIN}" stroke-width="2" marker-end="url(#arrow-gin)"/>')
    b.append(box_label(368, 332, 200, 52, VIOLET_BG, VIOLET, "投递外部事件", title_size=13, title_fill=VIOLET, r=8))
    b.append(f'<line x1="568" y1="358" x2="618" y2="358" stroke="{VIOLET}" stroke-width="2" marker-end="url(#arrow)"/>')
    b.append(box_label(626, 332, 140, 52, CLEAN_BG, CLEAN, "按 event_id 幂等", title_size=12, title_fill=CLEAN, r=8))

    b.append(tspans(400, 408, ["同步调用已足够时，不要上 Outbox。上了就要处理重投、积压和观测。"], 12, MUTED))
    b.append(tspans(400, 428, ["Portal 只呈现结果，资格规则与事务边界都在 Gin 用例这一侧。"], 12, MUTED))
    return svg("diagram-tx-outbox", w, h,
               "Portal + Gin + PostgreSQL 订阅原子写入与 Transactional Outbox + 幂等 Worker",
               "".join(b))


# ---------------------------------------------------------------------------
# 6. iac / ci reuse
# ---------------------------------------------------------------------------
def diagram_iac_ci_reuse() -> str:
    w, h = 800, 440
    b = []
    b.append(tspans(400, 24, ["先复用已有顺序与入口，再考虑加一层适配"], 15, INK, weight="800"))
    b.append(tspans(400, 44, ["GitHub Actions、CLI、HCL 与 Playbook 都优先声明和组合，而不是预建框架"], 12, MUTED))

    # left card: GHA
    b.append(rect(16, 62, 376, 360, VIOLET_BG, VIOLET, 1.8, 12))
    b.append(box_label(32, 78, 344, 36, VIOLET, VIOLET, "GitHub Actions 与跨入口渲染", title_size=13))
    items_l = [
        ("多作业、固定交付顺序", "先看 reusable workflow", "不要把同一条流水线复制进每个仓"),
        ("单作业内共享一组步骤", "先看 composite action", "公共顺序由调用方注入变化点"),
        ("多种入口复用同一渲染", "放进所属仓的 Python / Shell CLI", "HTTP、CI、本地命令走同一实现"),
    ]
    y = 128
    for title, action, note in items_l:
        b.append(rect(32, y, 344, 88, CARD, VIOLET, 1.2, 8))
        b.append(tspans(48, y + 20, [title], 12.5, INK, anchor="start", weight="700"))
        b.append(tspans(48, y + 40, [action], 12, VIOLET, anchor="start", weight="700"))
        b.append(tspans(48, y + 60, [note], 11, MUTED, anchor="start"))
        y += 96

    # right card: HCL / playbook
    b.append(rect(408, 62, 376, 360, AMBER_BG, AMBER, 1.8, 12))
    b.append(box_label(424, 78, 344, 36, AMBER, AMBER, "HCL 模块与 Playbook Role", title_size=13))
    items_r = [
        ("声明、参数、资源引用", "用组合表达结构", "不要为“以后可能分叉”先加一层"),
        ("Provider 确有差异", "再做独立适配", "例如云厂商 API 形状不同"),
        ("策略真正可变时", "再抽出 Strategy", "只有一种行为时直接写出配置"),
    ]
    y = 128
    for title, action, note in items_r:
        b.append(rect(424, y, 344, 88, CARD, AMBER, 1.2, 8))
        b.append(tspans(440, y + 20, [title], 12.5, INK, anchor="start", weight="700"))
        b.append(tspans(440, y + 40, [action], 12, AMBER, anchor="start", weight="700"))
        b.append(tspans(440, y + 60, [note], 11, MUTED, anchor="start"))
        y += 96
    return svg("diagram-iac-ci-reuse", w, h,
               "GitHub Actions（reusable workflow / composite action / CLI）与 HCL / Playbook 组合边界",
               "".join(b))


DIAGRAMS = {
    "diagram-ai-slop-vs-signal": diagram_ai_slop_vs_signal,
    "diagram-18-patterns-map": diagram_18_patterns_map,
    "diagram-boundary-layers": diagram_boundary_layers,
    "diagram-state-and-chain": diagram_state_and_chain,
    "diagram-tx-outbox": diagram_tx_outbox,
    "diagram-iac-ci-reuse": diagram_iac_ci_reuse,
}


CAPTIONS = {
    "diagram-ai-slop-vs-signal": "图 1  AI 代码通胀：整整齐齐的屎山，对上「先找变化点再落原语」。",
    "diagram-18-patterns-map": "图 2  十八个模式按四个变化点归位：入口边界、构造组合、链路行为、数据一致性。",
    "diagram-boundary-layers": "图 3  Portal 负责呈现与 BFF 转发，Gin 维护用例与责任链，端口隔离外部，PostgreSQL 守护不变量。",
    "diagram-state-and-chain": "图 4  左侧是可终止的鉴权责任链，右侧是订阅状态机，转换由条件更新守卫。",
    "diagram-tx-outbox": "图 5  订阅行与 outbox 事件同一事务提交，Worker 投递，接收方按 event_id 幂等。",
    "diagram-iac-ci-reuse": "图 6  先复用 reusable workflow、composite action 和所属仓 CLI；HCL 与 Role 以声明组合为默认。",
}


PLACEHOLDER = re.compile(
    r"(?:<p>)?<!--\s*diagram:([a-z0-9-]+)\s*-->(?:</p>)?",
    re.I,
)


def figure(name: str) -> str:
    if name not in DIAGRAMS:
        raise KeyError(name)
    cap = CAPTIONS.get(name, name)
    return (
        f'<figure class="diagram" id="{name}">'
        + DIAGRAMS[name]()
        + f"<figcaption>{esc(cap)}</figcaption></figure>"
    )


def inject(html_text: str) -> str:
    def repl(m):
        name = m.group(1)
        if name not in DIAGRAMS:
            return m.group(0)
        return figure(name)
    return PLACEHOLDER.sub(repl, html_text)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("name", nargs="?", help="diagram id to print as SVG")
    p.add_argument("--list", action="store_true")
    p.add_argument("--inject", metavar="HTML", help="rewrite an HTML file in place")
    args = p.parse_args(argv)
    if args.list:
        for k in DIAGRAMS:
            print(k)
        return 0
    if args.inject:
        path = args.inject
        text = open(path, encoding="utf-8").read()
        open(path, "w", encoding="utf-8").write(inject(text))
        return 0
    if not args.name:
        p.print_help()
        return 2
    if args.name not in DIAGRAMS:
        print(f"unknown diagram: {args.name}", file=sys.stderr)
        return 2
    sys.stdout.write(DIAGRAMS[args.name]())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
