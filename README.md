# ebooks

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE-code)
[![build](https://github.com/ai-workspace-services/ebooks/actions/workflows/build.yml/badge.svg)](https://github.com/ai-workspace-services/ebooks/actions/workflows/build.yml)

把书当仓库维护：每本书的 Markdown 正文、构建脚本和版本号在一起走版本，改版时章节和示例一起提交、一起评审。PDF 由 CI 构建，不入库。

| 书 | 版本 | 构建 | 图片素材 | PDF |
|---|---|---|---|---|
| 图解平台工程 · 云中立实践 | `v0.9.18` | `make platform-engineering` | Drive | [docs](https://xworktech.com/docs) |
| 图解 IT 简史 | `v4.9.1` | `make it-history` | Drive | [docs](https://xworktech.com/docs) |
| 趣谈数据基础设施 · AI 时代 | `v5.1` | `make data-infra` | Drive | [docs](https://xworktech.com/docs) |
| 出海第一步 · 一人公司合规全流程 | `v1.2` | `make chuhai-first-step` | — | [docs](https://xworktech.com/docs) |
| AI 工具出海通关 · 注册与订阅全流程 | `v0.2.5` | `make ai-tools-overseas` | — | [docs](https://xworktech.com/docs) |
| AI-Native 超级个体 · 新时代游戏 | `v0.9.6` | `make ai-native` | Drive | [docs](https://xworktech.com/docs) |
| 独立开发观察者计划：AI × 可观测 SaaS 首季 | `v0.1-r5` | `make indie-observer` | Drive | [docs](https://xworktech.com/docs) |
| XWorkspace Agent Skills 工程规范 · 开放方案 | `v0.2` | `make agent-skills-spec` | — | [docs](https://xworktech.com/docs) |
| 人民币 ⇄ 海外卡 · 三条路线攻略 | `v1.1` | `make cny-overseas-card-routes` | — | [docs](https://xworktech.com/docs) |

## 用法

```bash
make list          # 列出所有书
make all           # 构建全部（需要图片素材的书会先从 Drive 拉取）
make it-history    # 构建单本
make clean
```

目录约定：`books/<slug>/` 下有 `VERSION`、`build.sh`、`README.md`、正文与脚本；需要图片的书另有 `assets.manifest.json` 和 `fetch-assets.sh`。

## 图片与二进制不入库

`*.png *.jpg *.gif *.webp *.svg *.mp4 *.pdf` 等二进制全部在 `.gitignore` 里。图片按书打包上传在 Google Drive「Grok Bot 制品/books/<slug>/assets/」，
`assets.manifest.json` 记录 Drive 文件 id、分卷 sha256 和每个文件的 sha256。`tools/fetch_assets.py` 下载、校验后解压回原路径。

认证顺序：`GDRIVE_SA_JSON`（服务账号 JSON 内容或路径）→ `GDRIVE_ACCESS_TOKEN` → 公开下载。
**公开构建前提**：要么把这些 Drive 文件共享给 CI 服务账号，要么设成「知道链接的任何人可查看」。本仓库没有改动任何共享设置。


## 图片素材体积（v2 压缩后）

| 书 | 压缩前 archive | 压缩后 | 说明 |
|---|---:|---:|---|
| it-history | 658 MB | 110 MB | PNG→JPEG q82，长边≤1800；2 分卷 |
| indie-observer | 68 MB | 57 MB | 仍含大量动图 GIF，压缩空间有限 |
| ai-native | 29 MB | 7.6 MB | |
| data-infra | 12 MB | 7.1 MB | JPEG 再压缩 |
| platform-engineering | 2.9 MB | 0.7 MB | |

Drive 上保留了压缩前的旧包；CI 与 `assets.manifest.json` 指向 `*-assets-v2.tar`。公开下载不需要 `GDRIVE_SA_JSON`（文件夹已「知道链接的人可查看」），仍建议配置该 secret 作为备用。

## CI / Release

`.github/workflows/build.yml`：按 `books/*` 生成矩阵，每本书一个 job。

- PR / push main：构建并上传 PDF 为 workflow artifact。
- 推 tag `<slug>-v<version>`（如 `it-history-v4.9.1`）：只构建这本并发布到 GitHub Release。
- 推 tag `v*`（如 `v2026.11.03`）：构建全部并发布到同一个 Release。
- 只用 `GITHUB_TOKEN`（`contents: write` 仅在 release job）。

需要你在仓库 Settings → Secrets → Actions 添加：

| Secret | 用途 | 缺失时 |
|---|---|---|
| `GDRIVE_SA_JSON` | 能读取上述 Drive 素材的服务账号 JSON | 需要图片的书（platform-engineering, it-history, data-infra, ai-native, indie-observer）打 warning 并跳过，其余照常构建 |

## 许可

- 书籍内容：[CC BY-SA 4.0](LICENSE)（署名-相同方式共享 4.0 国际）。署名：**Haitao Pan / XWork Technologies LLC**。
- 构建脚本与工具代码：[MIT](LICENSE-code)。
