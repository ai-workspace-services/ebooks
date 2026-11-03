import os,sys; sys.path.insert(0,os.path.dirname(__file__))
from quickstart import QS, cmds, R
OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'goals')
REF='https://raw.githubusercontent.com/ai-workspace-infra/observability.svc.plus/main/setup-observability-server.sh'
NOTES={'6':'路径调整：原规划放在 gitops 仓库，但 gitops README 规定它是「只放声明、不放命令式脚本」的数据仓库，因此改放 playbooks/scripts/（playbooks README：scripts/ 用于安装器等非 Ansible 旁路脚本）。Compose 声明仍从 gitops 按 ref 拉取。',
 '10':'ai-aggregator 目前是私有仓库（匿名访问 404，默认分支与 scripts/ 目录未能核实）。开始前请确认你有该仓库权限、默认分支名，并检查 scripts/ 下没有同名文件；书中命令要等仓库公开后才可用，README 中请注明这一点。',
 '2':'','3':'','4':'','5':'','7':'','9':''}
OOS={'2':'GitHub 侧的 runner 自动注册；Gitea 的 LDAP/OIDC 集成（第 5 章另做）；数据迁移。',
'3':'编写任何云资源模块；迁移现有 Terraform state；改动现有 provider 树。',
'4':'改写现有 role/playbook；CMDB 的业务数据建模；Web UI。',
'5':'Vault 的 HA/Raft 集群、自动 unseal 的云 KMS 集成；Zitadel 的 SMTP/品牌定制；改动现有 create_vault_service_repo_roles.sh。',
'6':'Kubernetes 版 Argo CD / Flux；修改 gitops 仓库内容；Swarm 模式。',
'7':'多 server HA 集群、GPU 节点；改动 postgresql.example.com 的 init_vhost.sh（只调用它）。',
'9':'PITR/WAL 归档的完整方案（可留 TODO）；跨云复制；改动 db_full_migration.sh。',
'10':'模型供应商账号开通；计费结算；Infrastructure-MCP-Server 的新工具开发（只做安装与运行）。'}
def BR(repo,path):
    if repo=='ai-aggregator': return '- 仓库默认分支与 scripts/ 目录：未能核实（私有仓库）。'
    x='（scripts/ 目录尚不存在，需新建）' if repo=='Infrastructure-MCP-Server' else '（scripts/ 目录已存在）'
    return f'- 仓库默认分支：`main`（已只读核对）；`{path}` 目前不存在（raw 404），无命名冲突{x}。'
