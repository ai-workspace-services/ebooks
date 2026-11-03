# 出海第一步 · 一人公司合规全流程

- 版本：`v1.2`（见 `VERSION`；升版只改这个文件）
- 构建：`./build.sh` 或在仓库根目录 `make chuhai-first-step`，产物在 `dist/`（不入库）
- 依赖：python3 + pypdf, Chrome, poppler
- 正文是否为 Markdown：**否**：正文在 _build/content.py（结构化卡片数据），暂未转 MD
- 图片素材：无外部图片素材
- 许可：内容 CC BY-SA 4.0，署名 Haitao Pan / XWork Technologies LLC；构建脚本 MIT

---

## 原构建说明

# 独立开发者出海全流程合集 · 重建说明
1. 改内容：`_build/content.py`（章节 CH、卡片 CARDS、TIMELINE/MAP/MASTER、CHECKED 核对日期）；版式在 `_build/render.py`。
2. 构建：`./build.sh --version v1.1 --checked 2026-10-21 --png`（版本默认读 `VERSION` 文件）
3. 产出：`dist/出海全流程合集-<版本>.pdf`、可选 `dist/png-<版本>/01..NN.png`（XHS 用）、`dist/preview-p1-<版本>.png`、中间件 `dist/_work-<版本>/`（HTML、raw PDF）。
页数、页脚 P n/总页、目录页码、进度条、书签都按页面计划自动重算。验证：pdfinfo 页数=计划页数、页脚总页数一致、EIN/邮箱格式文本粗检、渲染第 1 页。
依赖：google-chrome、poppler-utils、python3 + pypdf。规则：内容中不得出现 EIN、地址、账号、邮箱。原 `collection.pdf`、`png/` 不会被改动。
