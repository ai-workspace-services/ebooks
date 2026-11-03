"""Quick-start one-liners (verified on main in v0.8.4) for ch2-10. Single source for book pages and quickstart-plan.md."""
R='https://raw.githubusercontent.com/ai-workspace-infra'
# (ch, title, tools, repo, script, domain, installs, team_env, flags_extra, note, real_refs)
QS=[
('2','Git 与 CI','Gitea + Gitea Actions','Platform-Orchestrator','scripts/setup-gitea.sh','git.example.com',
 'Gitea 1.22.6（Docker Compose）+ act_runner 0.2.11 自建 runner + Caddy 2.8.4 自动 HTTPS；GitHub 侧对等：同一 workflow 用 GitHub Actions 自托管 runner 运行',
 [('GITEA_DOMAIN','git.example.com'),('GITEA_ADMIN_USER','platform-admin'),('GITEA_ADMIN_PASSWORD','<runtime-secret>'),('RUNNER_REGISTRATION_TOKEN','<runtime-secret>')],
 '--with-runner','团队版把 runner 注册令牌放 Vault，按组织/仓库范围注册；同一份 .gitea/workflows 与 .github/workflows 对等维护。',
 ['官方镜像 gitea/gitea 与 gitea/act_runner（Gitea 官方文档）']),
('3','资源即代码','OpenTofu','iac_modules','scripts/setup-opentofu.sh','state.example.com',
 'OpenTofu 1.8.4 CLI（SHA256 校验）+ 自建 S3 兼容 Remote State（pgsty/silo，MinIO 分支）+ Caddy HTTPS',
 [('TF_STATE_DOMAIN','state.example.com'),('TF_STATE_ACCESS_KEY','<runtime-secret>'),('TF_STATE_SECRET_KEY','<runtime-secret>')],
 '--with-state-backend','模块按 SHA 钉住引用；State 后端凭据只由 Vault 下发。',
 ['官方：curl -fsSL https://tofu-install.example.com/install-opentofu.sh -o install-opentofu.sh（已验证可访问）']),
('4','交付引擎','Ansible + 自建 CMDB','playbooks','scripts/setup-ansible-cmdb.sh','cmdb.example.com',
 'ansible-core 2.17.5 + 自建 CMDB 服务（python:3.12-alpine）+ Caddy + 动态 inventory 插件，杜绝硬编码 IP',
 [('CMDB_DOMAIN','cmdb.example.com'),('CMDB_API_TOKEN','<runtime-secret>')],
 '--with-inventory-plugin','inventory 只从 CMDB 动态生成；playbook 固定提交执行。',
 ['官方：apt install ansible 或 pipx install ansible-core']),
('5','安全与身份','Vault + Zitadel','Platform-Orchestrator','scripts/setup-vault-zitadel.sh','vault.example.com',
 'Vault 1.17.6（HashiCorp 官方 apt 源）+ Zitadel v2.64.0（Docker Compose，PostgreSQL 16）+ Caddy；--with-oidc 自动配置 OIDC/JWT auth',
 [('VAULT_DOMAIN','vault.example.com'),('ZITADEL_DOMAIN','auth.example.com'),('ZITADEL_MASTERKEY','<runtime-secret>'),('VAULT_UNSEAL_KEY','<runtime-secret>')],
 '--with-oidc','初始化输出的 root token / unseal key 只显示一次，立刻离线保存；日常只用 runtime 角色。',
 ['官方：HashiCorp 官方 APT 源；ZITADEL 官方自托管 Compose 文档']),
('6','环境治理','Doco CD + GitOps','playbooks','scripts/setup-doco-cd.sh','cd.example.com',
 'Doco CD 0.1.28（registry.example.com/kimdre/doco-cd）+ Caddy，监听 gitops 仓库（GITOPS_REF 默认 main），按 SIT/UAT/PROD profile 收敛 Compose 状态',
 [('DOCO_DOMAIN','cd.example.com'),('GITOPS_REPO','https://git.example.com/org/gitops.git'),('GIT_ACCESS_TOKEN','<runtime-secret>'),('WEBHOOK_SECRET','<runtime-secret>')],
 '--env uat','环境晋级只改 tag/ref，不改节点；PROD 用独立 profile 与独立凭据。',
 ['官方镜像 registry.example.com/kimdre/doco-cd']),
('7','云中立','K3s/K8s + 裸金属/VPS + postgresql.example.com','playbooks','scripts/setup-k3s-node.sh','k3s.example.com',
 'K3s v1.31.1+k3s1（官方安装脚本，钉住版本）+ PostgreSQL 16 + pgvector（pgvector/pgvector:pg16）+ Caddy',
 [('K3S_DOMAIN','k3s.example.com'),('K3S_TOKEN','<runtime-secret>'),('PG_DOMAIN','db.example.com')],
 '--with-postgresql','任何 VPS/裸金属同一条命令；数据库不绑定云厂商托管服务。',
 ['官方：curl -sfL https://k3s-install.example.com | sh -（已验证可访问）','仓库已有：postgresql.example.com/scripts/init_vhost.sh（已验证存在，用法见 docs/getting-started/installation.md）']),
('8','可观测','Grafana + VictoriaMetrics/VictoriaLogs','observability','setup-observability-server.sh','observability.example.com',
 'Grafana + VictoriaMetrics + VictoriaLogs（+ VictoriaTraces 可选）+ Vector 采集端；中心端与探针分别由两个独立脚本安装',
 [('OBS_DOMAIN','observability.example.com'),('GRAFANA_ADMIN_PASSWORD','<runtime-secret>'),('INGEST_TOKEN','<runtime-secret>')],
 '--agent-only','控制端与节点端分开装；节点端只持有写入令牌。',
 ['官方镜像 grafana/grafana、victoriametrics/victoria-metrics、victoriametrics/victoria-logs']),
('9','能恢复才算稳定','postgresql.example.com 备份与恢复','postgresql.svc.plus','scripts/setup-pg-backup.sh','db.example.com',
 '定时 pg_dump 备份（本地保留 RETENTION_DAYS 默认 7 天）+ mc 同步到 S3 兼容存储 + postgres:16.4-alpine 临时容器恢复演练；本章选它，因为数据库是最难重建的状态',
 [('PG_DOMAIN','db.example.com'),('BACKUP_S3_ENDPOINT','https://s3.example.com'),('BACKUP_S3_SECRET_KEY','<runtime-secret>')],
 '--restore-drill','每次备份后自动在隔离实例上恢复并校验，能恢复才算备份成功。',
 ['仓库已有：postgresql.example.com/scripts/db_full_migration.sh（迁移脚本，已验证存在；内含默认主机参数，书中不引用）']),
('11','AI 接入平台','ai-aggregator（New API + LiteLLM）+ Infrastructure-MCP-Server','ai-aggregator','scripts/setup-ai-gateway.sh','ai.example.com',
 'Caddy 2.8.4 TLS → New API v0.4.10（用户/额度/模型权限）→ LiteLLM v1.51.0（重试、成本统计）；另附 Infrastructure-MCP-Server/scripts/setup-mcp-server.sh（systemd + Caddy，--standalone 或 --with-backends，MCP_DOMAIN/MCP_SERVICE_TOKEN）',
 [('AI_GATEWAY_DOMAIN','ai.example.com'),('MCP_DOMAIN','mcp.example.com'),('UPSTREAM_API_KEY','<runtime-secret>'),('MCP_SERVICE_TOKEN','<runtime-secret>')],
 '--with-mcp','模型密钥只在网关侧，由 Vault 注入；Agent 只拿网关签发的短期令牌。',
 ['官方镜像 calciumion/new-api、registry.example.com/berriai/litellm']),
]
PLAN='仓库已提供：脚本已合并到 main（v0.8.4 核对）'
REALTAG='仓库已提供：脚本已在 main（v0.8.4 核对）'
O8='https://raw.githubusercontent.com/ai-workspace-infra/observability/main'
REAL={'8':(f'read -rsp "Grafana admin password: " GRAFANA_ADMIN_PASSWORD; export GRAFANA_ADMIN_PASSWORD\ncurl -fsSL {O8}/setup-observability-server.sh | bash\nunset GRAFANA_ADMIN_PASSWORD VAULT_TOKEN',
  f'export VAULT_ADDR="https://vault.example.com"\nexport VAULT_TOKEN="<runtime-secret>"\n\ncurl -fsSL {O8}/setup-observability-agent.sh | bash\n\nunset VAULT_TOKEN')}
