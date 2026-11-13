# 《XWorkspace Agent Skills 工程规范 · 开放方案》完整目录索引（v0.3）

作者：Haitao Pan · XWork Technologies LLC 服务支持

> 页码取自 `dist/XWorkspace-Agent-Skills工程规范-开放方案-v0.3.pdf`（`./build.sh` 生成，不入库）。全书 **18** 页。正文锚定 `xworkspace-core-skills` 固定提交 `07c6e772`（2026-11-13，Asia/Shanghai）。全量 Skill 按 `skills/` 下 `SKILL.md` 递归计数：11 个能力域 92 项 + 2 项 vendored = **94**。

源文件：[`agent-skills-spec.md`](agent-skills-spec.md)

## 一、章节总览

| 部分 | 标题 | PDF 页码 |
|---|---|---|
| 前置 | 封面 | 1 |
| 前置 | 目录（含各章与附录能力域） | 2 |
| 正文 | 序章 · 统一规范与 Agent 技能体系 | 3 |
| 正文 | 第一章 · 先立规矩：五仓分工的那个早晨 | 4 |
| 正文 | 第二章 · 流水线不许太深：一张 9 层图的减肥记 | 4 |
| 正文 | 第三章 · 三把钥匙：系统、业务、审计各管各的 | 5 |
| 正文 | 第四章 · 不碰旧数据：升级、迁移与恢复的耐心 | 6 |
| 正文 | 第五章 · 上线那一夜：DNS、证书与值班 | 6 |
| 正文 | 第六章 · 多个 Agent 一起干活：交接不靠聊天记录 | 7 |
| 正文 | 第七章 · 功能泳道：一个功能一条临时跑道 | 7 |
| 正文 | 第八章 · 七类开发规范：把“怎么写代码”也写成技能 | 8 |
| 正文 | 第九章 · 白天写代码，晚上做内容 | 9 |
| 正文 | 第十章 · 工具箱的工具箱：办公、浏览器与装新技能 | 10 |
| 正文 | 第十一章 · 一天的用法速查 | 10 |
| 附录 | 附录 · 全量 Skill 目录索引（11 大能力域 / 94 个 Skill） | 11 |
| 文后 | 尾声 · 规矩写下来，Agent 才能长大 | 18 |
| 文后 | 许可 | 18 |

## 二、附录能力域（PDF 页码）

| 能力域 | 性质归属 | Skill 数量 | 对应章节 | PDF 页码 |
|---|---|---:|---|---|
| 能力域总览 | — | 92 + 2 | — | 11 |
| `engineering-standards` · 工程规范 | 自研核心；其中 3 项为设计契约，不计入 23 项 Author Verified | 15 | 第一、二、四、五、六、七章（部分兼第九、十章） | 12 |
| `operations-management` · 运维规范 | 作者实战验证核心（11 项均计入 Author Verified） | 11 | 第二、三、四、五章 | 13 |
| `development-standards` · 开发规范 | 自研开发规范（第三类，不计入上述 23 项徽标） | 8 | 第八章 | 14 |
| `content-planning` · 内容策划 | 上游引用（HyperFrames） | 2 | 第九章 | 14 |
| `image-production` · 图像生产 | 上游引用（HyperFrames） | 1 | 第九章 | 15 |
| `video-production` · 视频生产 | 上游引用（HyperFrames） | 7 | 第九章 | 15 |
| `audio-production` · 音频生产 | 上游引用（Web Audio / SFX） | 1 | 第九章 | 15 |
| `animation` · 动画动效 | 上游引用（GSAP / Anime.js） | 2 | 第九章 | 15 |
| `workflows` · 组合工作流 | 上游引用（HyperFrames 编排） | 6 | 第九章 | 15 |
| `marketplace` · Marketplace | 上游引用（市场与社区精选） | 15 | 第十章 | 16 |
| `workspace-core` · Workspace Core | 上游镜像（OpenClaw / Codex 运行时归档） | 24 | 第十章 | 17 |
| （vendored，不计入 11 域） | 开源社区锁定 commit 引入 | 2 | 第十章适用 | 18 |
| **合计** | 11 域 92 项 + vendored 2 项 | **94** | — | — |

