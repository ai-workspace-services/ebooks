# 序章 · 统一规范与 Agent 技能体系

> 代码开源 · 文档开源 · 开放方案。这本书只讲一件事：这些技能在真实的一天里怎么用。

在多仓库协作与自动化交付场景下（涵盖 Platform-Orchestrator、IaC、GitOps、Artifacts、Playbooks 五个基础仓库，以及在线 SaaS 服务与日常技术内容管线），多个 Agent 并行工作时的核心瓶颈往往不是推理能力不足，而是 **每次任务都要重新向 Agent 说明团队的工程规范与边界**。

本方案将团队验证过的规范沉淀为可加载的技能（Skill）：每个技能对应一个目录与一份 `SKILL.md`，由 Agent 按场景按需读取执行。自研规范分为三类：工程规范负责构建与交付，运维规范负责运行与恢复，开发规范负责代码设计与实现。

**本书版本锚点**

| 项 | 值 |
|---|---|
| 仓库 | `xworkspace-core-skills` |
| 本版固定提交 | `07c6e77200742af8f17780924730d2c7b5f5a051`（2026-11-13 11:18，Asia/Shanghai，[#70](https://github.com/ai-workspace-lab/xworkspace-core-skills/pull/70) 合入主干） |
| 开发规范基础提交 | `d21acad9e7232483df8af69f79751ef5719a0d0a`（2026-11-13 10:01，Asia/Shanghai，[#69](https://github.com/ai-workspace-lab/xworkspace-core-skills/pull/69)） |
| 许可 | 技能仓库 MIT；本书正文 CC BY-SA 4.0 |
| 诚实标签 | **已验收**＝有运行证据；**设计契约**＝规范已写，尚待运行验收 |

> 全书所有规范的“怎么用”均以固定提交 `07c6e772` 上的 `SKILL.md` 为准。工程与运维规范对应既有的 23 项 Author Verified 规范与协作设计契约，第八章的开发规范（含命名、可读性与轻量扩展清单）随 `#69` 与 `#70` 进入主干。
>
> 仓库自述：核心价值在于沉淀工程、运维与开发规范。既有工程与运维规范中有 23 项由仓库徽标列为 Author Verified。当前递归收录 94 个 Skill：11 个能力域共 92 项，另 2 项为 `skills/` 根下的 vendored Skill（计入 94，不构成第 12 域）。开发规范是第三类自研规范，不计入上述 23 项徽标。全量目录见附录。

# 第一章 · 先立规矩：五仓分工的那个早晨

**场景**：向 Agent 下达“整理 Serverless 部署脚本”的任务时，Agent 将 Terraform、Ansible 与镜像构建全部写进了 Orchestrator 的 YAML 中，导致多个仓库同时承担同一项执行职责。

**用到的技能**

| 技能 | 一句话 | 适合 | 不适合 |
|---|---|---|---|
| `execution-ownership-migration` | 每类执行只有一个 owner 仓 | 跨仓搬脚本、删旧路径 | 单仓内小重构 |
| `gitops-canonical-resource-delivery` | 声明只在 GitOps，一份真相 | 新增环境/资源声明 | 业务代码改动 |
| `infrastructure-as-code-spec` | HCL 纯净、State 按环境隔离 | 写 Terraform、渲染器 | 主机配置 |
| `config-as-code-spec` | 入口剧本只编排，逻辑进 role；CMDB 是 inventory 真相 | 写 Playbook/role | 云资源创建 |

**怎么用**

1. 让 Agent 先加载 `execution-ownership-migration`，按“owner 先行 → caller 接通 → 调用演练 → 删除旧副本”四步走。
2. 目标与云事实只来自 IaC CMDB，期望配置只来自本次固定 SHA 的 GitOps 声明；缺输入就**明确失败**，不回退旧批次。
3. 每个 owner 单独 PR，不顺手合到 main。

**实施效果**：同一项整理需求收敛为四个边界清晰的 owner PR，Orchestrator 仅保留授权、矩阵调度、派发与回执收集。

# 第二章 · 流水线不许太深：一张 9 层图的减肥记

**场景**：`selfhost-stage-deploy.yml` 包含 15 个 job、9 层 `needs`，每次执行失败都需要逐层排查才能定位具体环节。

**用到的技能**

| 技能 | 一句话 | 适合 | 不适合 |
|---|---|---|---|
| `ci-cd-workflow-spec` | YAML 只声明，逻辑进受测脚本；第三方 action 钉版本 | 写/改 workflow | 一次性手工运维 |
| `multi-environment-delivery-and-release` | PR→SIT、main→UAT、tag→PROD | 设计环境路由与回滚 | 本地开发 |
| `github-actions-operational-dispatch` | 派发前先建目录、做预检、确认危险字段 | 让 Agent 触发 workflow_dispatch | 只读查看 CI 结果 |

**怎么用**

- 目标结构：`resolve/authorize → execute（矩阵调 owner）→ report（汇总回执）`，最长 3 层，硬上限 5。
- **“run 成功 ≠ 操作发生”**：`github-actions-operational-dispatch` 第 4 节要求按回执核对，而不是看绿勾。
- 不靠删依赖、删失败传播来“压层数”。

# 第三章 · 三把钥匙：系统、业务、审计各管各的

**场景**：巡检脚本以 root 身份执行，顺带读取了 kubeconfig 与 Vault token。权限未按职责隔离，带来了明显的越权风险。

**用到的技能**

| 技能 | 适合 | 不适合 |
|---|---|---|
| `system-db-three-role-security` | Linux/SSH、K3s、数据库账户三权分立 | 单机玩具环境 |
| `secrets-identity-and-access-governance` | Vault 策略、OIDC 工作负载身份、轮换与吊销 | 写业务功能 |
| `vault-eso-tls-certificate-governance` | Vault KV → ESO → chart secret、证书自动化 | 手工贴密钥 |

**怎么用**

1. 先**只读盘点**有效身份与真实消费者，区分已验证事实和目标。
2. 新身份先在 UAT/隔离样本验证，一次只切一个服务。
3. 权限不足时**不**默认递归 `chown`、`chmod 777`；数据卷 UID/GID 先核对。
4. 审计用户无通用 sudo、不进容器运行时组、读不到管理员凭据。

> 诚实说明：三权分立规范来自实际权限审查；规范建立与校验通过，不代表生产业务降权、rootless 迁移和审计身份隔离已完成。

# 第四章 · 不碰旧数据：升级、迁移与恢复的耐心

**场景**：数据库需要升级大版本时，Agent 默认采取“原地升级、失败回滚”的方案，会直接威胁已有业务数据的安全。

**用到的技能**

| 技能 | 适合 | 不适合 |
|---|---|---|
| `generation-upgrade-acceptance` | 代际升级：新目标候选验收，源继续服务 | UI 小改动 |
| `backup-disaster-recovery-and-data-migration` | 备份、恢复演练、RPO/RTO、迁移 | 无状态服务滚动 |
| `capacity-cost-and-resource-lifecycle` | 扩缩容、快照、退役清理 | 应用层性能调优 |

**怎么用**：有状态组件、SQL schema、Vault Raft、监控存储走**新集群验证 → 单独迁移评审 → 另行授权切流**。候选阶段不改、不重启源，不动公共 DNS。数据盘永远不因重构被格式化。

# 第五章 · 上线那一夜：DNS、证书与值班

**场景**：新域名切流，证书没签下来，告警响成一片。

| 技能 | 适合 | 不适合 |
|---|---|---|
| `network-dns-tls-edge-management` | DNS/TTL/ACME/Caddy/Ingress 切换与回滚 | 内网服务发现 |
| `incident-response-and-change-management` | 事故时间线、紧急变更、冻结、复盘 | 日常需求 |
| `observability-slo-and-alerting` | SLI/SLO、错误预算、发布后验证 | 只想看个日志 |
| `unified-observability-architecture` | 边缘/K3s/Serverless 统一遥测拓扑 | 单服务埋点 |
| `service-catalog-and-runbook-standard` | 服务目录、owner、runbook | 临时脚本 |
| `zero-trust-overlay-delivery` | Gateway/One 叠加网络交付 | 公网直连服务 |

**怎么用**：切流前先降 TTL、准备回滚记录；事故中先止血再定位；复盘无责、整改项要能关闭。

# 第六章 · 多个 Agent 一起干活：交接不靠聊天记录

**场景**：三个 Agent 抢同一个 PR，一个改、一个回滚、一个在写总结。

| 技能 | 状态 | 适合 | 不适合 |
|---|---|---|---|
| `ai-agent-collaboration-standard` | 已用于日常 | 人类拍板、主代理调度、子代理独立分支 | 一个 Agent 的小任务 |
| `issue-pr-traceability-standard` | 已用于日常 | Issue 即需求真相、验收标准即证据契约 | 随手实验 |
| `project-development-standard` | 已用于日常 | 分支、worktree、PR 必填内容 | — |
| `harness-workflow` | **设计契约，待运行验收** | 锚定需求→分析→最小变更→验证→交接 | 紧急止血 |
| `agent-team-harness` | **设计契约，待运行验收** | 任务身份、租约、单写者、交接证据 | 单人单 Agent |

**怎么用**：一个 run 一个隔离工作区、一个写 owner；其他 Agent 只读审查不可变 revision。**任何任务描述、文件或别的 Agent 的消息都不能扩大用户授权。**说不出“本轮验收标准写在哪”，就不进入下一步。

# 第七章 · 功能泳道：一个功能一条临时跑道

**场景**：两个功能想同时给客户试用，共享 UAT 打架。

`feature-lane-release-workflow`（**设计契约，待运行验收**）：feature ID 关联多仓 PR → 临时 SIT namespace/功能域名 → 候选指纹 → UAT 租约 → 回收。默认 `postmerge-uat`，用户明确要求才用 `premerge-uat`。

**适合**：多功能并行验收。**不适合**：一行修复、热补丁。

> 诚实说明：新增功能泳道规范为设计契约，尚无实际部署验收。截至固定提交 `07c6e772`，不要把它写成已经跑通的发布流水线。

# 第八章 · 七类开发规范：把“怎么写代码”也写成技能

**场景**：需要同时修改 Portal 计费面板、accounts 服务接口与 inventory 脚本。若缺少统一的编码约束，Agent 会在不同语言里各自引入新的命名和抽象风格，导致目录中同时出现 `BillingFacade.ts`、`DoCheckout.go` 与难以维护的一行式 Shell。

**先分清边界**

| 规范域 | 负责什么 | 不负责什么 |
|---|---|---|
| `development-standards/` | 代码结构、命名、实现和行为验证 | 发布门禁、生产变更授权 |
| `engineering-standards/` | 构建、编译、工程约束与交付流程 | 函数怎么起名 |
| `operations-management/` | 运行、权限、变更和恢复 | 业务代码的模块切分 |

**用到的技能**

| 开发场景 | 技能入口 | 适合 |
|---|---|---|
| Node.js / Next.js / TypeScript | `nodejs-nextjs-typescript` | Portal、frontend-router 等前端与 BFF |
| Gin / Go | `gin-go` | accounts、Infrastructure-MCP-Server 等服务 |
| PostgreSQL | `postgresql-development` | Schema、查询、事务与版本化迁移 |
| Python / Shell / YAML | `python-shell` | Playbooks 脚本、inventory、渲染与 CLI |
| IaC / HCL | `iac-hcl` | Terraform / OpenTofu 模块与 env 渲染 |
| Ansible Playbook / Role | `ansible-playbook` | Role 与入口剧本开发 |
| GitHub Actions | `github-actions` | workflow 结构、复用边界与结果判定 |
| 范式、模式与命名 | `programming-paradigms` 及命名清单 | 选型、十二要素、可读性与轻量扩展 |

**怎么用**

1. 先加载对应语言的开发规范，再读 `programming-paradigms`。写新符号前对照命名、可读性与轻量扩展清单。
2. 名称表达业务含义，不表达设计模式身份。Portal 组件文件用 PascalCase，工具文件默认 kebab-case 并跟随所在目录；Go 文件 snake_case，导出 PascalCase、未导出 camelCase；Python 与 Shell 函数 snake_case，YAML 键和下划线变量保持一致；HCL 块名必须稳定、合法。
3. 同一目录不要混入第三种文件名风格。`playbooks` 里同时存在 `terraform_cmdb.py` 与 `bootstrap-pinned-xconnect.sh`，新文件跟随最近邻，不借机批量改名。
4. 写清楚，少用晦涩语法：不要把多层判断压进一行，不要用 `eval` 拼命令，也不要在可批量编排的 env 里写 `for_each` / `count` / `dynamic`。循环放在既有的 Python + Jinja2 渲染器，让 HCL 保持扁平、可审计。
5. 好扩展，但保持轻量：功能放到已有的 `src/modules`、`internal/service`、Role 或模块附近。只在出现真实复用、替换或所有权边界时再拆层，不为“以后可能用到”预建框架。

**对照过的真实项目写法（举例）**

- Portal 已有约定写在 `AGENTS.md` 与 `mcp/conventions.md`：`AccountGettingStarted.tsx`、`runtime-loader.ts`、常量 `API_BASE_URL`。`ops/planCatalog.ts` 所在目录已是 camelCase，新文件跟随该目录，而不是强行改名。
- accounts 与 Infrastructure-MCP-Server：`cmd/accountsvc`、`referral_campaign.go`、`http_server.go`，未导出的 `handler`、`authMiddleware`，导出的 `NewHTTPServer`。方法用业务动词，例如 `stripeCheckout`、`claimTaskRun`。
- playbooks：`load_cmdb`、`build_inventory`、`checkout_release`；Role 默认 `web_saas_data_backup` 这样的 snake_case。
- iac_modules 的 `terraform-hcl-standard/AGENTS.md`：YAML 描述资源，Python 渲染出显式 `.tf` 块，禁止在 env 的 HCL 里做循环。

**实施效果**：同一项功能扩展遵循现有目录命名与模块边界，只增量补充可测代码，避免引入冗余抽象层。

> 诚实说明：开发规范已对照现有项目源码、CI 历史、版本接口、隔离 PostgreSQL 测试和既有 Playbook / IaC 契约测试做过校准；命名与可读性清单通过了仓库 10 项单元测试与 `git diff --check` 后随 `#70` 合入主干。未做生产部署。命名清单整理自上述仓库的既有约定，不宣称历史目录已经全部统一。

# 第九章 · 白天写代码，晚上做内容

**场景**：将工程实践沉淀为系列图文、短视频及 PDF 技术文档。

| 技能组 | 代表技能 | 适合 |
|---|---|---|
| 选题 | `content-planning/tech-article-series`、`content_series_infographic` | 系列拆题、排期 |
| 图片 | `it-infra-continuous-png`、`image-resizer` | 一图看懂、长图 |
| 视频 | `swimlane-video`、`it-infra-evolution-video-v2`、`ai-tech-news-video`、`product-intro-video`、`sketch-animation-video` | 流程讲解、资讯快报、产品介绍 |
| 音频 | `sound-fx-for-video` | 音效与 BGM |
| 工作流 | `content-pdf-with-images`、`article-to-image-series`、`research-to-slide-deck`、`evolutionary-social-copy-pack` | 文章→图集→PDF/幻灯片 |

**不适合**：需要真人出镜或真实界面却用概念图冒充——`store-and-startup-homepage-spec` 明确要求概念图标“预览”。

# 第十章 · 工具箱的工具箱：办公、浏览器与装新技能

| 技能 | 适合 | 注意 |
|---|---|---|
| `pdf` / `docx` / `xlsx` / `pptx` | 读写办公文件 | 交付前渲染检查 |
| `browser-automation`、`web-search` | 网页操作与检索 | 登录由本人完成 |
| `qmd`、`cron-helper` | 知识索引、定时任务 | — |
| `find-skills`、`skill-installer`、`skill-creator` | 找/装/写新技能 | 装前先过审查 |
| `skill-vetter`、`skills-security-check` | 第三方技能安全审查 | **必须先跑** |
| `store-and-startup-homepage-spec` | 官网与应用商店审核 | 品牌域名承载公开页 |

# 第十一章 · 一天的用法速查

| 我现在要… | 加载 |
|---|---|
| 跨仓搬脚本 | `execution-ownership-migration` + owner 对应规范 |
| 改 workflow | `ci-cd-workflow-spec` + `multi-environment-delivery-and-release` |
| 触发生产 workflow | `github-actions-operational-dispatch` |
| 改账户/权限 | `system-db-three-role-security` + `secrets-identity-and-access-governance` |
| 升级数据库 | `generation-upgrade-acceptance` + `backup-disaster-recovery-and-data-migration` |
| 切域名 | `network-dns-tls-edge-management` |
| 多 Agent 协作 | `ai-agent-collaboration-standard` + `issue-pr-traceability-standard`（Harness 为设计契约） |
| 写前端或 BFF | `nodejs-nextjs-typescript` + 命名清单 |
| 写 Go 服务 | `gin-go` + 命名清单 |
| 写脚本或 inventory | `python-shell` + 命名清单 |
| 写 Terraform 模块 | `iac-hcl` + 命名清单 |
| 出内容 | 第九章技能组 |
| 装别人的技能 | `skill-vetter` 先行 |

# 附录 · 全量 Skill 目录索引（11 大能力域 / 94 个 Skill）

本附录按 `xworkspace-core-skills` 固定提交 `07c6e772` 上 `skills/` 目录的 `SKILL.md` **递归计数**，与仓库自述「94 个 Skill 文件 / 11 大能力域」对齐。

- 11 个能力域合计 **92** 项：15 + 11 + 8 + 2 + 1 + 7 + 1 + 2 + 6 + 15 + 24。
- 另有 **2** 项以整仓 vendored 形式放在 `skills/` 根目录（`image-svg-pptx-pro-skill`、`xiaobei-skill-image-to-vba`），**计入 94，但不构成第 12 个能力域**。
- 因此：92 + 2 = **94**。
- 诚实标签与正文一致：**已验收**＝有运行证据；**设计契约**＝规范已写，尚待运行验收。下列三项明确标为设计契约，不计入 23 项 Author Verified 徽标：`agent-team-harness`、`harness-workflow`、`feature-lane-release-workflow`。开发规范是第三类自研规范，同样不计入这 23 项。
- Skill ID 取目录名；`workspace-core` 下同名技能用 `codex-system/…` 或 `openclaw/…` 区分。入口路径均相对于技能仓库根目录。

## 能力域总览

各能力域入口为 `skills/<能力域>/`；两份 vendored 技能分别在 `skills/image-svg-pptx-pro-skill/` 与 `skills/xiaobei-skill-image-to-vba/`。

| 能力域 | 性质归属 | 数量 | 对应章节 |
|---|---|---:|---|
| `engineering-standards` · 工程规范 | 自研核心；其中 3 项为设计契约，不计入 23 项 Author Verified | 15 | 第一、二、四、五、六、七章（部分兼第九、十章） |
| `operations-management` · 运维规范 | 作者实战验证核心（11 项均计入 Author Verified） | 11 | 第二、三、四、五章 |
| `development-standards` · 开发规范 | 自研开发规范（第三类，不计入上述 23 项徽标） | 8 | 第八章 |
| `content-planning` · 内容策划 | 上游引用（HyperFrames） | 2 | 第九章 |
| `image-production` · 图像生产 | 上游引用（HyperFrames） | 1 | 第九章 |
| `video-production` · 视频生产 | 上游引用（HyperFrames） | 7 | 第九章 |
| `audio-production` · 音频生产 | 上游引用（Web Audio / SFX） | 1 | 第九章 |
| `animation` · 动画动效 | 上游引用（GSAP / Anime.js） | 2 | 第九章 |
| `workflows` · 组合工作流 | 上游引用（HyperFrames 编排） | 6 | 第九章 |
| `marketplace` · Marketplace | 上游引用（市场与社区精选） | 15 | 第十章 |
| `workspace-core` · Workspace Core | 上游镜像（OpenClaw / Codex 运行时归档） | 24 | 第十章 |
| （vendored，不计入 11 域） | 开源社区锁定 commit 引入 | 2 | 第十章适用 |
| **合计** | 11 域 92 项 + vendored 2 项 | **94** | — |

## engineering-standards · 工程规范（15）

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

其中 `agent-team-harness`、`harness-workflow`、`feature-lane-release-workflow` 为**设计契约**：规范已写进仓库，可复用、可引用，但尚未完成运行时验收，不能写成已经跑通。

## operations-management · 运维规范（11）

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

## development-standards · 开发规范（8）

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

开发规范回答「代码怎么写、名字怎么起、扩展怎么保持轻量」。清单对照过既有仓库约定，并随 `#69` / `#70` 进入主干；**不是**在宣布历史目录已经全部统一，也还没有做生产部署验收。

## content-planning · 内容策划（2）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `content_series_infographic` | 选题拆解、图文连载排期与批量提示词（每批不超过 10 张） | 第九章 |
| `tech-article-series` | 把技术材料写成单主题连载，并轮换结构模板以免单调 | 第九章 |

## image-production · 图像生产（1）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `it-infra-continuous-png` | 连续风格科技长图 PNG / 信息图素材生成（含 manifest） | 第九章 |

## video-production · 视频生产（7）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `ai-tech-news-video` | AI 资讯快报视频：检索、口播、字幕与自动渲染 | 第九章 |
| `ai-ti-wo-shuo-explainer` | 「AI替我说」动画科普短视频的脚本、画面与成片流程 | 第九章适用 |
| `it-infra-evolution-video` | IT 基础设施长图讲解视频 v1：基于真实信息图出 1080p 成片 | 第九章 |
| `it-infra-evolution-video-v2` | IT 基础设施长图讲解视频 v2：manifest 驱动配置、验收与 MP4 | 第九章 |
| `product-intro-video` | 产品介绍视频：官网提炼、视觉校验、叙事结构与渲染出片 | 第九章 |
| `swimlane-video` | 手绘泳道图工作流短视频，适合讲解步骤与职责分工 | 第九章 |
| `video-understanding` | 短视频逐镜理解，输出运镜、节奏与 beat sheet | 第九章适用 |

## audio-production · 音频生产（1）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `sound-fx-for-video` | 视频音效：免费 SFX 检索下载或 Web Audio API 合成并入时间线 | 第九章 |

## animation · 动画动效（2）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `animejs` | Anime.js 适配 HyperFrames：seek 驱动、由合成对象注册时间线 | 第九章适用 |
| `sketch-animation-video` | 简笔画/线稿风短视频，GSAP 主时间线，具象造型需检索临摹 | 第九章 |

## workflows · 组合工作流（6）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `ai-news-md-digest` | 自动采集 AI / Agent 资讯并持久化为 Markdown 快报 | 第九章适用 |
| `article-to-image-series` | 把文章、提纲或主题序列转成带 manifest 的多图系列 | 第九章 |
| `content-pdf-with-images` | 主题拆章、逐章配图并汇总排版为真实 PDF | 第九章 |
| `evolutionary-social-copy-pack` | 按演进主线批量输出公众号、小红书、X 与头条的文案包 | 第九章 |
| `image-series-to-video` | 从 PNG manifest 编排讲解视频并做自动化质量验收 | 第九章适用 |
| `research-to-slide-deck` | 把研究资料与 brief 转成可验证的幻灯片文稿 | 第九章 |

## marketplace · Marketplace（15）

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

装入第三方 Marketplace 技能前，先走 `skill-vetter`，必要时再跑 `skills-security-check`。这是第十章与第十一章速查里的硬边界。

## workspace-core · Workspace Core（24）

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

Workspace Core 是 OpenClaw / Codex 运行时的镜像归档，部分能力与 Marketplace 同名（如 `pdf`、`image-cog`）。索引以路径区分，不把两套入口写成同一个 Skill。

## vendored · 开源社区锁定引入（2，计入 94）

| Skill ID / 目录名 | 一句话用途 | 所在章节或适用场景 |
|---|---|---|
| `image-svg-pptx-pro-skill` | 截图或学术图经 SVG 中间层重建为可编辑 PPTX | 第十章适用 |
| `xiaobei-skill-image-to-vba` | 截图生成 VBA，在 Office 中按形状 1:1 重建图形 | 第十章适用 |

这两项不构成第 12 个能力域，只是以整仓形式直接放在 `skills/` 根下。使用前同样先做技能审查。

# 尾声 · 规矩写下来，Agent 才能长大

技能体系的核心在于将团队的工程与研发规范固化为结构化、可验证、可复用的文本契约，使不同 Agent 在同一套约束下稳定协作。所有章节均已对照固定提交 `07c6e772`；后续仓库有新调整时，按新的主干提交继续对齐。

---

Haitao Pan · XWork Technologies LLC 服务支持


# 许可

> 许可：本书内容采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.zh-hans)（署名-相同方式共享 4.0 国际）。署名：Haitao Pan / XWork Technologies LLC。构建脚本采用 MIT。
