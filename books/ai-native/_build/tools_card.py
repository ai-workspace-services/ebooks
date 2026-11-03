# v0.9：1.4 关卡插画改为 HTML 卡片（替换旧位图 04.png）。模型/工具名与第 03 章一致，信息截至 2026-10-23。
MODS=[('01','主流 AI 工具全景','选对入口，别装满整个工具箱',[('聊天','ChatGPT · Claude · Gemini · Grok'),('编码','OpenCode · Codex · Claude Code · Grok Build · Antigravity'),('研究','Deep Research · Grok X 搜索'),('创作','GPT-Image-2.5 Sunburst · Nano Banana 2.1 · Grok Imagine · Gemini Omni Flash')]),
('02','主流模型与选择策略','旗舰打 Boss，快速档清小怪',[('OpenAI','GPT-6 Astra｜GPT-6.1 Sol｜GPT-6 Luna'),('Anthropic','Claude Fable 5.1｜Opus 5.5｜Sonnet 5.5｜Haiku 5.5'),('xAI · Google','Grok 4.7｜Grok Build　·　Gemini 4 Argon｜Gemini 3.8 Flash'),('开放权重','DeepSeek-V4.1-Flash · Qwen3.8-Max · Kimi K3 · GLM-5.3 · MiniMax-M3 · Muse Spark Open · Mistral Large 4')]),
('03','AI Agent 入门路线','从对话到多 Agent 编队',[('路线','对话 → 任务拆解 → 工具调用 → 记忆 → 多 Agent 协作'),('官方 Agent 平台','OpenAI Agents API · Claude Agent SDK / Managed Agents · Antigravity Agent'),('本书主城','OpenCode + DSH + DS-Bot 主运行时；Codex / Claude Code / Grok Build 作适配器')]),
('04','个人知识库搭建','让 AI 读得懂你的资料',[('采集 → 整理','Obsidian · Notion · 文档 / 会话归档'),('三级存档','QMD 本地索引 · PG 权威状态 · Drive 冷备份'),('检索','RAG / 向量检索 → 写回 X-Memory-Hub')]),
('05','技术人群使用图','按职业配装（L0–L5）',[('L0 / L1','控制面与高频小任务：快速档模型'),('L2 / L3','工程与架构：均衡档 + 旗舰'),('L4 / L5','研究与专项：Deep Research · 电脑操作'),('网关','New API / LiteLLM 统一路由与计费')]),
]
h=''.join(f'''<div style="border:1px solid #dde5f0;border-radius:14px;padding:14px 18px;margin:0 0 14px;display:flex;gap:16px;background:#f8fbff">
<div style="flex:0 0 230px"><div style="font:800 40px/1 sans-serif;color:#1d5bd8">{n}</div><div style="font-weight:800;font-size:27px;margin-top:6px">{E(t)}</div><div style="font-size:19px;color:#667">{E(sub)}</div></div>
<div style="flex:1">'''+''.join(f'<div style="display:flex;gap:10px;font-size:20px;line-height:1.45;padding:3px 0;border-bottom:1px dashed #e3e9f2"><b style="flex:0 0 150px;color:#1d3d7a">{E(a)}</b><span>{E(b)}</span></div>' for a,b in rows)+'</div></div>' for n,t,sub,rows in MODS)
add(f'<div class="kicker">{kk} · 关卡插画（2026-10 装备版）</div><h1>5 大核心模块，构建你的 AI 增长飞轮</h1><div class="lead">从认知 → 工具 → 实践 → 沉淀 → 变现。原图的工具与模型已过期，本页按第 03 章重绘。</div>{h}<div class="note"><b>信息截至 2026-10-23</b>：模型与工具名摘自各厂商官方页面，详见第 03 章。</div>', f'{sec} 关卡插画 · 2026-10 装备版')