> `agent-team-harness`、`harness-workflow`、`feature-lane-release-workflow` 为**设计契约**（规范已写，尚待运行验收），不计入 23 项 Author Verified。开发规范是第三类自研规范，同样不计入这 23 项。

## 三、全量 Skill 索引（94）

### engineering-standards · 工程规范（15）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `agent-team-harness` | 多 Agent 协作的能力合同、单写入者、handoff 与归档规则 | 第六章（设计契约） |
| `ai-agent-collaboration-standard` | AI 代理协作纪律：脏检查、越权拦截、错误自检与熔断 | 第六章；第十一章速查 |
| `ci-cd-workflow-spec` | YAML 只声明，逻辑进受测脚本；第三方 action 钉版本 | 第二章；第十一章速查 |
| `config-as-code-spec` | 入口剧本只编排，逻辑进 Role；CMDB 是 inventory 真相 | 第一章 |
| `execution-ownership-migration` | 每类执行只有一个 owner 仓，跨仓搬脚本按 owner 先行 | 第一章；第十一章速查 |
| `feature-lane-release-workflow` | 功能泳道：关联 PR、固定候选、SIT/UAT 组合验证与合并 | 第七章（设计契约） |
| `generation-upgrade-acceptance` | 可重复代际升级验收，不在旧数据上原地赌回滚 | 第四章；第十一章速查 |
| `gitops-canonical-resource-delivery` | 声明只在 GitOps，运行时只有一份资源真相 | 第一章 |
| `harness-workflow` | Agent 工程回路与研发交付工作流，运维副作用按风险路由 | 第六章（设计契约） |
| `infrastructure-as-code-spec` | HCL 纯净、State 按环境隔离，云事实来自 IaC CMDB | 第一章 |
| `issue-pr-traceability-standard` | Issue/PR 关联与需求事实来源，保证变更可追溯 | 第六章；第十一章速查 |
| `multi-environment-delivery-and-release` | 环境路由：PR→SIT、main→UAT、tag→PROD，并可回滚 | 第二章；第十一章速查 |
| `project-development-standard` | 项目开发过程规范：需求、实现与验收的共同约束 | 第六章 |
| `store-and-startup-homepage-spec` | 官网、商店页与启动首页规范，品牌域名承载公开页 | 第九章、第十章 |
| `zero-trust-overlay-delivery` | 零信任 Overlay 交付，身份与路径按声明收敛 | 第五章 |

### operations-management · 运维规范（11）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `backup-disaster-recovery-and-data-migration` | 备份、灾备演练与数据迁移，能恢复才算稳定 | 第四章；第十一章速查 |
| `capacity-cost-and-resource-lifecycle` | 容量、成本与资源生命周期，含功能泳道租约与回收 | 第四章 |
| `github-actions-operational-dispatch` | 派发生产 workflow 前先建目录、预检并按回执核对 | 第二章；第十一章速查 |
| `incident-response-and-change-management` | 故障响应与变更管理，值班、升级与复盘闭环 | 第五章 |
| `network-dns-tls-edge-management` | 网络、DNS、TLS 与边缘切流，域名切换按声明执行 | 第五章；第十一章速查 |
| `observability-slo-and-alerting` | 可观测性、SLO 与告警，指标/日志/追踪守住目标 | 第五章 |
| `secrets-identity-and-access-governance` | Vault 策略、OIDC 工作负载身份、轮换与吊销 | 第三章；第十一章速查 |
| `service-catalog-and-runbook-standard` | 服务目录与 Runbook 标准，值班可按条目执行 | 第五章 |
| `system-db-three-role-security` | Linux/SSH、K3s、数据库账户三权分立，审计身份隔离 | 第三章；第十一章速查 |
| `unified-observability-architecture` | 统一可观测性架构，采集与控制面分离、口径一致 | 第五章 |
| `vault-eso-tls-certificate-governance` | Vault KV → ESO → chart secret，证书自动化与网关对账 | 第三章 |

