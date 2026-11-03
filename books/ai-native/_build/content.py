"""《AI-Native 超级个体 · 成长计划》内容。
来源 A：AI-Native-超级个体成长计划.docx（骨架，01-07 章正文 + 7 张宣传图）
来源 B：宣传图拆分设计.md 中「每页对应的干货地图」（各章要点图）
来源 C：《2026 Google AI 全家桶》攻略（Haitao Pan，2026-02-06）→ 第 03 章工具栈
来源 D：《AI Workspace、XWorkmate 多执行器与三级记忆技术白皮书规划》v0.2-plan（2026-10-23）→ 第 07、09 章
"""
import json, pathlib, re
HERE = pathlib.Path(__file__).parent
TITLE = 'AI-Native 超级个体 · 新时代游戏'
SUB = '一起加入 AI-Native 超级个体升级打怪的这个“新时代游戏”'
INFO_DATE = '2026-02-06'

def clean(t):
    t = re.sub(r'《AI-Native ?超级个体 ?成长计划》', '《AI-Native 超级个体 · 新时代游戏》', t)
    t = t.replace('先看清方向，再决定深入哪条路。', '')
    t = re.sub(r'这份 ?0\.99 元路线图', '这份路线图', t)
    t = re.sub(r'0\.99 元路线图', '这份路线图', t)
    t = t.replace('0.99 元买到的不是', '它给你的不是').replace('0.99 元买的是', '它提供的是')
    t = t.replace('用 0.99 元，买的不是教程', '它不是教程')
    t = t.replace('会以 PDF 文档和飞书文档形式交付。', '以 PDF 形式交付。')
    return t.strip()

BASE = json.loads((HERE / 'base_chapters.json').read_text())
# 各章要点图（来源 B）
MAPS = [
 ('全景地图', ['技术人', 'AI 工具使用者', 'AI 实践者', 'AI 系统构建者', 'AI 超级个体'], '知识 · 工具 · 工作流 · Agent · 产品 · 影响力', 'AI-Native 不是学工具，而是建立自己的 AI 生产力系统。'),
 ('变化地图', ['过去：学习技术 → 找工作 → 做项目 → 升职加薪', '现在：学习 → AI 协作　工作 → AI 增强　项目 → Agent 参与', '产品 → 个人可完成　品牌 → 个人可建立　收入 → 多元化'], '', 'AI 正在重构技术人成长路径。'),
 ('五层能力模型', ['工具力 · 知道用什么', '思维力 · 知道怎么拆', '实战力 · 知道怎么做', '系统力 · 知道怎么复用', '影响力 · 知道怎么放大'], '', '先看清自己所在的位置，再决定深入哪一层。'),
 ('工具生态地图', ['内容生成：ChatGPT / Claude / Gemini / Grok', '开发编程：OpenCode / Codex / Claude Code / Grok Build / Antigravity', '知识管理：Obsidian / Notion　搜索研究：Deep Research / Grok X 搜索', 'Agent：OpenAI Agents API / Claude Managed Agents / Antigravity Agent', '知识库：RAG / 向量数据库　自动化：n8n / Dify / Flowise'], '中心：AI 工作台（模型信息截至 2026-10-23，详见第 03 章）', '工具不重要，工具组合能力才重要。'),
 ('转型路线', ['程序员 → 效率提升 → 内容输出 → 个人品牌', '→ 独立开发 → 咨询服务 → 产品收入 → 超级个体'], '运维 / DevOps / 架构师 / 产品经理 均可走这条路线', '成长不是盲目用力，而是选对长期积累方向。'),
 ('资产地图', ['知识资产 · 工作流资产 · 内容资产', '产品资产 · 品牌资产 · 客户资产', '资产 → 复利 → 影响力 → 收入 → 自由度'], '', '真正值钱的不是工具，而是持续积累的资产。'),
 ('工作空间地图', ['模型（ChatGPT / Claude / Gemini）→ Agent → 知识库', '→ 文档 → 工作流 → 项目 → 个人品牌 → 产品收入'], '中心：XWorkmate', '从工具集合，升级为 AI-Native 工作空间。'),
]


