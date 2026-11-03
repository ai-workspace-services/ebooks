# 快速开始脚本 backlog（v0.8.4 核对）

全部脚本已合并到各仓库 main；书中命令与脚本 --help 中的 Printed Book Commands 一致。

## 第 2 章 Git 与 CI — Gitea + Gitea Actions

- 仓库：`ai-workspace-infra/Platform-Orchestrator`
- 路径：`scripts/setup-gitea.sh`
- URL：`https://raw.githubusercontent.com/ai-workspace-infra/Platform-Orchestrator/main/scripts/setup-gitea.sh`
- 状态：已在 main（合并 PR：Platform-Orchestrator/pull/1422）
- 参数：`--domain <fqdn>`（示例 git.example.com）、`--standalone`、`--with-runner`、`--dry-run`、`--uninstall`
- 环境变量：`GITEA_DOMAIN`、`GITEA_ADMIN_USER`、`GITEA_ADMIN_PASSWORD`、`RUNNER_REGISTRATION_TOKEN`
- 安装内容：Gitea 1.22.6（Docker Compose）+ act_runner 0.2.11 自建 runner + Caddy 2.8.4 自动 HTTPS；GitHub 侧对等：同一 workflow 用 GitHub Actions 自托管 runner 运行

## 第 3 章 资源即代码 — OpenTofu

- 仓库：`ai-workspace-infra/iac_modules`
- 路径：`scripts/setup-opentofu.sh`
- URL：`https://raw.githubusercontent.com/ai-workspace-infra/iac_modules/main/scripts/setup-opentofu.sh`
- 状态：已在 main（合并 PR：iac_modules/pull/457）
- 参数：`--domain <fqdn>`（示例 state.example.com）、`--standalone`、`--with-state-backend`、`--dry-run`、`--uninstall`
- 环境变量：`TF_STATE_DOMAIN`、`TF_STATE_ACCESS_KEY`、`TF_STATE_SECRET_KEY`
- 安装内容：OpenTofu 1.8.4 CLI（SHA256 校验）+ 自建 S3 兼容 Remote State（pgsty/silo，MinIO 分支）+ Caddy HTTPS

## 第 4 章 交付引擎 — Ansible + 自建 CMDB

- 仓库：`ai-workspace-infra/playbooks`
- 路径：`scripts/setup-ansible-cmdb.sh`
- URL：`https://raw.githubusercontent.com/ai-workspace-infra/playbooks/main/scripts/setup-ansible-cmdb.sh`
- 状态：已在 main（合并 PR：playbooks/pull/723）
- 参数：`--domain <fqdn>`（示例 cmdb.example.com）、`--standalone`、`--with-inventory-plugin`、`--dry-run`、`--uninstall`
- 环境变量：`CMDB_DOMAIN`、`CMDB_API_TOKEN`
- 安装内容：ansible-core 2.17.5 + 自建 CMDB 服务（python:3.12-alpine）+ Caddy + 动态 inventory 插件，杜绝硬编码 IP

## 第 5 章 安全与身份 — Vault + Zitadel

- 仓库：`ai-workspace-infra/Platform-Orchestrator`
- 路径：`scripts/setup-vault-zitadel.sh`
- URL：`https://raw.githubusercontent.com/ai-workspace-infra/Platform-Orchestrator/main/scripts/setup-vault-zitadel.sh`
- 状态：已在 main（合并 PR：Platform-Orchestrator/pull/1421）
- 参数：`--domain <fqdn>`（示例 vault.example.com）、`--standalone`、`--with-oidc`、`--dry-run`、`--uninstall`
- 环境变量：`VAULT_DOMAIN`、`ZITADEL_DOMAIN`、`ZITADEL_MASTERKEY`、`VAULT_UNSEAL_KEY`
- 安装内容：Vault 1.17.6（HashiCorp 官方 apt 源）+ Zitadel v2.64.0（Docker Compose，PostgreSQL 16）+ Caddy；--with-oidc 自动配置 OIDC/JWT auth

## 第 6 章 环境治理 — Doco CD + GitOps