### development-standards · 开发规范（8）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `ansible-playbook` | Playbook 与 Role：幂等、变量优先级和失败传播 | 第八章 |
| `gin-go` | Go / Gin 服务与 API：路由、鉴权、用例与存储边界 | 第八章；第十一章速查 |
| `github-actions` | 工作流、reusable workflow 与 composite action 的复用边界 | 第八章 |
| `iac-hcl` | Terraform / OpenTofu 模块：变量、引用与状态地址纪律 | 第八章；第十一章速查 |
| `nodejs-nextjs-typescript` | 前端与 Node.js/Next.js/TypeScript 的结构、命名与边界 | 第八章；第十一章速查 |
| `postgresql-development` | PostgreSQL：Schema、查询、事务与迁移的开发约定 | 第八章 |
| `programming-paradigms` | 编程范式、设计模式选择、十二要素，以及命名与轻量扩展 | 第八章 |
| `python-shell` | Python、Shell、YAML 脚本与 inventory 的可读性与安全约定 | 第八章；第十一章速查 |

### content-planning · 内容策划（2）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `content_series_infographic` | 选题拆解、图文连载排期与批量提示词（每批不超过 10 张） | 第九章 |
| `tech-article-series` | 把技术材料写成单主题连载，并轮换结构模板以免单调 | 第九章 |

### image-production · 图像生产（1）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `it-infra-continuous-png` | 连续风格科技长图 PNG / 信息图素材生成（含 manifest） | 第九章 |

### video-production · 视频生产（7）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `ai-tech-news-video` | AI 资讯快报视频：检索、口播、字幕与自动渲染 | 第九章 |
| `ai-ti-wo-shuo-explainer` | 「AI替我说」动画科普短视频的脚本、画面与成片流程 | 第九章适用 |
| `it-infra-evolution-video` | IT 基础设施长图讲解视频 v1：基于真实信息图出 1080p 成片 | 第九章 |
| `it-infra-evolution-video-v2` | IT 基础设施长图讲解视频 v2：manifest 驱动配置、验收与 MP4 | 第九章 |
| `product-intro-video` | 产品介绍视频：官网提炼、视觉校验、叙事结构与渲染出片 | 第九章 |
| `swimlane-video` | 手绘泳道图工作流短视频，适合讲解步骤与职责分工 | 第九章 |
| `video-understanding` | 短视频逐镜理解，输出运镜、节奏与 beat sheet | 第九章适用 |

### audio-production · 音频生产（1）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `sound-fx-for-video` | 视频音效：免费 SFX 检索下载或 Web Audio API 合成并入时间线 | 第九章 |

### animation · 动画动效（2）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `animejs` | Anime.js 适配 HyperFrames：seek 驱动、由合成对象注册时间线 | 第九章适用 |
| `sketch-animation-video` | 简笔画/线稿风短视频，GSAP 主时间线，具象造型需检索临摹 | 第九章 |

### workflows · 组合工作流（6）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `ai-news-md-digest` | 自动采集 AI / Agent 资讯并持久化为 Markdown 快报 | 第九章适用 |
| `article-to-image-series` | 把文章、提纲或主题序列转成带 manifest 的多图系列 | 第九章 |
| `content-pdf-with-images` | 主题拆章、逐章配图并汇总排版为真实 PDF | 第九章 |
| `evolutionary-social-copy-pack` | 按演进主线批量输出公众号、小红书、X 与头条的文案包 | 第九章 |
| `image-series-to-video` | 从 PNG manifest 编排讲解视频并做自动化质量验收 | 第九章适用 |
| `research-to-slide-deck` | 把研究资料与 brief 转成可验证的幻灯片文稿 | 第九章 |

