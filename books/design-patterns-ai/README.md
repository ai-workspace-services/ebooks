# 图解经典设计模式 · 遇到 AI 时代

- 版本：`v0.1`（见 `VERSION`；升版只改这个文件）
- 构建：`./build.sh` 或在仓库根目录 `make design-patterns-ai`，产物在 `dist/`（不入库）
- 依赖：python3 + markdown, Chrome；目录页码与书签使用 `pdftotext`（poppler-utils）和 `pypdf`（CI 已安装，本地缺 `pypdf` 时跳过书签、仍写出带页码的目录）。图解由 `diagrams.py` 在构建时生成内联 SVG，不依赖 Drive 素材，也不向仓库提交 `*.svg` / `*.png` / `*.pdf`。
- 正文是否为 Markdown：是（`design-patterns-ai.md`）
- 目录索引（章节与 18 个模式的 PDF 页码）：[index.md](index.md)
- 图片素材：无外部图片素材。封面为 CSS 排版，六张图解在 `build-core.sh` 中由 `diagrams.py` 注入。
- 许可：内容 CC BY-SA 4.0，署名 Haitao Pan / XWork Technologies LLC；构建脚本与示例代码 MIT