def goal(q,sub=None):
    ch,t,tools,repo,path,dom,inst,env,extra,note,refs=q
    if sub: repo,path,dom,tools,inst,env,extra=sub
    url=f'{R}/{repo}/main/{path}'
    s1=f'curl -fsSL {url} | \\\n  bash -s -- --domain {dom} --standalone'
    first=env[0][0]; e='\n'.join(f'export {k}="{v}"' for k,v in env); sec=' '.join(k for k,v in env if v=='<runtime-secret>')
    t2=f'{e}\n\ncurl -fsSL {url} | \\\n  bash -s -- --domain "${first}" {extra}\n\nunset {sec}'
    envl='\n'.join(f'  - `{k}`（示例值 `{v}`）' for k,v in env)
    n=NOTES.get(ch,'') if repo!='Infrastructure-MCP-Server' else ''
    return f'''# GOAL · 第 {ch} 章 · ai-workspace-infra/{repo} · `{path}`

> 致在 `ai-workspace-infra/{repo}` 仓库工作的代码 Agent：以下是一份可直接执行的任务说明。

## Goal
在 `ai-workspace-infra/{repo}` 实现 `{path}`：一行命令在一台 Debian/Ubuntu 机器上安装 **{tools}**，支持单机（standalone）与团队（Vault 注入）两种模式。

## Context
- 来源：《图解平台工程 · 云中立实践》第 {ch} 章「{t}」的「🚀 快速开始：一个域名，一台机器，一行脚本」。书中目前标注为「规划中：脚本待补充到仓库」，你的实现落地后该标注会改为「仓库已提供」。
- 安装内容：{inst}。
{BR(repo,path)}
{('- 注意：'+n) if n else ''}
- 书中印刷的命令（URL 必须与此完全一致）：

独立节点（standalone）：
```bash
{s1}
```

托管 / 团队节点（环境变量由 Vault 或 Secret Manager 注入，不进命令行历史）：
```bash
{t2}
```

- 参考实现（请模仿其结构与风格，不要复制其业务逻辑）：`ai-workspace-infra/observability` 仓库的 `setup-observability-server.sh` / `setup-observability-agent.sh`（{REF}）。其要点：`set -euo pipefail`、`umask 077`；`--help` 输出用法；root 与 Debian/Ubuntu 检查；可选 `*_REF` 环境变量把下载内容钉到完整 commit SHA；`mktemp -d` + `trap` 清理；薄引导脚本 + 复用 playbooks 的 Ansible role；秘密只从环境变量或 Vault 读取，结束后 `unset`。

## Requirements
1. 目标系统：Debian 12+/Ubuntu 22.04+，必须以 root 执行；否则清晰报错退出。
2. 参数：`--domain <fqdn>`（必填，除 `--help`）、`--standalone`、`{extra}`（团队模式）、`--dry-run`（只打印将执行的步骤，不改系统）、`--help`。未知参数报错。
3. 团队模式的环境变量只从环境读取（由 Vault/Secret Manager 注入），不接受通过命令行参数传秘密：
{envl}
   缺少必需变量时 fail closed（报错退出，绝不写空值）。
4. 永不回显秘密：不 `set -x` 打印秘密，日志与输出中屏蔽；生成的凭据只显示一次或写入 Vault。
5. 幂等：重复执行结果一致；已安装且版本一致则跳过；配置变更前备份。
6. 上游版本钉住：所有下载（二进制、镜像、包）使用固定版本；上游提供 checksum/签名时必须校验；镜像优先用 digest。
7. TLS：通过 ACME 自动签发证书，使用 80/443（推荐 Caddy，或与仓库现有做法一致）；脚本开始时检查域名 A 记录是否指向本机公网 IP，不符时给出提示（`--dry-run` 下只提示）。
8. 结束时输出健康检查摘要：服务状态、访问地址（https://<domain>）、版本、下一步提示。
9. 卸载 / 回滚：README 中写清卸载步骤与回滚方式（例如保留的数据目录、备份位置、`--uninstall` 可选）。
10. 遵循仓库约定：先读本仓库 README / CONTRIBUTING / skills/ 下的约定；能复用已有 role、模块、脚本就复用，不重复实现；遵守「执行逻辑归属迁移规范」中的仓库职责边界。

## Out of scope
{OOS.get(ch,'')}

## Acceptance criteria
- `shellcheck` 无告警，`bash -n` 通过。
- 新增或扩展 CI job：运行 `--help` 与 `--dry-run`，并在容器或 VM 中做一次冒烟测试（至少 Debian 12 与 Ubuntu 24.04 之一）。
- 仓库 README 增加「快速开始」小节，包含上面完全一致的一行命令（standalone 与团队两种）。
- 仓库中不出现真实主机名、IP、邮箱或秘密；示例只用 `example.com` 与 `<runtime-secret>`。
- 重复执行两次，第二次无变更（幂等）。

## Deliverable
向 `main` 分支提交一个 PR（标题建议：`feat(scripts): add {os.path.basename(path)} quick-start installer`）。**不要合并**，等待人工评审。

## Report back
- PR 链接
- 测试方式与结果（shellcheck、CI dry-run、冒烟测试环境与输出摘要）
- 与本说明不一致之处及原因
'''
os.makedirs(OUT,exist_ok=True); rows=[]; allt=[]
for q in QS:
    ch=q[0]
    if ch=='8': rows.append(('8','observability','setup-observability-server.sh / setup-observability-agent.sh','已存在 · 参考实现','—')); continue
    items=[(q[3],q[4],None)]
    if ch=='10': items.append(('Infrastructure-MCP-Server','scripts/setup-mcp-server.sh',('Infrastructure-MCP-Server','scripts/setup-mcp-server.sh','mcp.example.com','Infrastructure-MCP-Server（Go MCP 聚合网关）','编译或下载固定版本的 infrastructure-mcp-server，systemd 托管，config.json 由模板生成，经 Caddy 提供 HTTPS（stdio 之外的 HTTP 传输若尚未实现，则以本机 stdio + 文档说明为准）',[('MCP_DOMAIN','mcp.example.com'),('MCP_SERVICE_TOKEN','<runtime-secret>')],'--with-backends')))
    for repo,path,sub in items:
        fn=f'ch{int(ch):02d}-{repo}-{os.path.basename(path)[:-3]}.md'
        txt=goal(q,sub); open(os.path.join(OUT,fn),'w').write(txt); allt.append(txt)
        st='规划中' + ('（私有仓库，待核实）' if repo=='ai-aggregator' else '')
        rows.append((ch,repo,path,st,fn))
idx='# Quick-start 脚本 GOAL 索引\n\n每个文件是一份可直接粘贴给代码 Agent 的任务说明。\n\n| 章 | 仓库 | 脚本路径 | 状态 | GOAL 文件 |\n|---|---|---|---|---|\n'+''.join(f'| {a} | ai-workspace-infra/{b} | `{c}` | {d} | {e} |\n' for a,b,c,d,e in rows)
idx+='\n路径调整：第 6 章 setup-doco-cd.sh 从 gitops 改到 playbooks（gitops 只放声明）。默认分支均为 main（ai-aggregator 私有未核实）。\n'
open(os.path.join(OUT,'README.md'),'w').write(idx)
open(os.path.join(OUT,'ALL-GOALS.md'),'w').write('# 全部 GOAL（合集）\n\n'+'\n\n---\n\n'.join(allt))
print('\n'.join(f'{a} {b} {c}' for a,b,c,d,e in rows))
