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
> 仓库自述：核心价值在于沉淀工程、运维与开发规范。既有工程与运维规范中有 23 项由仓库徽标列为 Author Verified。当前递归收录 94 个 Skill，分 11 个能力域。开发规范是第三类自研规范，不计入上述 23 项徽标。

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

# 尾声 · 规矩写下来，Agent 才能长大

技能体系的核心在于将团队的工程与研发规范固化为结构化、可验证、可复用的文本契约，使不同 Agent 在同一套约束下稳定协作。所有章节均已对照固定提交 `07c6e772`；后续仓库有新调整时，按新的主干提交继续对齐。

---

Haitao Pan · XWork Technologies LLC 服务支持


# 许可

> 许可：本书内容采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.zh-hans)（署名-相同方式共享 4.0 国际）。署名：Haitao Pan / XWork Technologies LLC。构建脚本采用 MIT。
