# Changelog

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
