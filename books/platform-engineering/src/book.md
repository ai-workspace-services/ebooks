# 序 工具拼在一起 ≠ 平台

很多团队都有 Git、有流水线、有 Terraform 脚本、有 Ansible、有 Vault，也有 Grafana。把这些开源 Logo 摆在一张图上，看起来像一个平台，可真到了出事那天，大家才发现：谁改了生产配置查不到，环境要等两周，密码写在共享文档里，换一家云就得重来一遍。

这本书只讲一个判断：**工具拼在一起 ≠ 平台**。平台是每一层都有它该干的事，层与层之间有清楚的合同。我们把它拆成七层：Git 与 CI、资源即代码、交付引擎、安全与身份、环境治理、云中立、可观测。它是一个以 Git 为入口、OpenTofu 为资源引擎、Ansible 为交付引擎、Vault 为安全边界的 Open Platform。

全书有一条原则：**所有的一切都最大程度自建**。每一层都先给出能自建的方案，托管服务只作对照。所以 Git 这一层，自建的 Gitea + Gitea Actions 和 GitHub + GitHub Actions 并排对等着讲，Gitea 多讲一些，因为它能完全放在你自己的机器上。

书里的案例不是虚构的。每章末尾都有一个「实践：ai-workspace-infra」框，对应这个开源组织里真实的仓库、工作流和已合并的 PR。你可以点开源码，对照着看。

这是一本**活的书**。它跟着实践持续更新，像流动的水，不是图书馆里放旧了的教材。每出一个版本，都用同一个重建脚本出 PDF，版本号写在封面上。当前是 v0.9.17 预览版（「最佳实践参考」升为与上下篇平行的实践篇第 17 章，四个 case 编为 17.1–17.4；v0.9.16 Case C 发布解析补全为完整草案与检查清单；v0.9.15 新增最佳实践参考：OS 三身份、K3s role 依赖、发布解析、PROD-K3S 变更记录模版四个 case；v0.9.14 新增 10.2 五个仓库的职责分工表；v0.9.13 新增 5.11 Vault KV → ExternalSecret → chart Secret 的默认引用、5.12 容器与非容器 SaaS 的 OIDC 接入；v0.9.12 新增 5.10 主机与集群的三角色；v0.9.11 编排仓库更名为 Platform-Orchestrator；v0.9.10 新增 6.12 多环境 × 多分支 × 滚动发布 × 特性泳道）：全书分上篇、下篇和实践篇。上篇「经典平台工程」10 章，第 2–9 章各附一页快速开始；下篇「现代平台工程」由导言和第 11–16 章组成，第 11 章附快速开始；实践篇「最佳实践参考」为第 17 章，记录正在推进的真实 case。全书 17 章正文均已写成，之后按实践持续更新。

作者 Haitao Pan ｜ XWork Technologies LLC 服务支持 · xworktech.com 开源平台方案

[[fig0]]

## 1 从自由软件到平台工程

这一章是铺垫：平台工程不是凭空出现的新词。它站在几十年开放软件实践的肩膀上，从自由软件、开源社区、开源商业、社区发行版，一路走到中台和今天的平台工程。我们只讲每一步留下了什么，后面十章全部讲实践。

### 1.1 自由软件：GNU、copyleft 与 GPL

1983 年 9 月 27 日，Richard Stallman 发布了 GNU 计划的最初公告，目标是写一个完全自由的类 Unix 操作系统。1985 年，自由软件基金会（FSF）成立。

自由软件的「自由」不是价格，而是四项基本自由：为任何目的运行程序（自由 0）；研究并修改程序（自由 1）；再分发副本（自由 2）；分发修改后的版本（自由 3）。

为了让这些自由不被后来者收走，GNU 用了 copyleft：任何人都可以修改和分发，但分发的衍生作品必须带着同样的自由。GPL 就是 copyleft 的代表：第 1 版发布于 1989 年 2 月，第 2 版于 1991 年 6 月，第 3 版于 2007 年 6 月 29 日。

[[fig11]]

### 1.2 开源社区：Linux 与 OSI

1991 年 8 月 25 日，Linus Torvalds 在 comp.os.minix 新闻组发帖，宣布自己在写一个「只是爱好」的操作系统内核，这就是 Linux。Linux 内核采用 GPLv2，和 GNU 的工具链一起，组成了今天最常见的 GNU/Linux 系统。

1998 年 2 月 3 日，在加州 Palo Alto 的一次策略会上，「open source」这个说法被提了出来，同年开放源代码促进会（OSI）成立。开源换了一种更贴近商业的说法，但核心没变：代码开放，协作开发。

对平台工程来说，开源社区留下的最重要的东西是**协作方式**：公开的代码、公开的评审、公开的问题追踪。本书所有工具，从 Gitea 到 OpenTofu，都是这样长出来的。

### 1.3 开源商业：Red Hat 与 SUSE

代码免费，钱从哪里来？Red Hat 和 SUSE 给出的答案是**订阅与服务**：上游代码开放，企业买的是经过测试和认证的发行版、长期支持、安全更新和出了问题有人负责。

SUSE 成立于 1992 年，称自己是第一家提供企业级 Linux 发行版的公司。Red Hat 以 Red Hat Enterprise Linux（RHEL）为核心，后来扩展到 OpenShift 等产品；2019 年 7 月 9 日，IBM 宣布完成对 Red Hat 的收购，交易金额约 340 亿美元。

这个模式告诉我们：开放和商业不矛盾。平台团队也一样，可以完全建立在开源软件上，靠集成、运维和服务创造价值。

[[fig12]]

### 1.4 社区发行版：Debian 与社会契约

1993 年 8 月，Ian Murdock 在普渡大学读本科时创立了 Debian。和商业发行版不同，Debian 完全由社区志愿者维护。

1997 年 7 月 5 日，Debian 社会契约 1.0 版获得批准，同时提出了 Debian 自由软件指导方针（DFSG）。社会契约写明了 Debian 对用户和自由软件社区的承诺，DFSG 后来成为 OSI「开源定义」的基础。

社区发行版留下的是**治理**：规则写下来、公开、可以修改。本书反复强调的「把约定写成代码和合同」，就是这种精神在平台上的延续。

### 1.5 从中台到平台工程

国内最熟悉的说法是「中台」。2015 年 12 月 7 日，阿里巴巴 CEO 张勇在全员公开信中宣布启动「2018 年中台战略」，构建「大中台、小前台」的组织和业务机制，成立中台事业群，整合产品技术和数据能力，支撑前台业务。

之后很多公司都学着建中台，也出现了更轻的「小中台」、各种「技术平台」的做法。中台偏向共享业务和数据能力；技术平台和平台工程更关注基础设施和工程效率。

今天行业里说的平台工程，是建设一个**自助、可编程的内部平台**，把基础设施、交付、安全、可观测这些能力做成产品，让开发团队按需取用。CNCF 的 Platforms 白皮书对此有系统的阐述。

[[fig13]]

本书的立场是：平台要建立在开源软件和开放标准之上，所有的一切最大程度自建。下一章从平台的入口 Git 与 CI 开始。

:::practice
**process-exporter**：fork 自上游 Prometheus 社区的 /proc exporter：直接站在社区成果上，而不是从零重写。
**postgresql.example.com**：开源的 PostgreSQL + pgvector 方案，附部署脚本与文档：代码开放，价值在集成与运维。
:::

## 2 Git 与 CI：一切从 commit 开始

平台的第一层是 Git 与 CI。规则只有一条：**所有变更都从一次 commit 开始，走流水线**。没有「我上去改一下」，也没有只存在于某个人电脑上的脚本。

### 2.1 为什么一切变更都走流水线

手工变更有三个问题：没人评审，没有记录，没法重复。流水线把这三件事一次解决：变更以 PR 的形式被评审，执行记录留在 CI 日志里，同一条流水线可以在 SIT、UAT、PROD 重复执行。

CI 在平台里的角色要克制：**只读验证，产出构件**。它负责 lint、测试、构建、出 plan，产出不可变的构件和 tag；真正改变环境的，是后面消费这些构件的交付步骤。

[[fig21]]

### 2.2 为什么不是 Jenkins / GitLab CI

CI 工具的选择，本书只看三条原则：能不能自建、是不是云中立、同一份流水线能不能带着走。按这三条，把四个常见选项放在一起看：