- 仓库：`ai-workspace-infra/playbooks`
- 路径：`scripts/setup-doco-cd.sh`
- URL：`https://raw.githubusercontent.com/ai-workspace-infra/playbooks/main/scripts/setup-doco-cd.sh`
- 状态：已在 main（合并 PR：playbooks/pull/725）
- 参数：`--domain <fqdn>`（示例 cd.example.com）、`--standalone`、`--env uat`、`--dry-run`、`--uninstall`
- 环境变量：`DOCO_DOMAIN`、`GITOPS_REPO`、`GIT_ACCESS_TOKEN`、`WEBHOOK_SECRET`
- 安装内容：Doco CD 0.1.28（registry.example.com/kimdre/doco-cd）+ Caddy，监听 gitops 仓库（GITOPS_REF 默认 main），按 SIT/UAT/PROD profile 收敛 Compose 状态

## 第 7 章 云中立 — K3s/K8s + 裸金属/VPS + postgresql.example.com

- 仓库：`ai-workspace-infra/playbooks`
- 路径：`scripts/setup-k3s-node.sh`
- URL：`https://raw.githubusercontent.com/ai-workspace-infra/playbooks/main/scripts/setup-k3s-node.sh`
- 状态：已在 main（合并 PR：playbooks/pull/724）
- 参数：`--domain <fqdn>`（示例 k3s.example.com）、`--standalone`、`--with-postgresql`、`--dry-run`、`--uninstall`
- 环境变量：`K3S_DOMAIN`、`K3S_TOKEN`、`PG_DOMAIN`
- 安装内容：K3s v1.31.1+k3s1（官方安装脚本，钉住版本）+ PostgreSQL 16 + pgvector（pgvector/pgvector:pg16）+ Caddy

## 第 8 章 可观测 — Grafana + VictoriaMetrics/VictoriaLogs

- 仓库：`ai-workspace-infra/observability`
- 路径：`setup-observability-server.sh`
- URL：`https://raw.githubusercontent.com/ai-workspace-infra/observability/main/setup-observability-server.sh（中心端）, setup-observability-agent.sh（探针）`
- 状态：已在 main（参考实现）
- 参数：见仓库 README
- 环境变量：`OBS_DOMAIN`、`GRAFANA_ADMIN_PASSWORD`、`INGEST_TOKEN`
- 安装内容：Grafana + VictoriaMetrics + VictoriaLogs（+ VictoriaTraces 可选）+ Vector 采集端；中心端与探针分别由两个独立脚本安装

## 第 9 章 能恢复才算稳定 — postgresql.example.com 备份与恢复

- 仓库：`ai-workspace-infra/postgresql.svc.plus`
- 路径：`scripts/setup-pg-backup.sh`
- URL：`https://raw.githubusercontent.com/ai-workspace-infra/postgresql.svc.plus/main/scripts/setup-pg-backup.sh`
- 状态：已在 main（合并 PR：postgresql.example.com/pull/28）
- 参数：`--domain <fqdn>`（示例 db.example.com）、`--standalone`、`--restore-drill`、`--dry-run`、`--uninstall`
- 环境变量：`PG_DOMAIN`、`BACKUP_S3_ENDPOINT`、`BACKUP_S3_SECRET_KEY`
- 安装内容：定时 pg_dump 备份（本地保留 RETENTION_DAYS 默认 7 天）+ mc 同步到 S3 兼容存储 + postgres:16.4-alpine 临时容器恢复演练；本章选它，因为数据库是最难重建的状态

## 第 11 章 AI 接入平台 — ai-aggregator（New API + LiteLLM）+ Infrastructure-MCP-Server

- 仓库：`ai-workspace-infra/ai-aggregator`
- 路径：`scripts/setup-ai-gateway.sh`
- URL：`https://raw.githubusercontent.com/ai-workspace-infra/ai-aggregator/main/scripts/setup-ai-gateway.sh`
- 状态：已在 main（合并 PR：ai-aggregator/pull/2 + Infrastructure-MCP-Server/pull/2）
- 参数：`--domain <fqdn>`（示例 ai.example.com）、`--standalone`、`--with-mcp`、`--dry-run`、`--uninstall`
- 环境变量：`AI_GATEWAY_DOMAIN`、`MCP_DOMAIN`、`UPSTREAM_API_KEY`、`MCP_SERVICE_TOKEN`
- 安装内容：Caddy 2.8.4 TLS → New API v0.4.10（用户/额度/模型权限）→ LiteLLM v1.51.0（重试、成本统计）；另附 Infrastructure-MCP-Server/scripts/setup-mcp-server.sh（systemd + Caddy，--standalone 或 --with-backends，MCP_DOMAIN/MCP_SERVICE_TOKEN）
