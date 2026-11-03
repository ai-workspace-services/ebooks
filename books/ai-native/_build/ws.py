"""第 07 / 09 章：AI Workspace 白皮书规划 v0.2-plan 精简（来源 D）+ 已确认的工程决定。证据等级：E0=规划，E4=已合并。"""
WP = '《AI Workspace、XWorkmate 多执行器与三级记忆技术白皮书规划》v0.2-plan（2026-10-23）'
ARCH = [  # (层, 组件, 说明)
 ('入口', 'XWorkmate App', 'Flutter：Chat / Work / Code / Bot / History'),
 ('接入', 'XWorkmate Bridge :8787', '统一接入层，鉴权与路由'),
 ('调度', 'DSH · DS-Bot', 'DSH（DeepSeek Harness）调度 Agent；DS-Bot 规划多 Agent 任务'),
 ('执行', 'Agent Worker Pool', 'OpenCode 为主；Codex / Claude / Grok CLI 走适配器'),
 ('模型', 'AI Gateway', 'New API :3000 · LiteLLM :4000 · CPA :8317'),
 ('记忆', 'X-Memory-Hub · QMD · PG17', '三级记忆，见 2.6'),
]
DECISIONS = [
 '2026-10-12 栈收敛：Agent 运行时只保留 OpenCode + DSH + DS-Bot 插件；Codex / Claude Code 作为主运行时退役。',
 '本地路由先做 L0–L5 分级，再调用唯一的 AI 网关；Architect / Specialist 任务在 OpenCode 上配更强模型。',
 'v2.2 目标架构自托管，不依赖 OpenClaw Gateway。',
]
MEM = [
 ('L1 热记忆', 'QMD', '全文 + 语义检索；会话与上下文条目；中文检索先用 L1 + pg_trgm'),
 ('L2 结构化记忆', 'PostgreSQL 17 + pgvector', '元数据、实体 / 边 / 事实；向量统一 nemotron-3-embed-1b，halfvec 存储'),
 ('L3 归档', 'Google Drive', '每日归档一次；对象存储可作替代'),
]
FACTS = '事实写入先为 proposed；置信度 ≥ 0.8 且有 ≥ 2 条证据自动转 active；与旧事实冲突时写 superseded_by，只新增不删除。'
EVIDENCE = [
 ('E4 已合并', 'xworkmate-app：侧边栏「定时任务」与 token fallback'),
 ('E4 已合并', 'qmd fork：feat/memory-tiers（PR #7，2026-10-14 合并）'),
 ('E0 规划', 'Bridge 统一接入、DS-Bot 多 Agent 规划、Worker 适配器、All-in-One 部署'),
 ('E0 规划', 'Task / Run 状态机、三级记忆全链路、W0–W6 / G0–G6、验收与负向测试'),
]
# 白皮书中列出、本书未展开细则的条目（按标题保留，细则以白皮书为准）
WP_ITEMS = ['边界矩阵', 'Flow A / B / C', 'Task / Run 与 8 个运行状态', 'All-in-One 部署与端口隔离', '3 个部署 Profile',
            'W0–W6 实施波次', 'G0–G6 质量门', '10 条验收标准', '负向测试', '证据等级 E0–E5', 'ADR 决策记录', '10 条 Agent 规则']
RULES = [  # 附录：通用 Agent 工作约定（按作者已确认的工作方式整理，非白皮书第 10 节原文）
 '先读规则与现状，再动手；不确定的事实标注来源与日期，不编造。',
 '合并只在明确授权后进行；不 force-push；文档类 PR 通过检查后可直接合并，代码 / CI / 配置改动需人确认。',
 '同步仓库用 fast-forward，保留未提交与未跟踪文件。',
 '备份与公开内容先脱敏：不出现密钥、账号、地址、内网主机、本地路径与私有仓库细节。',
 '按 L0–L5 选择模型与推理强度：Chat / Worker 不超过 medium，xhigh 只给 Architect / Specialist。',
 '所有任务走统一网关与三级记忆，结果可追溯（Task → Run → 证据）。',
 '对外发布、付费、删除等不可逆操作必须先得到人的确认。',
]
