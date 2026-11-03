# AI-Native 超级个体 · 新时代游戏

- 版本：`v0.9.6`（见 `VERSION`；升版只改这个文件）
- 构建：`./build.sh` 或在仓库根目录 `make ai-native`，产物在 `dist/`（不入库）
- 依赖：python3 + markdown + pypdf, Chrome
- 正文是否为 Markdown：部分：sources/*.md 为原稿，排版正文在 _build/*.py（未转 MD）
- 图片素材：不入库，按 `assets.manifest.json` 从 Google Drive 拉取（`./fetch-assets.sh`，build.sh 会自动调用）
- 许可：内容 CC BY-SA 4.0，署名 Haitao Pan / XWork Technologies LLC；构建脚本 MIT

---

## 原构建说明

# AI-Native 超级个体 · 成长计划
重建：./build.sh [--version v0.1]，产出 dist/。依赖 google-chrome、poppler-utils、python3+pypdf。
内容在 _build/content.py 与 _build/base_chapters.json，图在 assets/。
