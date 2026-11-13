# Changelog

## 2026-11-13 · Agent Skills 工程规范 v0.3
- 《XWorkspace Agent Skills 工程规范 · 开放方案》升至 `v0.3`：正文改为直接的工程实践表述，去掉故事化称呼；版本锚点对齐 `xworkspace-core-skills` 固定提交 `07c6e772`（2026-11-13，Asia/Shanghai，[#70](https://github.com/ai-workspace-lab/xworkspace-core-skills/pull/70) 合入主干，含 [#69](https://github.com/ai-workspace-lab/xworkspace-core-skills/pull/69) 开发规范）。
- 新增第八章「七类开发规范：把“怎么写代码”也写成技能」，自研规范从工程、运维两类补齐为工程、运维、开发三类；诚实标签写清「已验收」与「设计契约」的边界。
- 补全「附录 · 全量 Skill 目录索引」：按 `skills/` 下 `SKILL.md` 递归计数，11 个能力域 92 项 + 2 项 vendored = 94；逐项给出 Skill ID、一句话用途、所在章节或适用场景，并标明 `agent-team-harness`、`harness-workflow`、`feature-lane-release-workflow` 为设计契约。
- PDF 目录改为两遍渲染，列出全部 `<h1>` 与附录能力域 `<h2>`，带页内锚点与实际页码（`p.X`）；在 `pypdf` 可用时写入 PDF 书签。仓库内另附 [`books/agent-skills-spec/index.md`](books/agent-skills-spec/index.md)。
- 页数为 18 页。许可仍为内容 CC BY-SA 4.0，署名 Haitao Pan / XWork Technologies LLC。


## 2026-11-09 · 人民币海外卡 v1.2：汇丰全球转账细节专题
- 新增「细节专题」第 06 章：汇丰香港网上理财国际电汇（全球转账）操作步骤、字段提示表、提交前检查与不可撤销提示。
- 第 02、04 章与附录清单交叉引用该专题；限额、费用、用途证明材料仍标注待向汇丰核实。
- 版本 `v1.2`；封面版本号同步；许可仍为 CC BY-SA 4.0，署名 Haitao Pan / XWork Technologies LLC。

## 2026-11-09 · 出海第一步 v1.3
- 《出海第一步 · 一人公司合规全流程》升至 v1.3：第 07 章补全「汇丰香港国际电汇（全球转账）」操作步骤、特殊填写提示与提交前检查；更新资金路径图、Mercury 入金闭环与总清单中对应待确认项（限额 / 费用 / 税务仍标待确认）。
- 核对日期改为 2026-11-09；版式新增简易三列表格块。
- 版式修复：页脚改为文档流布局；卡片正文与「本站产出→下一站」手递区分开，FIT 只缩放正文，避免手递区与页脚重叠。


## 2026-11-03 · designed covers
- agent-skills-spec & cny-overseas-card-routes: new light/dark covers in the xworktech.com/docs style (Drive `books/<slug>/assets`), used on the PDF cover page via `assets.manifest.json` + `fetch-assets.sh` (HTML cover kept as fallback); README uses Drive lh3 direct-render URLs with `<picture>` light/dark.

## 2026-11-03 · zip 制品 + 封面墙
- CI：每本书 PDF 经 Ghostscript 尝试压缩（仅当小 ≥10% 且页数不变才采用），再 `zip -9` 为 `<slug>-<version>.zip` 作为 artifact。
- Tag 发布：附各书 zip + SHA256SUMS；`v*` 全书 tag 另附 `ebooks-all-<tag>.zip`，Release notes 列出书目、版本与 CC BY-SA 4.0 许可。
- README：3×3 封面墙 + 「书目介绍」（封面图为 Drive「Grok Bot 制品/books/covers」新上传文件）。

## 2026-11-03 · 初始导入
- 9 本书源码 + 构建脚本入库：图解平台工程 v0.9.18、图解 IT 简史 v4.9.1、趣谈数据基础设施 v5.1、出海第一步 v1.2、AI 工具出海通关 v0.2.5、AI-Native v0.9.6、独立开发观察者计划 v0.1-r5、Agent Skills 工程规范 v0.2、人民币海外卡三条路线攻略 v1.1。
- 观察者计划升到 v0.1-r5：正文取自 knowledge main（含 #294 合并的 articles 00–15）。
- 图片不入库，改为 Drive 素材包 + assets.manifest.json + fetch-assets.sh。
- 许可统一为内容 CC BY-SA 4.0、脚本 MIT；各书版权页改为 CC BY-SA 4.0。
- 平台工程书：节点 IP、实例/磁盘 ID 改为占位符。
- 新增矩阵 CI：PR 构建；tag 发布 Release。

## 2026-11-03 · 素材压缩 + 公开拉取
- 五本有图的书素材压缩为 v2 包并新上传 Drive；it-history 658MB→110MB。
- `tools/fetch_assets.py` 支持无密钥公开下载（大文件 confirm）。
