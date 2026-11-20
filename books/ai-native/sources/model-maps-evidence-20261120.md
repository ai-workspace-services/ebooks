# 模型族谱图 · 官方证据（访问日期 2026-11-20，Asia/Shanghai）

规则：图中与第 03 章正文只写本文件列出的官方名称/上下文/状态；用户提供的暗色参考图仅作版式参考，**不作为事实来源**。未能在本轮打开的官方页上核实的名称一律不写入或标「未核实」。

区分：
- **模型族 / API 模型 ID** ≠ 产品订阅档 / App 名称（ChatGPT Plus、Claude Pro、SuperGrok、Google AI Pro 等）
- **开放权重（open weights）** ≠ OSI「开源」许可；许可证以各仓库 / 厂商页为准

## OpenAI
- https://developers.openai.com/api/docs/models — 选型：GPT-6.2 Astra / GPT-6.2 Sol / GPT-6 Luna
- https://developers.openai.com/api/docs/models/gpt-6.2-astra — `gpt-6.2-astra`；1,050,000 context；128,000 max output；知识截止 2026-05-18；拒绝 `reasoning.effort: none`
- https://developers.openai.com/api/docs/models/gpt-6.2-sol — `gpt-6.2-sol`；同窗口规格（页内）
- https://developers.openai.com/api/docs/models/gpt-6-luna — `gpt-6-luna`；支持 `none` 推理档
- 多媒体目录另列：GPT-Image-2.6 Sunburst/Flare、GPT-Live-1.1、Daybreak / GPT-6 Cyber（需审批，本书不展开）
- **相对 v0.9.6 正文修正**：`GPT-6 Astra` → `GPT-6.2 Astra`；`GPT-6.1 Sol` → `GPT-6.2 Sol`；图像主推由 2.5 更新为目录所见的 2.6 线

## Anthropic
- https://platform.claude.com/docs/en/models/overview — Latest：Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5；均 1M / 128K；API ID `claude-fable-5-2` 等（连字符）
- 官方建议多数负载从 Opus 5.5 起步；Fable 5.2 用于更高难推理与长程 Agent
- All models 仍列 Fable 5.1 等更早档；Opus 4.1 / Opus 4 / Sonnet 4 标注 retired（部分云平台例外）— **不臆测具体下线日**，指向 Model deprecations
- Mythos 线：limited availability，本书不展开
- **相对 v0.9.6 修正**：旗舰表述由「Fable 5.1」升级为「Fable 5.2」；5.1 仍可用但非最新

## xAI
- https://docs.x.ai/developers/models — `grok-4.7` / `4.6` / `4.5`（500k）；`grok-4.3` 与 `grok-4.20-*-0309`（1M）；Imagine / Voice 价目；Voice 2.0 Deprecated
- https://docs.x.ai/developers/grok-4-7 — Grok 4.7 开发者指南；知识截止 2026-05
- 选型页：Code/Chat → 4.7；图像 Image 2.0；视频 Video 1.5；语音 Voice API

## Google Gemini
- https://aistudio.google.com/docs/models — Gemini 4：Carbon / Neon / Hydrogen / Argon（均约 1M）；Gemini 3.8 Flash / Live / TTS；3.6 Flash；3.5 Flash-Lite；Nano Banana；Omni；Genie 4 等
- https://aistudio.google.com/docs/latest-model — Carbon 为最强推理档表述
- https://aistudio.google.com/docs/changelog — Carbon GA 2026-11-10；Argon GA 2026-10-13；`gemini-3.7-flash`→`3.8-flash`、`gemini-3.5-flash`→`3.6-flash` 弃用路由
- https://deepmind.google/models/model-cards/ — 模型卡列表交叉核对
- **相对 v0.9.6 修正**：旗舰由「仅 Argon」改为「Carbon 最强推理；Argon 为更高效前沿推理」；补充 Neon/Hydrogen；Genie 表述对齐 Genie 4；编程工具/Agent 名（Antigravity、Jules、Deep Research）标为产品/Agent 非模型 ID

## 开放权重（摘录，非穷尽）
- DeepSeek：https://api-docs.deepseek.com/quick_start/pricing — `deepseek-flash` = V4.1-Flash-1017（1M，视觉✓）；`deepseek-v4-pro`（1M，无视觉）
- Mistral：https://docs.mistral.ai/getting-started/models/models_overview — Large 4（开放权重）；Small 4（Apache 2.0）；Medium 3.5 **Deprecation 2026-10-31 / Retirement 2027-04-30**，替代 Large 4（**未等同于已不可用**）
- GLM：同页及 Z.ai 目录交叉 — GLM 5.3 / 5.3 Flash（1M）
- Qwen / Kimi / MiniMax / Meta Muse：本轮以既有 `ch03-sources-20261023.md` 为主、仅抽查未全量重核；正文保留并指向该证据文件，变更以厂商页为准

## 用户参考图（非事实源）
用户于 2026-11-20 提供 5 张暗色族谱 PNG（Gemini / 开放阵营 / Grok / Claude / OpenAI）。子代理因私有附件权限未能重读像素；版式按「明亮主题卡片族谱」重绘。图中若有与官方目录不符的名称，**不以附图为准**。

## 图文件
- 可编辑：`assets/model-maps/*.html`（生成脚本 `_build/gen_model_maps.py`）
- 印刷 PNG：`assets/model-maps/map-*.png`
- SVG 索引：`assets/model-maps/*.svg`（指向 HTML 源）
