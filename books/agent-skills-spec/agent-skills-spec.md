# 序章 · 一个人，十几个 Agent，和一座会说话的工具箱

> 代码开源 · 文档开源 · 开放方案。这本书只讲一件事：这些技能在真实的一天里怎么用。

故事的主角叫小潘：一个独立开发者，手里有五个基础仓库（Platform-Orchestrator、IaC、GitOps、Artifacts、Playbooks）、一个要上线的 SaaS、一个每天要更的内容号，还有十几个同时在跑的 Agent。

他发现最大的问题不是 Agent 不够聪明，而是 **每个 Agent 都要重新被教一遍“我们家的规矩”**。于是他把规矩写成了技能（Skill）：每个技能是一个目录、一份 `SKILL.md`，Agent 在对的场景里自己加载。

**本书版本锚点**

| 项 | 值 |
|---|---|
| 仓库 | `xworkspace-core-skills` |
| 固定提交 | `a545f5fa8717d7a764a8a06e8fcc6f08a7c71d4c` |
| 许可 | MIT |
| 诚实标签 | **已验收**＝有运行证据；**设计契约**＝规范已写，尚待运行验收 |

> 本书所有“怎么用”均以该提交下的 `SKILL.md` 为准。仓库后续变动请以新 SHA 重新核对。

# 第一章 · 先立规矩：五仓分工的那个早晨

**场景**：小潘让 Agent “把 Serverless 部署脚本整理一下”。Agent 很勤快——把 Terraform、Ansible、镜像构建全塞进了 Orchestrator 的 YAML 里。第二天，三个仓库都在执行同一件事。

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

**故事结局**：同样的“整理一下”，变成了四个干净的 owner PR，Orchestrator 只剩授权、矩阵、派发和收回执。

# 第二章 · 流水线不许太深：一张 9 层图的减肥记

**场景**：`selfhost-stage-deploy.yml` 有 15 个 job、9 层 `needs`。每次失败，小潘要往下翻十分钟才知道是哪一步。

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

**场景**：一次巡检脚本用了 root，顺手读到了 kubeconfig 和 Vault token。没出事，但小潘一夜没睡。

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

# 第四章 · 不碰旧数据：升级、迁移与恢复的耐心

**场景**：数据库要升大版本。Agent 的第一反应是“原地升级，失败就回滚”。小潘按住了它。

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

> 诚实说明：本章流程为规范层设计，截至 `a545f5fa` 未有完整生产运行证据。

# 第八章 · 白天写代码，晚上做内容

**场景**：小潘把当天的工程实践变成一组图文、一条短视频和一本 PDF。

| 技能组 | 代表技能 | 适合 |
|---|---|---|
| 选题 | `content-planning/tech-article-series`、`content_series_infographic` | 系列拆题、排期 |
| 图片 | `it-infra-continuous-png`、`image-resizer` | 一图看懂、长图 |
| 视频 | `swimlane-video`、`it-infra-evolution-video-v2`、`ai-tech-news-video`、`product-intro-video`、`sketch-animation-video` | 流程讲解、资讯快报、产品介绍 |
| 音频 | `sound-fx-for-video` | 音效与 BGM |
| 工作流 | `content-pdf-with-images`、`article-to-image-series`、`research-to-slide-deck`、`evolutionary-social-copy-pack` | 文章→图集→PDF/幻灯片 |

**不适合**：需要真人出镜或真实界面却用概念图冒充——`store-and-startup-homepage-spec` 明确要求概念图标“预览”。

# 第九章 · 工具箱的工具箱：办公、浏览器与装新技能

| 技能 | 适合 | 注意 |
|---|---|---|
| `pdf` / `docx` / `xlsx` / `pptx` | 读写办公文件 | 交付前渲染检查 |
| `browser-automation`、`web-search` | 网页操作与检索 | 登录由本人完成 |
| `qmd`、`cron-helper` | 知识索引、定时任务 | — |
| `find-skills`、`skill-installer`、`skill-creator` | 找/装/写新技能 | 装前先过审查 |
| `skill-vetter`、`skills-security-check` | 第三方技能安全审查 | **必须先跑** |
| `store-and-startup-homepage-spec` | 官网与应用商店审核 | 品牌域名承载公开页 |

# 第十章 · 一天的用法速查

| 我现在要… | 加载 |
|---|---|
| 跨仓搬脚本 | `execution-ownership-migration` + owner 对应规范 |
| 改 workflow | `ci-cd-workflow-spec` + `multi-environment-delivery-and-release` |
| 触发生产 workflow | `github-actions-operational-dispatch` |
| 改账户/权限 | `system-db-three-role-security` + `secrets-identity-and-access-governance` |
| 升级数据库 | `generation-upgrade-acceptance` + `backup-disaster-recovery-and-data-migration` |
| 切域名 | `network-dns-tls-edge-management` |
| 多 Agent 协作 | `ai-agent-collaboration-standard` + `issue-pr-traceability-standard`（Harness 为设计契约） |
| 出内容 | 第八章技能组 |
| 装别人的技能 | `skill-vetter` 先行 |

# 尾声 · 规矩写下来，Agent 才能长大

技能不是魔法，是把“我们家的规矩”写成 Agent 能读懂的文字。拉取 `a545f5fa`，挑一章的场景，今天就试一次。

---

Haitao Pan · XWork Technologies LLC 服务支持


# 许可

> 许可：本书内容采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.zh-hans)（署名-相同方式共享 4.0 国际）。署名：Haitao Pan / XWork Technologies LLC。构建脚本采用 MIT。
