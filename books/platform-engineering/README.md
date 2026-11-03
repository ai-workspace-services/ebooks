# 图解平台工程 · 云中立实践

- 版本：`v0.9.18`（见 `VERSION`；升版只改这个文件）
- 构建：`./build.sh` 或在仓库根目录 `make platform-engineering`，产物在 `dist/`（不入库）
- 依赖：python3, Chrome, poppler, Noto CJK
- 正文是否为 Markdown：否（Markdown 正文 src/book.md；figs.py 生成图示）
- 图片素材：不入库，按 `assets.manifest.json` 从 Google Drive 拉取（`./fetch-assets.sh`，build.sh 会自动调用）
- 许可：内容 CC BY-SA 4.0，署名 Haitao Pan / XWork Technologies LLC；构建脚本 MIT

