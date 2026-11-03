# 独立开发观察者计划：AI × 可观测 SaaS 首季

- 版本：`v0.1-r5`（见 `VERSION`；升版只改这个文件）
- 构建：`./build.sh` 或在仓库根目录 `make indie-observer`，产物在 `dist/`（不入库）
- 依赖：python3 + markdown, Chrome, poppler
- 正文是否为 Markdown：是（src/content/... series-v4 + articles，来自 knowledge main，含 #294）
- 图片素材：不入库，按 `assets.manifest.json` 从 Google Drive 拉取（`./fetch-assets.sh`，build.sh 会自动调用）
- 许可：内容 CC BY-SA 4.0，署名 Haitao Pan / XWork Technologies LLC；构建脚本 MIT

---

## 原构建说明

# 独立开发观察者计划：AI × 可观测 SaaS 首季 — 构建源

## 一条命令重建
    ./build.sh                       # 默认 v0.1-r4
    BOOK_VERSION=v0.2 ./build.sh     # 升版本：改这个变量即可（BOOK_DATE 可选覆盖日期）
产物：`dist/独立开发观察者计划-AI×可观测SaaS首季-<版本>.pdf`，`dist/book.html`，预览 `preview/cover.png`、`preview/toc.png`。
脚本会检查第 2 页必须是目录，否则报错（防空白页回归）。

## 改哪里
- `book/toc.json`：书名、三个月分组、12 篇标题（title=目录定稿标题）、小红书标题、状态、字数、R1–R3 替补。篇目状态改成「全文稿」即收公众号+小红书全文，否则只收大纲。
- `book/intro.md`：本季主题 / 主线 / 写作结构。
- `book/reading-notes.md`：阅读顺序说明。
- `book/style.css`：版式。封面固定 240mm 高，勿超过 261mm 可打印高度，否则会多出空白页。
- `src/content/...series-v4/<篇目>/`：文章正文（从 knowledge 仓库同步过来，替换后重跑即可）。
- `cover-front.png` / `cover-back.png`：封面封底。
- `legacy/`：旧的一次性脚本，仅留档。
