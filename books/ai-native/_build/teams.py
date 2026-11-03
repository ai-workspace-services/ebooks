# v0.9.6：2.5 附 · 组队两大代表（据官方 README，2026-10-31 查看；未实测）
add(f'''<div class="kicker">2.5 附 · 组队 · 从对话到团队</div><h1>AI 组队的三段进化：对话 → 任务 → 团队</h1>
<div class="lead">一个人单刷，靠的是对话；带一支小队，靠的是任务和规矩。</div>
<div class="gp"><p>第一段是<b>对话</b>：你问，AI 答，一问一答都在一个窗口里。第二段是<b>任务</b>：你交代一件事，它自己拆步骤、跑工具、交结果。第三段是<b>团队</b>：好几个 Agent 各占一个座位，有人派活、有人干活、有人审，你只在关键处拍板。</p>
<p>到了团队这一段，难的不再是「它会不会写」，而是三件事：<b>谁能碰什么</b>（权限与审计）、<b>活怎么分不打架</b>（分支、领取、状态）、<b>出事时人怎么接手</b>（暂停、接管、撤销）。</p>
<p>这一节挑两个开源代表细看：<b>OpenBot</b>（CopilotKit）管「办公室里的 AI 同事」，<b>Agent Orchestrator</b>（Orchestrator.inc）管「一群写代码的 Agent」。一个偏治理，一个偏交付，正好对应主城里的两条线。</p></div>
{tbl(['阶段','你的角色','关键问题'],[('对话','提问者','答得对不对'),('任务','派单人','做没做完、证据在哪'),('团队','队长 / 审批人','谁能碰什么、怎么不撞车、怎么接管')])}
<div class="note">以下能力均摘自两个项目的官方 README（2026-10-31 查看），作者未部署、未实测；正式试点前请固定 release 版本再核对。</div>''','02 组队 · 三段进化',bm='　2.5 附 组队：OpenBot 与 Agent Orchestrator')

add(f'''<div class="kicker">2.5 附 · 代表一 · OpenBot</div><h1>OpenBot：给每个 AI 同事一台「被看着的电脑」</h1>
<div class="lead">定位：一个可以自己拥有的 AI 助手平台模板——跑在你的基础设施上，MIT 许可，Beta。</div>
{its([('是什么','官方自称「模板而非产品」：没有托管版，克隆后把示例租户换成你自己的同事、频道与技能。Docker Compose 拉起，数据在自己的 PostgreSQL，模型和 Key 由管理员自配。'),
('怎么组队','任何讲 AG-UI 协议的 Agent（LangGraph、Mastra、CrewAI、Pydantic AI、Google ADK 或手写）都能作为一个 Bot 入队；新建频道时 To: 填两个以上 Bot 即成群聊。'),
('每人一台电脑','supervisor 给每个人一个容器，每个 Bot 有自己的文件夹和浏览器登录；可勾 Isolated 单独隔离，支持 gVisor。'),
('唯一网关','浏览器、文件、MCP、组件动作都先过网关：解析目标 → CEL 策略（先 deny、无策略即拒、规则坏了也拒）→ 写审计行 → 才执行。'),
('人能接手','遇到登录墙或 2FA，Bot 会求助；控制权在同一面板交接并记录，人在操作时 Bot 动作被拒而非排队。'),
('长期职责','可给 Bot 设持续目标与定时任务（最短 15 分钟、最多 20 条，连续失败 10 次自动停）。')])}
<div class="gbox pit"><b>⚠ 能力边界</b>单机默认 OPENBOT_SINGLE_USER=true，所有请求都当管理员——给别人用之前必须配好 Google / Microsoft / Okta 或 SAML / OIDC 登录并上 TLS。线程与记忆依赖 CopilotKit Intelligence（托管或自托管，需项目与许可）。</div>''','02 组队 · OpenBot')

add(f'''<div class="kicker">2.5 附 · 代表二 · Agent Orchestrator</div><h1>Agent Orchestrator：一块看板带一队编码 Agent</h1>
<div class="lead">定位：本地桌面工作台（Apache-2.0），让多个编码 Agent 并行干活又不把分支、评审和 CI 搞乱。</div>
{its([('主 Agent 派活','告诉项目的主 Agent 要做什么，它拆计划、为每块活起一个 worker，只在需要你时回来。'),
('一任务一隔离','每个任务独立的 agent + 分支 + worktree，代码留在本机；每个 worker 还有浏览器预览和测试应用。'),
('一块看板','会话按 Agent 状态、PR、CI、评审自动分道，需要你处理的浮在最上面。'),
('谁的锅谁修','CI 失败、评审意见、合并冲突回到拥有该分支的 worker，直到 PR 被批准；可加 reviewer Agent 先审。'),
('自带武器','按任务选 Agent 与模型：Claude Code、Codex、Cursor、opencode、Gemini CLI、Grok、Qwen 等，具体支持矩阵以官方文档为准。'),
('移动与云','手机 App 配对桌面收通知、批准、开新 worker；也可选 Cloud Agents，在托管工作区运行，关上电脑继续跑。')])}
<div class="gbox pit"><b>⚠ 能力边界</b>核心是本地桌面守护进程；云端模式意味着代码与 worktree 在厂商云上。产品会收集有限遥测（含安装 ID 与 GitHub 用户名），可在设置中关闭。它管的是编码交付，不是通用办公权限治理。</div>''','02 组队 · Agent Orchestrator')

add(f'''<div class="kicker">2.5 附 · 选型与组合</div><h1>超级个体怎么选：治理线 vs 交付线</h1>
{tbl(['维度','OpenBot','Agent Orchestrator'],[('主战场','办公 / 业务 AI 同事','写代码、出 PR'),('团队单位','Bot + 频道','主 Agent + worker'),('隔离单位','每人 / 每 Bot 容器 + 浏览器','每任务分支 + worktree'),('人管什么','策略、审批、审计、接管','看板、评审、合并'),('接 Agent 方式','AG-UI 端点','各家编码 CLI'),('运行位置','自托管（Compose / 单镜像 / Helm）','本地桌面，可选厂商云'),('许可','MIT · Beta','Apache-2.0')])}
<div class="gp"><p><b>组合思路</b>：编码活交给 Agent Orchestrator 这类工作台（正好能挂 OpenCode / Codex），浏览器、表单、业务系统里的活交给 OpenBot 这类有网关和审计的平台；任务事实仍以 GitHub Issue / PR 为准，合并按钮留在自己手里。</p></div>
<div class="gbox egg"><b>★ 不适用场景</b>想要「两台电脑各自账号共享同一任务队列」：两者 README 都没承诺跨机原子领取与租约，仍需主城 Bridge / QMD 自己保证。只想单机快速组队：dsh-agent-teams 更轻。</div>
<div class="map"><div class="mt">一行对照</div><div class="mi">Paperclip：任务领取 / 锁 / 审批预算控制面</div><div class="mi">Paradev：CLI + worktree 工作台，远程走 Relay</div><div class="mi">dsh-agent-teams：DSH 内 Captain 单机组队</div><div class="mi">AgentTeams（开源）：Manager/Worker + Matrix + K8s</div><div class="mi">OpenHands：一界面连多台 Agent Server</div></div>
<div class="src">来源：github.com/CopilotKit/openbot · github.com/OrchestratorInc/agent-orchestrator（README，2026-10-31）</div>''','02 组队 · 选型')
