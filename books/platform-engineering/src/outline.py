# Chapter outlines for unwritten chapters (opener pages). Summaries avoid unverified dates.
O={
'1':('从 GNU 与自由软件运动讲起：copyleft 与 GPL 的思想，Linux 与开源社区，Red Hat、SUSE 的订阅与服务模式，Debian 社会契约代表的社区发行版，再到国内的大中台、小中台与今天的平台工程。一章五节，只做铺垫，后面全部讲实践。',
 ['1.1 自由软件','1.2 开源社区','1.3 开源商业：Red Hat 与 SUSE','1.4 社区发行版：Debian','1.5 从中台到平台工程'],'process-exporter（使用社区上游）、postgresql.example.com（开源 + 服务）'),
'2':('所有变更都从 commit 开始、走流水线。自建 Gitea + Gitea Actions 与 GitHub + GitHub Actions 对等讲：同一套工作流两边运行，CI 只读验证、产出不可变构件；GitOps 声明按 URL + ref 引用；合同测试守住跨仓库接口。',
 ['2.1 为什么一切变更都走流水线','2.2 为什么不是 Jenkins / GitLab CI','2.3 Gitea + Gitea Actions：自建入口','2.4 GitHub + GitHub Actions：对等对照','2.5 Reusable Workflows 与组织基线','2.6 触发路由：PR、main、tag 各走各的路','2.7 发布分支与 PR 校验'],'.github、Platform-Orchestrator、gitops'),
'3':('环境应该 apply 就出来。用 OpenTofu 管资源，模块化、按 SHA 钉住引用，Remote State 自建，plan 阶段就暴露替换风险。',
 ['3.1 资源即代码的边界','3.2 OpenTofu 与开放许可','3.3 模块设计与版本钉住','3.4 自建 Remote State 与锁','3.5 plan guard：替换前先报警','3.6 多云 provider 组织'],'iac_modules、Platform-Orchestrator'),
'4':('软件要幂等地装上去。Ansible 按 role 组织、按场景编排，inventory 从自建 CMDB 动态生成，杜绝硬编码 IP；Golden Image 与 Helm chart 作为不可变交付物。',
 ['4.1 交付引擎的职责','4.2 Ansible role 与场景 playbook','4.3 自建 CMDB 与动态 inventory','4.4 幂等、check 与 diff','4.5 Golden Image 与 Helm chart','4.6 固定提交执行'],'playbooks、artifacts'),
'7':('一套配置部署到任意云。多云 IaC、VPS 与裸金属、K3s/K8s，加上不绑定任何云厂商的 PostgreSQL + pgvector，让退出成本始终可控。',
 ['7.1 什么是云中立','7.2 VPS 与裸金属：不是云的虚拟云','7.3 K3s/K8s 统一运行面','7.4 编排器：Selfhost / Serverless / Hybrid','7.5 自建数据库：postgresql.example.com','7.6 退出成本自评'],'iac_modules、postgresql.example.com、Platform-Orchestrator'),
'8':('没有仪表盘的车开不久。Metrics、Logs、Traces 全链路，Grafana 与 VictoriaMetrics / VictoriaLogs 自建，采集端与控制端分离。',
 ['8.1 可观测的三根支柱','8.2 Grafana + Victoria 全家桶','8.3 采集端：Vector 与 exporter','8.4 告警与值班','8.5 数据库与身份感知诊断'],'observability.example.com、postgresql.example.com'),
'9':('能恢复才算稳定。备份、迁移与灾备变成日常：不可变快照、数据库备份与恢复演练、跨主机迁移。',
 ['9.1 稳定的定义：能恢复','9.2 不可变快照与回滚','9.3 PostgreSQL 备份与恢复演练','9.4 跨主机迁移','9.5 灾备演练日常化'],'artifacts、postgresql.example.com、Platform-Orchestrator'),
'10':('AI 时代平台要接入模型、把运维交给 Agent。ai-aggregator 作为开源 AI 聚合网关（New API + LiteLLM），Infrastructure-MCP-Server 用 MCP 把 IaC、CMDB、运行时工具交给 Agent。',
 ['10.1 为什么需要 AI 聚合网关','10.2 ai-aggregator：New API + LiteLLM','10.3 额度、权限与成本','10.4 MCP 与 Infrastructure-MCP-Server','10.5 Agent 运维的边界与审计'],'ai-aggregator、Infrastructure-MCP-Server'),
'11':('把七层拧成一个 Open Platform：成熟度自评、开放标准清单，用代码生成的架构图描述你的平台走到了第几层。',
 ['11.1 七层回顾','11.2 成熟度自评表','11.3 开放标准清单','11.4 架构图即代码：diagram-generator','11.5 下一步'],'diagram-generator、.github、Platform-Orchestrator'),
}
# ---- 下篇骨架（v0.9）：每节 (标题, 待写摘要) ----
SK={
'12':('规范即事实源：人和 AI 守同一本规则','平台的规则不该只存在于人的脑子里。把工程与运维规范写成版本化的事实源，人和 AI Agent 按同一本规则做事、被同一套门禁检查。',[
 ('12.1 为什么规范要成为事实源','口头约定会走样，写进仓库、按版本引用的规范才可检查、可追溯。'),
 ('12.2 13 项工程规范','Harness 工作流、Issue/PR 溯源、分支纪律、CI/CD 规约、执行归属、多环境发布、代际升级验收、IaC、Config-as-Code、GitOps 事实源、AI 代理协作、官网规范、零信任 Overlay。'),
 ('12.3 8 项运维标准','备份恢复与迁移、事件响应与变更、密钥身份与访问、网络 DNS TLS 与边缘、可观测 SLO 与告警、容量成本与生命周期、服务目录与 Runbook、GitHub Actions 运维分发。'),
 ('12.4 版本化绑定：规范的不可变快照','流水线与 Agent 按 tag 或摘要引用某一版规范，规范升级走 PR，与第 6 章不可变构件同一思路。'),
 ('12.5 AI 代理协作标准','工作区脏检查、越权拦截、错误自检、破坏性操作熔断：Agent 的执行纪律与权限边界。')]),
'13':('开发者门户与黄金路径','一个入口看见平台的全部；黄金路径把规范串成模板，让「正确的做法」成为最省事的做法。',[
 ('13.1 一个入口：Cloud Hub / Operations / Releases','console.example.com 的三个视图：资源与服务目录、运维动作、发布与快照。'),
 ('13.2 黄金路径 = 规范串成模板','把第 12 章的规范按场景串成可复用模板，新项目从模板出发而不是从零开始。'),
 ('13.3 四条典型路径','静态站点、Web 服务、数据库、AI 应用：各自的模板、默认门禁与交付形态。'),
 ('13.4 偏离也要写进合同','需要偏离黄金路径时，按 5.5 的做法把例外写成有期限、可审计的合同。')]),
'14':('自助服务与外部集成','开发者自己申请资源，平台按策略自动交付；外部服务也以代码方式接入。',[
 ('14.1 自助链路：申请 → 策略/审批 → 交付 → 凭据 → 门户','申请经策略判定或人工审批，由 OpenTofu + Ansible 交付，凭据由 Vault 下发，结果回到门户。'),
 ('14.2 三种权限形态：全自助 / 审批 / 只读','按风险与环境划分：SIT 多数全自助，PROD 变更走审批，敏感资源只读展示。'),
 ('14.3 外部集成：CDN/DNS、监控告警、对象存储、通知、身份','常见外部服务的接入方式、凭据边界与退出成本。'),
 ('14.4 集成即代码','外部集成的配置同样进 Git、走 PR、可回滚，而不是在各家控制台里手工点。')]),
'15':('AI 辅助驱动业务应用平台维护','把观测、诊断、变更、复盘连成闭环：人看板、AI 值守，每一步可审计。',[
 ('15.1 维护闭环：观测 → 诊断 → 建议/执行 → 验证 → 复盘写回','闭环的每一环由谁做、留什么证据、在哪里停下等人。'),
 ('15.2 Releases / Operations：人看板，AI 值守','人通过门户看板决策，AI 在边界内做巡检、预诊断与低风险操作。'),
 ('15.3 安全边界：熔断、审批与回滚','破坏性操作熔断、需要审批的动作清单、默认可回滚。'),
 ('15.4 衡量：是否真的更稳、更省','用恢复时间、变更失败率、告警噪音、人工介入次数等指标衡量，而不是只看「用了 AI」。')]),
'16':('全书收尾：从七层平台到 AI 原生平台','回到全书：上篇的七层是地基，下篇的规范、门户、自助与 AI 值守是在地基上加的闭环。',[
 ('16.1 两篇回顾：经典回路与现代闭环','上篇每一层是一个单回路，下篇把它们并成一个以平台状态为中心的闭环。'),
 ('16.2 AI 原生成熟度自评','在 10.3 七层成熟度自评基础上，增加规范、门户、自助、AI 值守四个维度。'),
 ('16.3 下一步','从哪一层、哪一条黄金路径开始，以及本书后续版本的更新方向。')]),
'17':('最佳实践参考','按主题合并案例摘要、完整设计参考与近期实践变化；规划、已合并与待验收分别标注。',[
 ('17.1 总体架构　OpenplatForm Delivery Architecture','基础运行环境、统一架构、多环境发布、观测与安全边界。'),
 ('17.2 Linux OS 三类操作身份','Case A 摘要与 OS 三身份完整草案。'),
 ('17.3 K3s/K8s role：职责与依赖清单','Case B 摘要与 role 职责、依赖完整草案。'),
 ('17.4 环境与业务发布解析：最小实施','Case C 摘要与环境、业务发布解析完整草案。'),
 ('17.5 GitHub Actions 流水线实施草案','五父流水线保留、子流水线单一职责重构。'),
 ('17.6 PROD-K3S 变更记录与冷启动规划','Case D 变更记录模版与独立节点冷启动规划、状态归档，分别保留。'),
 ('17.7 运维看板与全量 Routes & APIs 资产矩阵','核心健康、渐进发布权重与全量资产矩阵的边界。'),
 ('17.8 Flux → GitOps → Flagger → Traefik：一条链，四份证据','调谐、分析、路由与看板的独立证据。'),
 ('17.9 近期 platform-delivery 实践变化（摘要）','后续材料摘要与多环境交叉维度。'),
]),
}
for k,(t,summ,secs) in SK.items(): O[k]=(summ,[a for a,_ in secs],'xworkspace-core-skills（规范）、console.example.com（门户）、Platform-Orchestrator、gitops')
