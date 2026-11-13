# XWorkspace Agent Skills 工程规范 · 开放方案

- 版本：`v0.3`（见 `VERSION`；升版只改这个文件）
- 构建：`./build.sh` 或在仓库根目录 `make agent-skills-spec`，产物在 `dist/`（不入库）
- 依赖：python3 + markdown, Chrome（Mermaid 走 CDN，需联网）；目录页码与书签使用 `pdftotext`（poppler-utils）和 `pypdf`（CI 已安装，本地缺 `pypdf` 时跳过书签、仍写出带页码的目录）
- 正文是否为 Markdown：是（agent-skills-spec.md）
- 完整目录索引（章节与 94 个 Skill 的 PDF 页码）：[index.md](index.md)
- 图片素材：无外部图片素材（封面图由 `fetch-assets.sh` 按需拉取）
- 许可：内容 CC BY-SA 4.0，署名 Haitao Pan / XWork Technologies LLC；构建脚本 MIT