### marketplace · Marketplace（15）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `autoglm-websearch` | 基于 AutoGLM Web Search 本地服务做高性能网络检索 | 第十章适用 |
| `blogwatcher` | 命令行持续监控技术博客、专栏与 RSS/Atom 变更 | 第十章适用 |
| `browser-automation` | 基于 agent-browser 的无头浏览：点击、填表与截图 | 第十章 |
| `docx` | 高保真生成与编辑 Word（.docx）文档、表格和修订 | 第十章 |
| `find-skills` | 按任务意图从生态中搜索、评估并匹配可用技能 | 第十章 |
| `image-cog` | CellCog 文生图、图生图、角色一致性与电商图合成 | 第十章适用 |
| `image-resizer` | 按宽高、等比或体积上限批量缩放压缩图片 | 第九章 |
| `pdf` | PDF 文本与表格提取、合并拆分、表单填写与排版 | 第九章、第十章 |
| `pptx` | 结构化生成 PowerPoint，应用母版、图表并做视觉验收 | 第十章 |
| `self-improving-1.1.3` | 带自我反思与持久化记忆的自改进 Agent 技能 | 第十章适用 |
| `skill-vetter` | 审查第三方 Agent Skill 的权限范围、安全性与合规性 | 第十章；第十一章速查 |
| `skills-security-check` | 静态扫描第三方技能源码，防范后门、越权与密钥泄露 | 第十章 |
| `video-translator` | 视频/链接人声听翻、时间戳对齐与多语言配音 | 第十章适用 |
| `wan-image-video-generation-editting` | 通义万象 Wan：文生图、图编辑、文生视频与图生视频 | 第十章适用 |
| `xlsx` | 读写 Excel 工作簿，保留公式、样式与模板 | 第十章 |

### workspace-core · Workspace Core（24）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `codex-system/imagegen` | Codex 运行时捆绑的官方图像生成入口 | 第十章适用 |
| `codex-system/openai-docs` | 查询当前 OpenAI 官方文档与接口说明 | 第十章适用 |
| `codex-system/plugin-creator` | Codex 插件工程脚手架，用于创建可安装插件 | 第十章适用 |
| `codex-system/skill-creator` | 编写新 Skill 的结构、字段与校验约定 | 第十章 |
| `codex-system/skill-installer` | 安装 Skill 到工作区，装前应先做安全审查 | 第十章 |
| `openclaw/browser-automation` | OpenClaw 运行时的浏览器自动化辅助 | 第十章 |
| `openclaw/cron-helper` | 周期性定时任务的编写与调度辅助 | 第十章 |
| `openclaw/excel-xlsx` | OpenClaw 运行时的 Excel / XLSX 读写辅助 | 第十章适用 |
| `openclaw/find-skills-skill` | 在运行时生态中查找并匹配技能 | 第十章 |
| `openclaw/hermes-learning-loop` | Hermes 学习闭环：反思、纠错与记忆回写 | 第十章适用 |
| `openclaw/image-cog` | OpenClaw 侧的 CellCog 图像生成入口 | 第十章适用 |
| `openclaw/image-resizer` | OpenClaw 侧的图片缩放压缩入口 | 第十章适用 |
| `openclaw/pdf` | OpenClaw 运行时的 PDF 处理辅助 | 第十章 |
| `openclaw/powerpoint-pptx` | OpenClaw 运行时的 PowerPoint 生成与编辑辅助 | 第十章适用 |
| `openclaw/qmd` | Quick Markdown 知识索引与秒级检索 | 第十章 |
| `openclaw/remote-desktop` | 远程桌面（xfreerdp）交互辅助 | 第十章适用 |
| `openclaw/self-improving` | OpenClaw 自改进与主动挑错 Agent 辅助 | 第十章适用 |
| `openclaw/skylv-hermes-agent-integration` | OpenClaw 与 Hermes Agent 的集成入口 | 第十章适用 |
| `openclaw/tiangong-notebooklm-cli` | NotebookLM / 天工知识库的 CLI 封装 | 第十章适用 |
| `openclaw/video-translator` | OpenClaw 侧的视频翻译与配音入口 | 第十章适用 |
| `openclaw/virtual-remote-desktop` | 虚拟远程桌面（KasmVNC）交互辅助 | 第十章适用 |
| `openclaw/wan-image-video-generation-editting` | OpenClaw 侧的通义万象 Wan 模型入口 | 第十章适用 |
| `openclaw/web-search` | OpenClaw 运行时的网络检索辅助 | 第十章 |
| `openclaw/word-docx` | OpenClaw 运行时的 Word / DOCX 处理辅助 | 第十章适用 |

### vendored · 开源社区锁定引入（2，计入 94）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `image-svg-pptx-pro-skill` | 截图或学术图经 SVG 中间层重建为可编辑 PPTX | 第十章适用 |
| `xiaobei-skill-image-to-vba` | 截图生成 VBA，在 Office 中按形状 1:1 重建图形 | 第十章适用 |