# 第 02 章 Google AI 工具栈（来源 C 摘编；对应到五层模型的「工具力 / 实战力 / 系统力」）
TOOLKIT = [
 ('3.4.1 为什么看 Google AI 生态', '2026-02-06 版第一章', [
   ('订阅共享', 'Google One AI Premium 订阅支持最多 6 人共享，2026-02 版认为人均成本较低。'),
   ('自研算力', 'Google 拥有自研第六代 TPU，2026-02 版称这种从芯片到应用的垂直整合带来响应速度与精度优势。'),
   ('超长上下文', '2026-02 版称 Gemini 3 支持百万级 Token 上下文，可一次放入多本书、长视频或整个代码仓库。'),
   ('原生多模态', '同时处理视频、音频与代码，并与 Google Docs、Gmail 协同。'),
   ('搜索增强', '借助 Google Search 实时索引增强（Search-Grounding），回答可结合最新信息。'),
 ]),
 ('3.4.2 知识内化：NotebookLM', '2026-02-06 版第二章 · 对应「知识库」模块', [
   ('多源导入', '支持一次导入 50+ 份 PDF、网页链接，甚至 YouTube 视频链接（自动提取脚本）。'),
   ('私密性', '2026-02 版称上传内容仅在独立实例中运行，不用于公开模型训练。'),
   ('跨文档推理', '可就多份资料提出综合性问题，让 AI 跨文档归纳。'),
   ('引用溯源', '每个回答带原文标注，点击跳转到 PDF 具体页码，降低「胡说八道」风险。'),
   ('AI 播客（Deep Dive Audio）', '2026-02 版称 2026 版支持「深入探索 / 核心摘要 / 辩论模式 / 批判性思维」四种风格；双人主持对谈，把枯燥材料聊成约 10 分钟的音频。'),
 ]),
 ('3.4.3 内容创作：Gemini 3 与 Nano Banana', '2026-02-06 版第三章 · 对应「内容输出」', [
   ('提示词四部曲', '角色定义 + 背景 + 任务 + 格式约束，让 Gemini 输出专业级研报。'),
   ('Thinking Mode', '复杂任务下开启思维链推理，观察 AI 如何一步步拆解问题。'),
   ('Nano Banana', '认准「香蕉图标」，2026-02 版称其为 Google 图像生成模型 Imagen 3 的进化版（代号 Nano Banana）；Quick 模式适合草图，Pro 模式（Thinking）能更准确地还原海报文字。'),
   ('生图模板', '极简商业：Minimalist product shot, Apple style, soft studio lighting, white background, 4k.\n赛博未来：Cyberpunk cityscape, neon bioluminescence, rainy street, cinematic volumetric fog.\n艺术油画：Impressionist oil painting, heavy brushstrokes, golden hour lighting, Monet style.'),
 ]),
 ('3.4.4 极客开发：Agent 与云端工作流', '2026-02-06 版第四章 · 对应「Agent」模块', [
   ('Antigravity（Agentic IDE）', '不只是代码补全，可同时管理多个自主智能体，例如 Agent A 重构后端、Agent B 编写前端单元测试。'),
   ('文档先行', '新想法与待补功能：① 详细列出来 ② 让 AI 启动分析 ③ 最后自己当好 QA。'),
   ('Jules（Cloud IDE）', '访问 jules.google，在 Google Cloud VM 中运行；可克隆 GitHub 仓库并自动配置 Node/Python 环境，异步跑耗时测试，完成后推送通知。'),
   ('OpenClaw', '前身 ClawdBot，允许 AI 操作浏览器、文件系统等；常用指令 openclaw status（健康检查）、openclaw memory search（搜索长期记忆）。'),
 ]),
 ('3.4.5 原型设计：Stitch', '2026-02-06 版第五章 · 对应「独立开发」', [
   ('从需求到 UI', '用自然语言描述 App（如深色主调的音乐 App），或上传手绘草图照片，2026-02 版称约 5 分钟可转为可交互的高保真 UI。'),
   ('设计开发协同', '生成的 UI 可复制粘贴到 Figma 并保留图层样式；可导出 React / Vue / Tailwind 前端代码。'),
   ('快速 Demo', '2026-02 版提到月度 350 次生成限额，足够在短时间内做多版 Demo 验证。'),
 ]),
 ('3.4.6 彩蛋：Chrome 内置 AI', '2026-02-06 版第六章 · 本地化', [
   ('参考项目', 'lcandy2/enable-chrome-ai（GitHub 开源项目）。'),
   ('三步开启', '① chrome://flags/#optimization-guide-on-device-model 设为 Enabled ② 确认组件状态为 Model Ready ③ 在 Console 运行 LanguageModel.availability()，返回 available 即成功。'),
   ('本地化优势', '对话在本机 CPU/GPU 处理，可离线使用，数据不出本机。'),
 ]),
]
LAYER_MAP = [  # 编者对照：五层模型 ↔ 本章工具（仅做归类，不新增事实）
 ('工具力', 'Gemini 3 / Nano Banana / Chrome 内置 AI'),
 ('思维力', '提示词四部曲 / Thinking Mode'),
 ('实战力', 'NotebookLM 知识库 / Stitch 原型 / Jules'),
 ('系统力', 'Antigravity 多 Agent / OpenClaw 记忆与自动化'),
 ('影响力', 'AI 播客 / 生图模板 → 内容与品牌输出'),
]

