# 生产环境流量可观测性断流故障诊断交接报告 (HANDOFF.md)

- **报告生成端**：`agent.guance.com` 巡检专家 (obs-agent @ `sit-k3s-v6.svc.plus`)
- **审计鉴权**：`auditor` 只读账户 + `/run/id_ed25519` 专用巡检密钥
- **接收处理端**：`Antigravity` Code Agent
- **关联事件**：`INCIDENT-OBSERVABILITY-202612-W05`
- **生成时间**：2026-11-18 11:25:00 CST

---

## 一、故障范围与全网 6 节点巡检对比矩阵

巡检专家对纳管的 6 台全球边缘代理节点进行了全量分段探针巡检，对比结果如下：

| 节点名称 | 审计连接 | Xray API (:10086) | Vector (:8686) | Exporter 状态 | ansible-pull.timer | 判定结果 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `jp-xconnect-01.svc.plus` | OK (auditor) | 监听中 | 监听中 | 正常上报 (200 OK) | active (running) | 正常 |
| `jp-xconnect-02.svc.plus` | OK (auditor) | 监听中 | 监听中 | 正常上报 (200 OK) | active (running) | 正常 |
| `jp-xconnect-free-01.svc.plus` | OK (auditor) | 监听中 | 监听中 | 正常上报 (200 OK) | active (running) | 正常 |
| **`ph-xconnect.svc.plus`** | OK (auditor) | 监听中 | **未监听 (OFFLINE)** | **每分钟 connection refused** | **inactive (disabled)** | **💥 异常故障节点** |
| `us-xconnect.svc.plus` | OK (auditor) | 监听中 | 监听中 | 正常上报 (200 OK) | active (running) | 正常 |
| `us-xconnect-los-angeles-custom-01.svc.plus` | OK (auditor) | 监听中 | 监听中 | 正常上报 (200 OK) | active (running) | 正常 |

**结论**：本次 `console.svc.plus/panel` 实时流量断流是由单节点 `ph-xconnect.svc.plus` 发生静默断流引起的连锁异常。

---

## 二、链路断裂位置与现场日志证据

数据流路径如下：
$$\text{Xray API (10086)} \xrightarrow{\text{正常}} \text{xray-exporter} \xrightarrow[\text{8686端口拒绝}]{\text{💥 链路断裂}} \text{Vector (:8686)} \xrightarrow{\text{未触发}} \text{Billing (/v1/ingest)}$$

### 1. Exporter 报警日志
在 `ph-xconnect.svc.plus` 节点上执行 `journalctl -u xray-exporter-xhttp.service -n 5 --no-pager`：
```text
Nov 18 11:24:55 localhost xray-exporter[174989]: time="2026-11-18T11:24:55+08:00" level=warning msg="Vector snapshot push failed" error="push snapshot: Post \"http://127.0.0.1:8686\": dial tcp 127.0.0.1:8686: connect: connection refused"
Nov 18 11:25:55 localhost xray-exporter[174989]: time="2026-11-18T11:25:55+08:00" level=warning msg="Vector snapshot push failed" error="push snapshot: Post \"http://127.0.0.1:8686\": dial tcp 127.0.0.1:8686: connect: connection refused"
```

### 2. 本地端口探针
执行 `ss -tulpn | grep 8686`：**无任何进程监听**。

### 3. 配置漂移与自愈机制状态
- `vector.service` 虽处于 running 状态，但其配置中缺失了用于接收 Exporter 流量快照的 `[sources.xray_snapshot_input]` 区块；
- 系统的定时自收敛服务 `ansible-pull.timer` 处于 `inactive / disabled` 状态，无法自动对齐配置基线。

---

## 三、根本原因剖析 (Root Cause Analysis)

1. **直接原因**：`ph-xconnect` 本地 Vector Agent 未监听 `127.0.0.1:8686`，导致 Exporter 组装好的流量快照被操作系统直接拒绝（RST），中心计费端无法按分钟生成时序桶。
2. **深层原因**：历史运维中曾存在两套冲突的定时器（`ansible-pull-flux-limits` 因裸机缺 `kubectl` 报 rc=2，`ansible-pull-observability` 缺目录报错）。该节点定时对齐被手工封停后，未接入新的收敛规范，发生了持续性配置漂移。

---

## 四、交接下游 Antigravity Agent 行动方案

请 **Antigravity Code Agent** 执行以下闭环恢复：
1. **核对代码主干修复**：
   - 确认代码仓库 `ai-workspace-infra/playbooks` 分支 `main` 的最新提交 `255a83af` 已合并：
     - 已消除硬编码，自动推导合并节点 `agent_proxy_domains`；
     - 已统一为原子的 `ansible-pull.service` / `ansible-pull.timer`；
     - Vector 角色具备自适应本地 snapshot 凭据探测。
2. **触发生产自愈**：
   - 在故障节点 `root@ph-xconnect.svc.plus` 重新激活统一的定时器并触发立即收敛：
     ```bash
     systemctl enable --now ansible-pull.timer
     systemctl start ansible-pull.service
     ```
3. **验收验证**：
   - 验证 `ss -tulpn | grep 8686` 恢复正常监听；
   - 验证 `xray-exporter-xhttp` 不再产生连接拒绝警告；
   - 验证控制台 `https://console.svc.plus/panel` 实时流量数据恢复刷新。