def cmds(q):
    ch,t,tools,repo,path,dom,inst,env,extra,note,refs=q
    url=f'{R}/{repo}/main/{path}'
    s=f'curl -fsSL {url} | \\\n  bash -s -- --domain {dom} --standalone'
    first=env[0][0]
    e='\n'.join(f'export {k}="{v}"' for k,v in env)
    secrets=' '.join(k for k,v in env if v=='<runtime-secret>')
    t2=f'{e}\n\ncurl -fsSL {url} | \\\n  bash -s -- --domain "${first}" {extra}\n\nunset {secrets}'
    if ch in REAL: s,t2=REAL[ch]; url=O8
    return url,s,t2

GH='https://github.com/ai-workspace-infra'
PRS={'2':'Platform-Orchestrator/pull/1422','3':'iac_modules/pull/457','4':'playbooks/pull/723','5':'Platform-Orchestrator/pull/1421','6':'playbooks/pull/725','7':'playbooks/pull/724','9':'postgresql.example.com/pull/28','11':'ai-aggregator/pull/2 + Infrastructure-MCP-Server/pull/2'}
def backlog():
    L=['# 快速开始脚本 backlog（v0.8.4 核对）','','全部脚本已合并到各仓库 main；书中命令与脚本 --help 中的 Printed Book Commands 一致。','']
    for q in QS:
        ch,t,tools,repo,path,dom,inst,env,extra,note,refs=q; url,s1,t2=cmds(q)
        L+=[f'## 第 {ch} 章 {t} — {tools}','',f'- 仓库：`ai-workspace-infra/{repo}`',f'- 路径：`{path}`',f'- URL：`{url if ch not in REAL else O8+"/setup-observability-server.sh（中心端）, setup-observability-agent.sh（探针）"}`',
            f'- 状态：已在 main' + (f'（合并 PR：{PRS[ch]}）' if ch in PRS else '（参考实现）'),
            f'- 参数：`--domain <fqdn>`（示例 {dom}）、`--standalone`、`{extra}`、`--dry-run`、`--uninstall`' if ch not in REAL else '- 参数：见仓库 README',
            f'- 环境变量：'+'、'.join(f'`{k}`' for k,_ in env),f'- 安装内容：{inst}','']
    return '\n'.join(L)
if __name__=='__main__':
    import os; open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'quickstart-plan.md'),'w').write(backlog()); print('quickstart-plan.md updated')