:::table
维度|Jenkins|GitLab CI|GitHub Actions|Gitea Actions
托管与自建|只能自建（Java 应用）|GitLab 官方 SaaS 托管，或自建 GitLab|GitHub 官方 SaaS 托管；runner 可自建|自建，内置于 Gitea（1.19 起）
流水线定义|Jenkinsfile（Groovy DSL）|.gitlab-ci.yml|.github/workflows/*.yml|.gitea/workflows/*.yml，语法与 GitHub Actions 基本兼容
插件与生态|插件体系，覆盖面广|内置功能为主，CI/CD 组件|Marketplace 中的 actions|可直接复用 GitHub Actions 的 actions
资源占用（官方文档）|最低 256 MB 内存，小团队建议 4 GB+|单节点基线 8 vCPU / 16 GB，受限环境至少 8 GB|托管侧不占自己的资源|小团队通常 2 核 / 1 GB 即可
流水线可移植性|绑定 Jenkins|绑定 GitLab|与 Gitea Actions 基本互通|与 GitHub Actions 基本互通
:::

Jenkins 的问题不在能力，而在形态：它只是 CI，Git 托管、评审、权限还要另外搭，再用插件把它们粘起来；流水线用 Groovy 写在 Jenkinsfile 里，换平台就得重写。GitLab 把 Git 和 CI 放在了一处，方向是对的，但自建一套的官方单节点基线是 8 vCPU、16 GB 内存，对「一台机器起步」的平台来说太重，而且 .gitlab-ci.yml 只在 GitLab 上跑。

GitHub Actions 加 Gitea Actions 的组合正好补上这两点。Gitea 自带 Git 托管、代码评审、包仓库和 CI，官方说 2 核 1 GB 通常就够小团队用；Gitea Actions 按 GitHub Actions 的语法设计，可以直接引用现成的 actions，runner 也是自建的独立程序。于是同一份 workflow YAML，既能在 GitHub 上跑，也能在自建的 Gitea 上跑：GitHub 当公共协作面，Gitea 当自建兜底，任何一方都不是锁定点。两者也有差异（例如 Gitea 会忽略 `jobs.<job_id>.environment`，job token 的权限范围也不同），所以组织基线里要把这些差异写进合同和测试。

这不是说 Jenkins 和 GitLab 不好。已经有大量 Jenkinsfile 和插件资产的团队、需要复杂构建编排或特殊硬件代理的场景，Jenkins 仍然合适；需要一站式 DevSecOps、愿意投入资源运维完整套件的组织，GitLab 仍是成熟的选择。本书只是按「自建优先、云中立、一台机器起步」的原则，选了迁移成本最低的那条路。

### 2.3 Gitea + Gitea Actions：自建入口

按全书「最大程度自建」的原则，Git 入口首选 Gitea。它是一个轻量的自建 Git 服务，单个二进制或一个容器就能跑起来。从 Gitea 1.19 开始，Gitea Actions 作为内置的 CI/CD 方案提供，官方文档的说法是它与 GitHub Actions 相似且**大部分兼容**。

执行任务的 runner 是 act_runner，同样自建在你自己的机器上。这意味着代码、流水线和执行环境全部在你掌控之中，不依赖任何外部托管服务。

### 2.4 GitHub + GitHub Actions：对等对照

GitHub + GitHub Actions 与 Gitea 对等着讲：工作流语法相同，概念一致，runner 可以用托管的，也可以自托管。很多团队两边都用：公开协作放 GitHub，内部或敏感仓库放自建 Gitea，同一份工作流尽量两边都能跑。

写工作流时守住两点，就能保持可迁移：不依赖某一边独有的特性；凭据一律通过 OIDC 向 Vault 换取（第 5 章），不在平台变量里存长期密码。

[[fig22]]

### 2.5 Reusable Workflows 与组织基线

仓库一多，每个仓库各写一套流水线就会走样。做法是把公共流水线写成可复用工作流，放在一个组织级基线仓库里，各仓库用 `uses:` 调用。安全基线、发布规则、合同测试，只在一个地方维护。

ai-workspace-infra 的 `.github` 仓库就承担这个角色：组织主页称它提供全局标准的 CI/CD Reusable Workflows 和 OIDC + Vault 零信任身份鉴权基线。

[[fig23]]

### 2.6 触发路由：PR、main、tag 各走各的路

流水线要回答一个问题：这次触发，对应哪个环境、能做什么。`Platform-Orchestrator` 的 README 把它写成了一张表：PR 默认对应 `sit`，只做验证和 plan；推送到 `main` 或 `release/*` 对应 `uat`，验证和 plan；`v*` tag 对应 `prod`，是生产发布路径；只有手动触发的 `workflow_dispatch` 才真正执行开通、部署、迁移、备份、恢复等动作。

这张表的价值在于：「什么事件能改什么环境」写在了明处，评审时一眼能看出越界。

### 2.7 发布分支与 PR 校验

发布线也要有规则。`playbooks` 仓库约定 `main` 是 preview 分支，`release/*` 是生产发布线，只接受 release manager 的 cherry-pick，禁止 force-push、要求线性历史，release 分支的 PR 由 `validate-release-pr.yml` 工作流做策略校验。规则写进流水线，就不用靠人记。

:::practice
**Platform-Orchestrator**：GitHub Actions 控制面与编排仓库，入口工作流 `.github/workflows/selfhost-orchestrator.yml`；触发路由 PR→sit、main/release/*→uat、v* tag→prod、workflow_dispatch 执行实际动作。
**.github**：组织级 Reusable Workflows 与 OIDC + Vault 身份基线（据组织主页）。
**playbooks**：`release/*` 发布线策略与 `validate-release-pr.yml` 校验，按业务域的 `*-domain-cd.yaml` 交付工作流。
:::

## 3 资源即代码：环境 apply 就出来

资源即代码的目标很直接：服务器、网络、存储、身份，全部写成声明，评审之后 apply，环境就出来了。没有控制台里点出来、没人说得清来历的资源。

### 3.1 资源即代码的边界

先划清边界：资源层只管**计算、网络、存储、身份**这些「有没有」的问题；机器上装什么软件、怎么配置，交给下一章的交付引擎。

`iac_modules` 的 README 把这条线写得很清楚：Terraform 只负责 compute / network / storage / identity，软件配置属于 CMDB 合同另一侧的 playbooks 仓库。两层之间唯一的接口是 CMDB。

### 3.2 OpenTofu 与开放许可

本书的资源引擎首选 OpenTofu：它由 Linux Foundation 旗下项目维护，采用 MPL-2.0 开源许可，命令和 HCL 写法与 Terraform 工作流一致，现有代码迁移成本很低。

需要说明的是，ai-workspace-infra 的 `iac_modules` 目前使用的是 Terraform；书里讲的模式两边通用，换用 OpenTofu 时主要是把命令从 `terraform` 换成 `tofu`，并按 OpenTofu 文档核对 provider 与 state 的兼容性。

[[fig31]]

### 3.3 声明、渲染、执行：HCL 里不写逻辑

`iac_modules` 采用了一个很干净的范式：唯一手工编辑的入口是 `gitops` 仓库里的 YAML 声明（`resources/<project>/<env>/<provider>/<group>.yaml`）；Python + Jinja2 把它渲染成显式的 HCL，每台主机一个独立的块；apply 之后输出运行时事实（IP、实例 ID），再生成 `cmdb.json` 和 `inventory.ini`，交给 Ansible。

由此引出几条硬规则：HCL 里不写 `for_each` / `count` / `dynamic` 这类控制结构，循环在渲染时展开；拓扑（地域、规格、数量、域名）只放在 YAML；HCL 里不嵌脚本，不用 `local-exec`；渲染产物不入库。

### 3.4 模块与版本钉住

模块是可复用的资源单元。消费方要按 tag 或提交 SHA 钉住模块版本：SIT、UAT、PROD 用同一个版本，升级本身是一次被评审的变更。跟着移动分支走的模块引用，会让同一份代码在不同时间 apply 出不同的结果。

[[fig32]]

### 3.5 State：每个环境一个命名空间，自建后端

State 是资源层最敏感的东西。`iac_modules` 的规则是：`sit` / `uat` / `prod` 永不共享同一个 backend key，规范路径形如 `terraform/<env>/<project>/<cloud>/<account>/<workspace>/terraform.tfstate`；后端是 S3 兼容存储，连接参数只从 Vault 的 `CICD/<env>/iac_state` 读取。

S3 兼容存储可以完全自建。再加上状态锁，保证同一时刻只有一个 apply 在改同一个环境。

[[fig33]]

### 3.6 多云 provider：同一个范式，不同成熟度

一个范式套多家云，才谈得上云中立。`iac_modules` 在 `terraform-hcl-standard/` 下为每家 provider 建同样的三层结构（声明、模板、组合逻辑），并如实标注成熟度：AWS 与 Vultr 为生产级，Akamai Cloud / Linode 为 MVP，阿里云为部分完成，GCP 为核心基线，Azure 为骨架。把成熟度写明，比假装每家都一样好更有用。

另外，密钥从不经过文件：API key 以 `TF_VAR_*` 环境变量传入，生成的凭据推回 Vault，供 Ansible 读取。


### 3.7 资源交接：从声明到 CMDB

实践中最容易出问题的是「资源建好之后」：IP、规格被人抄进配置，或者 Ansible 直接去读 tfstate，于是多出一份手工事实。做法是让交接只朝一个方向走：

[[figW3]]

- 循环和组合只写在 renderer 里，生成的 HCL 保持显式资源块，便于审查 plan。
- HCL、tfvars、cmdb.json、inventory 都是派生产物：可以重新生成，不手工修改，也不提交回声明仓库。
- 每次 IaC 变更后刷新 inventory；playbook 只读 CMDB，不读 tfstate。
- 声明仓库可以放公钥、公开 origin 和密钥引用，不放私钥、密码、API key 或数据库连接串。缺少预期声明时，下游直接失败。

**state 的路径按维度排列**。每一层都是 state 边界的一部分：

:::code
terraform/<scope>/<project>/<provider>/<account>/<workspace>/terraform.tfstate
:::

- account 写具体、稳定的账号标识，不用 default、primary、main 这类别名，否则两个账号会被悄悄合进同一份 state。
- 云厂商身份和 state backend 的凭据分开管理；改了密钥存放位置，并不会自动迁移 state。
- 迁移 state 的检查单：记录新旧 key → 受控执行迁移 → validate → plan 无漂移 → 验收前保留旧对象和旧 backend。

:::practice
**iac_modules**：gitops YAML → Python + Jinja2 渲染显式 HCL → apply → `cmdb.json` + `inventory.ini`；HCL 无控制结构、无拓扑、无嵌入脚本；每环境独立 state key，后端参数来自 Vault；多 provider 成熟度表。
**gitops**：`resources/<project>/<env>/<provider>/` 是资源声明的唯一手工入口。
**Platform-Orchestrator**：编排入口，按触发路由调用 IaC 渲染与执行。
:::

## 4 交付引擎：幂等地把软件装上去

资源出来以后，软件要装上去。交付引擎的要求是：**跑一次和跑十次，结果一样**；机器换了、扩了，执行逻辑不用改。

### 4.1 交付引擎的职责

交付引擎接过资源层交来的 CMDB，在机器上完成系统初始化、软件安装、配置渲染和服务启动。它不创建云资源，也不保存秘密，凭据在运行时从 Vault 取。

本书用 Ansible 做交付引擎：无需在目标机器上装 agent，通过 SSH 执行；任务以声明式模块描述期望状态。

### 4.2 role 与场景 playbook

Ansible 的组织方式是 role 加 playbook：role 是一个组件的安装与配置，playbook 把多个 role 拼成一个可执行的场景。

`playbooks` 仓库就是按「role 组织、playbook 编排」建起来的 Ansible 控制面。它的 README 列出的规模是：137 个顶层 playbook，184 个 role，分在 `vhosts`、`docker`、`charts`、`host` 和顶层五个命名空间下。

[[fig41]]

### 4.3 三种交付形态

同一个组件可能在三个命名空间下各有一份 role，这不是重复，而是交付形态不同：`roles/vhosts/` 直接装在宿主机上、由 systemd 托管；`roles/docker/` 渲染 docker-compose 文件、拉起单机服务栈；`roles/charts/` 以 Helm release 形式投放到 Kubernetes 集群。按目标环境选择形态，单机和集群共用同一套交付思路。

[[fig43]]

### 4.4 CMDB 与动态 inventory

不写死 IP 的关键是动态 inventory。资源层 apply 之后生成 CMDB，`playbooks` 仓库通过 `inventory/terraform_cmdb.py` 读取它，按地域加角色分组，playbook 按分组执行。新增一台机器，只是 CMDB 里多一条记录。

[[fig42]]

### 4.5 幂等、check 与 diff

幂等让交付可以放心重跑。执行前先干跑：`ansible-playbook -i inventory.ini <playbook>.yml --check --diff`，看清楚会改什么，再真正执行。`playbooks` 的快速开始就是这四步：确认依赖（ansible-core ≥ 2.14）、确认清单、`ping` 连通性、`--check --diff` 干跑。

### 4.6 秘密不落盘

交付端最容易泄露秘密。`playbooks` 的约定是不落静态密钥文件：S3 和数据库凭据在运行时经 Vault JWT 短期认证取得，只驻留内存；仓库启用 gitleaks 扫描。第 5 章会讲这一层更严格的做法：取不到凭据就停，绝不写空值。

另外，README 如实列出了仍是占位的 role（执行只打印 debug、不产生变更），并提醒连字符命名的是占位、下划线命名的是实现。把「还没做完」写在明处，是交付仓库最朴素的诚实。

:::practice
**playbooks**：Ansible 控制面，137 个顶层 playbook、184 个 role；`vhosts` / `docker` / `charts` 三种交付形态；动态清单 `inventory/terraform_cmdb.py`；凭据运行时经 Vault JWT 获取、仅驻留内存，启用 gitleaks。
**iac_modules**：产出 `cmdb.json` + `inventory.ini`，是 IaC 与 Ansible 之间的合同。
**artifacts**：不可变构建产物与镜像分发（据组织主页）。
:::

## 5 安全与身份：没有共享账号，没有固定密码

安全不是流水线上的减速带，而是墙里的钢筋。这一章讲平台的第四层：怎样让人和机器都不再持有长期密码，怎样把「谁能读什么」写成可以评审、可以测试的代码。

### 5.1 问题：密码一旦固定，就会被复制

一个固定的部署密码，最开始只存在一个地方。半年后，它会出现在 CI 变量里、某台跳板机的环境文件里、某个同事的笔记里。没人知道它被复制了多少份，也就没人敢换它。

共享账号的问题更隐蔽：出事之后，审计日志只能告诉你「deploy 账号做了这件事」，却说不出是哪条流水线、哪个提交、哪个人。

所以这一层的目标只有两句：**没有共享账号，没有固定密码**。机器用短期凭据，人用统一身份，所有授权都能追溯到一次评审过的变更。

### 5.2 三件套：Vault、OIDC/JWT、Zitadel

自建的安全层由三块组成，各管一件事。

**Vault 管秘密。** 它是唯一存放凭据的地方，按路径和策略授权，发出的令牌有有效期，到期即失效。

**OIDC/JWT 管机器身份。** CI 运行时向自己的平台要一张签名的身份令牌（JWT），上面写着仓库、工作流、分支或 tag。Vault 验证签名、核对这些声明，再换出一张短期令牌。CI 自己不保存任何密码。

**Zitadel 管人的身份。** 它是可以自建的身份提供方，人通过统一登录进入各个系统，不再每个系统一套账号。

[[fig1]]

### 5.3 CI 不持有密码：Gitea Actions 与 GitHub Actions 并列

这套流程对两种 CI 是对等的：Vault 那一侧只认 JWT 里的声明，不关心它来自哪家。GitHub Actions 早已原生签发 OIDC 令牌（`permissions: id-token: write`）。Gitea 的开发版文档已经写入同一能力：令牌沿用 GitHub Actions 的格式，声明里同样有 `repository`、`ref`、`job_workflow_ref`，但没有 `environment` 声明，令牌 5 分钟过期；而 Gitea 1.26 稳定版文档仍写着不支持 `id-token`。所以迁到自建 Gitea 时，要改的主要是 Vault 角色里的签发方和声明条件，不是每条流水线；在稳定版落地之前，自建一侧要先确认所用版本是否已包含这项能力。

在 ai-workspace-infra 里，目前跑在 GitHub Actions 上的流水线是这样拿凭据的：先拿 OIDC 令牌，再用一个 Vault JWT 角色登录。以 Portal 生产镜像构建的角色为例，它的声明合同只放行三类来源：`v*` tag、`release/v*` 分支，以及 Portal 专用的 `prod-v2-*` 发布 tag；工作流路径也被限定在流水线文件上。换出的令牌是 batch 类型，有效期 1 小时，不带默认策略，只能读共享的镜像仓库凭据。

[[fig2]]

### 5.4 角色即代码：58 个角色、39 条策略

授权规则不应该存在某个管理员的脑子里。Platform-Orchestrator 把 Vault 授权当成代码管理：`scripts/vault/policies/` 下每个 `.hcl` 文件是一条策略，`scripts/vault/roles/` 下每个 `.json` 文件是一个 JWT 角色，写明描述、信任的 OIDC 声明、令牌参数和策略名。截至本版读取时，仓库里有 58 份角色声明、39 条策略。

上层脚本只做两件事：校验和应用。它支持 `--check` 和 `--apply`，可以只针对一个角色，不碰其他声明。脚本本身不写任何针对某个角色的授权规则，规则全部在声明文件里。仓库的说明里也写明：角色和策略的改动按安全敏感变更评审，这个目录里不允许出现访问令牌、私钥或任何秘密值。

角色按环境拆开。同一个服务通常有 sit、uat、prod 三份角色，各自只能读自己环境的路径。这就是第 6 章「环境治理」在安全层的投影。

[[fig3]]

### 5.5 例外也要写进合同

最小权限最怕「临时放宽一下」。2026 年 10 月合并的 Platform-Orchestrator #1420 是一个好例子：Portal 新增了 `prod-v2-*` 发布 tag，生产镜像流水线需要用它触发。

这次改动没有新建一个更宽的角色，而是在原有只读角色上，只为这一个工作流放行这一类 tag；它不授予任何主机或部署凭据。同一个 PR 里还加了一个角色合同测试，并在说明文档里把这个窄口子写清楚。例外有出处、有测试、有文档，下一个人才敢改它。

### 5.6 引导和日常分开：bootstrap 与 runtime 角色

云账号的第一次接入（bootstrap）需要较高权限，日常运行（runtime）不需要。仓库把两者拆成不同的 Vault 角色。

以 GCP 为例：每接入一个账号，就为 UAT 和 PROD 各加一组策略和角色。bootstrap 完成后，日常的 IaC 工作流改用专门的只读 OIDC 角色，它们只能读本环境的身份联合配置和部署账号记录，永远读不到 bootstrap 用的访问令牌，也不能改 AWS 的角色或策略。

AWS 一侧有一条「AWS OIDC Bootstrap Recovery」工作流，分 plan 和 apply 两步：plan 只读出打算如何调整 OIDC 信任关系，apply 才会修改并验证运行时身份。它绑定在主分支和对应的 GitHub Environment 上；如果检测到凭据是账号的根身份，必须额外显式确认才允许 apply。仓库的说明强调：脚本只负责 Vault 角色和策略，AWS IAM 的信任调整是另一个需要单独批准的动作。

### 5.7 交付端 fail closed：凭据宁可报错，不可置空

安全层不止在 CI 里，也在交付引擎里。playbooks 仓库 10 月的两次改动（#714、#720）处理的是同一类风险：部署时如果模板渲染出一个空凭据，服务会带着空密码静默跑起来。

做法是 fail closed：先从 Vault 里解析出规范凭据，再改配置；解析不到就停止，不写空值。秘密模板保留受保护的备份、在 diff 输出里隐藏内容；修复入口支持 `--diff --check`，只预测、不应用。PR 里记录的验证是七个节点的检查模式运行：六台预测无变化，一台预测需要绑定凭据并重启对应进程，没有应用任何配置。

[[fig4]]

### 5.8 自建选项与对照

这一层全部可以自建：Vault 负责秘密和短期令牌，Zitadel 负责人的身份，Platform-Orchestrator 里分别有「Vault server」和「ZITADEL server」两条工作流来部署和验证它们，部署声明都从 GitOps 仓库按评审过的 ref 读取。

对照项是云厂商自带的 KMS 和 IAM。它们省事，但把你的身份体系绑在一家云上；第 7 章讲云中立时会再回到这一点。

如果你在意许可证，Vault 的社区分支 OpenBao 可以作为替代来评估（这是作者补充的选项，不是 ai-workspace-infra 当前在用的组件）。


### 5.9 权限逐项给、逐项查

「流水线能登录 Vault」不等于「什么都能做」。下面五件事分开授予、分开验证：

- 登录 Vault（OIDC 的 JWT 匹配到 role，role 限定仓库、工作流、ref、环境）；
- 读取某一条密钥（policy 落到精确路径和读写能力）；
- 取得云身份（各云的 OIDC 联邦身份，与 Vault 分开）；
- 初始化 state backend（另一套凭据）；
- 访问主机（SSH 信任单独建立）。

新增工作流不会自动获得任何权限。遇到 403，先核对 role 的声明条件和路径，不要先放宽通配符。迁移一条密钥时按顺序来：登记 owner、用途和全部读写方 → 核对 role 与 policy → 补齐检查、轮换和回退 → 最后切换调用方。

:::practice
**Platform-Orchestrator**：`scripts/vault/` 角色与策略即代码（58 个角色、39 条策略），`create_vault_service_repo_roles.sh --check / --apply`；工作流 Vault server、ZITADEL server、AWS OIDC Bootstrap Recovery；PR #1420 为 Portal prod-v2 tag 开窄口子并加角色合同测试。
**playbooks**：PR #714 保护并恢复 Exporter 凭据，PR #720 让凭据部署 fail closed、可 `--diff --check`。
**gitops**：Vault 与 Zitadel 的部署声明按评审过的 ref 被引用（第 2 章详述）。
:::

### 5.10 主机与集群的三角色：root / operator / auditor

前面九节管的是流水线和服务的身份。人登上主机、连上集群时，也要同样分清。下面这套设计目前是**通用规划草案，尚未实施**，写在这里是因为它把前面的原则落到了人身上。

每台主机只用三个固定的 Linux 用户，名字不随环境或批次变化：

- **root**：初始化、安装、恢复和必要的管理；
- **operator**：日常运行，受控 sudo、Docker，以及授权范围内的 Kubernetes 操作；
- **auditor**：只读审计，安全审计、在线分析、迁移源的只读导出和比对。

三者都规划用各自的 SSH 公钥登录；在 K3s/K8s 上，再各自绑定一个独立的认证主体和 kubeconfig。暂时共用一把公钥时要记下来：持钥人能登录全部三个账户，不能算人员已经隔离。

[[figR1]]

**Linux 用户名不是集群身份。** 集群认的是证书或 OIDC 映射出的主体，不是用户名、context 名，更不是 `sudo kubectl`。分工也随之拆开：`vhosts/common` 只管 OS 账户、SSH、受控 sudo；集群认证、kubeconfig 和 RBAC 交给 K3s/K8s 对应的 role。

**root 是例外。** K3s 默认的管理 kubeconfig 是高权限恢复入口，OS root 能读到集群 CA 和管理员文件，所以不能声称 OS root 被强制隔离。做法是给日常管理一个范围受限的独立主体，原来的入口留作受控恢复；新身份和调用方验证完之前，旧凭据一律不删不改。

**声明归 GitOps，交付归 Playbooks**

GitOps 声明「给谁什么」：身份映射、Role 与绑定、准入约束、凭据引用。它只存路径，不存私钥和 token。Playbooks 读取固定版本的声明，交付各用户专属的 kubeconfig（目录 0700、文件 0600），**绝不把管理员的 k3s.yaml 拷给别人**，最后用真实身份连上 API 做允许和拒绝验收。纯 RBAC 范围的变更交给 Flux 调谐，不必重做 OS 初始化。

[[figR2]]

集群客户端凭据规划放在 Vault KV 的 `kv/<environment>/<cluster>/{root,operator,auditor}`，每类身份一条，和已有的 OS SSH 公钥路径分开。记录绑定真实集群 UID，对不上就拒绝消费。路径、策略和写入工具都还是规划。

三类授权各有自己的 GitOps 更新路径：基础管理（Flux、Ingress、身份与准入）由 root 审查发布；业务范围由 operator 提交、管理员审查；审计读取范围由 auditor 提需求、管理员和数据 owner 审查。**谁都不能自己给自己扩权。**

**能看，不等于安全的审计**

[[figR3]]

operator 初期只能读授权 namespace 的状态，以及缩放点过名的无状态 Deployment；发布走 GitOps PR。Secret、exec、节点 proxy、RBAC 的 bind / escalate / impersonate 一律不给。能创建 workload，就能间接挂 Secret、借别的 ServiceAccount，所以模板修改要等准入策略验证过才放。

auditor 只读，但「只读」也会泄密：`get/list` 会返回完整对象，Pod spec、ConfigMap、事件里可能带敏感值。内置的 `view` 不能直接当安全审计，需要逐类评审或走脱敏报告。RBAC 没有拒绝规则，权限是所有绑定的并集，所以要查全部绑定，不能只看新角色。

做业务迁移时，auditor 负责盘点、只读导出和前后比对；目标写入由 operator 做，DDL、初始化、恢复由 root 做。每一步显式选身份，auditor 权限不够时停下，**不自动提权**。

**渐进交付**

先做阶段 A：Flux 仍是线上资源的 owner，只开放状态读取和点名缩放。确需直接改 workload 时才进阶段 B，前提是准入策略先在隔离环境验证通过。执行顺序是：只读盘点 → 声明与审查 → 隔离验证 → 在目标集群创建新身份（不撤旧的）→ 逐身份验证矩阵 → 迁移调用方 → 最后停用确认没有调用方的旧身份。生产上证明「拒绝」时，不真的去执行 DELETE 或 DDL。

尚未落地的部分，照实列出：

- 独立认证机制（OIDC 或短期客户端证书）与颁发、轮换 owner；
- Vault 记录、精确策略和跨角色拒绝验收；
- root 管理基础组件的准确权限，GEO 具体指什么组件还待确认；
- operator 的 namespace、对象名和发布入口清单；
- 直接改 workload 所需的准入策略；
- auditor 的读取清单与脱敏方式；
- 旧审计身份的全部调用方盘点，盘点完之前不删。

:::practice
**playbooks**：`vhosts/common` 管三个 OS 账户、SSH 与受控 sudo；K3s/K8s role 负责集群认证、kubeconfig 交付和允许 / 拒绝验收（规划中）。
**gitops**：身份映射、RBAC 与准入的声明源，只引用凭据路径；按 revision 由 Flux 收敛。
**Vault**：`kv/<environment>/<cluster>/<role>` 规划存放三类集群客户端凭据，消费方只读自己那一条。
:::

### 5.11 秘密的默认走法：Vault KV → ExternalSecret → chart Secret

5.7 说交付端解析不到凭据就停；5.10 说集群客户端凭据放在 Vault KV。业务服务在集群里拿秘密，也走同一条路，而且只有一条默认路：

1. **Vault KV 存值。** 秘密只在 Vault 里，路径按 `kv/<environment>/<cluster>/<role>` 这类约定组织。
2. **GitOps 只写引用。** 仓库里声明 SecretStore 和 ExternalSecret：去哪个 Vault、读哪条路径、同步成哪个 Kubernetes Secret。仓库里没有任何值。
3. **Flux 收敛，ESO 同步。** Flux 把这些声明按 revision 落到集群；External Secrets Operator（ESO）是唯一持有 Vault 读权限的组件，它把值同步成 Kubernetes Secret，并按周期刷新。
4. **chart 只认 Secret 名。** 业务 chart 的 values 里默认只引用 Secret 名和键，**不持有 Vault token，也不认识 Vault 地址**。换环境只换 ExternalSecret 里的路径，chart 不动。

[[figE1]]

**三角色顺着这条路往下走。** 数据库初始化（Init DB）这一步，规划从三条 Vault KV 路径读凭据，由 Playbooks / ESO 的 Secret 映射明确串起来：admin → chart 的 root，operator → operator，auditor → auditor。chart 只消费同步出来的 Secret，在初始化时配好对应的数据库角色：root 做 DDL 和初始化，operator 做业务读写，auditor 只读。这是和 5.10 同一套三角色，在数据层的延续；目前是**规划做法，还不是所有服务的通用默认**，接入一个服务就核对一个。

几条约定：

- **映射写明，不靠同名猜。** 哪个 Vault 键进哪个 Secret 键、给 chart 哪个角色用，都写在 ExternalSecret 里，评审时一眼能看全。
- **缺值就失败。** ESO 同步不到，Secret 不出现，Pod 起不来，这正是 5.7 的 fail closed；不给 chart 留默认密码兜底。
- **读权限按路径收窄。** ESO 用的 Vault 角色只放行本环境、本集群的路径；跨环境读同一条路径，会被 Vault 拒绝。
- **轮换在 Vault 做。** 改值只改 Vault，ESO 下一次刷新带下去；需要重启的服务由声明里的滚动策略处理，不手工改 Secret。

:::practice
**gitops**：SecretStore / ExternalSecret 声明路径与映射，按 revision 由 Flux 收敛。
**charts**：values 只引用 Secret 名和键，不出现 Vault token 或地址。
**Platform-Orchestrator / playbooks**：Init DB 阶段按 admin → root、operator → operator、auditor → auditor 校验映射存在后再初始化（规划中）。
:::

### 5.12 一套身份，两种接入：容器内应用与非容器 SaaS

5.2 把身份分成两半：机器走 OIDC/JWT，人走 Zitadel。放到接入方式上看，其实是同一个故事：**谁要访问什么，都先找身份提供方换一张短期令牌，再凭令牌进门。**没有长期共享密码。

**机器那一半，5.3 已经讲过。** CI 拿平台签发的 OIDC 令牌，到 Vault 的 JWT 角色换短期令牌；集群里的服务再经 5.11 的 ESO 拿到秘密。整条链上没有人手里的密码。

**人那一半，分两种接入，用同一个身份提供方：**

- **容器内应用。** 跑在集群里的门户、内部工具和业务后台，作为 OIDC 客户端接 Zitadel：登录跳转、拿 ID token，后端校验 JWT 的签发方、受众和有效期，按声明里的组映射角色。客户端密钥本身也是秘密，同样走 5.11 的 Vault KV → ExternalSecret。
- **非容器 SaaS。** 托管控制台、第三方协作工具、外部门户这类不跑在你集群里的系统，用它们支持的 OIDC 或 SSO 接同一个 Zitadel。账号不在每个 SaaS 里单独建，离职或换岗时在身份提供方停一处，各处一起失效。

[[figE2]]

两种接入守的是同一组规则：

- **令牌短期。** 会话和访问令牌都有有效期，过期重新换；不签发永不过期的令牌。
- **角色来自声明。** 应用按令牌里的组或角色授权，组成员关系在身份提供方里维护，和 5.10 的 root / operator / auditor 一样，谁都不能自己给自己扩权。
- **共享账号只当例外。** 某个 SaaS 不支持 OIDC，只能用共享账号时，按 5.5 写进例外合同：密码放 Vault，有 owner，有到期日，有替换计划。

从单机上的三个 Linux 账户，到集群 RBAC，到 ESO 下发的 Secret，再到 OIDC 令牌：工具一路在换，**最小权限、身份独立、凭据短期**这条线没变。

:::practice
**Zitadel**：容器内应用和非容器 SaaS 统一作为 OIDC 客户端登记，组映射角色。
**Vault**：机器身份走 JWT 角色换短期令牌；OIDC 客户端密钥走 KV + ExternalSecret。
**例外合同**：不支持 OIDC 的 SaaS 单列，写明 owner、到期日与替换计划。
:::

## 6 环境治理：SIT → UAT → PROD

这一章讲平台的第五层，也是一条探索了很多年的实践线：**多环境 → 不可变环境 → 滚动升级**。GitOps、环境副本、Kubernetes、Argo CD、Flux CD，其实都在实践同一个想法：环境不靠人去改，而是从 Git 里声明出来，用同一份构件一路晋级，升级时一点点替换、随时能退回。

[[fig61]]

### 6.1 多环境：SIT / UAT / PROD 的由来与问题

多环境的由来很朴素：不敢直接在生产上试。于是有了集成测试环境 SIT、用户验收环境 UAT 和生产环境 PROD，变更按顺序一级一级往上走。

问题也随之而来。三个环境往往是三批人、在三个时间点、用三种方式搭起来的。UAT 测过的东西，到了 PROD 还是会坏，原因常常不在代码，而在环境本身就不一样。环境越多，「它们其实不一样」的地方就越多。

除了三个业务环境，平台自己还有一层 **Shared**（Vault、可观测、身份）。它有独立的生命周期：业务发布只检查它是否就绪，不重建它。PROD 有独立的身份、state 和审批，消费已验收的构件，不复用 UAT 的运行回执。

### 6.2 配置漂移：环境为什么会悄悄变样

配置漂移指的是：环境的真实状态，一点点偏离了它应该有的样子。一次紧急登录改了个参数，一次手工补了个包，一次只在某台机器上调了内核参数。每一次都有理由，但没人把它写回去。

漂移的可怕之处在于它是沉默的。直到某天要重建环境、扩一台新机器，或者做灾备切换，才发现没人说得清「正确的样子」是什么。治理漂移只有一条路：**让 Git 里的声明成为唯一的真相，再让系统持续把真实状态拉回声明**。

[[fig62]]

### 6.3 不可变构件与不可变环境

第一步是不可变构件：**只构建一次，晋级同一个产物**。SIT、UAT、PROD 用的必须是同一个镜像、同一个包，按版本或摘要引用，而不是每个环境各自重新构建一遍。

第二步是不可变环境：不在运行中的环境上原地修改，而是用新版本的声明替换旧版本。要改，就改声明、出新版本、再收敛过去。

ai-workspace-infra 组织主页把这条写成了交付准则：**CI 阶段只读验证，CD 阶段消费唯一快照，严禁原地篡改**。Daily Main Snapshot 完成跨仓库协同打 tag 与构建，生成唯一的不可变快照，tag 形如 `uat-daily-build-YYYY.MM.DD[-rN]`。只有完整的 UAT 快照构建成功，才解析出确定的版本标识，再交给后面的编排去部署。

### 6.4 制品仓库：Harbor 与开源替代

「只构建一次，晋级同一个产物」，前提是产物有一个可信的家。这个家就是制品仓库：CI 把镜像推进来，签名、扫描在这里完成，GitOps 控制器从这里按摘要拉取。仓库自建，制品就不被任何一家云的镜像服务绑定。

**介绍说明。** Harbor 是 CNCF 毕业项目，一个自建的 OCI 制品仓库：容器镜像、Helm chart 和其他 OCI 制品放在同一个地方。它以项目（project）为单位做 RBAC，给 CI 发机器人账号（robot account）；内置 Trivy 漏洞扫描，可以推送即扫描、按漏洞等级阻止拉取；支持 Cosign 与 Notation 签名，可以要求只允许拉取已签名的制品；复制（replication）规则可以在 Harbor 之间、或向其他兼容 OCI 的仓库推送和拉取；标签保留（tag retention）与垃圾回收控制存储增长；代理缓存（proxy cache）项目缓存上游公共仓库，减少对外部的依赖。

[[fig66]]

**它在云中立流水线里的位置。** Gitea Actions 或 GitHub Actions 构建一次，用机器人账号推送到 Harbor 并签名；Harbor 推送即扫描，不合格就挡在晋级之前；`gitops` 声明里按摘要引用镜像，Doco CD、Argo CD 或 Flux CD 从 Harbor 拉取收敛。要上另一朵云或另一个机房，只需加一条复制规则，把同一份制品同步过去，声明不变。

**规划。** 动手前先定六件事：

:::table
维度|起步（单机）|团队 / 生产
规模|官方最低 2 CPU / 4 GB 内存 / 40 GB 磁盘|官方推荐 4 CPU / 8 GB / 160 GB，按镜像总量和保留策略估算
存储后端|本地磁盘（数据目录）|S3 兼容对象存储（自建或任意云），也支持 Azure、GCS、Swift、OSS
高可用|单节点 + 定期备份|Kubernetes 上 Helm 部署多副本，存储、数据库、缓存全部外置
TLS / 域名|一个域名，前置 Caddy 自动 HTTPS|Ingress + 证书 Secret 或 cert-manager
数据库 / 缓存|内置 PostgreSQL 与 Redis|外部 PostgreSQL 与 Redis（或 Sentinel），可复用 postgresql.example.com
网络与复制|单站点，代理缓存上游公共仓库|主仓库 + 各环境/各云只读副本，复制规则按项目过滤
:::

备份要覆盖三样东西：数据库（项目、权限、策略）、制品存储（对象存储自带版本或跨区复制）、配置文件 `harbor.yml` 或 Helm values。和第 9 章一样，备份要做恢复演练才算数。

**部署脚本。** 单机形态用官方离线安装包：下载 `harbor-offline-installer` 并校验 md5sum，渲染 `harbor.yml`（hostname、external_url、数据目录、可选 storage_service 与外部数据库），再执行 `./install.sh --with-trivy`。新版本已移除 ChartMuseum 与 Notary，安装时不要再加这两个参数。集群形态用官方 Helm chart `goharbor/harbor`，在 values 里设置 expose、externalURL、persistence.imageChartStorage 与 database/redis 的 type。`playbooks/scripts/setup-harbor.sh` 把两种形态包成一条命令（脚本已提交 PR，评审中）：

:::code
# 单机演示（官方离线安装包 + install.sh --with-trivy + Caddy HTTPS）
curl -fsSL https://raw.githubusercontent.com/ai-workspace-infra/playbooks/main/scripts/setup-harbor.sh | \
  bash -s -- --domain harbor.example.com --standalone
# 团队：S3 兼容存储，凭据运行时由 Vault 注入
export HARBOR_DOMAIN="harbor.example.com"
export HARBOR_ADMIN_PASSWORD="<runtime-secret>"
export HARBOR_S3_ENDPOINT="https://s3.example.com"
export HARBOR_S3_BUCKET="harbor"
export HARBOR_S3_ACCESS_KEY="<runtime-secret>"
export HARBOR_S3_SECRET_KEY="<runtime-secret>"
curl -fsSL https://raw.githubusercontent.com/ai-workspace-infra/playbooks/main/scripts/setup-harbor.sh | \
  bash -s -- --domain "$HARBOR_DOMAIN" --standalone --with-s3
unset HARBOR_ADMIN_PASSWORD HARBOR_S3_ACCESS_KEY HARBOR_S3_SECRET_KEY
# Kubernetes（K3s/K8s）：helm upgrade --install harbor/harbor，钉住 chart 版本
curl -fsSL https://raw.githubusercontent.com/ai-workspace-infra/playbooks/main/scripts/setup-harbor.sh | \
  bash -s -- --domain harbor.example.com --k8s --with-s3
:::

脚本单机模式渲染的 `harbor.yml` 核心部分如下（Caddy 在前面终止 TLS，Harbor 只监听本机 HTTP 端口）：

:::code
hostname: harbor.example.com
http:
  port: 8080
external_url: https://harbor.example.com
harbor_admin_password: <runtime-secret>
data_volume: /data/harbor
storage_service:            # 仅 --with-s3
  s3:
    bucket: harbor
    regionendpoint: https://s3.example.com
    accesskey: <runtime-secret>
    secretkey: <runtime-secret>
  redirect:
    disable: true
:::

集群模式的 values 核心部分；密码、对象存储密钥都放进已有 Secret，不写进 values：

:::code
expose:
  type: ingress
  tls: { enabled: true, certSource: secret, secret: { secretName: harbor-tls } }
  ingress: { hosts: { core: harbor.example.com } }
externalURL: https://harbor.example.com
existingSecretAdminPassword: harbor-admin
persistence:
  imageChartStorage:
    type: s3
    disableredirect: true
    s3: { existingSecret: harbor-s3, bucket: harbor, regionendpoint: https://s3.example.com }
database: { type: external }   # 生产：外部 PostgreSQL
redis: { type: external }      # 生产：外部 Redis
:::

装好之后的第一批操作：建项目、给 CI 发机器人账号（只授推送与拉取）、打开推送即扫描、配置标签保留和垃圾回收、按需开启「只允许已签名制品」。

**开源替代。** Sonatype Nexus Repository 是多格式仓库，除容器镜像外还管理 Maven、npm、PyPI 等语言包，适合构件以语言包为主的团队；Zot 是纯基于 OCI Distribution 规范的轻量仓库，单个二进制即可运行，适合边缘节点或只需要 OCI 镜像的小场景。第 2 章的 Gitea 也自带软件包仓库，起步阶段可以先用它，制品规模上来、需要扫描、签名和跨云复制时再迁到 Harbor。

### 6.5 GitOps：声明式收敛

GitOps 把环境变成了 Git 里的一组声明。变更通过 PR 评审合入，一个控制器持续对比「声明」和「现实」，发现不一样就把现实拉回声明。人不再直接登录环境改东西，改的是 Git。

在 ai-workspace-infra 里，`gitops` 仓库就是这一层的权威声明层：它只放声明，不放命令式脚本，也不放任何秘密，凭据运行时由 Vault 下发。环境按 `sit` / `uat` / `prod` 分开，主页称之为 SIT / UAT / PROD 多环境隔离与 Compose 状态机。消费方通过 URL 和 ref 引用它，而且要**钉住 ref**：跟着移动分支走的部署，会在运行那一刻继承所有改动。

[[fig63]]

### 6.6 环境副本与预览环境

当环境完全由声明生成，复制一个环境就变得便宜：同一份声明，换一组参数，就能拉起一个环境副本。最常见的用法是预览环境，每个 PR 起一个临时环境，评审完就销毁。

环境副本的前提，是声明里不写死随环境变化的值。`gitops` 仓库的约定正是这样：域名、主机名、规格由消费它的流水线传入，声明里也不放兜底默认值，因为「只在部分文件里错」的兜底比没有更糟。

:::practice
**功能泳道（6.6 的实践）**：不是为了微服务而微服务，也不是为了网格而网格，只为了让一个跨仓库的功能在合并 main 之前，就能在一条隔离的链路里跑完 SIT 和 UAT。
**设计**：以功能 ID（如 `billing-refund`）作为泳道身份，用一份候选清单关联 Console、Accounts、Billing 各自的 PR 与固定 commit SHA，并写明已验收基线与 `dataProfile: isolated-test`。改动组件用 PR 构建的镜像，未改动组件沿用已验收镜像；最终清单固定 commit、镜像 digest 和配置版本，每次变化记为新的 revision。一个功能一个 Namespace（如 `feature-billing-refund`），不必每个 PR 各起一套环境。
**理念**：测试部署由「功能候选清单」驱动，而不是等待业务代码合并 main。功能 ID 是身份，PR 只是输入；SIT 与 UAT 共用同一套物理资源，区别只在验收阶段和候选状态。SIT 允许随 PR 更新重建候选；UAT 固定版本，不自动跟随分支；新提交产生新 revision，旧的 UAT 结果不能放行新候选。验收前再核对组合候选与最新 main，通过后才合并 PR。
**解决的背景问题**：一个功能常常同时改前端、账户和账单，「先合并 main 才能进 UAT」会把未验收代码提前带进主干，也让多仓库改动无法作为一个整体验收。现有「合并后才进入 UAT」的工作流和 Vault 绑定，需要作为一项明确的流程变更调整；泳道名称与 SIT/UAT 权限边界仍分别管理。
:::

[[figL1]]

### 6.7 滚动升级：Kubernetes Deployment

到了集群层，Kubernetes 的 Deployment 把滚动升级做成了内建能力。默认策略是 RollingUpdate：一边起新版本的 Pod，一边停旧版本，`maxSurge` 控制最多多出几个、`maxUnavailable` 控制最多少掉几个，默认都是 25%。

决定「新 Pod 能不能接流量」的是就绪探针（readiness probe）：探针不通过，Pod 就不会进入 Service 的后端列表，滚动也就不会继续往下推。升级出了问题，用 `kubectl rollout undo` 回到上一个版本；Deployment 默认保留 10 个历史版本（`revisionHistoryLimit`）。

[[fig64]]

### 6.8 Argo CD 与渐进式发布

Argo CD 是 Kubernetes 上的 GitOps 控制器。它把 Git 里的目标状态和集群里的实际状态做对比，不一致时标记为 OutOfSync，可以手动或自动同步。开启自动同步后，还可以打开 `selfHeal`（集群被人手工改了就自动改回去）和 `prune`（Git 里删了的资源在集群里也删掉）。

管理很多应用时，常用 app-of-apps 模式：一个父 Application 只负责声明其他 Application，新增一个服务就是在 Git 里加一个文件。

再往前一步是渐进式发布。Argo Rollouts 在 Deployment 之外提供蓝绿（blueGreen）和金丝雀（canary）两种策略，按比例分批切流量，可以结合指标分析决定继续还是回滚。这一步不是必需的，先把滚动升级和回滚做稳，再考虑它。

:::practice
**泳道内的轻量渐进发布（6.8 的实践）**：第一版只用滚动更新和受控蓝绿，全链路染色与自动金丝雀放到后续。
**设计**：SIT 中频繁更新功能版本，直接更新泳道 Deployment，用原生 RollingUpdate；UAT 验证候选并需要快速切回上一候选时，保留 stable / candidate 两组应用，由入口切换，即蓝绿；需要指定测试人员先访问新版时，用专属候选域名（如 `candidate.billing-refund.preview.example.com`），或由入口按授权 Header/Cookie 选择。按 10%→50%→100% 自动放量，留待以后接入支持加权路由的入口和 Rollouts 控制器。
**理念**：原生滚动更新能控制 Pod 替换数量，但不能保证精确的请求比例（参见 Kubernetes Deployment 官方文档）。测试环境流量少，百分比放量没有足够样本，不能证明业务稳定，所以优先用指定测试人员和自动化用例推进验收。若以后选择 Traefik，它有加权后端能力（参见 Traefik 加权服务官方说明），但需要核对已安装版本和配置；不建议只为这个功能更换现有入口。
**解决的背景问题**：渐进发布容易被理解成「先上网格和金丝雀」。在当前规模下，这会引入比问题本身更重的组件。蓝绿共用测试库时 schema 必须兼容；要测试破坏性数据库变化，应为候选创建独立数据库，并明确切回时的数据怎么处理。
:::

### 6.9 Doco CD / Argo CD / Flux CD：从单机到集群的实践

自建平台不一定一开始就上集群。一个现实的演进路径是三个阶段，而且**三个阶段用同一套 Git 仓库布局**：环境按 `sit` / `uat` / `prod` 分目录，服务声明共享，变的只是由谁来收敛。

**阶段一：单机 Docker Compose + Doco CD。** Doco CD 是面向 Docker Compose 的轻量 GitOps 工具，通过轮询或 webhook 发现 Git 变更，自动部署和更新 Compose 项目，也支持 Swarm 栈；它支持多种 Git 提供方，可以接 SOPS 加密和外部秘密提供方。一台 VPS 加一个 Compose 文件，就有了 pull 式的 GitOps。

**阶段二：K3s/K8s + Argo CD。** 上了集群，Argo CD 提供 Web UI、Application 与 app-of-apps、自动同步与 self-heal，适合需要可视化和多团队协作的场景；一个 Argo CD 实例可以管理多个集群。

**阶段三（或并列）：K3s/K8s + Flux CD。** Flux 是一组 Kubernetes 控制器：source-controller 拉取 Git/OCI/Helm 源，kustomize-controller 应用 `Kustomization`，helm-controller 管理 `HelmRelease`，image-reflector 与 image-automation 控制器可以发现新镜像并把新 tag 写回 Git。Flux 本身不带 Web UI，以 CLI 和 CRD 为主。`gitops` 仓库的范围说明里就写着 Kubernetes 资源与 Flux Kustomizations。

:::table
工具|目标|模型|UI|多集群|最适合
Doco CD|Docker Compose / Swarm 单机或少量主机|轮询 / webhook 拉取 Git|无专用 UI（REST API、Prometheus 指标）|通过 Docker Contexts 部署到多台主机|一台 VPS 起步、Compose 为主的小团队
Argo CD|Kubernetes|控制器对比目标与实际状态，自动或手动同步|有 Web UI|一个实例管理多个集群|需要可视化、多团队、app-of-apps
Flux CD|Kubernetes|一组控制器 + CRD（Kustomization、HelmRelease）|无内建 UI|常见做法是每个集群各装一套，也可远程管理|偏好 CLI/声明式、需要镜像自动更新
:::

[[fig65]]

:::practice
**最轻量的全链路泳道与 main 合并前的 Flux 部署（6.9 的实践）**：K3s + Helm + Flux + 功能级 Namespace + 独立测试数据库，先通过固定服务地址形成完整泳道。
**设计**：第一版直接部署这条功能需要的调用链：`billing-refund.preview.example.com` → Next.js-feature → Accounts-feature → Billing-feature → PG `billing_refund` 测试库。运行环境是一个非生产 K3s，容纳多个功能 Namespace；模板复用现有 Helm Chart；服务发现用 Kubernetes Service DNS，配置明确的依赖地址；数据用共享的非生产 PG 实例，每条泳道独立 database 和角色；入口复用现有入口控制器，按功能域名路由；交付复用 Flux，消费受控生成的功能部署声明；验收用 Go/API 集成测试、Playwright 和既有业务用例。部署链路上，业务代码来源与部署声明来源分开：业务 PR 固定 SHA → CI 构建镜像 digest → 受信任的非生产编排工作流 → 更新功能泳道 GitOps 声明 → Flux / Helm 部署。声明进入专用、受保护的非生产 GitOps 分支，Flux 只读取该范围；HelmRelease 通过 values 配置具体版本和环境参数（参见 Flux HelmRelease 官方文档）。
**理念**：这是端到端隔离泳道，没有引入共享基线的逐跳 Header 染色，对当前服务规模更容易实施和维护。未修改的组件可以复用镜像，但涉及写入的服务应在泳道内运行并连接测试库；不要为了少几个 Pod，让功能链路写入共享生产数据。PR 构建与有凭据的部署阶段分开，凭据只由 Vault 在受信任阶段下发。
**解决的背景问题**：业务 PR 不需要合并就能部署，但如果直接用高权限工作流执行未经信任的 PR 代码，PR 就可能任意提交集群资源或取得管理凭据。把构建、编排和收敛拆开，让每一段只做一件事，问题就收敛到「声明是否可信」这一处。
:::

[[figL2]]

**第一版建议**：一个非生产 K3s → 一个功能一个 Namespace → 多仓库 PR 固定清单 → 独立测试库 → SIT 后固定候选做 UAT → 组合验证通过后合并 main。

### 6.10 自建选项与对照

这一层全部可以自建：Git 用 Gitea（与 GitHub 对等），收敛用 Doco CD、Argo CD 或 Flux CD，集群用 K3s 或 K8s，镜像仓库用 Harbor 自建（见 6.4），起步阶段也可以用 Gitea 自带的软件包仓库。托管的环境服务只作对照：它们省事，但环境的真相不在你的 Git 里。

Gitea Actions 与 GitHub Actions 在这一层的角色相同：CI 只读验证、产出不可变构件和快照 tag；真正改环境的，是从 Git 拉取声明的收敛控制器，而不是 CI 推过去的命令。


### 6.11 一条可跟踪的发布主链

把前面几节串起来，一条日常主链长这样：

[[figW6]]

- 每日快照为所有仓库打同一个不可变 tag，构建并验证构件，再检查共享平台是否就绪，只读，不重建它。
- UAT 混合编排按资源矩阵逐行选择 Provider、账号和子流水线，等待精确的子运行并核对回执；入口层只负责审批和派发。
- 共享平台（Vault、可观测、身份）走自己独立的入口，不跟随业务发布。
- 子运行成功不等于稳定域名已经切换，也不等于数据已同步。这几项分开验收（见 7.7）。

:::practice
**组织主页（.github）**：交付准则「CI 阶段只读验证，CD 阶段消费唯一快照，严禁原地篡改」；Daily Main Snapshot 生成不可变快照 `uat-daily-build-YYYY.MM.DD[-rN]`，成功后才解析 tag，交给 serverless-orchestrator（operation=deploy+migrate，vault_env_path=uat）与 selfhost-orchestrator（operation=deploy，部署后注册到 web-saas）。
**gitops**：权威声明层，只放声明；`environments/clusters/<env>/`、`services/`、`topology/<env>/<mode>/`、`resources/<project>/<env>/<provider>/`；env 为 sit / uat / prod；凭据只走 Vault；消费方按 URL + ref 引用并钉住 ref；缺失声明必须让消费步骤失败。
**artifacts**：不可变构建产物、GHCR 容器镜像分发与 Daily-Build 快照版本发布中枢（据组织主页）。
:::

### 6.12 多环境 × 多分支 × 滚动发布 × 特性泳道：交叉组合，各取所需

前面几节分别讲了多环境、分支触发、滚动升级和功能泳道。它们不是一条固定的线性流水线，而是四个互相正交、可以交叉的维度：**多环境**回答「在哪儿验」，**多分支**回答「从哪份代码来」，**滚动发布**回答「怎么换上去」，**特性泳道**回答「要不要单独隔离」。每次变更按需要选组合，不必每次都把四个维度走满。

[[figX1]]

**按生命周期分层**。环境不只按名字分，更按生命周期分：SIT 是临时的，一个需求一条泳道，命名空间形如 `feature-<id>-sit`，跟着 PR 生、跟着合并回收；UAT 是持久的准生产，只接收 main 的构建产物，跑在 Serverless 上（Cloud Run + Cloudflare + 云托管 PG），与开发主机脱钩；PROD 是受控的，只认签发过的 Release，按稳定镜像 digest 分批滚动更新、健康探针放行。现阶段 PROD 的红线是零触碰、零变更；入口规划是把 Caddy 剥离到独立网关命名空间，统一证书与多云反代。

[[figX2]]

**SIT 泳道四步**：

- 新建纯净的 PostgreSQL-0（新建 3Gi PVC），不复用旧数据；
- 用 migratectl 跑最新的 77 张表 Schema 与 Billing；
- 运行时注入 Secrets，密钥不进仓库、不进镜像；
- 拉起 4 个微服务 Pod，执行端到端自动化测试。

入口是一个独立、常驻的网关层（Caddy 反代 + TLS + 泛域名解析），按泛域名把请求分流到对应泳道；泳道回收了，网关不受影响。

**晋级关口**：SIT 组合验证通过 → 合并 main、归档 Feature 证据、回收泳道 → main 自动部署到 UAT → UAT 验收合规后签发 Release → PROD 受控滚动。

[[figX3]]

**验证原则**：

- 钉住构件：记录完整镜像 digest、源分支与 main 的 commit SHA、候选指纹；不使用 latest 或任何浮动 tag。
- UAT 复用 SIT 冻结的同一组 digest，不重新构建。
- 合并 main 之后再复核一次，确认进主干的就是验过的那一份。
- 每个阶段都记录结论：PASS / FAIL / BLOCKED / NOT_RUN，没跑就写 NOT_RUN，不写成通过。
- 看板跨环境共用，按 environment 标签（sit / uat / prod）区分，不为每个环境复制一套。
- 凭据按环境分开签发，从不借用 PROD 凭据给 SIT 或 UAT。

**交叉矩阵（建议组合，按本书实践整理）**：

:::table
变更类型|分支|经过的环境|是否需要泳道|发布方式
小修复（单仓库、无迁移）|feature 分支 → main|PR 校验后进 UAT，Release 后进 PROD|建议可省，直接用 PR 校验|PROD 按 digest 滚动
并行新功能（跨仓库）|各仓库 feature 分支，候选清单关联|SIT 泳道 → UAT → PROD|需要，一个功能一条泳道|SIT 直接更新 Deployment；PROD 按 digest 滚动
数据库迁移|feature 分支 → main|SIT 纯净库重放迁移 → UAT → PROD|需要，纯净库验证迁移可重放|迁移单独验收，再滚动应用（见 9.7）
基础设施 / 网关变更|基础设施仓库的 PR → main|先在非生产验证，再进 PROD|建议按需，常驻网关不随泳道回收|分批、可回滚；现阶段 PROD 零变更
:::

**如何选组合**：先问「会不会和别人的改动互相干扰」，会就开泳道；再问「有没有改数据结构」，有就必须在纯净库上重放迁移；然后问「影响面多大」，影响 PROD 的一律经 Release 签发、按 digest 分批滚动、探针放行。表中「建议」项是本书的推荐做法，不是已验证的度量结论，按自己的项目取舍。

:::table
功能|特性|成本|客观事实依据|适用场景
SIT 临时泳道|一个 PR / 功能一个命名空间，用完回收|每条泳道都要建库、跑迁移，启动比共用环境慢|77 表 Schema + Billing，4 个微服务端到端|需求并行、迁移频繁
独立网关层|常驻，按泛域名分流到泳道|网关要先写成代码|Caddy 反代 + TLS|多泳道共用一个入口
UAT 持久环境|只接收 main 产物，复用冻结 digest|Serverless 按用量计费|Cloud Run + Cloudflare + 云托管 PG|准生产集成与业务验收
PROD 受控发布|按镜像 digest 分批滚动，探针放行|要配健康探针与回滚预案|现阶段零触碰、零变更|要求业务不中断
:::

## 7 云中立：一套配置，任意部署

选云的时候大家都很开心，想搬走的时候才发现退不出来。云中立不是「不用云」，而是让每一层都**可替换**：同一套配置，可以落在公有云、VPS、裸金属，或者一个 K3s / K8s 集群上。

### 7.1 什么是云中立

云中立有三个判断标准：资源用开放的 IaC 描述，换一家 provider 只是换一组声明；运行面统一，应用不感知底下是谁家的机器；数据用开源组件自建，不锁死在某家的托管服务里。

做到这三点，退出成本就始终可控。云厂商依然可以用，只是它变成了「其中一个运行面」，而不是唯一的地基。

[[fig71]]

### 7.2 VPS 与裸金属

VPS 和裸金属是云中立最朴素的落点：一台有公网 IP 的 Linux 机器，加上域名，就能承载完整的服务。它们价格透明、迁移简单，正适合「一个域名，一台机器，一行脚本」的起步方式。

`iac_modules` 把 VPS 当作一等公民：Vultr 是渲染范式的参考实现，Akamai Cloud / Linode 有 VPS provider 树，与 AWS、GCP 使用同一套「声明、模板、组合逻辑」三层结构。

### 7.3 K3s / K8s：统一运行面

当服务多起来，Kubernetes 提供了跨云一致的运行面：同样的 Deployment、Service、Helm chart，在任何集群上行为一致。K3s 是轻量级、经过认证的 Kubernetes 发行版，一台小 VPS 就能跑起来，适合自建和边缘场景。

`playbooks` 仓库把 K3s 集群、GPU 集群的搭建也写成了 role 和 playbook，集群本身也是可重复交付的。

### 7.4 编排模式：Selfhost、Serverless、Hybrid

不是所有服务都要自建。ai-workspace-infra 把编排拆成几种模式：组织主页描述了 `serverless-orchestrator.yml`（部署应用并执行数据迁移）与 `selfhost-orchestrator.yml`（部署自建业务域，并注册到 serverless 侧交付的服务中）的组合联动；`gitops` 仓库则为 `selfhost`、`serverless`、`hybrid` 三种模式分别声明运行时拓扑，编排器只读取与自己职责匹配的那一份。

[[fig72]]

模式可以按服务取舍，但声明是统一的：换模式就是换一份声明，而不是重写一套系统。

### 7.5 自建数据库：postgresql.example.com

数据是最难搬的。`postgresql.example.com` 提供一个生产就绪的 PostgreSQL 运行时，带向量搜索、中文分词、消息队列等扩展。它支持两种部署模式：单机的 Stunnel + ACME（自动证书，默认 5443 端口作为 TLS 入口，80 端口仅用于证书验证），以及 Kubernetes / Helm（Sidecar 方式提供 TLS 隧道）。

它的构件也遵循不可变原则：镜像和 Helm chart 由 CI 矩阵构建并发布到 GHCR，CI 通过 Vault OIDC 取凭据，并按 Git 事件路由到 `sit` / `uat` / `prod`。

### 7.6 退出成本自评

最后给一个简单的自评：对每一层问一句「如果明天要换，要多久？」专有托管服务通常最难迁；开放标准加托管服务可以替换；开源自建可以随时搬家。

[[fig73]]


### 7.7 多账号、外部主机与边缘入口

**多账号检查单**。代码里有多家云的 provider 目录，只说明结构上可见。每接入一个账号，逐项确认：

- 声明里逐行写明 Provider 和具体账号，不靠默认 profile；
- 每个账号有对应的凭据或联邦身份，写入前核验实际身份和项目；
- 独立的 state 前缀，最小权限 policy；
- 准备一条「账号错配」的负例，确认会失败而不是写错地方。

**已有主机**。不是 Terraform 创建的主机，标记为外部纳管（existing / external）：只生成 inventory 和运行记录，不创建、不接管、不销毁，也不产生 state。名称相近的另一类云主机如果由 Terraform 管理，就不能套用这个生命周期。

**边缘入口**。Hybrid 模式下，可以在边缘放一层轻量网关，按模式把同一个稳定域名转到 Selfhost 或 Serverless 后端：

[[figW7]]

- 品牌主页、控制台、API、数据库是四个独立边界；换一个后端，不连带更换公开主页。
- 控制台静态资源直接由 CDN 提供，不让每个静态请求都经过 API 网关。
- 超时或 5xx 回退只用于 GET、HEAD、OPTIONS；网关不做数据库复制、写入重放或多主协调。
- 数据只有一个写者；两库之间是单向、只读来源的复制。切换写者要先停写、最终追平、逐项比对，再验证生产入口。
- 路由切换和数据一致性分开验收：入口返回 200，不说明两边数据一致。

**容量预算**。边缘函数、Serverless 实例和托管数据库的免费或包月额度，常按账户或组织共享，而不是按环境计。预算时注意几点：

- 多个环境共用一份额度，不能各算一份；
- 请求次数、计算时长、出口流量、数据库容量是不同的指标，分别估算；
- 额度以平台当期账单页为准，并随时间变化，在书里只记口径，不记数字。

:::practice
**iac_modules**：同一渲染范式覆盖 AWS、Vultr、Akamai Cloud / Linode、阿里云、GCP、Azure、UCloud 等 provider，并标注成熟度。
**gitops**：`topology/<env>/<mode>/runtime-topology.yaml`，mode 为 selfhost / serverless / hybrid。
**postgresql.example.com**：Stunnel + ACME 单机与 Kubernetes / Helm 两种模式；镜像与 chart 发布到 GHCR；一键安装 `scripts/init_vhost.sh`。
**Platform-Orchestrator**：Selfhost 入口工作流 `selfhost-orchestrator.yml`。
:::

## 8 可观测：平台的眼睛和手

平台跑起来以后，要能看见它。没有仪表盘的车开不久：出了问题不知道在哪，没出问题也不知道离出问题还有多远。

### 8.1 三根支柱

可观测有三根支柱：**Metrics** 是随时间变化的数值，适合看趋势和告警；**Logs** 是离散的事件记录，适合查细节；**Traces** 是一次请求走过的全链路，适合找慢在哪里。三者最好在一个界面里关联查询。

[[fig81]]

### 8.2 自建组合：Grafana + Victoria 全家桶

自建的组合是：Grafana 做统一查询、看板和告警；VictoriaMetrics 存指标，兼容 Prometheus 的写入与查询方式；VictoriaLogs 存日志；VictoriaTraces 存链路；OpenTelemetry Collector 负责标准化接入。

`observability` 仓库（ai-workspace-infra/observability）正是这套组合：遥测存储由 VictoriaMetrics、VictoriaLogs、VictoriaTraces 与 OpenTelemetry Collector 提供，Grafana 负责可视化与告警，Caddy 统一提供 HTTPS 入口。

### 8.3 采集端：探针与 Vector

采集端装在每台主机上。`observability` 仓库的主机探针使用 Node Exporter、Process Exporter、Blackbox Exporter 采集指标，用 Vector 采集 systemd 日志。

[[fig82]]

### 8.4 中心端与探针分离

这一层最重要的结构是**中心端和探针分离**。中心端负责存储、看板和告警；探针只负责采集和上报。`observability` 仓库提供两个独立的安装入口：`setup-observability-server.sh` 装中心服务，`setup-observability-agent.sh` 装探针。

探针的写入路径由 Caddy 的 HTTP Basic Auth 保护，账号默认从 Vault 读取；Grafana 管理员密码由 Vault Agent 注入或隐藏输入，安装后立即 `unset`。安装器不会把自动生成的明文凭据写进中心端文件或 Ansible 日志。

[[fig83]]

### 8.5 验收边界：本机健康 ≠ 中心收到

一个容易被忽略的细节：探针在本机显示健康，不等于中心端已经收到数据。`observability` 仓库把这条写成了交付准则：接入后还要检查指标和日志的**新鲜度**。验收要看终点，而不是起点。

另外，这个仓库只维护轻量安装脚本、部署说明和契约检查，服务角色和编排以 `playbooks` 为准，避免两处实现漂移。


### 8.6 每一种「绿」只证明一件事

CI 绿了、PR 合了、服务 active、接口 200，常被一路写成「已验收」。写报告时按下表对号入座：

:::table
你看到的|能说明|还不能说明
代码 / 合同存在|参数和调用关系可以检查|身份、凭据、目标可用
本地静态检查通过|格式、引用、部分负例正确|云上和主机上行为正确
CI 通过|这个版本的检查完成|真实环境或业务验收
已合并进 main|代码进入主干|权限已生效、调用方能跑
指定环境运行完成|这一次部署的结果|数据一致、具备晋级资格
业务验收通过|同构件、同环境、同目标满足门槛|能套用到别的版本或环境
:::

- 容器只是 running、没有健康检查，不算健康；
- DNS 变更要验证公开入口到后端的整条链路，不只看 provider 写入成功；
- 日志和报告里只留脱敏的标识、摘要和校验和，不留令牌、私钥或完整连接串。

:::practice
**observability**：中心服务与主机探针的一键部署入口，复用 playbooks 的 Ansible roles；VictoriaMetrics / VictoriaLogs / VictoriaTraces + OpenTelemetry Collector + Grafana + Caddy；凭据优先从 Vault 运行时读取。
**playbooks**：可观测性相关 role 与 playbook 是部署实现的唯一来源。
:::

## 9 能恢复才算稳定

很多团队都有备份，但很少有人真的恢复过。这一章只讲一句话：**能恢复才算稳定**。备份、迁移、回滚，都要变成日常操作，而不是出事那天才第一次尝试的冒险。

### 9.1 稳定的定义：能恢复

系统总会出问题：磁盘坏、误删、云厂商故障、发布出错。稳定不是「从不出事」，而是出事之后能在约定的时间内，回到约定的状态。

衡量它的是两个指标：RPO（最多能丢多少数据，由备份频率决定）和 RTO（多久能恢复服务，由恢复流程和演练决定）。先把这两个数字定下来，再谈工具。

[[fig92]]

### 9.2 不可变快照与回滚

版本层面的恢复靠不可变快照。第 6 章讲过：每个快照有唯一 tag，SIT、UAT、PROD 晋级同一个产物。回滚因此变得简单：把声明里引用的 tag 切回上一个，收敛控制器就会把环境拉回去。

[[fig93]]

### 9.3 数据的备份、迁移与恢复：三件套

数据层面，`playbooks` 仓库把 **backup / migrate / restore** 做成了按业务域复制的三件套：通用站点、AI Workspace、Agent Proxy、Web SaaS、基础平台等，每个域都有对应的 `*-backup.yml`、`*-migrate.yml`、`*-restore.yml`。`migrate` 分 extract → load 两阶段，运行期可以动态加入迁移主机。

同一套动作，在 `Platform-Orchestrator` 里通过手动触发的工作流执行：README 写明 `workflow_dispatch` 才真正执行开通、部署、迁移、备份、恢复等动作。

[[fig91]]

### 9.4 不落盘的流式搬迁

`playbooks` 的搬站链路有一个值得学习的取向：以 S3 对象存储作为流式中转，源端 `pg_dump` / `tar` 直接通过管道推上 S3，目标端边下边解，**不在本地磁盘落中间产物**；S3 凭据运行时经 Vault JWT 短期认证取得，任务结束即失效；增量同步复用 `aws s3 sync` 的比对，弱网可断点续传。S3 兼容存储同样可以自建。

### 9.5 数据库全量迁移

数据库是最难重建的状态，所以单独拿出来。`postgresql.example.com` 提供 `scripts/db_full_migration.sh`：可以先初始化目标机再全量迁移，也可以只测迁移流程；常用参数包括 `--target-domain`、`--target-tls-port`（默认 5443）、`--acme-mode`（auto / bootstrap / host-caddy）、`--import-globals`、`--skip-import`、`--skip-compare`。迁移后默认对比源与目标，校验结果。

### 9.6 演练日常化

最后一步是把恢复变成例行公事：定期在隔离实例上真的恢复一次，并检查行数、校验和和应用自检。只有恢复成功，这次备份才算成功。


### 9.7 数据升级的八个阶段

生产用的必须是 UAT 验收过的同一个构件（同一 digest），不重新构建 main；创建生产 tag 和部署生产是两个阶段。数据升级按八个阶段走：

[[figW9]]

- UAT 完整演练「升级 → 回滚 → 同一构件再升级」，才算拿到晋级资格；
- PROD 只消费资格，按实时条件重做 preflight，不在生产演练或注入故障；
- 迁移绑定起止 schema 版本和校验和；回滚只回退应用，保留向前兼容的 schema，不跑破坏性的 down migration。

「只读」有四种：只读账号、默认只读事务、单次只读事务、只读副本。任何一种都不能单独证明复制已经一致、写者已经停止。

:::practice
**playbooks**：按业务域的 backup / migrate / restore 三件套；`site_migration` role 的 extract / load；S3 流式中转、不落盘，凭据经 Vault JWT 短期获取。
**postgresql.example.com**：`scripts/db_full_migration.sh` 全量迁移，支持初始化、仅测流程、对比校验。
**Platform-Orchestrator**：`workflow_dispatch` 执行备份、迁移、恢复等动作。
**artifacts**：不可变快照与构建产物（据组织主页）。
:::

## 10 七层拧成 Open Platform

最后一章把前面的七层拧在一起。工具拼在一起不等于平台；平台是每一层都有它该干的事，层与层之间有清楚的合同。

### 10.1 七层回顾

Git 与 CI 是入口，资源即代码让环境 apply 就出来，交付引擎幂等地把软件装上去，安全与身份让人和机器都不再持有长期密码，环境治理让 SIT、UAT、PROD 晋级同一个产物，云中立让每一层都可替换，可观测让平台看得见；在此之上，能恢复才算稳定，AI 接入让平台走进 Agent 时代。

[[fig111]]

### 10.2 层与层之间的合同

本书反复出现的，是层与层之间的合同：`gitops` 的声明是资源层的唯一入口；`iac_modules` 产出的 `cmdb.json` 与 `inventory.ini` 是 IaC 与 Ansible 之间的合同；Vault 是所有凭据的唯一来源；不可变快照 tag 是 CI 与 CD 之间的合同。`Platform-Orchestrator` 的 README 用一句话概括：toolkit 是按钮，iac_modules 建资源，playbooks 安装和配置应用，gitops 声明期望的环境状态。

按仓库划分，职责也是一一对应、互不越界的。一个动作该改哪个仓库，先查这张表；表里找不到归属，说明合同还没写全：

:::table
仓库|职责
Platform-Orchestrator|输入、授权、DAG、派发、等待、回执汇总
IaC|云资源、DNS、State、CMDB
GitOps|环境与资源声明、Flux 配置
Artifacts|构建、镜像、Chart、制品发布
Playbooks|主机、服务、数据库、备份恢复与迁移执行
:::

编排仓库只排顺序、发指令、收回执，自己不建资源、不装软件；其余四个仓库各管一段，彼此只通过声明、CMDB、tag / digest 和回执交接。

落到日常操作，可以记成五层分工和五类事实：

[[figW10]]

- 入口层（CI 平台）只负责触发、审批、派发；控制面只做输入校验、调用 owner、校验回执、放行；具体执行分别归 IaC 和 playbook role。
- 入口里残留的 inline Terraform、主机命令、包装脚本，按行为逐个登记，迁回对应 owner。
- 必需阶段一律 fail closed：回执为空、失败、缺失，或来源 / 环境 / 版本对不上，都停止；可选阶段要事先写进合同，不能事后补一句「跳过」。

:::table
事实|放在哪里|怎么用
希望存在什么|GitOps 声明|执行的输入，不代表运行状态
Terraform 管了什么|按账号隔离的 state|只给 IaC 用
这一次的资源事实|CMDB / inventory|playbook 与验收读取，不手改
要发布的构件|tag / digest|不用重新构建的版本替代
身份和密钥|Vault / 动态身份|最小范围读取，不进声明
:::

### 10.3 成熟度自评

给每一层打个分：0 是手工，靠人记、靠登录；1 是脚本化，有脚本但没有评审；2 是声明式，Git 是唯一真相，可重复；3 是平台化，自助、有合同测试、可审计。找出最低的那一层，就是下一步要补的地方。

[[fig112]]

### 10.4 开放标准清单

云中立的底气来自开放标准：Git 管版本与评审，OCI 管镜像与构件，OIDC 管机器与人的身份，OpenTelemetry 管遥测数据，MCP 管 Agent 调用工具，HCL 与 YAML 管声明。每选一个工具，先问它是否站在开放标准上。

[[fig113]]

### 10.5 架构图即代码

平台的架构图也应该是代码。`diagram-generator` 用 `config.yaml` 描述 Open Platform Toolkit 总图，用 HTML / Tailwind CSS 模板和 Playwright 渲染出高分辨率 PNG：改图就是改配置、重新生成，而不是在绘图工具里拖框。本书的图 0 就来自它。

### 10.6 11 大核心服务类别：单机验收与 umbrella chart

七层落到可部署的东西，是 11 大核心服务类别。每一类都要同时回答两个问题：在一台开发机上能不能一条命令起来、本机验收；进了集群能不能用同一个 Helm chart 交付。所以每一类配两张矩阵：单机部署与验收矩阵，和 umbrella chart 子 chart 矩阵。

设计上有两条约束。第一，单机矩阵的端口一律只绑定 127.0.0.1：本机验收不需要对外暴露，公网入口交给 Caddy 和第 5 章的身份层。第二，子 chart 与单机脚本是同一个服务的两种交付形态，镜像版本钉住、端口合同一致，不是两套实现。

单机部署与验收矩阵（macOS OrbStack 等本机容器环境；compose 项目名、容器名与验收状态以各仓库验收记录为准，书中未核实的写「待确认」）：

:::table
序号|类别|固定镜像|本机端口（127.0.0.1）|健康探针 / 测试命令|单机入口
01|Gitea|gitea/gitea:1.22.6|3000|/api/v1/version|第 2 章 setup-gitea.sh
02|Harbor|goharbor/harbor-core、harbor-portal:v2.15.4|8080|/（portal）|6.x setup-harbor.sh --standalone
03|Silo S3|pgsty/silo（RELEASE 标签钉住）|9000 / 9001|/minio/health/live|待确认
04|CMDB|python:3.11-alpine|8000|/healthz|第 4 章 setup-ansible-cmdb.sh
05|可观测性|中心端与探针镜像版本待确认（由 playbooks 固定版本）|3030 / 9090 / 9428 / 10428；探针 9100 / 9256|中心端 /api/health、/health；探针 /metrics|setup-observability-server.sh / -agent.sh
06|Vault + Zitadel|hashicorp/vault:1.17.6、postgres:16-alpine|8200 / 5432|/v1/sys/health；pg_isready|第 5 章 setup-vault-zitadel.sh
07|doco-cd|ghcr.io/kimdre/doco-cd:0.1.28|80 / 9120|/v1/health|第 6 章 setup-doco-cd.sh
08|k3s + pgvector|pgvector/pgvector:pg16|5432|pg_isready|第 7 章 setup-k3s-node.sh
09|pg-backup|postgres:16-alpine|5432|pg_isready|第 9 章 setup-pg-backup.sh
10|AI 网关（New API + LiteLLM）|calciumion/new-api:v0.4.10、ghcr.io/berriai/litellm:v1.51.0|3000 / 4000|/api/status；/health/liveliness|第 11 章 setup-ai-gateway.sh
11|MCP 网关|alpine:3.20|8080|/|待确认
:::

05 可观测性的单机形态来自 observability 仓库：两个独立入口，中心端装 Grafana、VictoriaMetrics、VictoriaLogs、VictoriaTraces 与 Caddy 接入网关，探针端装 Node Exporter、Process Exporter、Blackbox Exporter 与 Vector。脚本本身很薄：只做 root / Debian 或 Ubuntu / Python 3.11 检查，然后拉取 `scripts/observability_install.py`，复用 playbooks 的 Ansible roles 部署；不接受命令行参数，配置全部来自导出的环境变量（凭据从 Vault 运行时读取），重跑会先备份配置、保留数据卷。

:::code
# 中心端（需 root；GRAFANA_ADMIN_PASSWORD 与写入凭据从 Vault 导出）
curl -fsSL https://raw.githubusercontent.com/ai-workspace-infra/observability/main/setup-observability-server.sh | bash
# 探针（与中心端使用同一对写入凭据）
export OBSERVABILITY_ENDPOINT=https://observability.example.com
curl -fsSL https://raw.githubusercontent.com/ai-workspace-infra/observability/main/setup-observability-agent.sh | bash
:::

安装器自带验收：中心端依次检查 127.0.0.1 上 3030、9090、9428、10428 的健康接口；探针端检查四个 systemd 服务处于 active，并抓取 9100、9256 的 /metrics。它最后会提醒一句：本机健康通过后，还要核对公网 DNS/TLS 和中心端是否真的收到探针数据，这正是 8.5 节的验收边界。

umbrella chart 子 chart 矩阵（ai-workspace-infra/artifacts 的 `oci/charts/open-platform/charts/<name>/`）：

:::table
序号|子 chart|固定镜像|端口合同|helm lint
01|gitea|gitea/gitea:1.22.6|3000 HTTP / 22 SSH|通过
02|harbor|goharbor/harbor-portal、harbor-core:v2.15.4|8080 / 80|通过
03|silo|pgsty/silo|9000 S3 API / 9001 Console|通过
04|cmdb|python:3.11-alpine|8000 REST|通过
05|observability-stack / observability-agent|stack：Prometheus、VictoriaMetrics/Logs/Traces、Grafana、OTel Collector（上游 chart 版本区间）；agent：timberio/vector:0.36.0-distroless-libc、ncabatoff/process-exporter:v0.8.3、node-exporter|agent 9256（process-exporter）|通过
06|vault-zitadel|hashicorp/vault:1.17.6、postgres:16-alpine|8200 / 5432|通过
07|doco-cd|ghcr.io/kimdre/doco-cd:0.1.28|80 HTTP / 9120 Metrics|通过
08|pgvector|pgvector/pgvector:pg16|5432|通过
09|pg-backup|postgres:16-alpine|5432|通过
10|ai-gateway|calciumion/new-api:v0.4.10、ghcr.io/berriai/litellm:v1.51.0|3000 / 4000|通过
11|mcp-gateway|alpine:3.20|8080|通过
:::

05 可观测性在集群里拆成两个子 chart：`observability-stack` 部署中心端（Prometheus、VictoriaMetrics、VictoriaLogs、VictoriaTraces、Grafana、OpenTelemetry Collector，以 Flux HelmRelease 引用上游 chart，集群需已有 Flux）；`observability-agent` 部署采集端（Vector 采集 journald 写入 VictoriaLogs、process-exporter，node-exporter 可选）。拆成两个的理由与单机脚本相同：中心端一套，探针每个集群或节点一份，升级节奏不同。

:::code
# 本地校验（artifacts 仓库根目录）
helm lint oci/charts/open-platform
helm template my-platform oci/charts/open-platform
:::

### 10.7 验证与测试结论

结论只写验证过的事实：子 chart 的 `helm lint` 全部通过（v0.9.7 核对）；单机列只说明入口，不代表某个环境已验收。每一类都能通过一条 shell 命令或一个 Helm chart 部署，具体如下：

:::table
序号|类别|一条 shell 命令|Helm chart
01|Gitea|setup-gitea.sh|open-platform/gitea
02|Harbor|setup-harbor.sh --standalone|open-platform/harbor
03|Silo S3|待确认|open-platform/silo
04|CMDB|setup-ansible-cmdb.sh|open-platform/cmdb
05|可观测性|setup-observability-server.sh / setup-observability-agent.sh|observability-stack / observability-agent
06|Vault + Zitadel|setup-vault-zitadel.sh|open-platform/vault-zitadel
07|doco-cd|setup-doco-cd.sh|open-platform/doco-cd
08|k3s + pgvector|setup-k3s-node.sh|open-platform/pgvector
09|pg-backup|setup-pg-backup.sh|open-platform/pg-backup
10|AI 网关|setup-ai-gateway.sh|open-platform/ai-gateway
11|MCP 网关|待确认|open-platform/mcp-gateway
:::

- lint 通过只证明模板能渲染，不等于部署成功；和 8.6 节一样，每一种「绿」只证明一件事。
- 「待确认」项补齐来源后再改写，不按惯例推测。

### 10.8 下一步

这是一本活的书。平台会继续演进，书也会跟着更新：新的实践、新的复盘、新的快速开始脚本。从你最低分的那一层开始，一个域名，一台机器，一行脚本。

:::practice
**Platform-Orchestrator**：「toolkit 是按钮，iac_modules 建资源，playbooks 装应用，gitops 声明状态」。
**diagram-generator**：`config.yaml` + HTML/Tailwind 模板 + Playwright 渲染 Open Platform Toolkit 总图。
**.github**：组织主页的四大支柱与组合式交付链。
:::

## 11 AI 接入平台：模型也是基础设施

导言把下篇的起点定在「状态可观测」。这一章先把平台状态向量化，让 AI 读得到上篇写下的一切；再讲 AI 时代平台多出的两件事：**接入模型**，和**把一部分运维交给 Agent**——聚合网关、MCP，以及 Agent 运维的边界。模型和数据库一样，是平台要管理的基础设施。

### 11.1 平台状态向量化：从代码化到可检索

导言说过：代码化让平台状态「写得下来」，向量化让它「找得出来」。这一节把第二步落到工程上。它是下篇闭环里**观测器**的一半——指标和日志告诉 Agent 现在发生了什么，向量索引告诉它平台本来应该是什么样、规则是什么。

**数据源**只取已经进 Git 的东西（对应 10.2 的五类事实）：GitOps 声明（6.5）、IaC 模块与拓扑 YAML（第 3 章）、playbook 与 role（第 4 章）、CMDB 导出（4.4）、Runbook 与服务目录，以及第 12 章的 21 项规范。不进 Git 的口头约定，不进索引。

**切分**按语义边界，而不是按固定字数：一个 Terraform module、一个 playbook role、一条 GitOps 应用声明、一篇 Runbook 的一个步骤，各是一块。每块带上元数据：仓库、路径、commit、环境、所属层。检索结果因此可以回指到具体文件和版本，Agent 的回答也就能引用出处。

**刷新**跟着 commit 走：合入 main 后，由 CI（第 2 章）只对变更的文件重新切分和向量化，索引里记下对应的 commit。索引和 Git 一样有版本，回答「上周五的 PROD 是什么配置」时，可以检索当时那一版。

**访问控制**是底线：Vault 里的秘密（第 5 章）、`.env`、私钥、state 文件里的敏感输出，一律在入库前过滤，永远不进索引。检索时按调用者的身份（OIDC，第 5 章）过滤可见范围：开发者看得到自己项目的声明，看不到别人的；Agent 的身份同样受限。

[[figV11]]

:::table
数据源|切分单位|刷新时机|不进索引
GitOps 声明|一条应用 / 环境声明|合入 main|渲染后的密钥值
IaC 模块与拓扑|一个 module / 一份拓扑 YAML|合入 main|state 中的敏感输出
playbook / role|一个 role / 一个场景 playbook|合入 main|vault 变量明文
CMDB|一个资产及其关系|导出或同步时|凭据、登录信息
Runbook 与规范|一个步骤 / 一项规范|合入 main 或打 tag|—
:::

向量库的选型本书不展开。第 7.5 节的 postgresql.example.com 自带 pgvector，可以作为一种起步选择；无论用什么库，上面四条——源、切分、刷新、访问控制——比选型更重要。有了可检索的平台状态，下一节开始讲另一件事：模型本身怎么接进平台。

### 11.2 为什么需要 AI 聚合网关

当团队同时使用多家模型，问题就来了：每个应用各自保存一套模型密钥，额度和成本无从统计，换一家模型要改所有调用方。聚合网关把这些收口：应用和 Agent 只对接一个统一入口，密钥只留在网关侧，由 Vault 注入。

[[fig101]]

### 11.3 ai-aggregator：New API + LiteLLM

ai-aggregator 是本书定位的开源 AI 聚合网关。按其 README（仓库即将公开），架构是：Caddy 提供 TLS 入口，可选接入 APISIX / Kong 网关，New API 负责用户、套餐、额度和模型权限，CPA 与 LiteLLM 负责重试和成本统计；支持三种部署模式，凭据不入仓库。

New API 和 LiteLLM 都是开源项目：前者侧重用户与额度管理，后者提供统一的 OpenAI 兼容调用接口和路由能力。两者组合，分别解决「谁能用多少」和「怎么调用得稳」。

### 11.4 额度、权限与成本

网关上要落三件事：额度（每个用户或团队能用多少）、权限（能调用哪些模型）、成本（每次调用花了多少）。这些都是平台策略，应该写成配置、可评审，而不是散落在各个应用里。

### 11.5 MCP 与 Infrastructure-MCP-Server

MCP（Model Context Protocol）是一个让 Agent 以标准方式调用工具的开放协议。`Infrastructure-MCP-Server` 是一个 Go 网关：它聚合现有的 MCP server，为 Agent 提供面向基础设施的稳定工具面，覆盖 IaC、CMDB、运行时、安全和环境图谱。

它目前是初始实现骨架：实现了 `initialize`、`ping`、`tools/list`、`tools/call`；通过进程方式复用下游 MCP server，不重写它们的领域工具；按命名空间聚合（如 `kubernetes.<tool>`、`netbox.<tool>`）；内置 `infra.backends`、`infra.health`、`infra.graph.query`；环境图谱目前存于内存，计划改用 PostgreSQL / pgvector。

[[fig102]]

### 11.6 Agent 运维的边界与审计

把运维交给 Agent，边界要先画清楚：只读查询默认允许，并留下日志；变更可以出 plan，但必须由人评审；apply 和删除默认禁止，人批准后才执行。

`Infrastructure-MCP-Server` 的下一步设计也写明了这一点：增加鉴权、审计事件、超时，以及**白名单式的变更操作**。先只读，再出 plan，最后才是受控的变更。

[[fig103]]

:::practice
**ai-aggregator**：AI 聚合网关，Caddy TLS → 可选 APISIX / Kong → New API → CPA 与 LiteLLM，三种部署模式，凭据不入仓（据 README，仓库即将公开）。
**Infrastructure-MCP-Server**：Go 实现的 MCP 聚合网关，命名空间聚合下游 MCP server，内置 infra 工具，下一步加鉴权、审计与白名单变更。
:::

这一章给了 Agent 两样东西：读得到的平台状态，和受控的工具入口。但 Agent 该按什么规则行动？下一章把规则本身变成事实源。

## 12 规范即事实源：人和 AI 守同一本规则

上一章让 Agent 读得到平台状态，也拿到了受控的工具。按导言的类比，现在要给控制器加上**约束条件**：哪些事能做、按什么顺序做、做到什么程度算完成。这一章讲作者自己的实践——把工程与运维规范写成版本化的事实源，人和 AI 按同一本规则做事。

### 12.1 为什么规范要成为事实源

口头约定有三个问题：会走样，新人和 Agent 读不到，出了问题无法追溯「当时按的是哪条规则」。上篇其实一直在做同一件事：资源写进 IaC，配置写进 playbook，部署写进 GitOps，例外写进合同（5.5）。规范是最后一块：**规则本身也进 Git，走 PR，有版本**。

这样做之后，人和 Agent 读的是同一份文本；CI 门禁检查的也是同一份。规范升级不是一句通知，而是一次可审查、可回退的提交。

### 12.2 13 项工程规范

作者在公开仓库 xworkspace-core-skills 中维护了 13 项工程规范，每项是一个带 SKILL.md 的技能目录，人可以读，Agent 也可以按技能加载。其中 Agent Harness 工作流是串联其余各项的主线。

:::table
规范|核心内容|上篇对应
Agent Harness 工作流|自测、代码审查、CI/CD 与多环境发布的统一循环，串联其余规范|第 2 章
Issue/PR 溯源与需求事实源|需求以 Issue 为事实源，Issue → 分支 → commit → PR → CI → 部署 → Tag 可追溯|2.7
工程开发规范|分支命名、主干保护、PR 合并策略、不可变 Release Tag、误提交密钥的撤回流程|2.6–2.7
CI/CD 工作流规约|CI 与 CD 解耦、流水线脚本外置复用、最小权限 OIDC、不可变制品与防假绿门禁|2.5、6.3
四边界执行归属迁移|划清 Toolkit、GitOps、IaC、Playbooks 四个仓库的职责与迁移步骤|10.2
多环境交付与发布|SIT / UAT / PROD 渐进交付路由，OIDC → Vault 隔离各环境凭据|第 6 章
可重复代际升级验收|按阶段执行新环境部署、数据对齐、业务回归与显式切换门禁|第 9 章
IaC 规约（iac_modules）|拓扑 YAML 驱动、State 按环境隔离、HCL 纯声明、与 CMDB 解耦|第 3 章
Config-as-Code 规约（playbooks）|Vault 优先、凭据不落盘、剧本幂等、直接消费 IaC 产出|第 4 章
GitOps 唯一资源事实源|GitOps matrix 驱动 Hybrid / Selfhost / Serverless，按 provider/account/state 隔离|6.5、7.4
AI 代理协作标准|人机角色边界、工作区脏检查、越权拦截、破坏性操作前的确认|11.6
应用商店与初创扶持官网规范|面向应用商店与初创计划审核的官网设计、域名边界与部署后检查|—
零信任网络 Overlay 交付规约|跨云网络互联、WireGuard-over-TLS 与鉴权审计|5.x
:::

职责迁移按固定顺序推进，一步不跳：

- C0 合同评审：写清职责和调用链，登记差异；
- C1 owner 落地：参数化的 IaC 入口或 playbook role，带失败、幂等和清理检查；
- C2 调用方切换：固定使用 owner 的版本，缺依赖即失败；
- C3 UAT：覆盖成功、失败、幂等和业务结果；
- C4 清理：前三步齐全后才删除旧副本；
- C5 文档归并：保留各文档的适用日期。

### 12.3 8 项运维标准

另一组是 8 项运维标准，覆盖平台上线后的日常。

:::table
标准|核心内容|上篇对应
备份、恢复与数据迁移|数据保护目标、异地恢复演练、切换后增量补同步、RPO/RTO|第 9 章
事件响应与变更管理|故障分级、紧急变更通道、发布冻结、无指责复盘并落地回归脚本|9.6
密钥、身份与访问治理|Vault policy/role、GitHub Actions OIDC、最小权限、动态凭据轮转与吊销|第 5 章
网络、DNS、TLS 与边缘管理|DNS 记录与 TTL 规划、ACME 证书续期、反代配置与流量回滚|7.x
可观测性、SLO 与告警规范|SLI/SLO、错误预算、看板标准、告警分级降噪、部署后健康检查|第 8 章
容量、成本与资源生命周期|资源核算、升降配与置换、快照留存、闲置与孤儿资源回收|7.6
服务目录与 Runbook 标准|服务元数据、依赖拓扑、应急 Runbook、下线退役约定|4.4
GitHub Actions 运维分发|Agent 发起运维工作流前的参数校验、workflow_dispatch 留痕与异步追踪|2.6
:::

两组规范共享几条原则：**门禁前置**（合并、发布、迁移先过质量门禁与可证伪测试）、**恢复要真实演练**（只备份不测恢复不算数）、**凭据不落盘**（一律从 Vault 取有时效的动态凭据）、**故障闭环要有回归**（复盘必须产出能拦截同类问题的测试用例，否则变更不算关闭）。最后一条，就是导言里「复盘写回」的出处。

### 12.4 版本化绑定：规范的不可变快照

规范有版本，就要解决「本机的 Agent 按哪一版做事」。仓库里的 `scripts/bind_global_standards.py` 把某个固定 commit 的规范绑定到本机，思路和第 6 章的不可变构件一样：**引用快照，不引用会动的分支**。

:::table
行为|说明
默认只预览|不加参数只打印将要做的变化，加 --apply 才修改本机
必须给完整 SHA|--ref 只接受 40 位 commit SHA，不接受分支名
detached worktree 快照|每个版本用 Git detached worktree 存一份完整快照，保留目录间的相对引用
current 指针|一个指向活动版本的链接，切换版本只改这一处
lock.json 与 history/|记录仓库、commit、快照和受管链接；旧记录进 history/，供显式回退
--check|校验快照 HEAD、内容漂移、版本指针和每条技能链接
不覆盖非受管目录|遇到同名但不是本工具管理的目录或链接，直接停止
不碰生产|只做本地 Git worktree 与技能目录操作，不运行部署、云 API、DNS、主机或数据库命令
:::

升级和回退用同一条命令，只是换一个 SHA；旧快照保留，不自动清理。任务记录里写下本机锁定的 commit，另一台机器就能按同一版规则复现。

[[figS12]]

### 12.5 AI 代理协作标准

21 项里，和 Agent 关系最直接的是 AI 代理协作标准。它先划角色：人是唯一决策者，负责需求、架构决策和验收；主代理拆解任务、调度进度；子代理在独立分支或上下文里做单一任务。Agent 不得自行改动构建流程、部署环境或分支保护规则。

执行上的几条红线：每次执行前读仓库的 `AGENTS.md`；不得用 `--admin`、`--force` 绕过评审和 CI；部署只由 Git 事件触发（PR → SIT，合入 main 或 release/* → UAT，v* tag → PROD，与 2.6 一致）；凭据只经 Vault + OIDC 动态获取；先 `git status` 保留用户现场，不 reset、不清理不属于自己的改动；删除实例、快照、DNS、state 之前，先只读列出精确目标、影响和回滚点，得到明确授权才执行，且授权删实例不等于授权删快照。

用导言的话说，这是控制器自己的**安全边界**。规则有了，下一章把它们串成开发者每天真正走的路。

## 13 开发者门户与黄金路径

第 12 章把规则写成了事实源，但 21 项规范不可能让每个开发者逐条读完再动手。这一章讲两件事：一个统一的入口，以及把规范预先串好的**黄金路径**。按导言的类比，黄金路径是在约束之内事先规划好的推荐轨迹。

### 13.1 一个入口：Cloud Hub / Operations / Releases

作者的门户 console.example.com 把平台分成三个视图。本书只按职责描述它们，不涉及具体界面：

:::table
视图|回答的问题|背后的事实源
Cloud Hub|我有哪些资源、在哪些云上、属于哪个项目|IaC 拓扑、CMDB（第 3、4 章）
Operations|平台现在运行得怎么样，有什么需要处理|可观测体系（第 8 章）、Runbook
Releases|什么版本在哪个环境，能否晋级或回退|GitOps 声明、不可变制品与快照（第 6、9 章）
:::

门户本身不是新的事实源。它读的是 Git、CMDB 和可观测数据，写操作也最终变成一次 PR 或一次受控的工作流。这一点决定了门户和 Agent 可以共用同一个后端：人点按钮和 Agent 调用工具，落到的是同一条链路。

### 13.2 黄金路径 = 规范串成模板

黄金路径是一个模板仓库加一组默认配置：分支与 PR 规则、CI 流水线、制品推送到 Harbor（6.4）、GitOps 声明、可观测接入、备份策略，都已经按第 12 章的规范预先接好。新项目从模板出发，第一天就满足规范，而不是上线前再补。

它的价值不是「强制」，而是**让正确的做法成为最省事的做法**。走黄金路径的项目，评审时只需关注业务改动；偏离的部分才需要额外讨论。

[[figS13]]

### 13.3 四条典型路径

:::table
路径|典型组成|默认门禁|交付形态
静态站点|静态构建 + Caddy 自动 HTTPS|构建通过、链接检查|单机或对象存储 + CDN
Web 服务|容器镜像 + 数据库连接 + 健康检查|单元测试、镜像扫描、SIT 部署验证|Compose（单机）或 K3s / K8s
数据库|postgresql.example.com（7.5）|备份与恢复演练脚本就位|自建实例 + 定期备份
AI 应用|应用 + ai-aggregator 网关（11.3）|模型密钥只在网关侧，额度已配置|与 Web 服务相同，外加网关路由
:::

四条路径共用同一条晋级链：PR 到 SIT，合入到 UAT，打 tag 到 PROD。区别只在模板里预置了什么。

### 13.4 偏离也要写进合同

总有项目不适合任何一条路径。这时不禁止，而是沿用 5.5 的做法：把偏离写成合同——偏离了哪条规范、为什么、谁批准、什么时候复查。合同进 Git，门户和 Agent 都看得到，例外也就有了期限和出处。

入口和路径有了，开发者接下来最常问的是：「我需要一个资源，能不能自己开？」这是下一章的内容。

## 14 自助服务与外部集成

第 13 章的黄金路径解决「从哪里开始」，这一章解决「需要资源时怎么办」。目标是：开发者自己发起申请，平台按策略决定是自动交付还是等人审批，整个过程和上篇的每一层一样，写在代码里。

### 14.1 自助链路：申请 → 策略/审批 → 交付 → 凭据 → 门户

一次自助申请沿着五步走：

- **申请**：在门户或通过 Agent 提出，本质上生成一个 PR 或一次带参数的工作流调用（参数先校验，见 12.3 的 GitHub Actions 运维分发）。
- **策略 / 审批**：按环境和资源类型判定——自动通过，或进入人工审批。
- **交付**：OpenTofu 创建资源（第 3 章），Ansible 完成配置（第 4 章），结果写回 CMDB（4.4）。
- **凭据**：访问方式由 Vault 下发（第 5 章），有时效、可吊销，申请人拿不到长期密码。
- **门户**：结果出现在 Cloud Hub，相关告警接入 Operations。

[[figS14]]

### 14.2 三种权限形态：全自助 / 审批 / 只读

:::table
形态|适用|示例
全自助|低风险、可随时回收|SIT 环境、预览环境（6.6）、个人测试资源
审批|影响共享环境或产生持续占用|UAT / PROD 变更、新数据库、对外域名
只读|敏感或由平台团队统一管理|身份配置、Vault 策略、网络边界
:::

划分规则本身也是代码：哪类资源在哪个环境属于哪种形态，写在策略文件里，走 PR 修改。人审批的不是「这个人可不可信」，而是「这个变更在这个环境下的影响」。

### 14.3 外部集成：CDN/DNS、监控告警、对象存储、通知、身份

平台不可能自建一切。常见的外部集成有五类，每一类都要回答三个问题：怎么接、凭据放哪、换掉它要多大代价（7.6 的退出成本）。

:::table
类别|接入方式|凭据|退出成本关注点
CDN / DNS|记录与配置写进 IaC，证书走 ACME|DNS / CDN API 令牌存 Vault|记录可导出，TTL 提前降低再切换
监控与告警|采集端与中心端分离（8.4），告警规则进 Git|写入端令牌存 Vault|开放协议采集，看板与规则可迁移
对象存储|按 S3 兼容接口使用（6.4）|访问密钥由 Vault 下发|只依赖 S3 兼容子集
通知|告警与审批事件推送到团队的消息渠道|Webhook 地址视同秘密存 Vault|通知层薄封装，可替换
身份|Zitadel + OIDC（第 5 章）|客户端密钥存 Vault|标准 OIDC，应用不绑定特定实现
:::

### 14.4 集成即代码

外部集成最容易退化成「在某家控制台里手工点的配置」。集成即代码的意思是：DNS 记录、告警规则、存储桶策略、通知路由、OIDC 客户端，全部以声明形式进 Git，走 PR、可 diff、可回滚，并被第 11.1 节的向量索引收录。

这样，外部服务也成了平台状态的一部分：门户看得到，Agent 检索得到，审计查得到。资源能自助开、外部能代码化接入之后，剩下的问题是：平台上线之后，日常维护由谁来做？

## 15 AI 辅助驱动业务应用平台维护

到这里，导言里的各个部件都已就位：状态可观测（11.1、第 8 章），工具入口受控（11.5），规则成为约束（第 12 章），推荐轨迹预先铺好（第 13 章），变更走自助链路（第 14 章）。这一章把它们连成维护闭环：**人看板，AI 值守**。

### 15.1 维护闭环：观测 → 诊断 → 建议/执行 → 验证 → 复盘写回

:::table
环节|做什么|主要执行者|留下的证据
观测|告警、巡检、部署后健康检查（第 8 章）|AI 持续值守|告警记录、巡检报告
诊断|结合指标、日志与向量索引中的声明和 Runbook 定位原因|AI 预诊断，人确认|诊断结论与引用的文件和版本
建议 / 执行|只读操作直接做；变更出 plan；低风险动作在白名单内执行|AI 提出，人审批|plan、PR、工作流记录
验证|执行后重新检查 SLO 与健康状态|AI|验证结果
复盘写回|把结论写回 Runbook、规范或回归测试（12.3）|人主导，AI 起草|PR 与新增测试
:::

最后一环是闭环和「自动运维脚本」的区别。按导言的类比，它对应自适应控制：系统根据结果调整自己的规则。但调整规则的那一步始终走 PR，由人合入。

诊断时沿交接链从上往下查：请求 → 声明 → 身份与权限 → backend 与 state → 云资源 → CMDB → 主机与服务 → 公开路由 → 业务数据 → 证据关联。403 先查 role 和路径，不扩大权限；账号不对就停在 Terraform 之前。Agent 预诊断也按这个顺序检索 11.1 的索引，结论落到具体某一层。

[[figS15]]

### 15.2 Releases / Operations：人看板，AI 值守

分工很简单：AI 在 Operations 视图背后持续巡检和预诊断，把需要决策的事整理成一条条带证据的待办；人在 Operations 和 Releases 上看结论、做决定——批准变更、批准晋级、决定回退。AI 值守的范围由第 12.5 节的协作标准和第 11.6 节的边界决定，而不是由它自己判断。

### 15.3 安全边界：熔断、审批与回滚

三道边界对应导言里的「安全边界」：

- **熔断**：删除实例、快照、DNS、state 等破坏性动作默认禁止；同一问题连续处理失败时停止并转人工。
- **审批**：一切写操作先出 plan，影响共享环境的变更按第 14.2 节的形态走审批。
- **回滚**：每次变更都要有回滚点——不可变制品与快照（6.3、9.2），GitOps 回退到上一个声明（6.5）。

### 15.4 衡量：是否真的更稳、更省

是否「用了 AI」不是指标。建议跟踪这几类，并和引入 AI 值守之前的同一指标对比：

:::table
指标|看什么
恢复时间|从告警到恢复的时间是否缩短
变更失败率|变更后需要回退或修复的比例是否下降
告警噪音|无需处理的告警占比是否下降
人工介入次数|需要人处理的事项数量与类型变化
复盘回归覆盖|复盘后落地回归测试的比例
:::

本书不给出这些指标的参考数值：它们取决于各自平台的规模和基线。重要的是从第一天就记录，用数据而不是感觉判断闭环有没有起作用。最后一章，回到全书。

## 16 全书收尾：从七层平台到 AI 原生平台

### 16.1 两篇回顾：经典回路与现代闭环

上篇搭起了七层：Git 与 CI 是入口，资源、交付、身份、环境、云中立、可观测、恢复各管一层，第 10 章用层间合同把它们拧成 Open Platform。每一层都是一个经典回路：commit 进去，环境出来，偏差被拉回。

下篇没有替换任何一层，而是在它们之上加了一个闭环：第 11 章让平台状态可检索、模型可接入；第 12 章让规则成为约束；第 13、14 章铺好推荐轨迹与自助链路；第 15 章由 AI 值守、人做决定，复盘写回规则。

经典与现代控制的对照，自始至终只是一个帮助理解结构的类比。它真正想说明的只有一句话：**先让状态完整、可读、可检索，再让 AI 在约束和安全边界之内参与控制，人保留最终决定权。**

[[figS16]]

### 16.2 AI 原生成熟度自评

在 10.3 七层成熟度自评的基础上，增加五个下篇维度。每一维从 0 到 3 打分，按最低的一维决定下一步做什么。

:::table
维度|0 尚未开始|1 起步|2 成形|3 闭环
状态可检索|平台状态散落各处|主要仓库已索引|按 commit 刷新、带出处|按身份过滤，秘密全部排除
规范事实源|规则靠口头|规范已成文|规范进 Git、走 PR|按 SHA 绑定，门禁自动检查
门户与黄金路径|没有统一入口|有入口，无模板|至少一条黄金路径|多条路径，偏离写进合同
自助服务|全部人工开通|部分资源脚本化|申请走代码与审批|三种权限形态由策略决定
AI 值守|无|AI 只读查询|AI 预诊断并出 plan|完整闭环，复盘写回回归
:::

### 16.3 下一步

从得分最低的一维开始。多数团队的顺序是：先把规范写进 Git（第 12 章），再把平台状态索引起来（11.1），然后铺第一条黄金路径（第 13 章），自助和 AI 值守放在最后——没有前面几步，后两步缺少约束和观测。

本书后续版本会继续补充各章的实践记录和快速开始。平台工程没有终点，但每一层、每一个回路，都可以从今天的一个 commit 开始。

## 17 最佳实践参考：四个正在进行的 case

上下两篇讲原则，这一章记**活的实践**：同一套平台在 2026-10-31 前后真实推进到哪一步。每条都分两档标注——**✅ 已合并**只说明代码或规范进了 main；**⏳ 待验收**说明还没有目标主机、目标集群上的运行回执。本章不宣称任何生产部署已完成。

### 17.1 Case A　Linux OS 三类操作身份：最小实施

5.10 给了三角色的原则，这里补实施细节。状态：OS 账户设计已收敛；`os_identity.yml` 与独立入口已实现（✅）；部署和真实账户验收以运行回执为准（⏳）。

**职责边界。** `vhosts/common` 只管 Linux OS 基线：主机名与身份检查、用户/组、SSH 公钥授权、受控 sudo、目录与文件权限、OS 侧允许/拒绝验收。所有 Linux 节点用同一套用户名，不因装没装 Kubernetes 而改变。K3s/K8s 认证主体与 RBAC、数据库连接授权、Docker 运行时，分别由专业 role 实现，它们**消费** common 建好的 OS 用户，不在 common 里造集群凭据或数据库角色。

:::table
Linux 用户|固定角色|OS 职责与权限
root|系统管理|初始化、安装、恢复与必要管理；不作业务进程身份；`PermitRootLogin prohibit-password`
operator|日常运行操作|SSH 公钥登录；操作授权服务与工作目录，受控 sudo
auditor|只读审计与分析|SSH 公钥登录；读授权状态与脱敏输出；无通用 sudo、无运行时 socket、无管理凭据
:::

三条要点：禁用密码认证，先验证 sshd 配置再 reload，保留旧管理入口直到新身份验收通过；`auditor` 的只读要靠有效组、文件权限、ACL、sudoers 和可执行入口逐项检查，不能凭用户名认定；`operator` 是通用保留名，接管前发现同名用户或未知 UID/GID 就停止，不改名、不重置。rootful Docker socket、`docker` 组和任意 sudo 都接近 root——授予之后不能再声称 operator 与 root 强制隔离。

**环境级 Vault KV。** 每个环境三条 KV v2 记录，所有节点消费同一份角色公钥，不按节点复制。环境必须显式给出（`sit`/`uat`/`prod`），缺失就停，绝不回退到生产路径。

:::table
用途|KV CLI 路径|字段
root SSH 公钥|kv/&lt;env&gt;/security/root|authorized_keys
operator SSH 公钥|kv/&lt;env&gt;/security/operator|authorized_keys
auditor SSH 公钥|kv/&lt;env&gt;/security/auditor|authorized_keys
:::

API/policy 路径形如 `kv/data/prod/security/root`。字段只放公钥，多把用换行分隔；暂时共用一把公钥时，持钥人能登录全部角色，不能算人员隔离。初始化用已认证的 Vault 管理终端跑 `scripts/bootstrap_os_identity_keys.py --environment <env>`：先查三个目标都不存在，再逐条 `cas=0` 创建；已有记录或状态不明就停。三次写入不是原子的，中途失败会报告已建路径，按 Vault owner 流程补齐，别盲目重跑。旧路径 `kv/prod/platform/prod-k3s-v6/ssh` 在消费者切换验收前不删、不复制。**新路径目前只代表规划与初始化工具，不代表已写入或已被 common 消费。**

[[figP1]]

**新节点接管五步。**

1. 核实受信 host key、CMDB/inventory、OS、主机名和既有用户权限，记脱敏基线；
2. 用 root 建立或核实 operator/auditor，配公钥、受控 sudo、工作目录与 SSH 策略；
3. 检查父目录、ACL、sudoers、有效组与敏感文件，先验证配置再 reload SSH；
4. 分别验证三用户的真实 SSH 登录与允许/拒绝，保留回执和恢复入口；
5. OS 基线通过后，才进入运行时、K3s/K8s、迁移等专业 role。

新接管入口须**显式启用**这套基线；通用 role 保留开关，避免老调用方升级后自动批量改账户。旧节点先盘点，再逐台变更。

**专业 role 的执行身份。** 不按任务名自动提权：系统管理阶段用 root，并记调用者与范围；日常与迁移目标写入用 operator（不新增迁移专用用户）；只读检查与源端导出用 auditor，不得写。身份缺失或权限不足时停止，不静默回退 root；OS 用户选择也不自动赋予数据库或 Kubernetes 权限。

### 17.2 Case B　K3s/K8s role：职责与依赖清单

一个 role 一种能力。冷启动的依赖链如下：

[[figP2]]

RBAC 必须先就绪才能做真实身份验收；它不能反向依赖尚未签发的三身份凭据，也不能用「管理员 impersonation 成功」代替真实身份登录。主机名、Flux root 名、环境批次目录和 source path 各自独立，不按名字推断流程。

:::table
项目|当前状态（2026-10-31）|责任与缺口
k3s_platform_bootstrap|✅ Playbooks #903 已合并|只编排子 role 与顺序
k3s-cluster-server|✅ #903 已合并|控制面初始化、hostname 校验、API 就绪
helm_cli / flux_controllers / flux_gitops / k3s_identity|✅ #903 已合并；⏳ 目标集群验收|真实身份、Vault writer 与 RBAC 待验
k3s 旧安装器|✅ #905 已合并并移除|非默认 CNI 明确拒绝
k3s_platform_addon、k3s-addon|✅ 已移除|插件改由 GitOps 按环境选择；Flux 接管待逐项验证
cert-manager / reloader / APISIX / ExternalDNS / NGINX|✅ GitOps #681 已合并|模板未接入任何环境；ExternalDNS 默认 dry-run
ESO、Caddy|✅ 已有 V6 HelmRelease；⏳ 调谐验收|不再经旧 addon 重复安装
k3s-reset|⏳ 安全边界待修|破坏性入口，旧默认值需收敛
三身份与 Flux RBAC|✅ GitOps #682、Playbooks #906 已合并；⏳ 集群验收|kubeconfig 用节点 loopback，远程另设计
Orchestrator → Playbooks|⏳ 参数交接未贯通|需传 GitOps SHA、资源路径、CMDB SHA、回执路径
Vault writer 与真实身份|⏳ 未完成|短期身份写三精确路径后，用真实账户验证
Flux 接管与服务部署|⏳ 无完整运行证据|不得据源码或静态测试宣称完成
:::

清单本身已随 Playbooks #904 迁入对应目录。主线 role 的输入输出合同：

:::table
Role|唯一能力|输出/验收
vhosts/common node_bootstrap.yml|校验节点身份、建 OS 三账户|COMMON_NODE_VERIFIED，只覆盖身份与账户探针
web_saas_data_volume|核验并准备独立文件系统|挂载点、UUID 证据；不自动重格式化
k3s-cluster-server|单节点控制面初始化|服务启动与 /readyz；既有安装跳过 ≠ 已升级
k3s_platform_bootstrap|按依赖编排子 role|失败即停；不代表业务验收
helm_cli|Helm 客户端|不部署 chart
flux_controllers|Flux CLI 与控制器|controller rollout 就绪
flux_gitops|source/root 交接|交接回执，不声称业务 Ready
k3s_identity|三身份生命周期|独立凭据、KV CAS 归档、真实允许/拒绝
:::

### 17.3 Case C　环境与业务发布解析：最小实施（目标草案）

> 状态：**目标草案，2026-10-31**。本节描述期望契约，现有工作流尚未全部实现，**不作为部署或验收回执**。✅ 表示已从当前声明或代码核对；⏳ 表示仍需实施或取得真实验收证据。

**1. 目标与职责。** 基础仓库默认选择 `main`，运行时各自解析一次 commit SHA 并传给下游；业务发布记录固定制品版本和 digest。业务发布 tag、工作流运行 ref、节点名和 state 身份是四个独立字段，不因字符串相同就自动绑定。

:::table
仓库|职责|tag / 版本引用
GitOps|环境、业务目标、资源、身份目标和 Flux 声明；保存非敏感引用|默认 main，记录本次解析的 commit SHA；可按需显式选 tag
IaC|云资源、DNS、state、云事实及 CMDB|默认 main，记录本次解析的 commit SHA；可按需显式选 tag
Playbooks|主机、K3s、身份、服务、数据库、备份恢复和迁移执行|默认 main，记录本次解析的 commit SHA；可按需显式选 tag
Platform-Orchestrator|输入、授权、DAG、派发、等待及回执汇总|默认 main，记录本次工作流 commit SHA；运行 ref 的 Vault OIDC 授权单独校验
Artifacts|构建、镜像、Chart、制品打包与发布|构建配置默认 main 并记录 SHA；业务制品用发布 tag + 核对后的不可变 digest
:::

**2. 发布解析链。**

[[figP3]]

- **1）发布 tag**：解析出环境、业务范围及 chart/镜像版本或 digest。现有 PROD Vault role 接受工作流 `v*` tag / `release/v*` 分支，优先用不可变 tag；基础仓库默认 `main` 的授权差异见 3.1 检查清单。
- **2）环境与业务**：解析结果形成不可变运行记录；dispatch 输入若也给了环境或业务，只做一致性校验，冲突即停止。
- **3）GitOps 目标声明**：用环境、业务、provider、account 和声明中的目标标识查找**唯一**目标；找不到或匹配多个都停止。
- **4）IaC**：消费声明中的资源路径、workspace 和 state key，输出节点名、地址、数据盘等 CMDB 事实；tag 不直接拼接 state key。
- **5）Playbooks/K3s**：使用本次解析的 GitOps commit 和 IaC CMDB，从声明读取节点名、K3s 配置和 Flux root/path，不按 `prod-v6` 分支判断。
- **6）Flux**：接管声明中的 source、Kustomization 和 HelmRelease，使用发布记录明确的业务制品版本。

`v*` tag 能表明「这是 PROD 发布」，但 tag 字符串本身**不能唯一确定** `web-saas` 和 GitOps 目标。需要补一份可审阅的**发布记录**，把 tag 关联到环境、业务和制品，再由 GitOps 声明确定节点及 state。发布记录应包含来源仓库/commit、镜像 digest、Chart 版本或 digest、配置版本及候选指纹；它的 owner、schema 与消费方式 ⏳ 仍待实现。基础仓库无需同步创建同名 tag。

**3. SIT、UAT、PROD。**

:::table
环境|目标发布规则|当前 Vault role ref（GitOps main d9ddcf56）|待统一
SIT|仅接受 Feature ID 关联的 GitHub task/issue 和制品 tag；固定 PR head、基础分支 SHA、完整构件和数据基线，部署独立 SIT namespace；排除 daily-build-*|refs/pull/*/merge、refs/heads/*|由受信编排器校验 task/issue、feature、制品 tag、仓库、workflow、候选、目标及 SIT 角色；ref 本身不代表部署授权
UAT|默认用合并后的固定候选；明确选合并前 UAT 时用冻结候选；候选或配置变化按影响重验|refs/heads/main、release/*、bugfix/*、daily-build-*（分支）、refs/tags/daily-build-*|目标：排除 refs/heads/release/*，其余保留；Vault role 与调用链 ⏳ 待改并验收
PROD|业务用经审查的不可变版本或 digest，tag 关联明确业务与目标；状态变更按独立集群方案|refs/tags/v*、refs/heads/release/v*|基础工作流默认 main 与现有 PROD role ref 不一致；需在受审查的认证契约中解决并做允许/拒绝验收
:::

默认流程是 **PR → SIT → 合并 → UAT → PROD 受控滚动升级**；用户明确选择时可走合并前 UAT。UAT 通过后，核对发布记录、业务范围、不可变制品和生产目标，按已有授权与发布门禁进入 PROD；部署后验证实际运行版本和关键业务流程。候选、配置或数据基线变化时按影响重新验收。**CI 成功不是运行验收**；SIT/UAT 与生产凭据隔离，公共证书等共享来源逐项审查授权。

PROD 滚动方式按变更类型选：纯展示的无状态 UI、向后兼容且无需 SQL schema 变更的小型 API 修复，可在所属单元原地滚动，保留旧制品并验证回退路径。PostgreSQL、Vault Raft、监控存储及其他持久卷工作负载的版本验证，以及 SQL schema 变化或数据迁移，**必须用新集群和独立存储**；数据库迁移使用空目标库并先验证备份恢复，写入切换另行评审。**代码回退不等于数据回滚。**

**3.1 应用 tag 与 Vault OIDC 检查清单。** 代码快照为 Orchestrator `main` `2e25af0f`、GitOps `main` `d9ddcf56`，后续运行须重新核对。

:::table
状态|应用制品与候选
✅|当前 selfhost 函数在 SIT/UAT 拒绝 v* 和 prod-v*，提示改用 daily-build-* 或 uat-daily-build-*
⏳|实现 SIT 正向候选校验：仅接受 Feature ID 关联的 task/issue 与制品 tag，拒绝 daily-build-*；tag 必须解析到已核对的不可变 digest（当前函数尚未实现）
⏳|定义并实现 UAT 完整正向 tag 白名单；当前没有完整白名单，未明确拒绝的格式可能通过
✅|当前函数允许 PROD 使用 v* 及部分 prod-v<数字>-* 格式；基础设施专用操作可省略应用 tag
⏳|按统一规范审查 PROD 格式，清理仅以批次名字驱动运行逻辑的专用规则；不把现状当最终规范
⏳|SIT 的 Feature ID、GitHub task/issue、制品 tag 与候选的关联校验（受信编排器侧）
:::

:::table
状态|工作流 ref 与 Vault 身份
⏳|基础仓库默认 main 的运行 ref 与各环境 Vault role 允许范围对齐；检查跨环境 ref 范围重叠，工作流 ref 不匹配时停止
⏳|Vault role 限定仓库、workflow、环境、audience 和有效期；分别验证目标身份允许访问、跨环境/相邻路径及不匹配 ref/workflow 被拒绝，记录脱敏证据
⏳|检查应用 tag、发布记录、目标环境、GitHub Environment 和 Vault role 一致，不存在静默跨环境回退
:::

:::table
状态|验收记录
⏳|保存候选指纹、各基础仓库解析的 commit SHA、工作流 ref、应用 tag、目标声明及运行回执；只读配置核对不能代替真实身份或服务验收
:::

**4. 目标、节点和 state。** GitOps 目标声明提供环境、业务、provider、account、资源 manifest、节点名与 state 身份；IaC 只消费经核对的目标并产出云事实；Playbooks 根据本次 CMDB 和声明执行通用 role。节点名由声明决定；tag 选择发布内容，不能单靠名字判断资源所有权。`prod-k3s-v6` 是当前**节点名**，`PROD-K3S-V6` 是**集群名**，它们不应成为通用代码里的条件分支。既有 state/workspace 与资源的一一对应必须保留，换发布 tag 不自动生成新 state 或替换资源；新集群和独立存储须有各自明确声明。Flux 根名和 source path 分别声明，不能推断必须等于节点名。

**5. 验证与交付边界。**

:::table
项目|状态
五仓职责与 main 默认规则|✅ 已确定；⏳ 运行时 SHA 记录与 caller 链路按实际运行验收
SIT 功能泳道候选契约|✅ 规范已确定；⏳ 与 selfhost tag 路由及 Vault 身份的端到端交接待实施验收
环境与业务发布记录|⏳ schema、owner、tag→业务映射及消费链待交付
目标与 state 通用解析|⏳ 现有代码仍含 prod-v* 特判；需 owner 实现、caller 切换与验证
PROD main 工作流 Vault 授权|⏳ 当前声明只允许 v* tag 和 release/v* 分支；修改需绑定受控身份并验证允许及跨环境拒绝
:::

关联：Case A（OS 三身份）、Case B（K3s role 依赖）、Case D（变更记录模版）；功能泳道遵循 6.12。现有状态以实际运行回执为准。

### 17.4 Case D　PROD-K3S 变更记录模版

每次动生产集群，都留一份同样结构的变更记录。下面的模版从 2026-10-30 的 PROD-K3S-V6 独立节点冷启动归档里抽出来，可以直接套用。它是**归档**，不是实时巡检：记录里的 ✅ 只说明当时有证据，不替代新节点、新批次的验收。

:::table
栏目|填什么|示例 / 约束
状态标记|✅ 已验收（附回执）· ⏳ 待验收 · ❌ 阻断 · — 不适用|只有带证据的才打 ✅
目标|这次变更要达到的唯一结果|「新建独立 V6 节点并完成 K3s 冷启动」
规划基线|依赖的 IaC/GitOps/Playbooks SHA、CMDB 节点与卷|全部写 commit SHA，不写分支名
规格|节点规格、OS、数据盘、K3s 版本、CNI|与 CMDB 声明逐项一致
证据时间|每条证据的采集时间与时区|过期证据不能拿来证明今天的状态
DNS 边界|dns_mode 与切换计划|如 dns_mode=none：本次不切流量，DNS 另走流程
节点边界|新增、保留、回收哪些节点|如：V5 保留，不因 V6 上线而回收
验收边界|哪些已验、哪些明确未验|role 回执 ≠ 业务验收；未验项列出责任人
后续|待办、回滚入口、归档全文链接|归档链接回填到任务源头
:::

**冷启动归档本身**作为这份模版的第一份实例保存在仓库文档里；本节只引用其结构，细节以归档全文为准。

**这一节怎么用。** 照抄的不是路径和 PR 号，而是三个习惯：每个 role 只做一件事并写清前置与回执；所有秘密路径按环境显式给出、缺失就停；文档里的「已合并」和「已验收」永远分两列写。

## 18 最佳实践设计参考：platform-delivery 全文收录

本章**全文收录** `ai-workspace-services/knowledge` 仓库 `docs/reference/platform-delivery/` 下的一份总体架构与五份专项参考（main @ `53492be`，2026-11-01 10:46 北京时间）。第 17 章是摘要式的 case，这里是原文：先总体架构，再专项参考 1–5。18.7–18.9 是 2026-11-08 补入的实践变化（运维看板与资产矩阵、Flux/GitOps/Flagger/Traefik 证据链、后续新增文档摘要），为改写摘要而非全文。原文标题层级已压平为本书排版，表格与代码块保持原样。

**诚实标注。** 这些文档大多是**规划草案或状态归档**：草案描述目标设计，不代表代码已实现；归档中的 ✅ 只代表当时的证据，不代表今天的线上状态，也不替代业务验收。读的时候请保持「规划 → 代码与契约验证 → 已合并 → 授权后实际交付 → 真实身份与业务验收」五档分开。

### 18.1 总体架构　OpenplatForm Delivery Architecture

来源：`knowledge/docs/reference/platform-delivery/OpenplatForm-Delivery-Architecture.md`（53492be），全文收录。

> **用途：** Open Platform 基础运行环境、多环境交付、流量治理与可观测性的总体架构。本文定义跨仓库、跨环境的协作边界；专项实现和时点状态以文末五篇参考文档为准。  >  > **状态边界：** 本文是目标架构与发布契约，不代表所有组件已部署、调谐或验收。GitOps 数量是规划基线，V6 运行事实以其状态归档顶部最新记录为准。本文变更仅为文档。

**▍1. 设计目标与原则**

平台使用同一套声明式交付模型连接基础设施、节点初始化、集群配置、业务发布与运行观测，同时保持环境和服务单元隔离。

- **声明驱动：** GitOps 提供环境、目标、依赖和非敏感版本引用；IaC 管云资源、DNS、state 和权威 CMDB；Playbooks 执行主机、集群身份、服务及数据操作；Platform-Orchestrator 管输入、授权、派发、等待与回执；Artifacts 构建和发布不可变制品。
- **职责分离：** 不在多个仓库重复实现同一资源或服务的 owner；Flux 接管 K3s 中声明的资源。Orchestrator 的交接成功不等于 Flux 调谐或业务验收成功。
- **独立晋级：** SIT、UAT、PROD 分别使用隔离的目标、凭据、数据基线和准入门禁。一个环境通过不自动放行另一个环境。
- **固定版本：** 每次运行解析并记录各基础仓库的完整 commit SHA；应用镜像和 Chart 使用经过核对的不可变 digest/版本。独立 GitRepository source pin 不因某服务更新而推进其他单元。
- **渐进变更：** 先验证，再按服务单元切换；保留原服务、数据写者和回退路径，直到对应切换另行验收。

**▍2. 基础运行环境**

**· 2.1 环境矩阵 V1.1**

下表给出三环境的 Selfhost/K3s 目标基线。UAT 也允许选择 Serverless 承载；该路径按其云服务与服务 owner 交付，不要求安装 K3s、Traefik 或 Flagger。实际组件和运行状态须由固定配置与回执证明。

:::table
层次|SIT|UAT（K3s）|PROD（K3s）
Kubernetes|K3s|K3s|K3s
GitOps|Flux CD|Flux CD|Flux CD
入口网关|Traefik|Traefik|Traefik
特性泳道|Namespace-per-Feature|不启用|不启用
发布控制|Flux + CI|Flux + Flagger|Flux + Flagger
发布模式|Feature SIT / Blue-Green|Blue-Green / Canary|Blue-Green / Canary
指标|vmagent → VictoriaMetrics|同左|同左
日志|Vector → VictoriaLogs|同左|同左
链路追踪|OTel → VictoriaTraces|同左|同左
可视化|Grafana|Grafana|Grafana
外部观测|DataKit|DataKit|DataKit
:::

主观测后端统一采用 Victoria Stack（VictoriaMetrics、VictoriaLogs、VictoriaTraces）与 Grafana。DataKit 作为观测云的独立并行采集与输出链路；按采集目标和信号去重，不重复部署第二套完整监控存储。Flagger 按服务适配情况启用，并以已验证的路由集成和新鲜指标作决策。

:::table
层|目标组件|职责边界
Infrastructure|Multi-cloud IaC、CMDB、DNS、独立 state 与存储|云资源、网络、节点和权威资源事实
OS / Runtime|Linux、containerd、K3s|Playbooks 初始化主机和集群；系统管理、业务运行与审计身份分开
GitOps control plane|Flux CD、Kustomize、HelmRelease|持续调谐已声明的集群资源与版本
Ingress|Traefik Proxy|SIT / UAT / PROD 的统一 HTTP(S) 入口；路由到集群 Service
Progressive delivery|Flagger（按需）|UAT/PROD 受控 Canary/Blue-Green 决策，不代理用户请求
Identity / secrets|Vault、External Secrets Operator、Kubernetes RBAC、TLS|短期身份、最小权限和受控 Secret 同步；GitOps 只引用非敏感信息
Database|PostgreSQL|服务独立凭据与数据边界；管理、业务读写和只读审计权限分别控制
Main observability|Grafana、VictoriaMetrics、VictoriaLogs、VictoriaTraces|主指标、日志、链路存储与查询展示
Collection|vmagent、Vector、OpenTelemetry Collector、观测云 DataKit|按信号与目标分工采集；避免同一信号无意重复采集
Delivery|GitHub Actions、Platform-Orchestrator、Artifacts|校验和编排交付、产生固定制品、汇总可追溯回执
:::

目标部署应分别声明 Traefik、Flagger、Grafana、Victoria Stack、vmagent、Vector 与 DataKit 等 HelmRelease，复用既有服务单元和 Flux 层级，不建立平行控制面。组件是否实际存在、Chart 能力和有效配置须以固定 GitOps commit 与运行证据核验。

**· 2.2 GitOps 规划基线**

现有 PROD-K3S-V6 规划为 **6 个 GitRepository、9 个 Flux Kustomization、8 个 HelmRelease**。这是目标图数量，不是一次运行的已就绪数量。历史初次引导回执为 6/6/7；V6 归档记录的新增 ESO/TLS 前置图尚不能与历史回执混作同一验收。

六个 source 共享 GitOps 仓库 URL，但各自独立 pin 配置版本；根 Kustomization 使用稳定根名 `prod-k3s`，仅管理根图并设 `wait: false`。子单元在各自 namespace 独立调谐和报告健康。HelmRelease 属于服务单元，不要求与顶层 Kustomization 一一对应。

:::table
服务单元|目标职责
`config-prod`|稳定管理根、ESO 与集群前置配置
`vault-prod-config`|Vault、TLS 身份与同步
`postgresql-prod-config`|PostgreSQL
`observability-prod-config`|Grafana、Victoria Stack 与采集器
`web-saas-prod-config`|Web SaaS 业务服务
`ingress-prod-config`|Traefik 与 Flagger
:::

当前 V6 归档仍记录 Vault 未就绪、PostgreSQL 镜像授权及 SecretStore 依赖失败、Observability 凭据/资源问题、Ingress 和业务未调谐等阻塞。以上基线只指导目标规划；发布状态须引用新的调谐与运行回执。

**▍3. 统一平台架构**

**· 总体**

:::code
# mermaid
flowchart TB
    GH["GitHub：Feature / PR / main / Release"] --> ORCH["Platform-Orchestrator：授权与编排"]
    ORCH --> IAC["IaC：云资源与 CMDB"]
    ORCH --> PB["Playbooks：主机、K3s 与服务操作"]
    GO["GitOps：目标声明与版本 pin"] --> FLUX["Flux CD：持续调谐"]
    ART["Artifacts：不可变镜像与 Chart"] -. 固定制品引用 .-> GO
    IAC --> RUNTIME["SIT / UAT / PROD 运行环境"]
    PB --> RUNTIME
    FLUX --> RUNTIME
    RUNTIME --> EDGE["Traefik 统一入口"] --> APP["业务服务"]
    FLAGGER["Flagger：按需渐进发布"] -. 流量决策 .-> EDGE
    APP -. 指标 / 日志 / 链路 .-> OBS["Grafana + Victoria Stack"]
    APP -. 并行采集 .-> DK["DataKit → 观测云"]
    OBS -. 发布指标 .-> FLAGGER
:::

总体图展示五仓协作、运行环境、入口、渐进发布与观测之间的关系。实线表示交付/调谐方向，虚线表示制品引用、观测数据或控制决策。局部图展开关键链路；业务 HTTP 流量经过 Traefik 到 Service，Flux 是配置调谐器，Flagger 是发布控制器，不是请求代理。

**· 局部 1：五仓职责与交付控制链**

:::code
# mermaid
flowchart LR
    GH["GitHub Feature / PR / Release"] --> ORCH["Platform-Orchestrator<br/>输入、授权、DAG、回执"]
    ORCH --> IAC["IaC<br/>云资源、DNS、State、CMDB"]
    ORCH --> PB["Playbooks<br/>主机、身份、K3s、服务与数据操作"]
    GO["GitOps<br/>环境目标、版本 pin、Flux 声明"] --> FLUX["Flux CD<br/>持续调谐"]
    ART["Artifacts<br/>镜像 / Chart 固定 digest"] -. 不可变制品引用 .-> GO
    IAC --> CMDB["目标资源与 CMDB 事实"] --> PB
    FLUX --> K3S["K3s 集群资源"]
    PB --> HANDOFF["主机与 Flux 交接回执"] --> FLUX
:::

IaC 是云资源和 CMDB 的 owner，Playbooks 是主机、身份、服务及数据操作的 owner，GitOps 声明集群期望状态，Flux 执行持续调谐。Orchestrator 负责授权、派发和验证各 owner 回执，不在编排层复制执行逻辑。CI 或交接成功不能替代 Flux/业务运行验收。

**· 局部 2：SIT、UAT、PROD 发布与流量链**

:::code
# mermaid
flowchart TB
    subgraph SIT["SIT：Feature 隔离"]
      FEATURE["GitHub Feature ID / PR 候选"] --> FSOURCE["Flux CD"] --> FNS["Feature Namespace"]
      FNS --> TEDGE["Traefik"] --> TE2E["E2E"]
    end
    subgraph UAT["UAT：K3s 路径；另支持 Serverless"]
      UCAND["冻结候选"] --> UFLUX["Flux CD"] --> UFLAG["Flagger（适用时）"]
      UFLAG --> UEDGE["Traefik"] --> UAPP["Primary / Canary"]
    end
    subgraph PROD["PROD：K3s"]
      RELEASE["Release + 不可变 digest"] --> PFLUX["Flux CD"] --> PFLAG["Flagger（适用时）"]
      PFLAG --> PEDGE["Traefik"] --> PAPP["Primary / Canary"]
    end
    METRICS["vmagent → VictoriaMetrics"] -. 健康 / SLO 判断 .-> UFLAG
    METRICS -. 健康 / SLO 判断 .-> PFLAG
    PFLAG -. 放量或中止决策 .-> PEDGE
:::

SIT 按 Feature ID 部署隔离 Namespace 并通过 Traefik 运行 E2E。UAT 可采用 Serverless 或 K3s；图中展开 K3s 路径。UAT/PROD 的 Flagger 根据已验证且新鲜的指标控制渐进放量，实际流量仍通过 Traefik；服务不适配时不启用 Flagger。

**· 局部 3：主观测与并行采集链**

:::code
# mermaid
flowchart LR
    APP["节点 / Kubernetes / Traefik / 应用"]
    APP -->|metrics| VMAGENT["vmagent"] --> VM["VictoriaMetrics"]
    APP -->|logs| VECTOR["Vector"] --> VL["VictoriaLogs"]
    APP -->|traces| OTEL["OpenTelemetry Collector"] --> VT["VictoriaTraces"]
    APP -. 按需并行、按信号去重 .-> DK["DataKit"] --> GUANCE["观测云"]
    VM --> GRAFANA["Grafana"]
    VL --> GRAFANA
    VT --> GRAFANA
    VM -. 发布指标查询 .-> FLAGGER["Flagger"]
:::

Victoria Stack 是主观测存储，Grafana 提供统一查询与可视化。DataKit 独立向观测云采集/输出，不经 Grafana 转发，也不重复部署另一套主存储。重复采集前先限定目标、信号、标签、过滤和采样。

**▍4. 环境与发布模型**

**· 4.1 SIT：按 Feature 隔离**

SIT 固定链路：

`GitHub Feature ID → Flux CD → Feature Namespace → Traefik → E2E`

Feature ID 关联 Issue/task、PR head 和基线 commit、制品 tag 与 digest、Chart/配置版本及数据基线。编排器核对候选与 SIT 目标后，由 Flux 部署到独立 Feature Namespace，Traefik 提供隔离路由，E2E 对该候选执行验证。Feature ref 或 CI 成功本身不构成部署授权或验收。SIT 凭据与 UAT/PROD 隔离；Feature 生命周期清理按资源清单和既定保留策略执行。

**· 4.2 UAT：两种承载模式**

UAT 可选择：

1. **Serverless：** 使用 UAT 专属身份、网络、密钥和数据基线，通过相应服务 owner 发布固定制品并验收。  2. **K3s：** 使用统一 Traefik 入口、Flux CD 声明发布和 Flagger 渐进交付。Flagger 仅在所选服务、指标和流量模型适配时启用。

同一候选和配置固定后执行验收。UAT 成功不代表生产资源、身份或数据状态相同；晋级前核对目标差异、发布记录和生产准入。

**· 4.3 PROD：受控渐进发布**

PROD 采用 `GitHub Release → Flux CD → Flagger（适用时）→ Traefik → Primary / Canary`。Traefik 提供稳定入口，Flagger 按已验证的成功率、延迟和 SLO 指标逐步推进权重；Blue/Green 或 Canary 按服务风险、路由能力及回退特性选择。若指标不可用、陈旧或查询语义未经验证，不允许自动放量。

发布记录绑定业务范围、不可变制品 digest、Chart/config 版本、源 commit、目标环境和候选指纹。生产工作流身份必须符合 Vault OIDC 环境授权；应用 tag 不改变工作流 OIDC ref。稳定版本只增不改。

回退按变更类型处理：无状态且向后兼容的应用可回到已保留制品；数据库 schema、数据、Vault Raft 和其他持久卷变更必须使用兼容策略与独立恢复方案。代码回退不等于数据回滚。

**▍5. Traefik、Flagger 与服务边界**

- Traefik 是 SIT、UAT K3s 与 PROD 的统一集群入口，负责 TLS 终止（按已声明证书方案）、Host/path 路由和 Service 负载均衡；不管理云 DNS、证书秘密源或应用发布版本。
- Flagger 控制支持服务的渐进发布，通过已声明的路由集成调整 Canary 流量并查询指标；它不接管所有服务，也不取代 Flux 的期望状态管理。
- Traefik 与 Flagger 控制器由 Ingress 服务单元管理；业务单元拥有各自 Canary/发布声明。Ingress 基础设施升级与业务发布版本独立 pin。
- 蓝绿切换需要保留旧版可用并验证路由回切；Canary 中止应将流量留在稳定版本并保留失败证据。单节点资源与容量可能导致重启窗口，不能预先承诺零停机。

**▍6. 可观测性与采集去重**

主观测由 Grafana 配合 VictoriaMetrics、VictoriaLogs、VictoriaTraces 提供；Grafana 查询主存储，不作为采集器。发布决策所需指标由 vmagent 进入 VictoriaMetrics，Flagger 查询兼容接口并在放量前验证数据新鲜度、标签和指标语义。

:::table
信号|主采集路径|主后端|DataKit 并行路径
节点、Pod、Traefik、应用指标|vmagent / 目标 exporter|VictoriaMetrics|仅在目标和指标范围明确时启用
Kubernetes 与应用日志|Vector|VictoriaLogs|按需选择采集源，避免重复全量上报
应用链路|OpenTelemetry Collector|VictoriaTraces|仅在协议、属性和采样策略核实后接入
:::

DataKit 对接观测云作为独立的并行观测通道，不由 Grafana 转发，也不要求部署第二套主存储。对同一目标或信号启用第二采集路径前，明确 owner、标签、过滤、采样、保留期和上报成本，避免重复采集及高基数膨胀。组件协议、Chart 功能和容量须按固定版本验证。

**▍7. 身份、密钥、网络与数据保护**

:::table
控制域|责任边界|最低验收要点
Linux / 主机身份|系统管理、日常操作、审计身份分开；业务进程使用独立非 root 服务账户|实际身份登录与权限验证；审计身份读授权状态、拒绝写入/提权/读取管理秘密
Vault / ESO|Vault 管理短期身份与策略；ESO 按环境和服务同步所需 Secret；GitOps 只保存非敏感引用|核对 repo/workflow/ref、role、路径和 ServiceAccount；授权路径允许、相邻路径拒绝；不在日志与回执输出秘密
Kubernetes / Flux|Flux 依据 GitOps 声明调谐；集群 operator 与 auditor 使用独立 RBAC|以真实身份检查允许/拒绝；审计身份无写、exec、Secret 读取或提权能力；记录 source 与运行版本
PostgreSQL|管理/DDL、各服务业务 DML、只读审计分离|业务凭据只获必需 schema/对象权限；审计使用授权视图并验证写入拒绝；迁移单独核对备份恢复
网络 / TLS|IaC 管云网络和 DNS；Traefik 管明确批准的业务入口；证书由受控身份与同步链路交付|检查入口 Host/path、TLS/SNI、证书链和回退路由；集群 API、数据库与管理面不公开暴露
state / 持久数据|IaC state、数据盘、PVC 和数据库数据按目标独立管理；变更 owner 保留恢复路径|核对资源/卷身份、活动写者、备份及恢复；未验证前不格式化、覆盖、重建或切换写入权
:::

表格列出跨层控制摘要；具体身份配置、K3s role 与 V6 运行证据见下方五篇专项参考文档。

- **三权分立：** 系统管理身份负责必要管理和恢复，不作为日常业务进程；每个业务使用独立的最小权限身份并渐进 rootless；审计身份由系统权限强制只读，不能依赖脚本约定或管理员 impersonation 证明。
- **Secrets：** Vault 与 ESO 通过短期、受限身份交付 Secret。GitOps 保存非敏感引用；工作流、日志、制品与回执不包含秘密值。SIT/UAT/PROD 的 Vault role、路径、Kubernetes service account 与证书按环境隔离。
- **集群访问：** Kubernetes root/operator/auditor 与 Linux OS 用户是不同的授权面。RBAC 按具体资源和动作验证允许及拒绝；审计角色不得 exec、写资源、读取 Secret 或提权。
- **数据库：** PostgreSQL 管理/DDL、业务 DML 和审计读取身份分开；业务身份只访问必需 schema 与对象，审计优先读授权视图。应用连接不得使用数据库超级权限。
- **网络：** 集群 API、数据库和 Vault 管理面走受控管理/集群网络；不因验收方便公开管理端口或数据库。Traefik 只暴露明确批准的业务入口。
- **状态数据：** 独立 IaC state、节点数据盘与 PVC 保留边界。变更或迁移前核对实际写者、备份恢复、卷身份和回退范围；不得通过重建、格式化或覆盖未确认的持久数据解决调谐失败。

**▍8. 资源容量与单节点边界**

V6 归档中的 2 vCPU / 4 GB 是选定的候选规格，**全业务栈容量验收尚未完成**。Pod requests/limits、K3s 控制面预留、镜像拉取与滚动升级峰值、PostgreSQL 连接和内存、监控保留、日志增长、磁盘空间/inode、备份与恢复余量均须汇总评估。容量不足时在对应门禁停止并提交单独规格评审；本文不自动授权扩容。

单节点故障会影响该集群，独立数据盘或单副本 Vault 不构成高可用。发布方式和恢复目标应反映该限制。

**▍9. 验收、回滚与晋级门禁**

:::table
阶段|放行证据|失败处理
候选冻结|Feature/release 关联、完整源 SHA、制品/Chart digest、配置 pin、数据基线和环境目标|候选变化时重算指纹并按影响重验
基础设施与交接|IaC/CMDB 目标唯一、state 身份核对、主机与集群身份回执、Flux 接管回执|停在失败 owner；不得据交接推断工作负载就绪
GitOps 调谐|指定 source、Kustomization、HelmRelease 的条件和实际版本|修复对应服务单元；保留其他单元 source pin
发布健康|Traefik 路由/TLS、服务健康、指标新鲜度、日志与链路路径、Flagger 判断|中止灰度、维持稳定版本，检查观测缺口
业务验收|E2E/API/业务流程、权限允许/拒绝、回归和恢复证据|记录未运行/失败，不把 CI 或只读检查记为通过
环境晋级|UAT 固定候选验收、PROD 身份/发布记录/回退准备和明确批准|不自动推进下一个环境
:::

回执区分 `success`、`failed`、`expected_skip`、`not_run` 与 `missing`，并关联环境、目标、固定 SHA、制品 digest、工作流 ref、owner 和运行 ID。不得记录秘密。运行证据必须注明核对时间；合并、CI 绿灯、GitOps 更新和控制器 Ready 分别不能替代端到端业务验收。

**▍10. V6 到目标架构的增量迁移**

V6 现况以 [PROD-K3S-V6 状态归档](PROD-K3S-V6-规划与部署状态归档.md) 最新条目为准。迁移按服务 owner 和单元推进，不重建整个集群，不同时切换所有写者。

1. **建立固定基线：** 固定 GitOps SHA、六个 source 的当前 pin、服务对象、PVC/数据盘身份、IaC state 和活动写者；收集只读现况及恢复证据。  2. **修复阻塞单元：** 依据 Vault、PostgreSQL、Observability、Ingress 和业务 owner 的实际错误逐项处理；同单元完成一项验证后再继续下一项。保持已有 K3s/Flux 与 Bound PVC，不因部署失败清理或重建。  3. **观测先行：** 在不重复安装的前提下核对现有 Observability Release。逐个验证 Grafana/Victoria 组件、vmagent/Vector/DataKit 输入输出、资源预算和持久化，再调整独立 HelmRelease。  4. **Ingress 迁移：** V6 当前路由为 Caddy 目标，未来迁往 Traefik 必须先核对 TLS Secret、Host/path、跨 namespace 后端、健康检查和回退路由。先以 V6 专属域名/隔离入口验证 Traefik，后逐服务切换；SNI、证书链、API/E2E 和可恢复路径通过后才扩大。  5. **Flagger 验证：** 仅为适配的无状态服务启用；先验证指标与路由权重行为、自动中止及稳定版本回切。持久服务单独评审。  6. **晋级与切换：** 保持原服务和 writer 可用。每服务独立完成发布候选、业务回归、数据一致性和恢复验收；DNS、流量及写入权切换各自遵循其 owner 与独立授权。  7. **结束条件：** 目标版本在固定观察窗口内稳定，回执关联到确切版本和身份；未完成项目明确标为未验收。旧服务或写者只有在用户明确确认最终切换并完成恢复证据后再退役。

本迁移路线是文档计划，不触发任何集群、DNS、数据库或生产变更。

**▍11. 专项参考文档**

以下五篇是本目录现有实施细节和时点证据的权威来源。本总体文档仅引用其边界和结论，不复制流水线、身份、K3s role、发布解析或节点部署细节。

1. [环境与业务发布解析：最小实施草案](环境与业务发布解析-最小实施草案.md) — 五仓职责、候选/tag 与环境、Vault OIDC、目标/state 解析和发布验收缺口。  2. [GitHub Actions 流水线实施草案](GitHub-Actions流水线实施草案.md) — 编排职责、workflow DAG、owner 调用迁移、逐目标回执和 CI 边界。  3. [Linux OS 三类操作身份：最小实施草案](Linux-OS三类操作身份-最小实施草案.md) — Linux 管理、运行操作、审计身份和 OS 验收约束。  4. [K3s role 职责与依赖清单](K3s-role职责与依赖清单.md) — K3s bootstrap、Flux 交接、RBAC、role owner 与当前验收缺口。  5. [PROD-K3S-V6 独立节点、集群冷启动规划与部署状态归档](PROD-K3S-V6-规划与部署状态归档.md) — V6 节点、容量、GitOps 目标图及最新部署实况。

### 18.2 专项参考 1　环境与业务发布解析：最小实施草案

来源：`knowledge/docs/reference/platform-delivery/环境与业务发布解析-最小实施草案.md`（53492be），全文收录。

> 状态：目标草案，2026-10-31。本文描述期望契约；现有工作流尚未全部实现，不作为部署或验收回执。

**▍1. 目标与职责**

基础仓库默认选择 `main`，运行时各自解析一次 commit SHA 并传递给下游；业务发布记录固定制品版本和 digest。业务发布 tag、工作流运行 ref、节点名和 state 身份是独立字段，不因相同字符串自动绑定。

:::table
仓库|职责|tag / 版本引用
GitOps|环境、业务目标、资源、身份目标和 Flux 声明；保存非敏感引用|默认 `main`，本次运行记录解析出的 commit SHA；可按需显式选择 tag
IaC|云资源、DNS、state、云事实及 CMDB|默认 `main`，本次运行记录解析出的 commit SHA；可按需显式选择 tag
Playbooks|主机、K3s、身份、服务、数据库、备份恢复和迁移执行|默认 `main`，本次运行记录解析出的 commit SHA；可按需显式选择 tag
Platform-Orchestrator|输入、授权、DAG、派发、等待及回执汇总|默认 `main`，记录本次工作流 commit SHA；运行 ref 的 Vault OIDC 授权单独校验
Artifacts|构建、镜像、Chart、制品打包与发布|构建配置默认 `main` 并记录 commit SHA；业务制品使用发布 tag 和核对后的不可变 digest
:::

**▍2. 发布解析链**

:::code
# mermaid
flowchart TD
    A["选择不可变发布 tag"] --> B["解析发布记录：环境、业务、制品版本"]
    B --> C["校验工作流 ref 与 Vault role"]
    B --> D["在固定 GitOps commit 中选择目标声明"]
    D --> E["IaC 读取目标、节点及既有 state 身份"]
    E --> F["IaC 输出 CMDB"]
    F --> G["Playbooks 消费 CMDB 与 GitOps 配置"]
    G --> H["初始化 OS、K3s 与 Flux"]
    H --> I["Flux 按声明部署业务"]
:::

1. **发布 tag**：解析出环境、业务范围及 chart/镜像版本或 digest。现有 PROD Vault role 接受工作流 `v*` tag / `release/v*` 分支；优先使用不可变 tag。基础仓库默认 `main` 的授权差异见下方检查清单。  2. **环境与业务**：解析结果形成不可变运行记录；dispatch 输入若提供环境或业务，只用于一致性校验，冲突时停止。  3. **GitOps 目标声明**：使用环境、业务、provider、account 和声明中的目标标识查找唯一目标；未找到或匹配多个目标时停止。  4. **IaC**：消费声明中的资源路径、workspace 和 state key，输出节点名、地址及数据盘等 CMDB 事实；tag 不直接拼接 state key。  5. **Playbooks/K3s**：使用本次解析的 GitOps commit 和 IaC CMDB，从声明读取节点名、K3s 配置和 Flux root/path，不按 `prod-v6` 分支判断。  6. **Flux**：接管声明中的 source、Kustomization 和 HelmRelease，使用发布记录明确的业务制品版本。

`v*` tag 可表明 PROD 发布类别，但 tag 字符串本身不能唯一确定 `web-saas` 和 GitOps 目标。需补充可审阅的发布记录，将 tag 关联到环境、业务和制品，再由 GitOps 声明确定节点及 state。发布记录包含来源仓库/commit、镜像 digest、Chart 版本或 digest、配置版本及候选指纹；其 owner、schema 与消费方式仍待实现。基础仓库无需同步创建同名 tag。

**▍3. SIT、UAT、PROD**

:::table
环境|目标发布规则|当前 Vault role ref 声明（GitOps main `d9ddcf56`）|待统一
SIT|仅接受 Feature ID 关联的 GitHub task/issue 和制品 tag；固定关联 PR head、基础分支 SHA、完整构件和数据基线，部署独立 SIT namespace；排除 `daily-build-*`|`refs/pull/*/merge`、`refs/heads/*`|受信任编排器校验 task/issue、feature、制品 tag、仓库、workflow、候选、目标及 SIT 角色；ref 本身不代表部署授权
UAT|默认使用合并后的固定候选；明确选择合并前 UAT 时使用冻结候选。候选或配置变化按影响重验|现状：`refs/heads/main`、`refs/heads/release/*`、`refs/heads/bugfix/*`、`refs/heads/daily-build-*`、`refs/tags/daily-build-*`|目标：排除 `refs/heads/release/*`；保留 `refs/heads/main`、`refs/heads/bugfix/*`、`refs/heads/daily-build-*`、`refs/tags/daily-build-*`。Vault role 与调用链尚待修改和验收
PROD|业务使用经审查的不可变版本或 digest，tag 关联明确业务与目标；状态变更按独立集群方案|`refs/tags/v*`、`refs/heads/release/v*`|基础工作流默认 `main` 与现有 PROD role ref 不一致；需在受审查的认证契约中解决并做允许/拒绝验收
:::

默认流程为 **PR → SIT → 合并 → UAT → PROD 受控滚动升级**；用户明确选择时可采用合并前 UAT。UAT 验收通过后，核对发布记录、业务范围、不可变制品和生产目标，按已有授权与发布门禁进入 PROD；部署后验证实际运行版本和关键业务流程。候选、配置或数据基线变化时按影响重新验收。CI 成功不是运行验收；SIT/UAT 与生产凭据隔离，公共证书等共享来源须逐项审查授权。

PROD 滚动方式按变更类型选择：纯展示的无状态 UI 和向后兼容、无需 SQL schema 变更的小型 API 修复可在所属单元原地滚动，保留旧制品并验证回退路径。PostgreSQL、Vault Raft、监控存储及其他持久卷工作负载的版本验证，以及 SQL schema 版本变化或数据迁移，必须使用新集群和独立存储；数据库迁移使用空目标库并先验证备份恢复，写入切换另行评审。代码回退不等于数据回滚。

**· 3.1 应用 tag 与 Vault OIDC 检查清单**

以下勾选表示对应事实已从当前声明或代码核对；未勾选项仍需实施或取得真实验收证据。代码快照为 Orchestrator `main` `2e25af0f`、GitOps `main` `d9ddcf56`，后续运行须重新核对。

**应用制品与候选**

- [x] 当前 selfhost 函数在 SIT/UAT 拒绝 `v*` 和 `prod-v*`，提示使用 `daily-build-*` 或 `uat-daily-build-*`。
- [ ] 实现 SIT 正向候选校验：仅接受 Feature ID 关联的 GitHub task/issue 与制品 tag，拒绝 `daily-build-*`；tag 必须解析到已核对的不可变制品 digest。当前函数尚未实现此规则。
- [ ] 定义并实现 UAT 完整的正向 tag 白名单；当前函数没有完整白名单，其他未明确拒绝的格式可能通过。
- [x] 当前函数允许 PROD 使用 `v*` 及部分 `prod-v<数字>-*` 格式；基础设施专用操作可省略应用 tag。
- [ ] 按统一规范审查 PROD 格式，清理仅以批次名字驱动运行逻辑的专用规则；不得把现状当作最终规范。
- [ ] SIT 的 Feature ID、GitHub task/issue、制品 tag、PR/head SHA、目标分支基线、镜像 digest、Chart/配置和数据基线形成完整候选；受信任编排器核实关联、候选和目标，tag 不替代候选清单。
- [ ] UAT/PROD 核对发布记录与业务范围、制品版本/digest 一致；工作流输入与发布记录冲突时停止。

**工作流 ref 与 Vault 身份**

- [x] 区分 Vault OIDC 的 `ref`（实际工作流运行 ref）和应用 `deploy_tag`（应用制品版本）；输入的 `deploy_tag` 不会改变 OIDC `ref` claim。
- [x] 现有 PROD role 只允许 `refs/tags/v*` 和 `refs/heads/release/v*`；`release/v*` 是可变化分支，tag 的不可变性需由仓库保护和发布流程保障。
- [ ] 统一五仓默认 `main` 与环境授权契约。当前 prod role 不接受 `refs/heads/main`，不能仅靠选择 PROD 应用 tag 获得该身份。
- [ ] UAT role 排除 `refs/heads/release/*`，仅保留 `refs/heads/main`、`refs/heads/bugfix/*`、`refs/heads/daily-build-*` 和 `refs/tags/daily-build-*`；核对所有调用方并验证允许与拒绝。
- [ ] 明确 SIT/UAT ref 优先级，处理 SIT `refs/heads/*` 与其他环境分支范围的重叠；工作流 ref 不匹配时停止。
- [ ] Vault role 限定仓库、workflow、环境、audience 和有效期；分别验证目标身份允许访问、跨环境/相邻路径及不匹配 ref/workflow 被拒绝，记录脱敏证据。
- [ ] 检查应用 tag、发布记录、目标环境、GitHub Environment 和 Vault role 一致，且不存在静默跨环境回退。

**验收记录**

- [ ] 保存候选指纹、各基础仓库解析的 commit SHA、工作流 ref、应用 tag、目标声明及运行回执；只读配置核对不能代替真实身份或服务验收。

**▍4. 目标、节点和 state**

GitOps 目标声明提供环境、业务、provider、account、资源 manifest、节点名与 state 身份；IaC 只消费经核对的目标并产出云事实。Playbooks 根据本次 CMDB 和声明执行通用 role。节点名由声明决定；tag 选择发布内容，不能单靠名字判断资源所有权。

`prod-k3s-v6` 是当前节点实际名称，`PROD-K3S-V6` 是集群名称；它们不应成为通用代码中的条件分支。既有 state/workspace 与资源的一一对应必须保留，变更发布 tag 不自动生成新 state 或替换资源；新集群和独立存储须有各自明确声明。Flux 根名和 source path 分别声明，不能推断必须等于节点名。

**▍5. 验证与交付边界**

:::table
项目|状态
五仓职责与 main 默认规则|✅ 已确定；运行时 SHA 记录与 caller 链路需按实际运行验收
SIT 功能泳道候选契约|✅ 规范已确定；与 selfhost tag 路由及 Vault 身份的端到端交接待实施验收
环境与业务发布记录|❌ schema、owner、tag 到业务的映射及消费链待交付
目标与 state 通用解析|❌ 现有代码仍含 `prod-v*` 特判；需 owner 实现、caller 切换与验证
PROD `main` 工作流 Vault 授权|❌ 当前声明只允许 `v*` tag 和 `release/v*` 分支；修改需绑定受控身份并验证允许及跨环境拒绝
:::

关联文档：[V6 冷启动规划与部署状态归档](PROD-K3S-V6-规划与部署状态归档.md)；[Linux OS 三类操作身份](Linux-OS三类操作身份-最小实施草案.md)；[K3s role 职责与依赖清单](K3s-role职责与依赖清单.md)。功能泳道遵循 `feature-lane-release-workflow`；现有状态以实际运行回执为准。

### 18.3 专项参考 2　GitHub Actions 流水线实施草案

来源：`knowledge/docs/reference/platform-delivery/GitHub-Actions流水线实施草案.md`（53492be），全文收录。

状态：规划草案；未经代码实现、部署或生产验收。基线：2026-10-31 核对的 Platform-Orchestrator `main`；具体提交与运行证据以每次实施记录为准。

**▍顶部概览：当前主要派发关系**

当前经代码核实的主要派发关系：

:::code
# mermaid
flowchart TD
    D[Daily Snapshot] -->|按环境及部署条件| S[Selfhost Orchestrator]
    D -->|按环境及部署条件| V[Serverless Orchestrator]
    H[Hybrid Orchestrator] -->|目标矩阵条件| S
    H -->|目标矩阵条件| V
    H -->|目标矩阵条件| X[XConnect / 既有节点入口]
    S --> SF[Selfhost Infra 阶段]
    SF -->|需要 IaC 且非 existing host| I[IaC Orchestrator]
    I --> M[IaC 多云阶段 reusable workflow]
    V -->|直接 uses| IA[IaC Actions]
:::

该图反映已核实的调用方向；下文层级缩进用于职责分组，不表示现有串行父子关系。

**▍1. 目标与范围**

保留五个顶级父流水线的文件、入口、输入以及现有 job 和 `needs` 链，按单一职责彻底重构其子流水线及共享实现。允许调整父流水线各 job 内的 steps、action 引用和参数交接，以消除适合抽取的内嵌逻辑。子流水线负责授权、目标矩阵、调用 owner、等待回执及汇总；资源和服务执行属于对应 owner。部署以 GitOps 声明和 IaC CMDB 为依据；K3s 交接后由 Flux 调谐，通知由 Flux 自身处理。

父流水线的 job 标识、`needs` 关系及现有入口契约保持不变；在此边界内可以修改 job 内部。重复的输入校验、派发关联和回执验证等控制逻辑，优先复用受测试的共享 action；云资源、主机、服务及数据执行迁至对应 owner。父流水线保留必要的审批、授权、阶段选择和结果汇总。迁移前核对实际调用方、权限与输出契约，迁移后验证行为与失败传播，不为减少代码而弱化门禁或改变 operation 语义。

:::table
保留的父流水线|当前 job 数|静态最长链|职责
`hybrid-orchestrator.yml`|5|5|混合环境目标选择和跨入口调度
`selfhost-orchestrator.yml`|5|5|Selfhost 全流程调度
`iac-orchestrator.yml`|8|5|IaC 阶段、目标矩阵和回执汇总
`serverless-orchestrator.yml`|6|5|Serverless 交付调度
`daily-main-snapshot.yaml`|5|5|快照构建和环境派发
:::

job 数按静态定义统计，矩阵副本不另计；最长链按同一 workflow 的静态 `needs` 计算，不把跨 workflow 等待相加。运行时实际 job 数随条件和矩阵变化。

**▍2. 职责与约束**

:::table
仓库|职责
Platform-Orchestrator|输入、授权、DAG、目标矩阵、派发、等待、回执校验和汇总
IaC|云资源、DNS、State、云事实与权威 CMDB
GitOps|环境、业务目标、资源、权限目标、版本引用和 Flux 声明；不存秘密值或执行器
Artifacts|构建、镜像、Chart、制品打包和发布
Playbooks|主机、服务、身份、数据库、备份恢复、迁移及健康检查
:::

- 每个子 workflow 只聚焦一项核心能力；同类目标使用矩阵，环境、provider、账号和部署模式由声明及参数决定，不根据节点名或批次推断。
- 每个 workflow 静态 `needs` 最长链目标为 3 层，硬上限 5 层。矩阵副本算同一层；禁止通过删除权限、依赖或失败传播压缩图。
- YAML 负责声明调用、权限、参数与依赖，避免内嵌非平凡 shell/Python。优先复用现有可测试 action 或 owner 入口；简单任务优先 shell、YAML，复杂逻辑放在职责归属明确且有测试的实现中。不能把执行代码换名藏进 orchestration action。
- 基础仓库默认选择 `main`，每次运行解析并记录一次完整 SHA，下游消费同一结果；调用所需的受信任机制应遵循现有授权。业务镜像、Chart 独立固定不可变版本或 digest。
- 凭据经受控短期身份取得，不写入声明、日志或回执；保留 OS、Kubernetes 和数据库三类身份的独立边界。
- 有状态组件、SQL schema 变更和数据迁移遵循新集群、备份恢复与单独迁移评审；数据盘不因重构格式化、重建或覆盖。只读验证不得伪装成业务验收。

**▍3. 通用子流水线能力**

能力名称是规划，不意味着新增同名文件。实施前先盘点并复用现有入口和调用方。

:::table
能力|唯一核心功能|调用范围|owner
目标解析|校验输入，匹配唯一 GitOps 目标并固定本次版本|Selfhost、Hybrid、Serverless、IaC|GitOps 提供声明；Orchestrator 校验
云资源交付|对选定目标执行 IaC，产出资源回执与 CMDB|Selfhost、Hybrid、IaC|IaC
主机与 K3s 交接|完成节点基础初始化和 Flux 交接|Selfhost、需要同类节点的入口|Playbooks
原生主机服务交付|按声明的目标和服务调用主机服务 owner|Selfhost、Hybrid|Playbooks
Agent Proxy 交付|使用统一目标接口交付 IaC 与已有节点|Selfhost、Hybrid|Playbooks；IaC 提供云事实
Serverless 资源交付|对声明目标交付云资源|Serverless、Hybrid|IaC
Serverless 服务交付|使用固定制品交付服务|Serverless、Hybrid|对应服务执行 owner；Artifacts 提供制品
数据操作|按明确 operation 调用初始化或迁移执行|Selfhost、Hybrid、Serverless|Playbooks
DNS 操作|按明确授权和目标变更 DNS|Selfhost、Hybrid、Serverless|IaC
制品构建发布|构建与发布组件及不可变制品|Daily Snapshot|Artifacts
回执汇总|核验已完成的 owner 回执、覆盖及失败|各入口|Orchestrator
:::

建议子 workflow 的一般结构：

:::code
resolve / authorize → execute（目标矩阵，调用 owner）→ report（汇总回执）
:::

特殊权限或审批需要独立 job 时可调整层数，不能超过 5。复用通过参数、规范化契约和声明完成，不以复制工作流或相同脚本改名实现。

**▍4. Selfhost Deploy 目标**

`selfhost-stage-deploy.yml` 当前基线为 15 个 job、最长 9 层；目标：

:::code
provision：父运行与输入授权、CMDB 和 GitOps/owner SHA 校验、目标矩阵
  → deploy_base：逐目标调用 Playbooks owner，输出逐步骤回执
  → stage-output：核对覆盖、身份、版本及交接结果
:::

Playbooks 负责 common（主机名、三账户/组、主机基线及独立数据盘）、K3s 控制面、三身份和 Flux 交接。 三身份目标顺序为：master 生成并验证三套独立证书和私有 kubeconfig → 向各 OS 账户交付并验证实际身份/RBAC → 使用受控身份归档 Vault KV → 汇总回执。Vault 归档失败时整体身份验收失败，不能产生成功回执；CA 私钥保留在 master。该顺序的实现目前仅在 Playbooks 分支 `fix/k3s-existing-flux-preflight` 的提交 `e61245df`、`8e9f64ae` 中，尚未进入 main，也尚未线上执行。顺序及依赖保留在 Playbooks；回执须能区分每项结果。交接完成表示身份及配置就绪、Flux 已配置消费指定声明；不表示业务调谐或验收完成。部署流水线不更新 GitOps 应用 tag，不等待业务调谐，不执行接口或数据库业务验收；Flux 通知由 Flux 自身负责。

从该子流水线移除 `capture_web_saas_baseline`、`update_gitops_tags`、`initialize_empty_web_saas`、`deploy_web_saas`、`accept_web_saas_upgrade`、`deploy_agent_proxy_non_iac`、`deploy_monitor_agent` 以及其专属依赖、输出和测试引用，不得改名隐藏。其他原生服务、Agent Proxy 和 XConnect 调用先核对目标及现有消费者，替代 owner 路径完成后再退出本流水线；共享实现仍有其他 caller 时只移除此调用。对无法承接的目标明确失败，不得静默跳过。

当前节点可能已有活跃 Flux 与持久卷。重试需先依据权威事实辨别首次交接与已有集群，核验节点、卷及 source/root 身份并提供安全幂等路径；不得暂停或重置活跃资源来绕过保护。

**▍5. 消除不可复用与重叠**

:::table
现状|目标|验证要求
环境与 provider 分支嵌入入口|根据 GitOps schema 匹配唯一目标、provider、账号、模式和 state 身份；无法选择或多重匹配即失败|跨 SIT/UAT/PROD、provider 和批次的正负用例；不弱化已有授权或资源保护
IaC / 既有 Agent Proxy 分别组织 inventory、凭据和执行|共用一个 Playbooks owner；区别以声明中的目标来源和受控凭据表达|验证实际目标集合、SSH 身份、凭据及同一目标不重复执行
空库和 XConnect 固定目标、仓库、workflow 或域名|声明或明确参数提供目标与资源标识|缺参、冲突、错环境及超范围均失败；空库操作须验证目标为空
owner 使用固定 SHA 与 `@main` 混杂|入口选择 ref、默认 main，运行解析 SHA 并贯通调用和回执|变更 ref 后的快照一致性、不能回退到浮动分支；核对 GitHub Actions 对动态 reusable workflow 的限制，采用可审查的 checkout/local action 或受控派发
Orchestrator 内直接执行 Ansible、监控和服务|执行迁回 Playbooks，云资源/DNS 迁回 IaC，调用端只传参与验证回执|owner → caller → 调用演练 → 删除旧副本；不把脚本原样复制认定为重构
监控和 Agent Proxy 多处部署|梳理实际目标集合及职责，确认是否同节点重复|先验证 IaC 与既有节点的集合和有效运行配置，再去重
:::

**▍6. Operation 契约**

:::table
operation|原有语义|重构约束
`plan`|校验|不触发生产变更
`infra`|基础设施|只调用云资源 owner
`deploy`|全新环境的基础设施创建 + 首次部署|K3s 交接 Flux，原生服务调用对应 owner；失败重试须识别已创建资源并安全幂等，不自动重建或迁移数据
`deploy+init`|空库初始化 + 部署|显式空库检查和数据 owner 操作不得丢失
`deploy+migrate`|部署 + 迁移|显式迁移流程与授权不得丢失
`upgrade`|已部署业务或环境的受控升级|UI 和向后兼容且不变更 SQL schema 的 API 可按声明原地滚动；数据库版本、SQL schema、Vault Raft、监控存储及其他持久卷工作负载须在独立新集群验证与转换；数据迁移和流量切换另行明确授权
`migrate`|仅迁移|不附带部署或 DNS
`destroy`|销毁|保留独立保护、范围校验与授权
:::

组合 operation 可由既有父入口按已授权的顺序组合多个单一能力；不得以拆分之名吞掉某一步，也不得把业务验收隐藏进 Flux 交接。`upgrade` 是新增的目标契约，当前工作流尚未实现该选项，不得将文档定义当作已经支持。首次 `deploy` 的重试不能通过覆盖已有 state、重建节点或格式化已有数据盘实现；发现已有资源与期望不一致时停止并核对。

**▍7. 逐目标回执与失败传播**

回执至少包含 schema 版本、环境、目标 ID、host/实例身份、来源 CMDB 摘要及关联 run、GitOps SHA、owner SHA、父子运行 ID 和 attempt、各步骤状态、Flux 交接结果及时间。状态至少区分 `success`、`failed`、`expected_skip`、`not_run`、`missing`；仅在已验证相应证据后记录成功，不记录秘密。Flux 调谐与业务验收单独记录，不由交接推断。

矩阵目标清单来自已核验的 IaC CMDB 与 GitOps 声明；空目标、重复目标、目标不一致或声明不唯一失败。每目标产生独立 artifact，不能依赖矩阵 job 单个 output 表示所有 host。汇总需核对预期目标集合、唯一性、版本和关联身份；必需项失败或回执缺失使阶段失败。执行被取消、runner 异常或未生成回执时，明确为未运行或缺失，不能伪造成功。

**▍8. 测试与切换顺序**

1. **盘点调用方**：固定 main 基线，记录每条 workflow、action、脚本、触发条件、调用者、输入输出、权限和目标；盘点直接及间接引用。  2. **owner 先行**：补齐参数化 owner 接口与回执，分别提交 owner PR；单独验证幂等、数据保护及授权，保留旧路径和回滚点。  3. **接通 caller**：基于合入的 owner 引用接通可复用子流水线；在隔离环境和无副作用演练验证目标、凭据范围、回执关联与失败传播。  在保持五个父流水线 job 与 `needs` 不变的前提下，同步将父 job 中可复用的内嵌控制步骤替换为共享 action，将资源执行改为调用对应 owner；保留既有审批、条件和输出契约。  4. **删除旧路径**：验证调用链后删除被替代的本流水线 job、执行脚本及专属条件、输出和测试；共享实现有其他使用者则保留。  5. **收敛深度**：运行全 workflow 深度门禁。子流水线实测达到 5 层以内后，删除对应历史例外，不放宽门禁。

最少覆盖：空目标、重复目标、环境或目标不匹配、CMDB/声明/owner SHA 不一致、无权限、owner 失败、部分矩阵失败、预期跳过、未运行、缺回执、跨运行重放、业务制品不存在及幂等重试。数据盘使用隔离样本测试，不在验证中格式化已有盘。保留 operation 组合的调用语义测试，跨仓分别报告 CI 证据。

运行状态分开报告：**规划 → 代码与契约验证 → 已合并 → 授权后的实际交付 → 真实身份与业务验收**。CI 通过或 Flux 交接回执均不能替代线上验收。部署、迁移和 DNS 操作沿用各自授权；本草案不授权执行。

**▍9. 关联文档**

- [环境与业务发布解析：最小实施草案](环境与业务发布解析-最小实施草案.md)
- [Linux OS 三类操作身份：最小实施草案](Linux-OS三类操作身份-最小实施草案.md)
- [K3s role 职责与依赖清单](K3s-role职责与依赖清单.md)
- [PROD-K3S-V6 独立节点、集群冷启动规划与部署状态归档](PROD-K3S-V6-规划与部署状态归档.md)

**▍10. 当前调用清单与统计基线**

以下为 2026-10-31 对 Platform-Orchestrator `main` `68f00eb1997d982bbd4430627cdafefad4416046` 的静态盘点，用于迁移前追踪，不是实际运行成功的证据。统计范围为五个父入口、五个 Selfhost 阶段子 workflow 及 `iac-pipeline-multi-cloud-stages.yaml`，共 11 个文件。共 **286 处 `uses` 引用、50 个不同完整引用字符串**；同一 action 的不同版本分别计算，不包含脚本内部派发的 workflow，也不是全仓或所有递归子链的完整统计。

:::table
范围|`uses` 引用次数|不同完整引用数
`hybrid-orchestrator.yml`|9|3
`selfhost-orchestrator.yml`|10|2
`iac-orchestrator.yml`|23|10
`serverless-orchestrator.yml`|24|12
`daily-main-snapshot.yaml`|25|6
`selfhost-stage-resolve.yml`|61|16
`selfhost-stage-infra.yml`|12|7
`selfhost-stage-deploy.yml`|59|19
`selfhost-stage-migrate.yml`|15|6
`selfhost-stage-verify.yml`|12|4
`iac-pipeline-multi-cloud-stages.yaml`|36|9
:::

**· 10.1 Actions 与 workflow 名称**

:::table
类别|当前引用名称（省略版本；各文件实际版本应单独核验）
GitHub 官方 Actions|`actions/checkout`、`actions/upload-artifact`、`actions/download-artifact`、`actions/cache`、`actions/create-github-app-token`、`actions/setup-node`
第三方 Actions|`hashicorp/vault-action`、`google-github-actions/auth`、`google-github-actions/setup-gcloud`、`docker/setup-buildx-action`
Orchestrator 本地 Actions|`gitops-yaml-json`、`dev-bootstrap-handoff`、`serverless-runtime`、`setup-yq`、`prod-selfhost-control`、`configure-gcp-oidc`
IaC Actions|`iac-legacy-inputs`、`iac-targets`、`iac-self-check`、`iac-summary`、`iac-receipt-verify`、`iac-caller-targets`、`iac-caller-inventory`、`iac-stage-context`、`iac-bootstrap`、`iac-account`、`iac-resources`、`iac-cleanup`、`iac-receipt`、`gitops-gcp-target`、`cloud-run-serving-facts`、`prod-selfhost-access`、`platform-resource-operations`
Playbooks Actions|`k3s-bootstrap`、`setup-deployment-runner`、`caddy-certificate-restore`、`non-iac-agent-proxy-inventory`、`prod-native-standby`、`prod-native-init`、`prod-native-billing-upgrade`、`prod-full-business`、`prod-availability`、`service-probes`
Playbooks reusable workflows|`web-saas-domain-cd.yaml`、`open-platform-domain-cd.yaml`、`ai-workspace-domain-cd.yaml`
:::

`k3s-handover-receipt` owner 已在 Playbooks 合入；Orchestrator 接入候选位于 [PR #1594](https://github.com/ai-workspace-infra/Platform-Orchestrator/pull/1594)，本统计基线尚未包含该调用。重构前应再次核对合入状态和引用版本。

**· 10.2 Playbooks 入口及 role**

:::table
层|名称|范围
Selfhost 相关入口|`k3s_platform_bootstrap.yml`、`bootstrap-node.sh`、`setup-agent-proxy-domain.yml`、`deploy_observability_agent.yml`|直接引用或通过 K3s owner action 调用的已核对入口；不是全部间接 playbook 清单
K3s 主线 roles|`vhosts/common`、`web_saas_data_volume`、`vhosts/k3s_platform_bootstrap`、`vhosts/k3s-cluster-server`、`vhosts/helm_cli`、`vhosts/flux_controllers`、`vhosts/flux_gitops`、`vhosts/k3s_identity`|依据 K3s bootstrap 入口及 role 编排静态核对；运行是否执行取决于目标和条件
:::

**· 10.3 IaC 模块**

Akamai 模块族包括 `compute`、`compute_protected`、`storage`、`storage_protected`、`vpc`。V6 的 Akamai 模板按节点声明生成 `compute_<host>` 和 `volume_<host>`，并在声明要求时生成防火墙等资源；普通或 protected 变体及实际实例以该次渲染结果和 IaC 回执核验，不能从模块目录存在推断全部执行。

后续实施须补全 Hybrid、Serverless、Daily Snapshot 脚本派发和各 owner 内部递归调用的清单，并记录引用版本、输入输出、调用条件及实际消费者。新的静态基线不能覆盖历史运行证据。

**▍11. 五个顶级入口的层级与实际关联**

下面按需求给出的顺序组织统计。这个树是**职责分组视图**，缩进本身不表示已存在父子派发；实际调用方向见后表。

:::code
daily-main-snapshot.yaml           制品快照与选择环境派发
  iac-orchestrator.yml             云资源交付与 CMDB
    hybrid-orchestrator.yml        混合环境目标编排
      selfhost-orchestrator.yml     主机/K3s 交付编排
      serverless-orchestrator.yml   Serverless 交付编排
:::

:::table
分组中的入口|静态 job / 最长链|本次审计范围内 `uses` 次数 / 不同引用|当前关联
`daily-main-snapshot.yaml`|5 / 5|25 / 6|选择部署时，SIT/UAT 可派发 Serverless、PROD 可派发 Selfhost；并不直接派发 IaC 或 Hybrid
`iac-orchestrator.yml`|8 / 5|23 / 10|调用 IaC 多云 reusable workflow；可由 Selfhost Infra 子流水线派发
`hybrid-orchestrator.yml`|5 / 5|9 / 3|按声明目标派发 Selfhost、Serverless 等入口；未发现由 IaC 作为父入口派发 Hybrid
`selfhost-orchestrator.yml`|5 / 5|10 / 2|派发五个 Selfhost 阶段；Infra 阶段按条件派发 IaC
`serverless-orchestrator.yml`|6 / 5|24 / 12|消费 IaC Actions；数据阶段可派发数据操作 workflow；未据此认定调用 IaC Orchestrator
:::

统计为本节基线的静态文件引用；不同版本算不同完整引用，条件跳过和矩阵展开不影响上述静态数值。各子 workflow、action 内部的递归引用未全部计入。

因此，**现状不是 Daily → IaC → Hybrid → Selfhost/Serverless 的串行父子链**；特别是现有 Selfhost 的 Infra 阶段调用 IaC，方向与分组缩进相反。若未来要使 IaC 成为 Hybrid 的上层调用者，必须先单独设计无循环的职责和调用切换，不能在保持现有父流水线 job 与 `needs` 不变的前提下假定已实现。保持当前父入口的方案是将 IaC 作为可复用资源交付能力，由声明驱动的目标入口按需调用。

### 18.4 专项参考 3　Linux OS 三类操作身份：最小实施草案

来源：`knowledge/docs/reference/platform-delivery/Linux-OS三类操作身份-最小实施草案.md`（53492be），全文收录。

> 来源：Playbooks `main` commit `7b7f44164ef1429dc86c01582393e704257ac386` 的 `roles/vhosts/common/three-role-design.md`；此为归档副本，运行状态需以最新回执为准。

状态：OS 账户设计已收敛；`os_identity.yml` 和独立入口已实现，部署和真实账户验收以运行回执为准。

**▍1. 职责边界**

`vhosts/common` 仅负责 Linux OS 基线：主机名与身份检查、用户/组、SSH 公钥授权、受控 sudo、目录与文件权限，以及 OS 侧允许/拒绝验收。

所有 Linux 节点采用同一套用户名，不因是否安装 Kubernetes 而改变。

- K3s/K8s 的认证主体、kubeconfig、RBAC 和集群权限验收由对应集群 role 实现。
- Linux OS 用户与 Kubernetes 主体的映射、各自 kubeconfig 的生成/交付，以及指定用户的默认 `~/.kube/config` 均由 K3s role 实现；`k3s_platform_bootstrap` 只编排对应子 role。common 不写入 kubeconfig，也不授予集群权限。
- 数据迁移及数据库连接授权由对应迁移/数据库 role 实现，调用方显式选择执行角色。
- Docker 安装和运行配置由对应运行时 role 实现；common 仅负责 OS 账户和权限边界。

上述专业 role 消费 common 已建立的 OS 用户，不在 common 中创建集群凭据、数据库角色或迁移连接。

**▍2. 统一用户名与 SSH 登录**

:::table
Linux 用户|固定角色|OS 职责与权限
`root`|系统管理|保留现有 root；用于初始化、安装、恢复和必要管理，平时不用作业务进程身份
`operator`|日常运行操作|通用操作账户，可 SSH 公钥登录并使用交互 shell；操作被授权的服务和工作目录，通过受控 sudo 执行必要运行操作
`auditor`|只读审计与分析|可 SSH 公钥登录；读取授权系统状态及脱敏输出；无通用 sudo、系统配置写权限、运行时 socket 或管理凭据访问权限
:::

三者通过受信管理网络使用独立公钥/证书授权，禁用密码认证；root 使用 `PermitRootLogin prohibit-password`。保留现有管理入口直至新身份登录及权限验收通过；先验证 sshd 配置，再 reload。密码锁定与公钥登录须在实际 OS/PAM 配置下验证。

`auditor` 的只读针对系统配置和业务状态，允许在自己的受控工作目录保存报告或授权导出文件。不能仅凭用户名、默认无 sudo 或脚本自律认定只读；需检查有效组、文件权限、ACL、sudoers 和可执行入口。

`operator` 为通用保留名：接管前检查现有用户、UID/GID、文件归属和组；发现同名用户或未知权限时停止，不直接接管、改名或重置。

日常运行操作员是人或自动化操作身份；实际应用进程另用非 root 服务身份，不继承操作员的 sudo 或管理权限。K3s 节点上的 OS `operator` 使用普通交互 shell 执行客户端命令；K3s 安装、独立 kubeconfig、认证与 RBAC 由 K3s role 管理。普通 `kubectl` 调用不需要宿主机 root、Docker/containerd 组或 root 管理 kubeconfig。rootful Docker socket、`docker` 组和任意 sudo 都具备接近 root 的主机管理能力；不得在授予这些权限后声称 operator 与 root 强制隔离。确需这些能力时按显式系统管理阶段处理，审计账户不得获得。

**▍3. 环境级 Vault KV 记录**

各环境按角色保存三条 KV v2 记录，所有节点消费相同角色公钥授权，不按节点复制配置。调用方必须显式指定 `<environment>`，允许 `sit`、`uat`、`prod`，缺失或不支持时停止，不回退到生产路径。

:::table
用途|KV CLI 路径|字段
root SSH 公钥授权|`kv/<environment>/security/root`|`authorized_keys`：root 公钥文本
operator SSH 公钥授权|`kv/<environment>/security/operator`|`authorized_keys`：operator 公钥文本
auditor SSH 公钥授权|`kv/<environment>/security/auditor`|`authorized_keys`：auditor 公钥文本
:::

例如 root 生产路径为 `kv/prod/security/root`，KV v2 API/policy 路径为 `kv/data/prod/security/root`，其他两角色各有独立路径。字段为公钥，不存放 SSH 私钥；多把公钥以换行分隔。暂时允许使用同一公钥，后续应轮换为独立公钥。持有该私钥的人能登录所有获此公钥授权的角色，因此不能声称这些角色在人员身份层面相互隔离。读取授权按消费者和具体记录划分，由 Vault owner 管理。

使用已认证 Vault 管理终端手动初始化：

:::code
export VAULT_ADDR=https://vault.svc.plus
python3 scripts/bootstrap_os_identity_keys.py --environment prod \
  --root-public-keys /path/to/root.pub \
  --operator-public-keys /path/to/operator.pub \
  --auditor-public-keys /path/to/auditor.pub
:::

每个文件可包含多行 SSH 公钥。脚本先检查三个目标均不存在，复用公钥时输出权限边界提示，逐条使用 KV v2 `cas=0` 创建；已有记录或无法确认状态时停止，不能覆盖。三次写入不是原子操作：中途失败会报告已创建路径，应先检查各路径再按 Vault owner 的受控流程完成，不能盲目重跑。已有记录的更新和轮换另按 Vault owner 的受控流程执行。脚本不会生成私钥或将数据写入 Git。`prod` 是示例，目标环境必须明确指定。也可使用 `bash scripts/bootstrap_os_identity_keys.sh`，参数与 Python 入口相同。

旧 `kv/prod/platform/prod-k3s-v6/ssh` 保持原有调用方使用，消费者切换验收前不删除、不复制秘密到新路径。当前新路径只代表规划及初始化工具，不代表已写入或 common 已消费。

**▍4. 新 OS 节点接管顺序**

以后每次接管新 Linux 节点，标准入口先执行 `vhosts/common`：

1. 核实受信 host key、CMDB/inventory、OS、主机名和既有用户/权限，记录脱敏基线。  2. 使用 root 建立或核实 operator/auditor，配置各自公钥、可交互登录 shell、受控 sudo、工作目录和 SSH 策略。  3. 检查父目录、ACL、sudoers、有效组和敏感文件访问；先验证配置，再 reload SSH。  4. 分别验证三用户实际 SSH 登录、OS 允许/拒绝和必要运行操作，保留回执及管理恢复入口。  5. OS 基线通过后，由调用方进入服务、运行时、K3s/K8s 或迁移等对应 role。

新接管入口必须显式启用此基线；通用 role 保留参数开关，避免已有 common 调用方升级后自动批量改账户。接管旧节点先盘点，再逐节点变更。

**▍5. 专业 role 的执行身份选择**

专业 role 执行时显式选择或通过参数指定以下角色，不根据任务名称自动提权：

:::table
角色选择|OS 用户|调用原则
系统管理|`root`|初始化、安装、恢复及确需管理能力的步骤；记录调用者、授权范围和结果
日常运行操作|`operator`|授权范围内的运行操作；目标迁移写入复用 operator，不新增迁移 Linux 用户
只读审计|`auditor`|只读检查、分析及授权源端导出/比对；不能用于系统或业务状态写入
:::

迁移调用方分别显式指定源、目标和每个步骤的执行角色；身份缺失或权限不满足时停止，不静默回退到 root。需要更高权限时显式切换系统管理阶段，完成后返回普通操作权限。OS 用户选择不自动赋予数据库或 Kubernetes 权限，由对应 role 校验授权。

本节仅约定跨 role 的身份选择边界，common 不执行迁移、不读取迁移连接，也不实现集群授权。

**▍6. 新节点身份**

新节点统一使用 `root`、`operator` 和 `auditor`。历史节点的账号和数据不由新节点初始化清理；历史回执保留实际身份，不能改写为新身份验收。

**▍7. 最小实现与 OS 验收**

:::table
检查|通过条件
显式启用|默认不影响已有调用方；新接管入口显式启用；目标身份和变量缺失时停止
root|现有管理员仍可 SSH 登录和执行必要管理，避免锁死；日常业务进程不使用其身份
operator|可 SSH 登录、访问授权工作目录及执行规定运行命令；越权 sudo 和管理秘密读取被拒绝
auditor|可 SSH 登录并读取授权 OS 状态；实际拒绝系统/业务状态写入、管理秘密读取和提权；允许个人受控目录写入
SSH 与 sudo|语法校验通过、用户独立授权、父目录/ACL/组及实际访问符合预期；配置变更才 reload
幂等与恢复|重跑不重建用户或无故重启；保留老管理入口；新增访问可独立撤销，不删除未知配置
:::

`vhosts/common/tasks/node_bootstrap.yml` 在 hostname 检查之后调用 `os_identity.yml`，完成三用户 OS 身份检查后才输出 common 回执；真实 SSH 验收、主机安全基线和集群身份另行记录。

### 18.5 专项参考 4　K3s role 职责与依赖清单

来源：`knowledge/docs/reference/platform-delivery/K3s-role职责与依赖清单.md`（53492be），全文收录。

> 归档说明：本文保留原有 role 清单与各时点证据；当前 V6 的实际状态请以 [V6 规划与部署状态归档](PROD-K3S-V6-规划与部署状态归档.md) 顶部最新条目为准，勿将历史运行记录视为当前验收。

> 来源：Playbooks `main` commit `7b7f44164ef1429dc86c01582393e704257ac386` 的 `roles/vhosts/k3s_platform_bootstrap/k3s-role-map.md`；此为归档副本，运行状态需以最新回执为准。

**▍最新调用链核对（2026-10-31）**

:::table
环节|现状和重构项
Orchestrator → Playbooks|运行 [41200258539](https://github.com/ai-workspace-infra/Platform-Orchestrator/actions/runs/41200258539) 的 Resolve、IaC/Provision 成功；[Deploy 子运行 41200534051](https://github.com/ai-workspace-infra/Platform-Orchestrator/actions/runs/41200534051) 从 CMDB 和 GitOps 选中节点后调用 Playbooks。Deploy job 仍混有原生 Web SaaS 变量及逻辑，应逐项迁移至对应 owner，先建立调用链再移除旧实现。
common / OS 身份|operator 登录检查因 Ansible 参数提前展开 `$HOME` 失败；[Playbooks #927](https://github.com/ai-workspace-infra/playbooks/pull/927) 已提出修复并拆分诊断，尚待合并。只读复现和修正后的三项检查均有 `changed=0` 的现场证据。
主机安全基线|`k3s_platform_bootstrap.yml` 使用 `vhosts/common` 的 `node_bootstrap.yml` 入口；该入口执行 hostname、OS 身份和数据盘，但未调用 `common/tasks/main.yml` 中的 SSH、fail2ban、limits 和防火墙任务，不能据此宣称完整基线完成。应审查可复用的基线任务和 SSH/K3s 网络规则，补齐调用及真实回执，避免直接套用会重写 hostname/hosts 的旧入口。
数据盘、K3s、Flux|本次在身份检查处停止；auditor 复核 `/dev/sdc` 100 GB 未格式化/挂载，K3s 未运行。后续步骤与真实身份/RBAC、服务验收均无成功回执。
:::

上表是实际运行状态；下方带日期的条目保留历史快照。不得因角色存在、代码合并或先前 CI 通过而标记当前节点已验收。

**· 工作流 DAG 与矩阵重构目标**

控制面工作流的最长 `needs` 串联链控制在 3–5 个 job；矩阵的同层副本按一个阶段计数。根工作流当前已有 Resolve → IaC/Provision → Deploy → Migrate/Configure → Verify 五个阶段；Deploy 子工作流仍包含多条混合的旧服务链，需要按实际依赖重构，不能通过隐藏依赖或把执行代码塞进编排器来缩短图。

在 Orchestrator `main` `2e25af0f` 静态核对，`selfhost-stage-deploy.yml` 的最长链为 **10 个 job**：

:::code
parent-gate → provision → capture_web_saas_baseline → update_gitops_tags
→ initialize_empty_web_saas → deploy_web_saas → accept_web_saas_upgrade
→ deploy_agent_proxy_non_iac → deploy_monitor_agent → stage-output
:::

仓库深度策略目前对该文件保留 10 层历史例外；目标是在真实 owner 调用和回执完整的前提下逐步降至最多 5 层，并删除例外。历史依赖不能仅因图表过长而删除；涉及数据初始化、变更、代理和监控的路径需分别确认其实际顺序与影响。

:::table
阶段|责任与矩阵|输出和失败传播
1 Resolve|控制面解析输入、固定基础仓库 SHA、核对发布记录与 GitOps 唯一目标|输出目标清单和作用域；不匹配即失败
2 IaC|按声明的 provider/account/namespace 矩阵派发 IaC owner；相同 state 必须串行|各目标独立 state 与 CMDB 回执；失败目标不得进入部署
3 Bootstrap / Deploy|按 CMDB 节点矩阵调用 Playbooks owner：common、数据盘、K3s、身份和 Flux；Flux 管理插件及业务资源|验证节点、身份和 Flux 交接回执；节点失败不得冒充成功
4 Migrate / Configure|仅对应明确选择的迁移或配置操作派发 owner；`deploy` 不隐式执行数据迁移|按目标收集结果；跳过必须可区分于成功
5 Verify / Report|汇总各 owner 和矩阵项回执，按实际执行范围调用只读验收|缺失、失败、跳过和未运行分别记录；CI 成功不能代替真实身份/业务验收
:::

矩阵输入来自本次固定的 GitOps 声明和 IaC CMDB，不能依据节点名或批次拼接拓扑；矩阵输出须逐目标关联，避免只保留最后一个输出。需要不同权限、审批或 runner 的工作保留独立 job，实际顺序由 owner 或 Flux 依赖表达。拆分前记录现有调用方和操作语义，按 owner 实现 → 切换 caller → 验证回执 → 删除旧副本推进；本节为目标设计，尚无对应重构完成回执。

**▍当前主线与依赖**

:::code
IaC CMDB + 本次解析到 commit 的 GitOps 期望配置
  → 入口绑定目标
  → common：hostname、OS 三账户/组，并调用 web_saas_data_volume 准备独立数据盘
  → k3s_platform_bootstrap（只编排）
      → flux_gitops / k3s_identity：输入预检
      → k3s-cluster-server：控制面初始化及 API 就绪
      → helm_cli：Helm 客户端
      → flux_controllers：Flux 控制器及 rollout
      → flux_gitops：source/root 交接及独立回执
      → k3s_identity：三套认证凭据交付及真实允许/拒绝
      → flux_workload_readiness：声明的 source、Kustomization 和 HelmRelease 就绪证据
  → Flux 按 GitOps 依赖调谐 RBAC、ESO/TLS、Vault、DB、监控和业务资源
:::

RBAC 必须先就绪才能执行真实身份权限验收；不能让它反向依赖尚未签发的  三身份凭据，也不能用“管理员 impersonation 成功”替代真实身份登录。  主机名、Flux root 名、环境批次目录和 source path 各自独立，不按名字推断流程。

**▍当前相关 role 列表（2026-10-31）**

以下状态区分仓库 `main`、待合并候选和生产实际验收。Role 存在或 CI 通过不等于目标集群已完成部署。

:::table
项目|当前状态|当前责任与缺口
`vhosts/common` 与独立数据盘|✅ [Playbooks #916](https://github.com/ai-workspace-infra/playbooks/pull/916) 已合并；❌ 目标节点盘就绪待验收|通用 K3s 入口由 common 调用数据盘 role，挂载及 UUID 验证通过后才发出 common 回执；此前节点的 100 GB 盘未挂载、无文件系统，需实际执行后重新核验
PROD-K3S-V6 当前节点只读观察|❌ 2026-10-31 18:16 Asia/Shanghai SSH 现场检查；非流水线回执|hostname `prod-k3s-v6`、Debian 13、2 vCPU/约 3.8 GiB；root/operator/auditor 均成功 SSH 登录。operator `/bin/bash` 且 home 可写，sudo 仅限 `systemctl is-system-running`；auditor 不能读 `/etc/shadow`、写 `/etc` 或使用 sudo。`/dev/sdc` 100 GB 无文件系统/挂载；K3s/kubectl 和 operator kubeconfig 不存在；`fail2ban`、`auditd`、`ufw` inactive。云防火墙需由 IaC 核验。检查只读，未改变生产状态
`k3s_platform_bootstrap`|✅ Playbooks #903 已合并|只编排子 role 及依赖顺序
`k3s-cluster-server`|✅ #903 已合并|K3s 控制面初始化、hostname 校验、API 就绪；不承担插件发布
`k3s-cluster`|✅ #903 已删除旧实现|两个安装入口已切换到 `k3s-cluster-server`
`helm_cli`、`flux_controllers`、`flux_gitops`、`k3s_identity`|✅ #903 已合并|分别负责 Helm 客户端、Flux 控制器、声明交接、三身份交付和验证；真实身份、Vault writer 与 RBAC 仍需目标集群验收
`k3s` 旧安装器|✅ [Playbooks #905](https://github.com/ai-workspace-infra/playbooks/pull/905) 已合并并移除旧实现|安装由 server 负责；非默认 CNI 明确拒绝，需另行交付独立的 CNI 能力
`k3s_platform_addon`、`k3s-addon`|✅ 已从当前代码及调用方移除|平台插件由 GitOps 按环境显式选择；现有发布的 Flux 接管与运行验收仍需逐项验证
cert-manager、reloader、APISIX、ExternalDNS、NGINX Ingress|✅ [GitOps #681](https://github.com/ai-workspace-infra/gitops/pull/681) 已合并|已提供可独立选择的 Flux 模板，未接入任何环境；ExternalDNS 默认 dry-run
ESO、Caddy|✅ GitOps 已有 V6 HelmRelease 声明；❌ 实际调谐及服务验收待核验|不再通过旧 addon role 重复安装
`k3s-reset`|❌ 安全边界待修复；[Playbooks #915](https://github.com/ai-workspace-infra/playbooks/pull/915) 待合并|空节点无操作修复已在目标节点验证；已安装集群的重置仍需单独验证，不属于初始化依赖
`k3s_runtime_secret_sync`|✅ 独立运维入口|不属于 bootstrap；通用 KV 同步与环境专用投影仍需梳理
OS operator 与 K3s 客户端前置|✅ Playbooks [#925](https://github.com/ai-workspace-infra/playbooks/pull/925) 已合并；❌ 目标节点 common 正式回执待执行|common 在创建时配置并检查 operator 交互 shell。现场 SSH 已证明 shell/home 可用，但 `kubectl`/`k3s` 未安装；common 不交付 kubeconfig/RBAC，也不增加 sudo 或 runtime socket 权限
operator kubeconfig 与 RBAC|⚠️ Playbooks [#924](https://github.com/ai-workspace-infra/playbooks/pull/924)、GitOps [#686](https://github.com/ai-workspace-infra/gitops/pull/686) 检查通过、待合并|`k3s_platform_bootstrap` 编排 K3s identity role 为 operator 交付默认 kubeconfig；GitOps RBAC 声明限定业务 namespace 读取 Pods/ReplicaSets/Events 与 Deployment scale-only。现场 K3s 未安装、无 kubeconfig，真实身份 allow/deny 未运行
三身份与 Flux RBAC|✅ [GitOps #682](https://github.com/ai-workspace-infra/gitops/pull/682)、[Playbooks #906](https://github.com/ai-workspace-infra/playbooks/pull/906) 已合并；❌ 目标集群验收待执行|三身份及 RBAC 基础声明已在 main；operator 的额外运行态读取由待合并 #686 补充。operator 默认 kubeconfig 由 K3s identity role 管理，不能由 common 映射。真实认证、权限允许/拒绝仍待目标集群运行
Orchestrator → IaC CMDB → Playbooks|⚠️ 参数选择与调用入口已合并；生产端到端执行未验收|[Orchestrator #1585](https://github.com/ai-workspace-infra/Platform-Orchestrator/pull/1585) 已合并：根据 IaC CMDB catalog 精确选择目标声明，并支持从 GitOps host vars 解析 K3s bootstrap reader、SSH Vault 字段与三身份 writer 参数。GitOps [#684](https://github.com/ai-workspace-infra/gitops/pull/684) 与 Playbooks [#920](https://github.com/ai-workspace-infra/playbooks/pull/920) 已合并，但生产 reader 认证与目标路径 allow/deny 尚无新回执。最近 apply [#41187083044](https://github.com/ai-workspace-infra/Platform-Orchestrator/actions/runs/41187083044) 使用合并前版本，在旧 Vault `ref` claim 处停止，common、数据盘、K3s/Flux 均未运行；必须从当前 main 重新验收完整调用链
Vault writer 与真实身份验收|❌ 运行验收未完成；[Playbooks #918](https://github.com/ai-workspace-infra/playbooks/pull/918)、[GitOps #683](https://github.com/ai-workspace-infra/gitops/pull/683) 已合并|K3s identity writer policy/role 已定向应用，精确授权三条 create/read 路径并绑定受保护 PROD Deploy 身份；该身份负责签发凭据归档，不负责节点 SSH 登录或 common 公钥读取。真实 JWT 登录、相邻路径拒绝和三账户 RBAC 尚待验证
common Vault 公钥 reader|✅ GitOps [#684](https://github.com/ai-workspace-infra/gitops/pull/684)、Playbooks [#920](https://github.com/ai-workspace-infra/playbooks/pull/920) 已合并；❌ 生产认证与路径拒绝未验收|声明和 HTTPS KV v2 reader 实现已在 main；仍需实际认证验证只允许三条 OS 公钥记录并拒绝相邻路径
Verify 阶段前置条件|✅ [Orchestrator #1587](https://github.com/ai-workspace-infra/Platform-Orchestrator/pull/1587) 已合并；⚠️ [#1589](https://github.com/ai-workspace-infra/Platform-Orchestrator/pull/1589) owner-contract 修复待合并|Verify 要求 Resolve、IaC/Provision、Deploy 成功后才执行；#1589 的 workflow 检查已通过但仍 OPEN
Flux 接管和服务部署|❌ 尚无完整运行验收证据|最近 apply 在 Provision 阶段失败，Deploy/Migrate/Verify 均跳过；最近只有 push/PR CI，无后续生产 `workflow_dispatch`。没有 common、数据盘、OS/K3s 身份、K3s/Flux、Vault、PostgreSQL、Observability、Web SaaS、Ingress 的本次运行就绪证据。待相关 PR 合并后从当前 main 重派并记录真实回执
:::

**· 可选检查项：Vault OIDC**

按本次部署或工作流实际使用的身份提供方选择检查；这两项不是每次 K3s  初始化或服务部署的必选门禁。选中后，核对本次固定 GitOps commit 中的声明、  Vault role 的精确身份绑定、所引用策略的最小路径和能力，并通过实际认证验证  授权路径允许、相邻路径拒绝。未选择时标记“不适用”，不能据此推断已配置或已验收。

:::table
可选检查项|适用范围|核对内容|状态记录规则
`vault_github_oidc`|使用 GitHub Actions OIDC 向 Vault 认证的任务|仓库、workflow、ref/environment claims；GitOps policy 引用；最小路径授权及允许/拒绝结果|仅按需检查；本项不代表 Vault role 或运行身份已验收
`vault_google_oidc`|使用 Google OIDC 向 Vault 认证的任务|issuer、audience、subject claims；GitOps policy 引用；最小路径授权及允许/拒绝结果|仅按需检查；本项不代表 Vault role 或运行身份已验收
:::

OIDC 可选检查不替代 K3s `root`、`operator`、`auditor` 的独立 Kubernetes  认证和 RBAC 验收，也不自动授权修改 Vault auth mount、role 或 policy。  上述 SSH 状态是指定时刻的人工现场观察，不构成 `COMMON_NODE_VERIFIED`、  K3s/Flux bootstrap 或正式流水线回执；完整安全基线、数据盘 UUID/挂载证据和  云防火墙状态仍须由各自 owner 执行并验收。

当前清单文件迁入本目录的 [Playbooks #904](https://github.com/ai-workspace-infra/playbooks/pull/904) 已合并。所有角色遵循 `AGENTS.md` 的单一职责规则。

**▍主线执行 role**

:::table
Role|唯一能力|前置条件|输出/验收
`vhosts/common` 的 `node_bootstrap.yml`|校验节点身份、建立 OS 三账户并串联声明的独立盘准备|CMDB 精确节点、受控 SSH 公钥；既有节点和 PV 亲和性检查|主线要求盘挂载及 UUID 证据后才产生 `COMMON_NODE_VERIFIED`；不代表完整主机安全基线
`vhosts/common` 的 OS Vault reader|以受控 Vault 会话读取三账户公钥|明确的 HTTPS Vault、目标环境和只读会话；证书严格校验；分别依赖 GitOps reader 声明和精确只读 Vault role|#920 候选使用 KV v2 HTTPS 接口，无需在 runner 安装 Vault CLI；缺失或拒绝读取时失败；目前没有 V6 实际调用回执
`web_saas_data_volume`|核验并准备声明的独立文件系统|CMDB 实例、卷及设备匹配；空盘初始化需显式授权|挂载点、UUID、文件系统证据；不自动重格式化已有文件系统
`k3s-cluster-server`|初始化单节点 K3s 控制面|common 已设置 hostname；要求独立盘时卷证据已通过|K3s 服务启动及 API `/readyz`；既有安装跳过安装器，不等于已升级
`k3s_platform_bootstrap`|按依赖顺序编排子 role|已完成入口绑定、common 和数据盘角色|子 role 顺序执行；失败停止后续执行，不代表业务服务验收
`helm_cli`|Helm 客户端准备|主机包/CA/网络|现有客户端或安装成功，不部署 chart
`flux_controllers`|Flux CLI 与控制器初始化|K3s API、私有 admin kubeconfig|controller rollout 就绪
`flux_gitops`|经审查的 source/root 交接|解析过 commit 的 GitOps 配置与 ready Flux|Flux 交接回执，不声称业务 Ready
`k3s_identity`|OS 用户到 Kubernetes 主体的映射及三身份生命周期|common 已建立 OS 三账户、实际 CA/UID、GitOps RBAC、受控 Vault writer|独立密钥/证书/私有 kubeconfig；当前仅 `operator` 的 `~/.kube/config` 指向其受限身份配置；KV CAS 归档、真实认证与允许/拒绝
`flux_workload_readiness`|只读观察声明的 Flux 对象|三身份任务完成且 GitOps 提供待观察对象|独立 `FLUX_OBJECTS_READY` 回执；记录各对象 revision，不替代应用接口、数据和用户流程验收；候选随 #918，未生产验证
:::

生成器、模板、默认值及验收脚本随能力移动；没有复制第二套实现。  现有 `k3s_platform_*` 和 `k3s_identity_*` 为调用合同，未增加环境专用别名。

**▍输入、证据与重复执行边界**

:::table
阶段|必要输入与失败条件|可记录证据和重复执行边界
入口选择|`MATRIX_HOST`、CMDB 文件及 SHA、固定 GitOps checkout/SHA、仓库内资源声明路径和新的回执路径；目标/区域/实例/盘不匹配即失败|本次 GitOps/Playbooks SHA、CMDB SHA 和实例 ID；当前入口仍校验 Linode 字段，跨 provider 不可假定已支持
common|节点名称、OS 身份和声明的独立盘输入；已有节点/PV 亲和性冲突或磁盘未就绪即停止|主线的 `COMMON_NODE_VERIFIED` 包含节点、OS 身份、实例 ID 和挂载证据；不表示 fail2ban、auditd、UFW 或云防火墙通过
独立盘|精确卷 ID、设备、挂载目标及文件系统；他处挂载、未知签名或目标已有文件时停止|记录真实 UUID 和挂载结果；已挂载时核对同一设备并保留数据；仅无签名空盘可在显式授权下初始化
控制面及 Flux|hostname、K3s 版本、私有管理 kubeconfig、声明的 source/root/path；声明或实际节点/版本/磁盘不匹配时失败|`FLUX_HANDOVER_VERIFIED` 记录 source/applied revision 与集群和节点标记；不表示 RBAC、身份或业务就绪。当前 active 验证器约束单节点及 ext4
三身份|声明的 RBAC Kustomization 当前 generation Ready 且应用所选 commit；独立短期 Vault writer、实际 CA、UID 和 allow/deny 清单|master 签发独立凭据、验证信任链并以 KV v2 CAS=0 写入，CA 私钥留在 master；不同记录、部分签发或过期证书失败，不以删除数据强制重试
服务与 DNS|GitOps 依赖图、服务所需的受控凭据与制品、目标环境声明|分别记录各服务健康、接口和数据证据；DNS 变更必须符合单独声明与授权，Flux 交接回执不是流量切换或服务验收
:::

**回执时序：** 当前 `flux_gitops` 在 `k3s_identity` 运行之前写入交接回执。  身份任务失败时该文件仍可能存在；消费者必须同时检查整个 playbook/owner 进程退出状态及真实身份验收，不能仅凭文件或 `FLUX_HANDOVER_VERIFIED` 判定整条主线成功。

入口的身份字段断言在 common 和数据盘之前；`flux_gitops` 与 `k3s_identity` 的完整 role 预检则在两者之后。因而缺少某些 Flux 输入时，不能声称所有主机或数据盘操作都尚未发生；应先在 caller 补足前置检查。

匹配已有挂载和受保护的身份状态可支持部分重试；当前没有目标节点的完整重复运行证据。数据库版本、SQL schema、Vault Raft、监控存储及其他持久卷的升级或迁移仍按新集群和独立存储处理；代码或回执的回退不等于数据回滚。

**▍验证和发布边界**

本次同步受影响的 Python 包装器、测试导入、Ansible 入口和 CI 路径过滤。  契约测试检查编排器没有直接副作用、独立 role 可解析、前置失败不会进入  安装，以及真实身份生成器的证书/目标绑定/CAS 行为。生产验证必须另记  实际 GitOps/Playbooks SHA、CMDB 实例、运行 ID 与真实身份/服务结果。

本次已合并的拆分未执行卸载、原地升级、删盘、数据迁移、DNS 更新或凭据轮换。  回退 PR 只恢复代码调用路径，不回滚数据，也不撤销已签发证书。

**▍历史 role 与迁移记录**

以下表格记录 #903 完成时的旧实现与处理；后续变化以文首状态表和对应 PR 为准。

:::table
原 role|实际职责/问题|本次处理与后续边界
`k3s_platform_bootstrap`|原来混合 K3s、Helm、Flux、交接、凭据生成与验收；README 含暂停式旧描述|改为仅调用子 role 的编排器；执行实现全部归对应子 role
`k3s-cluster-server`|原 bootstrap 同时安装 K3s/Flux/ESO，写业务 namespace/Vault token Secret；静态 vars 写死目标；其余五个 action 文件为空|保留为唯一主线控制面安装 role；替换旧混合 bootstrap，删除空 action、静态 vars、无调用模板与旧生成脚本。只实现初始化，非 bootstrap 的 action 明确拒绝
`k3s-cluster`|脚本安装 K3s，随后隐式装 nerdctl/CNI、本地 Registry 和自签 CA；重复安装且夹带额外资源|合并控制面能力到 `k3s-cluster-server`；更新两个 playbook 调用方后删除目录。新主线不隐式创建 Registry；此行为变化必须在审查中确认
`k3s`|旧脚本混合 K3s/Helm/CNI；meta 自动依赖 common；含固定域名和忽略错误|K3s 安装统一到 server，调用方切换，旧实现删除。非默认 CNI 明确拒绝，需由独立 GitOps 声明与执行链另行交付
`k3s_platform_addon`|直接 Helm 管理 cert-manager/ESO/reloader/Caddy/APISIX/external-dns，默认含业务路由与域名；与 GitOps 资源 owner 重叠|旧实现及入口已移除；环境按需选择 Flux 模板，现有发布的接管另行验证
`k3s-addon`|脚本管理 ingress/DNS，meta 自动安装 cert-manager，存在忽略错误与销毁操作|旧实现及调用方已移除；Ingress 和 DNS 由经审查的 GitOps/IaC 交付
`k3s-reset`|调用重置脚本，旧默认 `cluster_reset=enable`；属于破坏性恢复|独立保留，不列入初始化依赖。本次未执行；显式确认、精确范围、备份和恢复验证等防护仍需另行收敛
`k3s_runtime_secret_sync`|Vault KV 字段 CAS 同步，并包含 dev-registry 投影模式；不是 K3s 安装/RBAC|保留独立运维入口，不进入 bootstrap。后续拆分通用 KV 同步与环境投影；不能自动扩大路径权限或覆盖业务记录
:::

这些历史 role 的问题是盘点结论；本次未对所有旧实现逐一改造，不能将  “本次主线不调用”写成“全仓陈旧代码已清理”。

**· 入口与历史调用迁移**

:::table
入口|调用路径|范围
`k3s_platform_bootstrap.yml` / `scripts/pipeline/bootstrap-k3s.sh`|CMDB → common（调用独立盘 role）→ bootstrap 子 role DAG|正常 IaC 交付
`k3s_platform_bootstrap_with_gitops.yml`|bootstrap 子 role DAG|调用方先完成 common/存储及非敏感输入绑定
`k3s_identity_bootstrap.yml`|直接 `k3s_identity`|已有 master 的独立身份初始化，不重装集群
`k3s-cluster.yaml`、`setup-k3s-node.yaml`、`init_k3s_cluster_server`|直接 `k3s-cluster-server`|仅初始化控制面，目标组统一 `k3s`；不再隐式部署 Registry/Flux/ESO
`k3s_reset.yml`、`reconcile_k3s_runtime_secrets.yml`|保持独立旧入口|非新 bootstrap 的依赖，不自动执行
:::

空的 worker role 和入口已移除。独立脚本模拟安装 Flux/ESO 不是本 DAG 验收；  OrbStack 历史模拟探针不构成拆分后调用链或幂等性的证据。

旧 Dev reusable workflow 仍固定 checkout 历史 Playbooks SHA，不会自动采用本次  拆分；其专用 adapter 仍依赖旧 source/root 默认值且未提供完整身份合同。  它不属于已接通的新入口，更新该消费者前需从所选 GitOps 声明补齐配置与  common 前置，不能仅移动 checkout SHA 或据其旧回执宣称本次部署通过。

### 18.6 专项参考 5　PROD-K3S-V6 独立节点、集群冷启动规划与部署状态归档

来源：`knowledge/docs/reference/platform-delivery/PROD-K3S-V6-规划与部署状态归档.md`（53492be），全文收录。

**▍最新部署状态（2026-11-01，北京时间）**

以下为本次独立节点的实际证据，不代表业务验收或流量切换完成。

:::table
项目|状态|证据与缺口
节点和独立盘|✅ 已验证|Akamai `manbuzhe2026`、`jp-tyo-3`，实例 `<instance-id>`、`<node-ip>`；100 GB 盘 `<volume-id>` 为 ext4，挂载 `/data`。[部署运行 #41251575217](https://github.com/ai-workspace-infra/Platform-Orchestrator/actions/runs/41251575217) 的 IaC 成功、部署失败。
OS 身份和安全基线|⚠️ 部分验证|`root`、`operator`、`auditor` 用户与同名组存在，`auditor` SSH 可登录且无 sudo。`fail2ban`、`auditd`、UFW 未运行，容器集群按节点安全方案选择是否启用；必需的 SSH、主机和云防火墙基线仍需按声明核验。
K3s、Flux 与身份|⚠️ 部分验证|K3s 节点 Ready（v1.37.1+k3s1），Flux 管理根与单元 source 已就绪；单元 source 固定到 GitOps main SHA `c19f35185aa9004c0a973e49327d54889aa3a575`。三套 X.509 kubeconfig 均可认证：`root` 当前 RBAC 不能读取 Pod/PVC 状态；`operator` 仅有 `web-saas-prod` 内 Service/Deployment/HelmRelease 查看及 Deployment scale 权限；`auditor` 可读 nodes、namespaces，但不能列出工作负载、事件、Service、PVC 或 HelmRelease。三身份读取 Secrets、创建 Deployment、exec 和修改 RBAC 均被拒绝。扩展 root/auditor 状态读取、node-exporter 资源修复的 GitOps PR #689 待合并，尚未调谐。
K3s 身份 Vault 归档|❌ 未完成|当前归档目标存在与本集群 UID 不匹配的旧记录，安全检查拒绝覆盖；在受控轮换/归档路径完成前，不得报告三身份 Vault 归档完成。
公共 Vault TLS reader|✅ 已验证|专用 JWT 公钥与当前集群匹配；单条 TLS 记录允许读取，相邻路径、错误 audience 和错误 ServiceAccount 拒绝。reader policy 包含 `auth/token/lookup-self`，不扩大 KV 读取范围。
ESO 与证书|✅ 已验证|SecretStore `Valid`，ExternalSecret `SecretSynced`，`vault-prod/vault-server-tls` 已生成。证书有效至 2027-01-05，SAN 包含 `*.svc.plus`、`svc.plus`；完整链、证书与私钥公钥匹配、集群内 TLS/SNI `vault-selfhost-prod-v6.svc.plus` 均已验证。DNS 未启用；TLS 验证通过指定 SNI 直连集群 Service。
Vault|❌ 未完成|Pod Running 但 `0/1` Ready；只读 status 为 `initialized=false`、`sealed=true`。TLS 已启用，集群内受信任链与 `vault-selfhost-prod-v6.svc.plus` SNI 验证通过。Vault HelmRelease upgrade 因 StatefulSet readiness 等待超时而失败，PVC `data-vault-0` 仍 Bound（10 GiB）。按约定由 Vault owner 手动初始化与解封；未删除或重建 PVC。
PostgreSQL|❌ 未完成|HelmRelease 安装失败，Pod `ImagePullBackOff`；拉取固定 GHCR digest 返回未授权，Pod 未配置 `imagePullSecrets`。三条 PostgreSQL SecretStore 均为 `InvalidProviderConfig: unable to create client`，ESO 日志明确返回对应 Vault JWT role `prod-k3s-v6-postgresql-{admin,operator,auditor}-reader` 不存在；GitOps 中已有操作声明，但 Vault 运行态角色尚未创建，对应 ExternalSecret 为 `SecretSyncedError`，DB Secret 未交付。PVC 20 GiB Bound。需由 Vault/Playbooks owner 经受控配置执行创建精确角色，再提供最小权限 GHCR pull 凭据；数据库初始化、三身份权限、备份恢复均未验收。
Observability|❌ 未完成|DataKit 为 `CreateContainerConfigError`（缺 `datakit-dataway-secret`）；Grafana 缺 `grafana-admin`，namespace 尚无 SecretStore/ExternalSecret。监控栈 Pod `4/5`，PVC 20 GiB Bound；node-exporter liveness 超时后拒绝连接并持续重启。GitOps PR #689 提高其资源预算，待合并与 Flux 调谐后复验。
Web SaaS、Ingress 与 DNS|❌ 未验收|Web SaaS 与 Ingress namespace 当前无资源；其 GitOps Kustomization 因 `vault-prod` 未就绪而阻塞，业务依赖尚未部署验收。全程 `dns_mode=none`，未请求迁移或 DNS 变更；V5/canonical DNS 未触碰。
活跃集群续跑|✅ 已观察|活跃 K3s/Flux 管理根和已绑定 PVC 均保留；最新部署运行已完成 IaC，但部署阶段失败。当前无需重建节点或存储；后续只针对未就绪的 Flux 单元修复并核验回执。
:::

**身份交付顺序：** master 生成并验证独立证书和私有 kubeconfig → 各用户交付默认配置并以真实身份验收 RBAC → 通过受控 writer 归档 Vault KV → 校验回读后形成成功回执。Vault 归档失败不能产生完整成功回执；不得覆盖冲突记录或从管理员配置复制凭据。

**▍1. 状态标记与目标**

:::table
标记|含义
✅ 完成|已有明确证据支持该项完成；如果只验证了历史引导，在说明中限定其时间和范围
❌ 未完成|尚未执行、缺少验收证据、存在阻断或当前状态待核实；不等于已证明资源不存在
:::

**V6 的目标**：在独立节点、独立集群和独立存储上完成全部服务冷启动与验收，形成可供后续数据迁移和切换评审的候选环境。

- V5/canonical DNS 保持不变；V6 专属域名在新节点地址确认后新增解析，不指向 V5 节点。`dns_mode=none` 禁止 canonical 默认更新，V6 专属记录由受控 DNS owner 单独处理。
- 保留 V5 集群、数据库及原业务写入方。
- 新节点创建、全量服务部署、业务验收和流量/写入权切换分别判定，不相互替代。
- 当前工作为规划和状态整理；数据迁移、切换及旧环境退役另按具体任务授权执行。

**▍2. 规划基线与工作树**

当前批次采用独立节点、集群、数据盘和 IaC state；本次运行的云端资源与状态见顶部。各仓库默认 `main`，每次运行解析并记录 commit SHA。工作树状态只对核对时有效，不作为部署验收证据。

**· 2.1 V6 批次域名分配**

:::table
服务|V6 批次域名|访问/路由边界|DNS/TLS/验收状态
Console UI|`console-selfhost-prod-v6.svc.plus`|Caddy → `web-saas-console.web-saas-prod.svc.cluster.local:80`；TLS Secret `ingress-prod/console-tls`|DNS 当前未核验；HTTPS/SNI、登录和 runtime `NOT_RUN`
Accounts API/UI|`accounts-selfhost-prod-v6.svc.plus`|Caddy → `web-saas-accounts.web-saas-prod.svc.cluster.local:80`；TLS Secret `ingress-prod/accounts-tls`|DNS 当前未核验；HTTPS/SNI、API 回归、错误率和 runtime `NOT_RUN`
Billing API/UI|`billing-selfhost-prod-v6.svc.plus`|Caddy → `web-saas-billing.web-saas-prod.svc.cluster.local:80`；TLS Secret `ingress-prod/billing-tls`|DNS 当前未核验；TLS、webhook 和 runtime `NOT_RUN`；真实扣款/退款未授权
PostgreSQL|`postgresql-selfhost-prod-v6.svc.plus`|DNS 解析到 V6 新节点；应用使用集群内 Service DNS，迁移经受控 `migratectl` 连接；不开放公网 DB 端口|DNS 当前未核验；Service、PVC、备份恢复及迁移连接均待部署验收
Vault|`vault-selfhost-prod-v6.svc.plus`|V6 专属服务/TLS 名称；不通过 Caddy 对公网暴露管理/API。初始 TLS 材料仍从公共 `https://vault.svc.plus` 只读获取|DNS 当前未核验；须确认受控证书 SAN、Vault `tlsServerName` 和集群内服务解析后才可放行
Observability|`observability-k3s-v6.svc.plus`|保留已声明的 Grafana `rootUrl` 候选；只按 VPN/受限运维通道设计，未配置公开 Caddy 路由|DNS 当前未核验；入口认证、TLS 和监控 runtime 均待验收
Content|暂不分配独立公网域名|作为内部服务候选；业务 owner 未确认外部域名/独立 Caddy 路由|旧声明 `content-k3s-v6.svc.plus` 不作为本轮分配结果；待确认用途后再决定
:::

V6 域名需重新核验 A/AAAA/CNAME、权威 DNS、解析目标和冲突。V6 TLS 证书需独立验证 SAN、有效期、信任链及证书/私钥匹配；GitOps Secret 引用不等于 Secret 已同步。

**▍3. 独立节点与集群目标规格**

本节是目标设计。已创建及已验收的范围见顶部最新状态，不将规格表本身视为运行证据。

:::table
项目|规划要求
云账户、地域|Akamai `manbuzhe2026`、`jp-tyo-3`；执行前核实实际账户身份和地域能力
计算|1 台 `g6-standard-2`，2 个共享 vCPU / 4 GB
系统|当前声明为 Debian 13；核实镜像和制品架构兼容性
集群展示名|`PROD-K3S-V6`
节点标识|hostname、inventory 主键、K3s node name 统一为 `prod-k3s-v6`；下一批次从同一个 `node_hostname` 输入派生
稳定管理标识|根 Flux Kustomization 使用 `prod-k3s`，不随批次改名；批次目录、state、卷及凭据仍独立，见第 13 节
独立身份|SSH host key、machine ID、集群 CA/UID、节点 UID 独立生成并留证
Terraform|独立 workspace、backend/state key；不接管 V5 state
数据盘|独立 100 GB ext4 卷，挂载 `/data`，持久卷路径 `/data/k3s/storage`
数据保护|实例和卷防误删；PVC/PV 保留行为、备份和恢复分别验收
SSH|当前声明临时使用 `0.0.0.0/0`；正式运行前落实操作员白名单
Kubernetes API|使用受控管理路径；不为公共 Vault 身份验证开放公网 API
DNS|V6 专属记录在新节点地址确定后新增；V5/canonical DNS 不修改，见第 14 节
:::

**· 3.1 容量与可用性边界**

❌ **全业务栈容量验收未完成。** 2 vCPU / 4 GB 是用户选定的候选规格，不直接等于满足整个业务栈。

放行业务前应汇总固定 chart 渲染后的：

- requests/limits 与控制面预留；
- 镜像拉取、容器运行及滚动发布峰值；
- PostgreSQL 连接数和内存预算；
- 监控保留量、日志增长、磁盘空间与 inode；
- 数据备份、隔离恢复所需空间及 I/O。

容量不足时停在对应阶段，另行评审规格，不自动扩容。

单节点故障会影响整个 V6；独立数据盘和单副本 Vault Raft 不构成高可用。单节点入口及应用发布可能存在重启窗口，不能预先承诺零停机。

**▍4. GitOps 层级与五个独立服务单元**

✅ **层级规划已形成。** ❌ **完整目标图及各服务的运行验收尚未完成。**

所有 GitRepository 和 Flux Kustomization 位于 `flux-system`；HelmRelease 位于各服务 namespace。

六个 GitRepository 共用一个仓库 URL：[`https://github.com/ai-workspace-infra/gitops.git`](https://github.com/ai-workspace-infra/gitops)。每个 source 的配置 ref 独立固定。

下表按最新规划使用稳定根名 `prod-k3s`；旧回执中的 `prod-k3s-v6` 根对象名称保留为历史事实。本轮未修改 Flux YAML，也未对已有集群执行对象改名。

:::table
环境|集群|层/单元|工作负载 namespace|Flux Kustomization|HelmRelease|GitRepository|source path
PROD|PROD-K3S-V6|管理根|`flux-system`|`prod-k3s`|—|`config-prod`|`environments/clusters/prod-k3s-v6`
PROD|PROD-K3S-V6|ESO 前置|`external-secrets`|`external-secrets`|`external-secrets`|`config-prod`|`services/prod-k3s-v6/cluster-prerequisites/external-secrets`
PROD|PROD-K3S-V6|TLS 身份|`vault-prod`|`vault-tls-identity`|—|`vault-prod-config`|`services/prod-k3s-v6/vault-prod/tls-identity`
PROD|PROD-K3S-V6|TLS 同步|`vault-prod`|`vault-tls-bootstrap`|—|`vault-prod-config`|`services/prod-k3s-v6/vault-prod/tls-bootstrap`
PROD|PROD-K3S-V6|Vault|`vault-prod`|`vault-prod`|`vault`|`vault-prod-config`|`services/prod-k3s-v6/vault-prod`
PROD|PROD-K3S-V6|PostgreSQL|`postgresql-prod`|`postgresql-prod`|`postgresql`|`postgresql-prod-config`|`services/prod-k3s-v6/postgresql-prod`
PROD|PROD-K3S-V6|Observability|`observability-prod`|`observability-prod`|`observability`、`observability-agent`、`datakit`|`observability-prod-config`|`services/prod-k3s-v6/observability-prod`
PROD|PROD-K3S-V6|Web SaaS|`web-saas-prod`|`web-saas-prod`|`web-saas-prod`|`web-saas-prod-config`|`services/prod-k3s-v6/web-saas-prod`
PROD|PROD-K3S-V6|Ingress|`ingress-prod`|`ingress-prod`|`caddy-ingress`|`ingress-prod-config`|`services/prod-k3s-v6/ingress-prod`
:::

目标图共 **6 个 GitRepository、9 个 Flux Kustomization、8 个 HelmRelease**。包含五个服务 namespace，以及 ESO 和 Flux 控制 namespace。

> 历史初次引导回执只有 6 个 GitRepository、6 个 Kustomization、7 个 HelmRelease；当时尚未加载新增 ESO/TLS 前置图。目标图数量与历史回执数量不同，不能把两者混作同一次验收。

**· 4.1 共用 chart 包与独立版本**

PostgreSQL、Caddy、Web SaaS 共用 `distributed-web-saas-fullstack` chart 包，通过独立 values 选择组件、分别固定版本。

:::table
HelmRelease|启用范围|必须关闭的重复组件
`postgresql`|PostgreSQL、Service、PVC 和数据库运行配置|Caddy、UI/API 及其他无关组件
`caddy-ingress`|Caddy、TLS 引用和显式跨 namespace 后端|PostgreSQL、UI/API 及其他无关组件
`web-saas-prod`|UI/API Deployment、Service 和应用配置|内嵌 PostgreSQL、Caddy 及其他无关组件
:::

独立发布约定：

1. 根更新只推进选中单元的 source pin，其他单元保留原版本。  2. 配置 Git ref、chart digest、应用镜像版本分别记录。  3. 子 Kustomization 和 HelmRelease 的放行状态配套声明，避免相互等待。  4. 根只应用管理图，`wait: false`；各子单元独立报告健康。  5. Web SaaS 当前仍为一个 HelmRelease，不宣称 UI/API 已各有独立 HelmRelease。  6. 独立选择版本和调谐范围，不取消依赖、数据保护或有状态升级限制。

**▍5. 冷启动顺序与放行条件**

本表的状态指“阶段完整放行条件是否已有证据”。历史子项通过不自动使整个阶段通过。

:::table
阶段|状态|工作内容|放行条件与当前缺口
0 Plan 证据、制品与容量准备|❌ 未完成|记录本次运行解析的基础仓库 SHA；业务制品固定不可变版本|完整制品核验和 2C4G 全栈容量评审仍无充分证据
1 IaC|✅ 已创建|独立节点与数据盘|实例 `<instance-id>`，盘 `<volume-id>` 已绑定；运行 #41251575217 的 IaC 通过
2 common|⚠️ 部分完成|hostname、三账户和声明要求的主机基线|身份和 auditor 登录已验证；fail2ban、auditd、UFW 未运行，是否启用按节点安全方案选择，其他必需基线待核验
3 存储与控制面|⚠️ 部分完成|独立盘、K3s 和 Flux|100 GB ext4 挂载 `/data`，K3s 运行；安全幂等续跑未验收
4 管理根|✅ 已观察|管理 source/root|`prod-k3s` Ready，GitOps commit `e5bc36a5…`；业务就绪另验
4.5 主机安全基线|❌ 必需基线未完成验收|SSH、账户授权、主机及云防火墙|`fail2ban`、`auditd`、UFW 未运行，属于按节点安全方案选择的可选项；必需控制及拒绝证据待核验，详见 5.5 节
5 ESO 与 TLS 身份|✅ 已验证|ESO、专用身份和权限|指定 TLS KV 允许，邻接路径、错误 audience 和 ServiceAccount 被拒绝；SecretStore Valid
6 TLS 同步|✅ 已验证|`vault-prod/vault-server-tls` SecretSynced；证书有效期/SAN、完整链、证书密钥匹配及集群内 SNI/TLS 均已验证。
7 Vault|❌ 未完成|Raft 初始化、unseal、内部认证与健康|Pod 运行但未 Ready，`initialized=false`、`sealed=true`；TLS 已验证，HelmRelease 因 StatefulSet readiness 超时失败。需按约定人工初始化/unseal。
8 PostgreSQL|❌ 未完成|新 PVC、空目标库、审查后的 SQL schema 和分权角色|HelmRelease 失败；GHCR digest 拉取未授权；三个 ESO SecretStore 均 `InvalidProviderConfig`，DB identities 未交付；PVC Bound。需修复受控 Vault 身份和镜像授权；schema、权限及恢复待验收
9 Observability|❌ 未完成|监控存储、采集、查询、Dashboard、告警|DataKit/Grafana Secret 缺失且无 SecretStore/ExternalSecret；栈 Pod 4/5，node-exporter 持续探针失败。PR #689 的资源调整待合并调谐，完整链路未验收
10 Web SaaS|❌ 未验收|应用、数据库连接和隔离验证模式|等待 PostgreSQL；业务身份及内部链路未验收
11 Ingress|❌ 未验收|最后部署 Caddy、TLS 和跨 namespace 路由|等待依赖；Host/SNI、域名解析尚待单独核验
12 整体验收|❌ 未完成|迁移评审、业务恢复、回归、重跑与观察|尚未形成完整证据及待切换报告
:::

**Vault 初始化顺序**：安装后先确认 Pod、卷和 TLS 挂载具备初始化条件，再由 Vault owner 初始化/unseal，最后等 Vault Ready。不能先要求未初始化的 Vault Ready，才允许初始化。

首次部署顺序明确为：

:::code
独立 IaC → common → 存储/K3s/Flux → 管理根
→ ESO → TLS 身份及允许/拒绝验收 → TLS Secret 同步
→ Vault 初始化与内部认证 → PostgreSQL → Observability
→ Web SaaS → Ingress → 整体验收 → 待切换评审
:::

部署编排顺序不全部转换成永久硬依赖：Web SaaS 不依赖独立监控的发布健康；监控维护不应阻断业务发布。数据、证书、身份等实际硬前置仍须保留。

**· 5.5 主机安全基线**

**当前状态：❌ 必需基线尚未完成验收。** 在 `prod-k3s-v6` 的只读检查中，`fail2ban`、`auditd` 和 UFW 均未运行。三者在容器集群中属于可选能力，是否启用由节点安全方案和实际职责决定；未运行本身不构成必需项失败。

:::table
安全项|当前证据|待确认
`fail2ban`|未运行|确认 SSH 防护是否由云防火墙、访问白名单或其他机制承担，按方案决定是否启用
`auditd`|未运行|确认安全审计和日志留存由哪一机制承担，按方案决定是否启用
UFW|未运行|核对云防火墙和主机网络策略，避免与 K3s 网络规则冲突后再决定是否启用
OS 三账户|`root`、`operator`、`auditor` 存在；`auditor` 可 SSH 登录且无 sudo|按声明核验 SSH 密钥和账户授权边界
SSH 与节点访问|尚无完整基线验收证据|核对 SSH 配置、云防火墙、允许来源和实际拒绝结果
:::

完成基线验收时，记录选用或不选用可选组件的理由，以及必需控制的实际验证证据；不要仅依据三个服务运行状态判定安全基线是否通过。

**▍6. 密钥、网络与三权分立**

**· 6.1 初始 TLS 信任引导**

:::code
公共 https://vault.svc.plus
→ V6 专用 JWT 身份
→ 仅读取 kv/data/CICD/domains/svc.plus
→ ESO
→ vault-prod/vault-server-tls
:::

:::table
项目|状态|约定或证据
V6 公共 Vault 专用身份|✅ 已配置与验收|指定记录允许，相邻路径、错误 audience、错误 SA 拒绝
初始 TLS 来源|✅ 已明确规划|使用公共 Vault 已有证书记录，不在本机签发
ESO 到目标 Secret 同步|✅ 已验证|`vault-prod/vault-server-tls`，类型 `kubernetes.io/tls`，SecretSynced
证书验证|✅ 已验证|完整信任链、有效期、证书/私钥匹配、SAN `*.svc.plus`；实际 SNI `vault-selfhost-prod-v6.svc.plus` 握手通过
内部 TLS 连接契约|✅ 已验证|通过集群内 Service 地址并使用 `vault-selfhost-prod-v6.svc.plus` SNI 完成受信任 TLS 握手；未依赖公网 DNS
V6 Vault 内部运行凭据/ESO 路径|❌ 未验收|V6 Vault 就绪后独立建立，不能依赖未启动的 V6 Vault 提供初始证书
:::

公共 Vault JWT 身份与 V6 Vault 内部认证分开管理；不使用静态 Vault token 兜底，不输出证书私钥、token 或 DSN。

**· 6.2 服务 KV 路径**

服务 KV 路径按 V6 所需收敛，不包含部署批次标识。路径是规划声明，不代表 Vault 记录、字段或 ESO 同步已实时验收。

:::table
服务范围|V6 KV 逻辑路径|使用边界
Accounts、Billing、Content 运行时及 OAuth 配置|`kv/prod/accounts/runtime`|三个服务按需从此路径映射运行时及 OAuth 配置；共享 token 也在此路径。目标 Kubernetes Secret 为 `web-saas-secrets`。OAuth 与其他敏感字段只交付给获准的消费者；若三者都挂载同一 Secret，则三者都能读取其中全部字段。
PostgreSQL DB|`kv/prod/database/postgresql`|PostgreSQL 初始化与运行所需身份凭据归入此路径范围；数据库侧仍按 admin、operator、auditor 三类身份分别授权。Vault KV 路径级策略不能隔离同一记录内的字段，ESO 读取身份和 Secret 投递范围需据此审查。
域名 TLS|公共 Vault `kv/CICD/domains/svc.plus`、`kv/CICD/domains/xworktech.com`|V6 按域名读取现有公共证书来源；不复制或迁移 V5 私有证书内容。具体证书字段与同步目标须在部署验收时核对。
:::

V6 验收仍需确认上述路径的 Vault 实存与字段合同、ESO 映射和目标 Secret 内容，以及 PostgreSQL 三身份权限边界；在完成核验前均标记为未验收。Vault 首次初始化和 unseal 材料由外部安全托管；新集群迁移时须人工初始化与解封，不将这些材料写入上述常规 KV 运行时路径。旧记录的复制、迁移或退役不属于本节声明。

**· 6.3 跨 namespace 访问契约**

:::table
链路|规划要求|运行验收状态
Caddy → UI/API|明确 Service FQDN 和端口，核对固定 chart 实际渲染名称|❌ 未验收
UI/API → PostgreSQL|集群内 Service；数据库不经 Caddy、不对公网开放|❌ 未验收
Caddy → Vault/Observability|独立路由及认证，启用后端 TLS 校验|❌ 未验收
Caddy 读取 TLS|Secret 位于 `ingress-prod`，由该 namespace 受控同步路径生成|❌ 未验收
NetworkPolicy|只开放必要链路，并实际验证 CNI 执行隔离|❌ 未验收
V6 DNS 与无 DNS 路由验收|先以受控解析覆盖验证 Host/SNI 和 TLS，再按第 14 节添加 V6 专属 DNS；V5 DNS 不变|❌ 未验收
外部 OAuth/Webhook|无真实外部回调证据时不能标通过|❌ 未验收
:::

**· 6.4 三权分立**

:::table
身份|职责与权限边界|已有状态
系统管理|主机、控制面、初始化及恢复；不作为日常业务进程或应用数据库连接身份|⚠️ root kubeconfig 可认证，但其 ClusterRole 当前缺 Pod/PVC 状态读取；PR #689 待审以补齐平台运维所需只读诊断能力
独立业务账户|服务独立 SA/Vault role/DB DML 角色；业务进程非 root；只授予必需对象权限|❌ 待逐服务部署与验收
强制只读审计|独立系统身份与 RBAC；允许必要状态读取，拒绝配置写入、Secret、exec、提权和业务数据写入|⚠️ Secret/写入/exec/RBAC/impersonation 均拒绝；工作负载状态读取不足，PR #689 待审
:::

当前真实审计身份为 X.509 用户 `auditor`（Groups: `system:authenticated`），不是 `cluster-audit` ServiceAccount。可读 nodes、namespaces；当前无权列举 pods、events、services、PVC、HelmRelease。Secret 读取、资源写入、`pods/exec`、RBAC 修改、impersonation 均拒绝；auditor 无 passwordless sudo。`operator` 认证身份为 X.509 用户 `operator`，当前仅能在 `web-saas-prod` 查看 Service/Deployment/HelmRelease 并缩放 Deployment。GitOps PR #689 补充 root/auditor 状态读取权限，尚未合并/调谐。

该回执不证明已有通用 SSH 审计登录或 Flux/PVC/业务数据的完整只读盘点权限，也不等于所有业务服务已经落实分权。

**▍7. 已有 V6 的续建策略与当前阻断**

当前运行阻断：Vault 未人工初始化/unseal（这是已约定的人工门禁）；PostgreSQL 的三个专用 Vault JWT reader role 在运行态不存在（ESO 日志明确报 role not found），DB 凭据未交付且 GHCR 镜像拉取未授权；Observability 缺少 DataKit/Grafana Secret，node-exporter 探针持续超时/重启；root/auditor 状态读取权限修复 PR #689 待审。Flux 的 Vault/PostgreSQL/Observability/Web SaaS/Ingress 单元未全部 Ready。PostgreSQL role 需要 Vault/Playbooks owner 经受控操作创建，不能由 Flux 读取 GitOps 声明自动替代 Vault 写入；之后再逐项由 Flux 调谐验证。不暂停 Flux、不重建集群或 PVC、不迁移数据、不修改 DNS，也不自动化 Vault 手动门禁。

**▍8. 数据、整体验收与未来升级**

**· 8.1 三类完成条件**

:::table
结果|状态|判定条件
冷启动通过|❌ 未完成|五个单元已安装，身份、TLS、存储和内部链路通过
数据与业务验收通过|❌ 未完成|审查后的 `migratectl` 迁移、数据比对、含业务数据的隔离恢复、真实回归及观察通过
可切换|❌ 尚未达到|在前两项通过后，另行评审最终追平、源写者隔离、流量切换及恢复方案
:::

**· 8.2 数据迁移与恢复要求**

- 迁移前 V6 业务写者、后台任务、真实支付和通知受控。
- 迁移源连接只读；V5 原业务写入方保留。
- 固定工具版本、源快照边界、目标身份、SQL schema 和迁移范围。
- 新集群使用空目标库和审查后的 schema；先验证备份恢复，再应用审查后的迁移计划。
- 记录数据比对、权限、应用实际连接、业务不变量和失败恢复证据。
- 对已导入业务数据的候选进行隔离备份恢复；空库恢复不能替代业务数据恢复。
- 源继续写入时，初次复制不等于零延迟追平；写者交接和流量切换单独评审。

❌ 本轮数据迁移、业务恢复、真实回归、重复运行、中断恢复和观察预算均未完成。

**· 8.3 后续版本发布规则**

:::table
类别|原地滚动发布规则|验收与恢复边界
前端 UI|纯展示、无状态变化可在所属单元发布|保留旧制品；验证页面、关键流程和错误率
API|小型、向后兼容且不改 SQL schema/持久格式的修复可原地发布|验证接口、回归、错误率；代码回退不等于数据回滚
独立监控服务|仅非业务、非账单且不涉及有状态存储版本/格式转换的明确例外可原地维护|固定单元版本，验收采集/查询，保留必要备份恢复证据
DB 与有状态组件|PostgreSQL、Vault Raft、监控存储、其他持久卷的版本或状态转换，以及 SQL schema 版本变化，必须在下一代独立集群和存储验证|保留源集群和原写入方；按审查后的路径迁移/恢复，不以镜像回退代替数据回滚
:::

未来代际使用独立 IaC state、集群身份、存储、Flux 配置引用和证据。V6 冷启动通过不代表下一版本升级已经通过。

**▍13. 泛化命名与幂等执行修订（2026-10-30，目标设计）**

✅ 本节规则已记录。❌ 通用声明渲染、流水线、Vault 授权与运行验收尚未按本节全部改造；本轮只调整文档。

**· 13.1 稳定对象名与批次隔离**

明确区分两层：**GitOps 环境入口**供 Flux CD 选择 SIT/UAT/PROD 声明，根 Kustomization 分别使用稳定名 `sit-k3s`、`uat-k3s`、`prod-k3s`；**批次环境实例**如 `prod-k3s-v6`，才对应本次独立节点、集群及目录、state、存储和凭据隔离。稳定根名不标识某台节点或某一批次。

:::table
GitOps 环境选择|Flux 根 Kustomization（namespace 为 flux-system）|批次环境实例示例|根 source path 示例
SIT|`sit-k3s`|`sit-k3s-v6`|`environments/clusters/sit-k3s-v6`
UAT|`uat-k3s`|`uat-k3s-v6`|`environments/clusters/uat-k3s-v6`
PROD|`prod-k3s`|`prod-k3s-v6`|`environments/clusters/prod-k3s-v6`
:::

本表是命名对照，不代表三个示例批次均已创建。根名由所选 GitOps 环境派生；实际目标仍由批次声明、CMDB 和经过验证的集群连接共同确定，不能仅凭根对象名称选择或证明目标。

同类环境在基础规格与组件候选不变时，先选择 `gitops_environment`，每次新建批次只填写 `deployment_batch` 和 `node_hostname`。其他目标路径和资源名统一派生，不逐个文件手改 `v6`。以下是设计接口示例，尚非现有执行器已支持的 schema：

:::code
gitops_environment: prod
deployment_batch: v6
node_hostname: prod-k3s-v6
:::

统一派生 `flux_root_name = <gitops_environment>-k3s`，再派生 `environment_instance = <flux_root_name>-<deployment_batch>`；本例分别为 `prod-k3s` 和 `prod-k3s-v6`。批次目录通过共享 base/默认配置和本批次 overlay 生成可审查声明；不人工复制一套执行 role、工作流或版本判断分支。批次与 hostname 是两个独立输入，不靠反解析 hostname 猜批次。

:::table
配置项|稳定部分|V6 解析结果 / 下一批次行为
GitOps 环境入口|`sit-k3s` / `uat-k3s` / `prod-k3s`|从 SIT/UAT/PROD 环境选择派生；跨环境另选配置，不隐式回退到 prod
批次环境实例|派生公式不变|`prod-k3s-v6`；下一批次如 `v7` 则为 `prod-k3s-v7`
节点 hostname / inventory / K3s node name|使用同一个输入|`node_hostname`；不与根 Kustomization 名绑定
根 Flux Kustomization|`flux-system/prod-k3s`|每个独立集群内同名；根不再叫 `prod-k3s-v6`
根配置源|`flux-system/config-prod`|同一仓库 URL，固定该批次审查后的 tag/commit
根调谐路径|`environments/clusters/<environment_instance>`|`environments/clusters/prod-k3s-v6`
子调谐路径|`services/<environment_instance>/<unit>`|`services/prod-k3s-v6/vault-prod` 等；由相同批次环境实例派生
子 Kustomization / namespace / HelmRelease|现有 `vault-prod`、`postgresql-prod`、`observability-prod`、`web-saas-prod`、`ingress-prod` 及其 release 名|各独立集群内复用名称，不添加批次后缀；ESO/TLS 前置也保持稳定名
IaC target / state / 云卷归属|派生规则与 provider/account 配置|target、state namespace 和卷标签包含 `environment_instance`，不复用旧批次 state 或数据盘
K3s 三身份 Vault KV|`kv/<environment>/<cluster>/<role>` 契约|`<environment>` 取已选 GitOps 环境，`<cluster>` 取独立的 `environment_instance`，如 `kv/prod/prod-k3s-v6/auditor`；不能改为所有批次共用一条稳定根名对应的凭据记录
OS SSH 公钥|`kv/<environment>/security/<role>`|环境级公钥保持现有约定；不混入集群客户端私钥
执行与验收回执|固定字段与校验规则|记录批次、hostname、实际实例 ID、节点 UID、集群标记、卷 UUID、声明 SHA 与 run ID；每个新目标重新取证
:::

这里的 source path 准确对应 **`Kustomization.spec.path`**；`GitRepository.spec.ref` 是独立的配置版本引用。根对象使用稳定名称，但其 path 随批次改变，例如：

:::code
metadata:
  name: prod-k3s
  namespace: flux-system
spec:
  path: ./environments/clusters/prod-k3s-v6
  sourceRef:
    kind: GitRepository
    name: config-prod
:::

该片段仅说明命名，不是完整可部署对象。V7 在新集群仍创建 `prod-k3s`，path 指向 `prod-k3s-v7`；**不能把旧集群的 path 改成新批次目录来代替创建新集群**。同名根安全复用的前提是 Kubernetes 集群本身独立。

“每次只变批次与 hostname”指目标配置输入。IaC、GitOps、Playbooks、Orchestrator 默认从 `main` 执行，必要选择由 `workflow_dispatch` 参数控制；运行回执记录实际解析到的 SHA 用于审计，不把基础仓库 tag 作为每轮发布前置。业务 chart、镜像及 SQL schema 候选按各自不可变制品/版本规则管理；批次名不充当工作流代码版本或应用制品版本。

**· 13.2 一份目标声明驱动所有阶段**

:::code
# mermaid
flowchart LR
  D["固定 GitOps 环境配置<br/>批次 + hostname"] --> R["统一解析目标<br/>派生路径、state、凭据引用"]
  R --> I["IaC 创建或对账<br/>输出权威 CMDB"]
  I --> O["vhosts/common<br/>OS 三账户与主机基线"]
  O --> K["K3s bootstrap<br/>控制面、Flux、三身份、ESO、Ingress 控制器"]
  K --> F["Flux 接管稳定发布单元<br/>按已审查声明与门禁调谐"]
  F --> V["验收实际 revision、身份、TLS、卷和业务链路<br/>形成批次回执"]
:::

- 控制面、IaC、Playbooks、Flux 与验收器消费同一份解析结果，不分别维护 `prod-v6` 白名单、固定 hostname、根名等第二套目标矩阵。通用 root 名、node 名、批次路径必须分别传递和校验；不能继续要求 `root_name == node_hostname`。
- 目标配置放在 GitOps；执行器保留通用接口。组件清单按选定候选声明核验，避免以永久写死的对象数量替代所有权、路径、版本及健康检查；缺失必需对象仍须拒绝放行。
- Vault writer 和公共 Vault TLS reader 的批次授权由受控身份配置流程消费同一目标声明，派生本批次精确路径、签名公钥和角色绑定。可以自动生成目标专用 role/policy，但不要求每次手写一套代码；不能用跨批次通配读写授权代替自动化。该授权自动化尚未实现。
- 初始化回执通过后，服务资源由 Flux 调谐，流水线只负责已声明门禁、状态观察与证据汇总。ESO 与 Ingress 控制器属于初始化；Vault → PostgreSQL → Observability → Web SaaS 的首次部署按阶段验收，正式 Ingress 路由最后验证，再按第 2.1 节核验并由 DNS owner 处理 V6 批次域名解析；V5 DNS 始终不切换。
- 放行状态必须进入固定 GitOps 声明；后续发布不靠重复 SSH apply/resume。监控验收顺序不成为业务发布的永久依赖，真实存储、身份和证书依赖仍保留。

**· 13.3 幂等与恢复契约**

:::table
场景|预期行为与证据
同一批次、同一 hostname、同一 dispatch 输入及相同解析 SHA 的幂等重试|核对实际实例/节点/集群/卷身份后继续；不重复创建资源、不格式化已验收数据盘、不重签 CA，不无条件重启。记录变更量及健康结果。若 `main` 已前进，则作为新的代码候选重新验证并记录 SHA，不把旧 SHA/tag 当成基础仓库默认版本
同一 state 输入变为另一 hostname、provider、账户或批次|拒绝隐式替换；新批次使用独立 state 和存储，不能以“幂等”名义销毁旧资源
同一目标已完成部分阶段|验证对应回执仍匹配目标与候选，跳过已完成部分，从首个未通过门禁继续；不把 active Flux 图重新变成全部暂停，不退回旧声明覆盖现场
三身份初始化及 Vault 归档重跑|同一实际集群下复用一致且有效的节点私有凭据，验证信任链与 Vault 回读；首次归档 CAS 防覆盖。过期、不同记录或部分签发失败进入受控修复/轮换，不无限自动重签
节点删除后同名重建|hostname 相同不等于原集群。实例 ID、集群标记或卷归属变化使旧证据失效；不得自动复用旧 CA、凭据或有业务数据的卷。目标身份冲突时改用新批次，或执行另行审查的恢复流程
Flux 日常独立发布|稳定 KS/HR 名称不变，只推进被选中单元的不可变配置/制品引用；其他单元保持原候选。数据/SQL schema 状态转换仍使用下一批次新集群
失败、并发与复验|同一目标加锁，禁止两个运行同时初始化；保留已创建资源、受保护签发状态和脱敏失败回执，重试前对账。候选或实际目标改变时，重验受影响阶段，不能沿用旧 PASS
:::

凭据例行轮换属于独立生命周期任务，不通过重跑冷启动来实现；需要精确的更新授权、消费者切换及旧凭据退出证据。上述幂等规则是目标契约，现有“仅接受全图暂停”的 bootstrap 还不能直接用于任意阶段恢复。

**· 13.4 当前实施差异**

`prod-k3s` 管理根及 Flux 控制器已在当前节点观察到，root/operator/auditor X.509 kubeconfig 均可认证；root/auditor 状态 RBAC 尚待 PR #689，PostgreSQL Vault 身份交付和应用服务验收仍未完成，以顶部最新状态为准.

**▍14. PROD-K3S-V6 批次域名规划与验证边界（2026-10-30）**

本节域名方案按用户给出的 V5 现状命名，并把 PROD-K3S-V6 的批次名称与 DNS 开通、服务上线分别管理。**域名分配不代表 DNS 已创建，不代表 TLS 已就绪，也不代表服务已验收。** 用户已要求 V6 专属域名最终解析生效；新增记录须使用新 V6 节点地址，V5 canonical 域名不改，V6 名称不指向 V5。`dns_mode=none` 继续保护 canonical 名称；六个 V6 专属记录另经受控 DNS owner 更新。

**· 14.3 声明与放行状态**

- Console、Accounts、Billing 的 Caddy 路由与节点 `service_domains` 采用本节确认名称；Observability 保留 `observability-k3s-v6.svc.plus`。六个指定域名都需要 DNS 解析到 V6 新节点；PostgreSQL 端口仍关闭，Vault/API 和 Observability 访问仍受入口及认证策略限制；Content 不再以旧名称作为已分配域名。
- GitOps 声明与本节方案已提交 [GitOps PR #672](https://github.com/ai-workspace-infra/gitops/pull/672)，归档提交在 [Docs PR #1](https://github.com/ai-workspace-infra/docs/pull/1)；均待审查。当前没有合并或发布的 V6 域名版本。域名方案进入 PR 不等于 DNS 变更或运行验收。
- 新增 DNS 前先对 V6 节点 IP 使用 `curl --resolve <host>:443:<V6-IP>` 验证适用的 Host/SNI 和证书；不得跳过证书校验。PostgreSQL 域名解析不代表开放 Caddy 路由或 5432 端口。
- 新增 V6 专属 DNS 记录是用户已明确提出的目标，但实际改 DNS 尚未执行；`dns_mode=none` 只禁止默认更新 canonical 域名。应由受控 DNS owner 对六个确切 V6 批次名称新增解析，目标取本次 IaC/CMDB 核实的 V6 节点地址；记录只负责名称解析，不自动授权开放 PostgreSQL 端口或 Vault 管理/API。六个不更新的 canonical 名称为 `vault.svc.plus`、`observability.svc.plus`、`console.svc.plus`、`accounts.svc.plus`、`billing.svc.plus` 和 `postgresql.svc.plus`。
- 证书签发/更新、V5 canonical 切换、外部 webhook/业务流量、数据库公网接入都需要各自独立的审查与授权；不得由冷启动或 `service_domains` 清单隐式触发。V5 canonical 切换不属于本次 DNS 目标。

**▍16. 服务凭据路径与 Vault 初始化方案确认（2026-10-30）**

本节记录用户最新确认，替代此前建议的 `kv/prod/services/prod-k3s-v6/...` 业务凭据前缀及“初始化托管方案待确认”的状态。**✅ 路径与托管规则已确认；❌ 记录存在性、字段适配、最小权限及运行验收尚未完成。** 文档更新不代表已读取、创建、复制或修改任何 Vault 记录。

**· 16.1 不带部署批次版本的服务 KV 路径**

当前路径与使用边界见第 6.2 节，不重复维护另一份清单。

**· 16.2 公共 Vault 域名 TLS 来源**

:::table
TLS 证书所属域|公共 Vault KV 逻辑路径|实施要求
`svc.plus` 及实际 SAN 覆盖的域名|`kv/CICD/domains/svc.plus`|路径不变；V6 的 `vault-server-tls` 和对应 Ingress TLS Secret 按实际域名映射
`xworktech.com` 及实际 SAN 覆盖的品牌域名|`kv/CICD/domains/xworktech.com`|保留独立来源；按实际路由域名选择证书，不能用 `svc.plus` 证书替代
:::

现有消费者使用 `tls_fullchain_pem_b64` 与 `tls_key_pem_b64`，实际字段存在性仍需验收。公共 Vault 地址仍为 `https://vault.svc.plus`，只读身份按所需精确路径授权；不因加入第二条来源就扩大为 `kv/CICD/domains/*`。

TLS 同步必须验证证书有效期、完整链、证书与私钥匹配及实际 SNI/SAN。公共域名证书不自动覆盖 `*.svc.cluster.local`，集群内 Vault TLS 仍须使用有效验证名称或受控内部 SAN 证书，不能关闭校验。加入证书来源不增加 DNS 或公网路由授权；第 14 节 V6 专属域名及 canonical 禁止变更边界继续生效。

**· 16.3 Vault 初始化/unseal：外部安全托管与手动操作**

- ✅ 初始化及 unseal 材料采用外部安全托管；不在本节服务 KV 中新增 root token/unseal shares 记录。
- ✅ 迁移过程中通过受控管理通道手动初始化新 Vault，并手动完成所需 unseal。本轮不引入自动初始化或 Transit/KMS auto-unseal。
- 执行前核对实际新集群/实例及 Vault 的 `initialized`、`sealed` 状态；仅对未初始化的新目标执行 init。已初始化的实例不得重复初始化。
- 新目标使用自己的初始化材料。旧 Raft 快照恢复、加入已有 Raft 集群及其材料使用采用对应恢复流程，不能将旧 unseal shares 当作新初始化材料。
- root token、unseal shares 不交给 IaC/GitHub Actions，不写入 Git、workflow inputs、artifact、日志或聊天。流水线只观察 `initialized=true`、`sealed=false` 和服务健康，不输出材料。
- ❌ 外部托管完成、手动初始化/unseal 及新 Vault 健康证据尚未验收。门禁未通过时停止后续服务验收，不能把安装成功记成 Vault 可用；完成后按同一候选继续，无需重新创建节点或存储。

**· 16.4 来源核对与当前实施状态**

V5 K3s 的业务 SecretStore 声明指向 `https://vault-raft.platform-vault.svc.cluster.local:8200`，其业务来源包括 `kv/prod/services/web-saas-k3s-v5/database`、`.../jwt`、`.../tls` 和 `.../brand-tls`。这些是旧集群内 Vault 的声明引用，不能据此认定公共 Vault 已有相同记录。旧 Selfhost/Compose 另有 `kv/prod/databases`、`kv/WEB_SAAS` 等入口，不作为 V6 的默认 fallback。

来源文件：GitOps `services/distributed-web-saas-fullstack/prod/{external-secret,secret-store}.yaml`；Playbooks `roles/vhosts/vault_operator_material/README.md`；白皮书配套 `knowledge/docs/reference/platform-ops-toolkit/04-security-vault-and-iam/{kv_tier_model,manual-unseal}.md`。这里只核对路径、字段与规则，没有读取秘密值。

GitOps [草稿 PR #673](https://github.com/ai-workspace-infra/gitops/pull/673) 正在清理 V6 混合暂停状态和已删除节点的旧回执引用。完整冷启动 DAG、三身份交付、ESO 字段映射及服务验收仍在配套实现，不能将本节确认写成部署完成。

### 18.7 实践变化 1　运维看板与全量 Routes & APIs 资产矩阵

来源：`knowledge/docs/reference/platform-delivery/Web-Console-前端全量路由与后端微服务-API-目录统计白皮书.md` 及 2026-11-08（北京时间）的控制台与 Grafana 截图观察。本节是摘要式改写，不全文收录；截图数字只代表当时界面，不是独立验收，也不是发布授权。示例地址统一用 `console.example.com`、`accounts.example.com`、`billing.example.com`。

**▍一页三个视图，不能互相替代**

运维看板从上到下是三张表：**核心健康矩阵**（Service × Endpoint，10 个精选指标）、**Flagger 渐进发布权重矩阵**、**全量 Routes & APIs 三级折叠树**。核心矩阵只挑 10 个端点做门禁，全量树登记全部资产；「门禁 10 项全过」不等于「181 项资产都健康」，反过来也一样。

:::table
视图|回答什么问题|数据来源
核心健康矩阵|这次发布能不能放行|探针指标：结果、HTTP 码、时延、新鲜度
Flagger 权重矩阵|流量现在切到哪里|Canary Phase 与候选权重
Routes & APIs 三级树|我们到底有哪些页面和接口，各自状态如何|静态资产目录 + 动态遥测
:::

**▍三级树：前端 / 后端 → 大类 → 路由或接口**

一级是前端页面与后端接口两棵根；二级是功能大类（子组件），带中英文名和 `fe-*` / `be-*` 标识；三级是逐行明细：Method、Path、Service、Description、Expected、Observed、Latency、Result（控制台另有 Age 列，Grafana 把新鲜度放在 Top 10 明细表）。两级都能折叠，支持一键展开/收起和全文搜索（路径、微服务、大类、描述）。

截图当时目录共 181 项：前端 65 项 7 大类，后端 116 项 8 大类。

:::table
标识|前端大类|条目
`fe-portal`|产品、服务与门户|16
`fe-panel`|平台运维与控制台|13
`fe-support`|客户支持与服务条款|10
`fe-docs`|知识库、文档与博客|8
`fe-auth`|统一身份认证与用户中心|7
`fe-edge`|边缘套件与基础设施工具|7
`fe-workspace`|智能体与工作空间|4
:::

:::table
标识|后端大类|条目
`be-auth`|身份认证与用户账户|26
`be-admin`|平台治理与管理控制台|23
`be-billing`|商业化、计费与订阅|17
`be-ops`|运维监控与发布门禁|14
`be-agent`|AI 智能体与工作空间|13
`be-content`|文档检索、营销与集成服务|13
`be-mfa`|MFA 多因素安全认证|6
`be-edge`|边缘协同与互联网络|4
:::

**181 是生成结果，不是常量。** 目录从源码生成（页面路由文件 + API 路由文件，按 service + method + path 去重），新增页面后计数自然变化。一个实际教训：控制台截图只露出 6 个前端大类，标题却写 7 类 65 项；缺的那一类（智能体与工作空间，4 项）是从另一张截图和源码目录补齐的，而不是凭空猜一个名字填上。另一个缺口仍然开着：Accounts / Billing 目前只登记了健康与就绪探针，它们自己的业务 API 还没从各自仓库枚举。

**▍静态目录 + 动态遥测 + 来源标签**

:::table
状态|含义|不能被当成
`PASS` / `FAIL`|来自真实遥测的判定|—
`NO DATA`|该资产没有有效观测|PASS，也不是 FAIL
`NOT PROBED`|POST/PUT/DELETE、退出登录、退订、动态模板路径：只登记不探测|缺陷
`—`|单元格不适用（别的服务的端点）|失败
`mock` / `preview`|设计样例数据|发布依据；门禁只显示 PREVIEW，永远不出 ALLOWED
:::

三条容易踩的坑：其一，资产采集不等于对每个 API 发请求，为了「发现接口」去调 DELETE 或 `/logout` 是事故；其二，`probe_success` 是 gauge，对它做 `increase` 得不到请求数，候选样本要来自真正的请求计数器；其三，只有 `probe_duration_seconds` 这种 gauge 时算不出 p95，界面上要老实写「最近一次耗时」。

### 18.8 实践变化 2　Flux + GitOps + Flagger + Traefik：一条链，四份证据

来源：platform-delivery 下的架构、Vault 工作负载身份契约（记录了入口流量割接到 Traefik）与上述白皮书。第 6.8、6.9 节讲了工具，这里讲它们在一次真实发布里怎么分工。

`Git 期望状态 → Flux 调谐 → Flagger 渐进分析 → Traefik 加权路由 → 探针与指标 → 控制台 / Grafana 只读展示`

:::table
环节|证据|它证明不了什么
Git / PR 合并|commit SHA、评审记录|集群已经收敛
Flux 调谐|Kustomization / HelmRelease Ready 与 revision|新版本健康
Flagger 分析|Canary Phase、当前权重、分析指标|入口真的按比例分流
Traefik 加权路由|入口权重配置与入口侧请求计数|业务验收通过
看板展示|只读汇总|它不向控制器下发放行指令
:::

四份证据各自独立，**不能合并成一个绿灯**。看板里也没有为了「体现 Flux / Traefik」去虚构业务 API：相关的运维与发布门禁接口都已在 `be-ops` 大类里登记。

**▍证据冲突要保留，不要挑一个赢家**

同一天的三份材料对金丝雀状态说法不一：

:::table
来源|Console|Accounts|Billing
白皮书|Progressing|Progressing|Not configured（空权重）
控制台截图|Progressing 20%|Succeeded 0%|Succeeded 0%
Grafana 截图|Progressing 20%|Progressing 10%|Progressing 10%
:::

源码里能找到一个可能的解释：BFF 拿不到 Flagger 指标时会按环境给出默认降级值（PROD 视为 Succeeded 0%、SIT 视为 Progressing），这会让「遥测缺失」看起来像「已成功」。正确的做法是把四种状态分开：**确认未配置**、**进行中**、**已成功**、**遥测缺失（Unknown）**；最终以集群里的 Canary 资源和 Flagger 指标核实，再回头修文档。

**▍门禁规则**

任一端点失败、数据过期、缺少样本（NO DATA），或候选请求样本不足（下限 10,000），发布即 BLOCKED。mock 或降级数据不能产生 ALLOWED；缺样本时宁可显示 UNKNOWN 并阻断。

### 18.9 实践变化 3　platform-delivery 其他新增材料（摘要）

18.1–18.6 收录于 2026-11-01。之后 platform-delivery 新增或更新了下列文档。它们多为规划或某一时刻的验收记录，这里只摘结论和边界；状态一律按「规划 / 已合并 / 已交付 / 已验收」分开读。

:::table
主题|文档状态|要点
双轨可观测：VictoriaMetrics 权威源 + 商业 SaaS（MetricMap 映射）|SIT 验收记录|权威源零扰动；双写分路由；指标名映射集中维护
DataKit 跨云采集与 OpenTelemetry 数据网关|交付白皮书|K3s、Serverless、边缘节点统一经网关出口；自建留存与 SaaS APM 各取所长
Grafana 独立数据库与 GitOps 持久化|目标架构，未迁移|共用 PostgreSQL 实例、独立 `grafana` 库与专用账户；删 Pod/namespace 不得连带删库；外置数据库不等于高可用
Grafana 租户隔离与 Portal 嵌入|待实现|Portal 权益 → Grafana Organization → 查询授权三层；Dashboard 变量不是权限边界
Grafana 面板丢失排查与 21 面板数据流验收|恢复与验收记录|先分清「列表为空 / 组织错 / 无权限 / 无数据 / 插件缺失」；修复前后对面板模型做规范化校验和，零篡改
通用 Vault 工作负载身份契约|设计，调用方未完成|每个集群独立的 JWT 认证挂载与最小权限 reader 角色；创建命令只作模板，不重跑覆盖
SIT 模块化交付与特性泳道|规划|基础 / 服务 / 业务模块化组合，Playbook 引导节点底座，Flux 装配模块
Agent 交付：本机 QMD 接力与 Knowledge 归档|规划与实践|任务状态放结构化存储，结论进 Knowledge PR，再重建索引；敏感现场证据只归档脱敏摘要
Hand-Off 交付与交接报告|某次交接终态|三权分立审计身份只读核验 + 双轨采集拓扑；是当时的回执，不是今天的线上状态
:::

**▍多环境是交叉维度，不是一条直线**

第 6.12 节已经说过：环境、分支、滚动发布、特性泳道是四个相互交叉的维度。上面的材料再次印证了这一点——SIT 独立节点用特性泳道单独验收某个功能，PROD 用 Flagger 小比例放量，两者并不排成 `SIT → UAT → PROD` 的唯一阶梯。

:::table
维度|可选取值|由谁决定
环境|SIT、UAT、PROD，或某个客户专属空间|资源与数据隔离要求
分支 / 版本|main、release、feature 分支对应的构件摘要|Git 与制品仓库
发布方式|直接替换、滚动、金丝雀加权、指定测试人员|风险与样本量
特性泳道|按功能开关或路由隔离的子流量|业务验收范围
:::

一次发布取各维度中需要的那一格组合起来：例如「feature 分支构件 + SIT 环境 + 指定测试人员 + 单一特性泳道」，或「release 构件 + PROD + 金丝雀 10% + 全量用户」。看板与资产矩阵按「环境 × 服务」展示，正是为了让任何一个组合都能被同一套证据检验。