MODEL_DATE = '2026-10-23'
# 信息截至 2026-10：仅收录已在官方页面核实的型号
MODELS = [
 ('Google', 'Gemini 4 Argon（gemini-4-argon）', '旗舰推理模型，百万级统一上下文；Antigravity 托管 Agent 已支持', 'ai.google.dev/gemini-api/docs/models'),
 ('Google', 'Gemini 3.8 Flash（gemini-3.8-flash）', '快速档，面向长程软件工程与 Agent', 'ai.google.dev/gemini-api/docs/models'),
 ('Google', 'Nano Banana 2.1', '图像生成与对话式编辑', 'ai.google.dev/gemini-api/docs/models'),
 ('OpenAI', 'GPT-6.1 Sol（gpt-6.1-sol）', 'Codex 默认模型，百万级上下文；GPT-6 Astra 为最强档，GPT-6 Luna 用于高频轻任务', 'developers.openai.com/api/docs/models'),
 ('Anthropic', 'Claude Opus 5.5 / Sonnet 5.5 / Haiku 5.5', '全系百万级上下文；Haiku 5.5 适合做轻量子 Agent', 'docs.claude.com'),
 ('xAI', 'Grok 4.7（grok-4.7）', '50 万级上下文，推理强度可调，面向编码与知识工作', 'docs.x.ai/docs/models'),
 ('DeepSeek', 'DeepSeek V4.1 Flash（deepseek-flash）', '开放权重，百万级上下文，可配合 DeepSeek Harness', 'api-docs.deepseek.com'),
]
# L0–L5 角色矩阵（摘自作者的 AI 协作指南推荐，2026-10）
ROLES = [
 ('L0 Chat 控制面', '理解、讨论、拆解、协调，不直接写代码', 'GPT-6.1 Sol / Sonnet 5.5 / Grok'),
 ('L1 Worker', '高频、重复、边界清楚的小任务', 'GPT-6 Luna / Gemini 3.8 Flash / Haiku 5.5'),
 ('L2 Engineer', '日常编码、修 Bug、写测试', 'GPT-6.1 Sol / Sonnet 5.5 / Grok 4.7 / Gemini 3.8 Flash'),
 ('L3 Architect', '架构设计、跨仓库重构、关键决策', 'GPT-6 Astra / Opus 5.5 / Gemini 4 Argon / Grok 4.7'),
 ('L4 Researcher', '选型、政策与资料核对（与 L3 平级）', 'Deep Research / Grok + X 搜索'),
 ('L5 Specialist', 'GUI 多步操作、安全等专项', 'Computer-Use 类模型 / Gemini Deep Think'),
]
