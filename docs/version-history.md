# 电子书全版本目录（PDF · 源码 · 脚本）

- 生成时间：2026-11-20 15:42 CST（Asia/Shanghai）
- 仓库：[https://github.com/ai-workspace-services/ebooks](https://github.com/ai-workspace-services/ebooks)（默认分支 `main`）
- 规则：每条 PDF 版本列出 Drive 链接；源码仅在能核对到对应 `VERSION` 提交/标签/Release zip 时填写，**绝不**把旧 PDF 指向当前 `main` 冒充同源。
- 变体：`-cover` / `-slim` / `-chat` / `试读` / `分章` / `成长计划` 单独标注，不与正文章节合订本混为一谈。
- 重复副本：同名规范化 + 同大小只保留一条规范链接，其余记「另有 N 份」。

## 系列索引

| 编号 | 系列 | slug | PDF 最新 | main 源码 VERSION | 构建脚本 |
|---|---|---|---|---|
| `XW-EB-01` | 图解 IT 简史 | `it-history` | `v4.9.1` | `v4.9.1` | `books/it-history/build.sh` · `Makefile` · `scripts/build.py` |
| `XW-EB-02` | 图解平台工程 · 云中立实践 | `platform-engineering` | `v0.9.20` | `v0.9.20` | `books/platform-engineering/build.sh` → `build-core.sh` |
| `XW-EB-03` | 趣谈数据基础设施 · AI 时代 | `data-infra` | `v5.1` | `v5.1` | `books/data-infra/build.sh` → `book/build_book.py` |
| `XW-EB-04` | 出海第一步 · 一人公司合规全流程 | `chuhai-first-step` | `v1.4` | `v1.3` | `books/chuhai-first-step/build.sh` → `build.py` |
| `XW-EB-05` | AI 工具出海通关 · 注册与订阅全流程 | `ai-tools-overseas` | `v0.2.6`† | `v0.2.7` | `books/ai-tools-overseas/build.sh` → `src/build.py` |
| `XW-EB-06` | AI-Native 超级个体 · 新时代游戏 | `ai-native` | `v0.9.6` | `v0.9.6` | `books/ai-native/build.sh` → `build.py` |
| `XW-EB-07` | XWorkspace Agent Skills 工程规范 | `agent-skills-spec` | `v0.3` | `v0.3` | `books/agent-skills-spec/build.sh` → `build-core.sh` |
| `XW-EB-08` | 人民币海外卡三条路线攻略 | `cny-overseas-card-routes` | `v1.3` | `v1.2` | `books/cny-overseas-card-routes/build.sh` → `src/build.py` |
| `XW-EB-09` | 独立开发观察者计划 | `indie-observer` | `v0.1-r5` | `v0.1-r5` | `books/indie-observer/build.sh` → `build-core.sh` |
| `—` | 图解经典设计模式 · 遇到 AI 时代 | `design-patterns-ai` | `v0.1` | `v0.1` | `books/design-patterns-ai/build.sh` → `build-core.sh` |

† Drive 最新 PDF 仍为 `v0.2.6`；main 源码 `v0.2.7`。PDF 最新与 main 源码不一致时并列标注，不以源码静默覆盖 PDF 最新。

## 分册历史

### `XW-EB-01` · 图解 IT 简史 (`it-history`)

- 构建脚本：`books/it-history/build.sh` · `Makefile` · `scripts/build.py`
- `main` 上 VERSION：`v4.9.1`
- Release zip：[`it-history-v4.9.1.zip`](https://github.com/ai-workspace-services/ebooks/releases/download/v2026.11.03/it-history-v4.9.1.zip)

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `从机柜到算力中心-图解IT演进史-v4.6.pdf` | 91.9 MB | 2026-10-20 15:19 CST | [打开](https://drive.google.com/file/d/1dCWMaprhnr9Vllrv3x-ZPHnnNFXdgST8/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `从机柜到算力中心-图解IT演进史-v4.7.pdf` | 91.9 MB | 2026-10-20 15:22 CST | [打开](https://drive.google.com/file/d/16l0yiV_dO92NfenqRLL2xw5o2bd2yEzM/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解IT简史-合订本-v4.8.pdf` | 91.9 MB | 2026-10-20 15:37 CST | [打开](https://drive.google.com/file/d/1VwqgmprhopfS3vD_xLDVeE1sgY_4iOIS/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解IT简史-合订本-v4.9.pdf` | 92.0 MB | 2026-10-20 15:52 CST | [打开](https://drive.google.com/file/d/1AGNprtQE5IY0QNmxq54WFN6yCIE1vNqh/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解IT简史-合订本-v4.9.1.pdf` | 92.0 MB | 2026-10-22 11:49 CST | [打开](https://drive.google.com/file/d/1heEAEsvb03bLqjETctFP50TM--bwyvMO/view?usp=drivesdk) | git `1346d3f` (2026-11-09) · 与 `origin/main` VERSION 一致 | — |
| `full-alt-title` | `图解IT简史-合集.pdf` | 95.2 MB | 2026-10-19 13:22 CST | [打开](https://drive.google.com/file/d/18vLV2wQMkyj973SXAAFDVRe4lvo0AQJ5/view?usp=drivesdk) | — | — |
| `full-alt-title` | `图解IT简史-合集-v2.pdf` | 95.2 MB | 2026-10-19 14:30 CST | [打开](https://drive.google.com/file/d/1GlofIhnc8hWLxz2K_fsJlyELjDw3GcDC/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full-alt-title` | `图解IT简史-合集-v3.pdf` | 91.2 MB | 2026-10-19 14:39 CST | [打开](https://drive.google.com/file/d/19Hec7KGf_IKZ79oYjgrEH3bYRhfPcb02/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full-alt-title` | `图解IT简史-合集-v3.1.pdf` | 91.2 MB | 2026-10-19 14:55 CST | [打开](https://drive.google.com/file/d/112XjomH9BFw0dRDet9CaqnwY0EGUaeZw/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full-alt-title` | `图解IT简史-合集-v4.pdf` | 91.4 MB | 2026-10-20 14:06 CST | [打开](https://drive.google.com/file/d/1_440vCCn38KBTISWKkoJpSu4aCR4rmDP/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full-alt-title` | `图解IT简史-合集-v4.1.pdf` | 91.5 MB | 2026-10-20 14:23 CST | [打开](https://drive.google.com/file/d/10ZVXKSZSCBYPO25UupizFmmy9INl2G8b/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full-alt-title` | `图解IT简史-合集-v4.2.pdf` | 91.6 MB | 2026-10-20 14:30 CST | [打开](https://drive.google.com/file/d/1XEeXIMErwkKXedZ5GfiXOhuuCkXgW1gE/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full-alt-title` | `图解IT简史-合集-v4.3.pdf` | 91.8 MB | 2026-10-20 14:53 CST | [打开](https://drive.google.com/file/d/1mNjGgjcIuoMU8eChOZjL09Eo3X1Y7b_-/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full-alt-title` | `从机房到AI-图解IT-合集-v4.4.pdf` | 91.8 MB | 2026-10-20 15:02 CST | [打开](https://drive.google.com/file/d/1olqkISPn2D4NbeLzY7mNSuvq11AcVtlz/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full-alt-title` | `从机房到AI-图解IT-合集-v4.5.pdf` | 91.9 MB | 2026-10-20 15:05 CST | [打开](https://drive.google.com/file/d/1ghGeuSbWZgaN34u4mrjaaxzymbxgI3Kl/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `cover` | `图解IT简史-合订本-v4.9.1-cover.pdf` | 92.1 MB | 2026-11-09 16:34 CST | [打开](https://drive.google.com/file/d/1FiYpzr0l7zuGQkyApPA4u93AABZeKPYP/view?usp=drivesdk) | 封面变体（非正文权威） | 3 |
| `trial` | `图解IT简史-试读版.pdf` | 1.6 MB | 2026-10-30 15:26 CST | [打开](https://drive.google.com/file/d/1SlrcpYFsLQB__ULOVRc6wFDqjeQpoAyF/view?usp=drivesdk) | 变体 `trial`（非正文章节合订本权威） | — |

### `XW-EB-02` · 图解平台工程 · 云中立实践 (`platform-engineering`)

- 构建脚本：`books/platform-engineering/build.sh` → `build-core.sh`
- `main` 上 VERSION：`v0.9.20`
- Release zip：[`platform-engineering-v0.9.18.zip`](https://github.com/ai-workspace-services/ebooks/releases/download/v2026.11.03/platform-engineering-v0.9.18.zip)

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `图解平台工程-云中立实践-v0.1.pdf` | 14.9 MB | 2026-10-22 12:59 CST | [打开](https://drive.google.com/file/d/1f5nu-8SBcTtEdURlLXu_5pQ-cqzTiKqp/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.2.pdf` | 15.1 MB | 2026-10-22 13:06 CST | [打开](https://drive.google.com/file/d/1ijCyVCK1m3nloFaed7ZJt2e8u57pViok/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.3.pdf` | 15.3 MB | 2026-10-22 13:20 CST | [打开](https://drive.google.com/file/d/1H_spCb8_D9BFmogJacigVTvSJQt49NTZ/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.4.pdf` | 15.5 MB | 2026-10-22 13:26 CST | [打开](https://drive.google.com/file/d/1qe8wD726HlRKLF5mKaxvhcN8gwaZRevp/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.5.pdf` | 15.6 MB | 2026-10-22 13:35 CST | [打开](https://drive.google.com/file/d/1tTW-XoSqifjKorbPMnXxcljbqmEKZLOW/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.6.pdf` | 15.8 MB | 2026-10-22 13:39 CST | [打开](https://drive.google.com/file/d/1EkkBF8yIZNyiieJpoB3b5FIzNSs-Eqqj/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.7.pdf` | 15.9 MB | 2026-10-22 13:41 CST | [打开](https://drive.google.com/file/d/15LQjOhO4NDok5f49PA2L_9F41y0iF3vb/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.8.pdf` | 16.0 MB | 2026-10-22 13:55 CST | [打开](https://drive.google.com/file/d/1y04yrH0WCvsD9WgO2KwAeRM1QakrIhtq/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.8.1.pdf` | 23.1 MB | 2026-10-22 15:44 CST | [打开](https://drive.google.com/file/d/1bD8Sk4ZuyzyjUm6IYJhmCnrjvNeMouKc/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.8.2.pdf` | 23.1 MB | 2026-10-22 15:52 CST | [打开](https://drive.google.com/file/d/1KVkEn8xrr69nRePElzfvooKL-mAsz3_8/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.8.3.pdf` | 23.1 MB | 2026-10-22 16:00 CST | [打开](https://drive.google.com/file/d/18W6Dlh4pdcJaBtroFFuI1SoAXhDSJ8D6/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.8.4.pdf` | 23.2 MB | 2026-10-22 17:48 CST | [打开](https://drive.google.com/file/d/1ByUrCE1_6DMIgdFL1vh2DI2l-lxwWrV1/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.8.5.pdf` | 23.2 MB | 2026-10-22 19:14 CST | [打开](https://drive.google.com/file/d/1htCGKo69Yz5OeP3-aLXy-1WsAQ0rblp5/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `图解平台工程-云中立实践-v0.9.13.pdf` | 25.3 MB | 2026-10-30 20:27 CST | [打开](https://drive.google.com/file/d/1b7zYmm3SgWfQ0Lzu368Gkvv5W6dPQvR6/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `图解平台工程-云中立实践-v0.9.14.pdf` | 25.3 MB | 2026-10-31 10:18 CST | [打开](https://drive.google.com/file/d/1X9-brVXnZCoGyZ1LA6yceoHT13rPYfeI/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `图解平台工程-云中立实践-v0.9.15.pdf` | 25.5 MB | 2026-10-31 20:18 CST | [打开](https://drive.google.com/file/d/1l6HEY7GbzB21FZlWOuSGLP9Lj1ajs4n4/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `图解平台工程-云中立实践-v0.9.16.pdf` | 25.5 MB | 2026-10-31 21:24 CST | [打开](https://drive.google.com/file/d/1EYzdILseVYi9UiloWyT6AiOr6PGLfhnn/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `图解平台工程-云中立实践-v0.9.17.pdf` | 25.6 MB | 2026-10-31 21:24 CST | [打开](https://drive.google.com/file/d/1BYjjpphncOTPuYkwRr82jxIldTdBaIQe/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `图解平台工程-云中立实践-v0.9.18.pdf` | 26.9 MB | 2026-11-01 11:18 CST | [打开](https://drive.google.com/file/d/1zIMw-K_cppDddF5Vwvb3SELC6Aga64cO/view?usp=drivesdk) | git `0caad32` (2026-11-03) | 2 |
| `full` | `图解平台工程-云中立实践-v0.9.19.pdf` | 27.5 MB | 2026-11-08 20:27 CST | [打开](https://drive.google.com/file/d/1LWfBq6ZcEitdrgwW-1NCGfLmvT9nNwnh/view?usp=drivesdk) | git `5dbc021` (2026-11-08) | 2 |
| `full` | `图解平台工程-云中立实践-v0.9.20.pdf` | 27.5 MB | 2026-11-09 16:34 CST | [打开](https://drive.google.com/file/d/1-3ZlangvoxT8qswBIFGGvq5Jsrz9b3-8/view?usp=drivesdk) | git `1346d3f` (2026-11-09) · 与 `origin/main` VERSION 一致 | 3 |
| `cover` | `图解平台工程-云中立实践-v0.9.13-cover.pdf` | 25.4 MB | 2026-10-31 17:29 CST | [打开](https://drive.google.com/file/d/10my0bLT5W0WjFLSOIiPIeGnlJ-KqPrXD/view?usp=drivesdk) | 封面变体（非正文权威） | 2 |
| `slim` | `图解平台工程-云中立实践-v0.9.19-slim.pdf` | 26.1 MB | 2026-11-08 20:27 CST | [打开](https://drive.google.com/file/d/1MM4mLH3xGD3cdG9uszIqokvMqrygSh5A/view?usp=drivesdk) | 变体 `slim`（非正文章节合订本权威） | — |
| `chat` | `图解平台工程-云中立实践-v0.9.19-chat.pdf` | 19.8 MB | 2026-11-09 20:25 CST | [打开](https://drive.google.com/file/d/1tzHmjzCsesBej0pAZpsaIUqOFR_pFJIT/view?usp=drivesdk) | 变体 `chat`（非正文章节合订本权威） | — |
| `build-artifact-name` | `dist__图解平台工程-云中立实践-v0.9.12.pdf` | 25.3 MB | 2026-10-30 13:25 CST | [打开](https://drive.google.com/file/d/1SH9Ujxd4lLt8i0rGzmp3t1ZY4Mo_4b-h/view?usp=drivesdk) | 变体 `build-artifact-name`（非正文章节合订本权威） | — |

### `XW-EB-03` · 趣谈数据基础设施 · AI 时代 (`data-infra`)

- 构建脚本：`books/data-infra/build.sh` → `book/build_book.py`
- `main` 上 VERSION：`v5.1`
- Release zip：[`data-infra-v5.1.zip`](https://github.com/ai-workspace-services/ebooks/releases/download/v2026.11.03/data-infra-v5.1.zip)

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `数据基础设施-AI时代-合订本-2026-10-20.pdf` | 38.9 MB | 2026-10-30 15:26 CST | [打开](https://drive.google.com/file/d/1HYFxvwKzVHVOSBm3zSk_yPPuGvsmaTDe/view?usp=drivesdk) | — | — |
| `full` | `数据基础设施-AI时代-合订本-品牌标封面.pdf` | 38.9 MB | 2026-10-22 11:50 CST | [打开](https://drive.google.com/file/d/1X8TLrKzfLAxYv9UjahWjqrMPrZJl3dFg/view?usp=drivesdk) | — | — |
| `full` | `数据基础设施-AI时代-合订本-xwork封面.pdf` | 38.9 MB | 2026-10-20 20:08 CST | [打开](https://drive.google.com/file/d/1gIpewhB3wHPwLytryV5MkfGqYE8YlOwp/view?usp=drivesdk) | — | — |
| `full` | `数据基础设施-AI时代-合订本.pdf` | 38.9 MB | 2026-10-20 19:31 CST | [打开](https://drive.google.com/file/d/1AnMWT_Qdd6MEtDRisI_q_BSPZDxfZl5k/view?usp=drivesdk) | — | — |
| `full` | `数据基础设施-AI前后-合订本.pdf` | 38.7 MB | 2026-10-20 13:18 CST | [打开](https://drive.google.com/file/d/1WXgwuFJ-3WuETm2JYUGUSn7j2PepBDHE/view?usp=drivesdk) | — | — |
| `full` | `数据基础设施-AI前后-合订本-v2.pdf` | 38.8 MB | 2026-10-30 15:26 CST | [打开](https://drive.google.com/file/d/13HpCS0oYSHu7r_hwLhtNSx5pDwYdlLWH/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `数据基础设施-AI前后-合订本-v3.pdf` | 38.8 MB | 2026-10-30 15:26 CST | [打开](https://drive.google.com/file/d/1vJwPL_b1Q7mrT3EQrPypXNLcKPfp1b29/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `数据基础设施-AI前后-合订本-v4.pdf` | 38.9 MB | 2026-10-30 15:26 CST | [打开](https://drive.google.com/file/d/1sOPAIh3yjYg5JNXV3JsQK_MlAvBfx7z_/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `趣谈数据基础设施-AI时代-合订本-v5.pdf` | 38.9 MB | 2026-10-23 12:23 CST | [打开](https://drive.google.com/file/d/1-15FQTw7S3M69MeVcDn6Ca2KnIxs4wvX/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `趣谈数据基础设施-AI时代-合订本-v5.1.pdf` | 38.9 MB | 2026-10-30 20:26 CST | [打开](https://drive.google.com/file/d/1OaenKGbINFoJ9_AZnXLxcOCd0sqDZo7p/view?usp=drivesdk) | git `1346d3f` (2026-11-09) · 与 `origin/main` VERSION 一致 | — |
| `cover` | `趣谈数据基础设施-AI时代-合订本-v5.1-cover.pdf` | 39.0 MB | 2026-11-09 16:34 CST | [打开](https://drive.google.com/file/d/18w7rBthBg4xML1HcvtNv7NxkUSA_RRso/view?usp=drivesdk) | 封面变体（非正文权威） | 3 |
| `trial` | `数据基础设施-AI时代-试读版.pdf` | 26.8 MB | 2026-10-30 15:26 CST | [打开](https://drive.google.com/file/d/14JNCz9pzUs-s3E7lXb3qenelRCVWQhd-/view?usp=drivesdk) | 变体 `trial`（非正文章节合订本权威） | — |
| `build-artifact-name` | `data-ai__book__趣谈数据基础设施-AI时代-合订本-v5.pdf` | 38.9 MB | 2026-10-30 13:26 CST | [打开](https://drive.google.com/file/d/1VtKeSoinukS4M8rIRaK4AHR1wjYD5vNI/view?usp=drivesdk) | 变体 `build-artifact-name`（非正文章节合订本权威） | — |
| `build-artifact-name` | `data-ai__book__趣谈数据基础设施-AI时代-合订本-v5.1.pdf` | 38.9 MB | 2026-10-30 13:26 CST | [打开](https://drive.google.com/file/d/1vKE2rnAS7drHIxqfynES-ARpyEd81LFf/view?usp=drivesdk) | 变体 `build-artifact-name`（非正文章节合订本权威） | — |

### `XW-EB-04` · 出海第一步 · 一人公司合规全流程 (`chuhai-first-step`)

- 构建脚本：`books/chuhai-first-step/build.sh` → `build.py`
- `main` 上 VERSION：`v1.3`
- Release zip：[`chuhai-first-step-v1.2.zip`](https://github.com/ai-workspace-services/ebooks/releases/download/v2026.11.03/chuhai-first-step-v1.2.zip)

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `出海第一步-一人公司合规全流程-v1.1.pdf` | 2.6 MB | 2026-10-23 12:23 CST | [打开](https://drive.google.com/file/d/1VI19y1Vuh8Askfp93YalhEgfatz0s2JB/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `pk__a__出海第一步-一人公司合规全流程-v1.2-xhs.pdf` | 2.5 MB | 2026-10-30 13:26 CST | [打开](https://drive.google.com/file/d/1YSeLTldvLduXN2D92cmmYosvwURqEUef/view?usp=drivesdk) | git `0caad32` (2026-11-03) | 2 |
| `full` | `出海第一步-一人公司合规全流程-v1.3.pdf` | 2.8 MB | 2026-11-09 15:59 CST | [打开](https://drive.google.com/file/d/1x0VKuTWtLQXVZLBQFkQNWMZjUstlZ1Dg/view?usp=drivesdk) | git `1346d3f` (2026-11-09) · 与 `origin/main` VERSION 一致 | — |
| `full` | `出海第一步-一人公司合规全流程-v1.4.pdf` | 2.8 MB | 2026-11-14 19:10 CST | [打开](https://drive.google.com/file/d/1z36up2-1qnYN_vFT_DlMx2TXX_Dv93bg/view?usp=drivesdk) | git `2f8e9fb` (2026-11-20) | 3 |
| `cover` | `出海第一步-一人公司合规全流程-v1.2-cover.pdf` | 2.6 MB | 2026-10-31 17:29 CST | [打开](https://drive.google.com/file/d/1FvBdqNWLP0asnLcSMkwSYHp98e1VGJBT/view?usp=drivesdk) | 封面变体（非正文权威） | 2 |
| `cover` | `出海第一步-一人公司合规全流程-v1.3-cover.pdf` | 2.6 MB | 2026-11-09 20:25 CST | [打开](https://drive.google.com/file/d/1iu-4Q4xOBhVg7STpndY7VTiGgy4FzbA7/view?usp=drivesdk) | 封面变体（非正文权威） | 3 |
| `cover` | `出海第一步-一人公司合规全流程-v1.4-cover.pdf` | 2.3 MB | 2026-11-13 20:29 CST | [打开](https://drive.google.com/file/d/1bOWjRT5nSiCn8ZwtGAefuk8nxGIwLGTX/view?usp=drivesdk) | 封面变体（非正文权威） | 2 |
| `bundle` | `出海全流程合集-v1.0.pdf` | 2.2 MB | 2026-10-21 15:32 CST | [打开](https://drive.google.com/file/d/11t6fa9zoy9mxGuGW7-1Vzr482NHW3OEg/view?usp=drivesdk) | 变体 `bundle`（非正文章节合订本权威） | — |

### `XW-EB-05` · AI 工具出海通关 · 注册与订阅全流程 (`ai-tools-overseas`)

- 构建脚本：`books/ai-tools-overseas/build.sh` → `src/build.py`
- `main` 上 VERSION：`v0.2.7`
- Release zip：[`ai-tools-overseas-v0.2.5.zip`](https://github.com/ai-workspace-services/ebooks/releases/download/v2026.11.03/ai-tools-overseas-v0.2.5.zip)

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `AI-Native超级个体-含AI工具出海前置章节.pdf` | 7.7 MB | 2026-10-29 22:19 CST | [打开](https://drive.google.com/file/d/173_Ig96lT9LqK55ShXtnwKc89jWUdkEI/view?usp=drivesdk) | — | — |
| `full` | `AI工具出海通关-注册与订阅全流程-v0.1.pdf` | 17.0 MB | 2026-10-25 20:38 CST | [打开](https://drive.google.com/file/d/1l91T7TchXnX0QQeLlNuqw6eKz8PxGzm2/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI工具出海通关-注册与订阅全流程-v0.2.pdf` | 1.0 MB | 2026-10-25 20:42 CST | [打开](https://drive.google.com/file/d/1mhJOOJ0v5zFrRT8GMIpdnaOQ_TKUMtEi/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI工具出海通关-注册与订阅全流程-v0.2.1.pdf` | 1.0 MB | 2026-10-25 20:44 CST | [打开](https://drive.google.com/file/d/1KMQZqUgmGI_PILaVxjmsR4Mcb74hT99d/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI工具出海通关-注册与订阅全流程-v0.2.2.pdf` | 1.0 MB | 2026-10-25 20:47 CST | [打开](https://drive.google.com/file/d/1v_-pzYJZ6q4ihhZ3F_wJALU6M1djv55Z/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI工具出海通关-注册与订阅全流程-v0.2.3.pdf` | 1.0 MB | 2026-10-25 20:47 CST | [打开](https://drive.google.com/file/d/17TdZTPuX6fEulf2Htuu2agS7Of7J0dlA/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI工具出海通关-注册与订阅全流程-v0.2.4.pdf` | 1.0 MB | 2026-10-25 20:51 CST | [打开](https://drive.google.com/file/d/1K6YNbs2K-vvzOe7rdKmm2tsmxhdh69Ci/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI工具出海通关-注册与订阅全流程-v0.2.5.pdf` | 1.1 MB | 2026-10-30 20:30 CST | [打开](https://drive.google.com/file/d/1qEqo7rKo08vgzwRCMCDJI_LjGKG5UOR2/view?usp=drivesdk) | git `1346d3f` (2026-11-09) · 与 `origin/main` VERSION 一致 | — |
| `full` | `AI工具出海通关-注册与订阅全流程-v0.2.6.pdf` | 1.2 MB | 2026-11-14 19:09 CST | [打开](https://drive.google.com/file/d/15V24YDIendKxzegDhO1yUq3Tr1z8EOVF/view?usp=drivesdk) | git `2f8e9fb` (2026-11-20) | 3 |
| `full` | `AI工具出海通关-注册与订阅全流程-v0.2.7`（源码在 main；Drive PDF 未入库） | — | 2026-11-20 | — | git `2b79558` / `8aaf69f` · 与 `origin/main` VERSION `v0.2.7` 一致 | — |
| `cover` | `AI工具出海通关-注册与订阅全流程-v0.2.5-cover.pdf` | 1.2 MB | 2026-11-09 16:34 CST | [打开](https://drive.google.com/file/d/1rr02eUNN3TXS2VjtY7TO7DGHKn6sBE6z/view?usp=drivesdk) | 封面变体（非正文权威） | 3 |
| `cover` | `AI工具出海通关-注册与订阅全流程-v0.2.6-cover.pdf` | 1.1 MB | 2026-11-13 20:29 CST | [打开](https://drive.google.com/file/d/1G4-NJ2fZ5JBbqpJQH9f5KLC_G-_6YnNI/view?usp=drivesdk) | 封面变体（非正文权威） | 2 |

### `XW-EB-06` · AI-Native 超级个体 · 新时代游戏 (`ai-native`)

- 构建脚本：`books/ai-native/build.sh` → `build.py`
- `main` 上 VERSION：`v0.9.6`
- Release zip：[`ai-native-v0.9.6.zip`](https://github.com/ai-workspace-services/ebooks/releases/download/v2026.11.03/ai-native-v0.9.6.zip)

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `AI-Native超级个体-含AI工具出海前置章节.pdf` | 7.7 MB | 2026-10-29 22:19 CST | [打开](https://drive.google.com/file/d/173_Ig96lT9LqK55ShXtnwKc89jWUdkEI/view?usp=drivesdk) | — | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.2.pdf` | 13.9 MB | 2026-10-23 14:35 CST | [打开](https://drive.google.com/file/d/1Qt1a8iWibCVM5i27xgBjyxRrdcJlFAri/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.3.pdf` | 13.3 MB | 2026-10-23 14:42 CST | [打开](https://drive.google.com/file/d/1_sxsb7_VSyk1TUhyJWBfccgvMMn3evUw/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.4.pdf` | 13.5 MB | 2026-10-23 14:43 CST | [打开](https://drive.google.com/file/d/1P059Y7Y-PMKr4jIaUmQoC_GQrtvDg0-a/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.5.pdf` | 14.4 MB | 2026-10-23 15:10 CST | [打开](https://drive.google.com/file/d/1vVXo1GJVK1tnd-y_nGVRoiIEqieB5hxu/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.6.pdf` | 14.6 MB | 2026-10-23 15:18 CST | [打开](https://drive.google.com/file/d/1tZwnqML6kTVAGWWVsjXACzUf87Z6f6_e/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.7.pdf` | 19.3 MB | 2026-10-23 15:33 CST | [打开](https://drive.google.com/file/d/1NvMsLxPXu4ZTS5yQMtGQFx6vbK9dkf0M/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.7.1.pdf` | 19.3 MB | 2026-10-23 15:37 CST | [打开](https://drive.google.com/file/d/1Xd9cr6F7i52TxC8txC6T5MyuWQU5wpZl/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.7.2.pdf` | 19.3 MB | 2026-10-23 15:40 CST | [打开](https://drive.google.com/file/d/1S7PD4E3JPpfEjgMKa6fxHoTewgeUX2wh/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.8.pdf` | 30.5 MB | 2026-10-23 15:50 CST | [打开](https://drive.google.com/file/d/1UEL1H5yETSn6ib-fWdiC-uUFgXELTlRM/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.9.pdf` | 7.3 MB | 2026-10-23 16:15 CST | [打开](https://drive.google.com/file/d/1qrFIJ8tvLUfHYK7THskdp4n24nJfGrmq/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.9.1.pdf` | 7.3 MB | 2026-10-23 16:45 CST | [打开](https://drive.google.com/file/d/1WsXk-ITz6fUG9lLy8lmsksjyEEgchvdz/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.9.2.pdf` | 7.3 MB | 2026-10-23 16:40 CST | [打开](https://drive.google.com/file/d/1YbFR_58pAk9gb9RrVrDB69mX1KuwmYww/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.9.3.pdf` | 7.3 MB | 2026-10-23 16:54 CST | [打开](https://drive.google.com/file/d/1KBLI7wdg5Ghp42ea6vrqrr7zK3-7uv3m/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `AI-Native超级个体-新时代游戏-v0.9.4.pdf` | 7.1 MB | 2026-10-23 16:59 CST | [打开](https://drive.google.com/file/d/1UylMMVnDKx3rOwLqYlHoQT3fxlMJp87m/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.9.5.pdf` | 7.1 MB | 2026-10-30 20:29 CST | [打开](https://drive.google.com/file/d/1dw3JKKFHKEdyYK0D0QgCUsAssOrEurAY/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | — |
| `full` | `AI-Native超级个体-新时代游戏-v0.9.6.pdf` | 7.2 MB | 2026-11-09 16:38 CST | [打开](https://drive.google.com/file/d/1YRNgaJ9xyqIOfJio7qa3RbXUVM4C7VKD/view?usp=drivesdk) | git `1346d3f` (2026-11-09) · 与 `origin/main` VERSION 一致 | 5 |
| `cover` | `AI-Native超级个体-新时代游戏-v0.9.5-cover.pdf` | 7.1 MB | 2026-10-31 17:29 CST | [打开](https://drive.google.com/file/d/1KxkoyDcVyYS1SU68dJMcEq_-w0RFwDYp/view?usp=drivesdk) | 封面变体（非正文权威） | 2 |
| `early` | `AI-Native超级个体-成长计划-v0.1.pdf` | 13.6 MB | 2026-10-30 13:26 CST | [打开](https://drive.google.com/file/d/1XZDEHB5HBJLwoq_hvy5zIc5Vmzwxr9-b/view?usp=drivesdk) | 变体 `early`（非正文章节合订本权威） | 2 |

### `XW-EB-07` · XWorkspace Agent Skills 工程规范 (`agent-skills-spec`)

- 构建脚本：`books/agent-skills-spec/build.sh` → `build-core.sh`
- `main` 上 VERSION：`v0.3`
- Release zip：[`agent-skills-spec-v0.2.zip`](https://github.com/ai-workspace-services/ebooks/releases/download/v2026.11.03/agent-skills-spec-v0.2.zip)

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `agent-skills-shots-latest.pdf` | 1.1 MB | 2026-11-09 20:25 CST | [打开](https://drive.google.com/file/d/14fA8klDknKd-SLy8Ws-Fn5R-izRQhGLC/view?usp=drivesdk) | — | — |
| `full` | `XWorkspace-Agent工程规范包-开放方案-v0.1.pdf` | 1.2 MB | 2026-10-31 21:24 CST | [打开](https://drive.google.com/file/d/15vQ_mVKn9sPvv9tKoZdeC2JUkdi_lQl_/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `XWorkspace-Agent-Skills工程规范-开放方案-v0.2.pdf` | 1.1 MB | 2026-11-09 16:38 CST | [打开](https://drive.google.com/file/d/14E3pw7rxZyY8Ois0CsWmm29et8t2T-5c/view?usp=drivesdk) | git `1346d3f` (2026-11-09) | 5 |
| `full` | `XWorkspace-Agent-Skills工程规范-开放方案-v0.3.pdf` | 1.4 MB | 2026-11-13 20:28 CST | [打开](https://drive.google.com/file/d/1YBUcJ_98XopUBvSLTkw2NR5mi9y7r6Qm/view?usp=drivesdk) | git `cd92089` (2026-11-13) · 与 `origin/main` VERSION 一致 | 7 |

### `XW-EB-08` · 人民币海外卡三条路线攻略 (`cny-overseas-card-routes`)

- 构建脚本：`books/cny-overseas-card-routes/build.sh` → `src/build.py`
- `main` 上 VERSION：`v1.2`
- Release zip：[`cny-overseas-card-routes-v1.1.zip`](https://github.com/ai-workspace-services/ebooks/releases/download/v2026.11.03/cny-overseas-card-routes-v1.1.zip)

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `人民币海外卡三条路线攻略-v1.0.pdf` | 726 KB | 2026-11-03 20:23 CST | [打开](https://drive.google.com/file/d/1BFvJXKtqLggw3_0lIVFmezxlSp4Z8gwB/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `人民币海外卡三条路线攻略-v1.1.pdf` | 856 KB | 2026-11-03 23:08 CST | [打开](https://drive.google.com/file/d/197gS3oRpKPgU4PUBOXQhHkjS_LZGu6vS/view?usp=drivesdk) | git `0caad32` (2026-11-03) | 3 |
| `full` | `人民币海外卡三条路线攻略-v1.2.pdf` | 954 KB | 2026-11-09 20:25 CST | [打开](https://drive.google.com/file/d/1zdauxtHp5qaSA6bckKDhhgBwADw1uxJS/view?usp=drivesdk) | git `1346d3f` (2026-11-09) · 与 `origin/main` VERSION 一致 | 3 |
| `full` | `人民币海外卡三条路线攻略-v1.3.pdf` | 1.0 MB | 2026-11-13 20:29 CST | [打开](https://drive.google.com/file/d/1ftAz_9O8RdRXvfuIyH_RFEQYs4ooYH17/view?usp=drivesdk) | git `2f8e9fb` (2026-11-20) | 2 |

### `XW-EB-09` · 独立开发观察者计划 (`indie-observer`)

- 构建脚本：`books/indie-observer/build.sh` → `build-core.sh`
- `main` 上 VERSION：`v0.1-r5`
- Release zip：[`indie-observer-v0.1-r5.zip`](https://github.com/ai-workspace-services/ebooks/releases/download/v2026.11.03/indie-observer-v0.1-r5.zip)

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1.pdf` | 7.0 MB | 2026-10-31 18:23 CST | [打开](https://drive.google.com/file/d/1fXyZiWuii4YVnT7snvm_KaQK6L9X3epL/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1-r2.pdf` | 7.1 MB | 2026-10-31 18:23 CST | [打开](https://drive.google.com/file/d/1aSadPlEC5cYH9SAIz1pV4re79jGq2e7R/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1-r3.pdf` | 7.1 MB | 2026-10-31 18:23 CST | [打开](https://drive.google.com/file/d/1oBLT6Zkmr76XBB8BreFO5KOwFVVgyWFS/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 4 |
| `full` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1-r4.pdf` | 7.1 MB | 2026-10-31 18:23 CST | [打开](https://drive.google.com/file/d/1sbWIgFCBfi2BFNUwm9XleqrUUERIoGHY/view?usp=drivesdk) | **源码未核对到**（Drive 有 PDF；ebooks 仓 VERSION 历史/Release 无对应项） | 2 |
| `full` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1-r5.pdf` | 9.9 MB | 2026-11-09 16:34 CST | [打开](https://drive.google.com/file/d/1HXiQyf3tLghYUGcBQfjgf2q1QIhOecQj/view?usp=drivesdk) | git `1346d3f` (2026-11-09) · 与 `origin/main` VERSION 一致 | 2 |
| `cover` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1-r4-cover.pdf` | 7.2 MB | 2026-10-31 17:29 CST | [打开](https://drive.google.com/file/d/1-LWTESk9I4S0rjJGryL904arT4UI6nIh/view?usp=drivesdk) | 封面变体（非正文权威） | 2 |

### `—` · 图解经典设计模式 · 遇到 AI 时代 (`design-patterns-ai`)

- 构建脚本：`books/design-patterns-ai/build.sh` → `build-core.sh`
- `main` 上 VERSION：`v0.1`

| 类型 | 版本/名称 | 大小 | Drive 修改时间 | PDF | 源码核对 | 重复 |
|---|---|---:|---|---|---|---:|
| `full` | `图解经典设计模式-遇到AI时代-v0.1.pdf` | 2.1 MB | 2026-11-13 20:28 CST | [打开](https://drive.google.com/file/d/16EzI1vYY6okyMkOyAnk64NtR3UH2I8KK/view?usp=drivesdk) | git `a1cd8d8` (2026-11-13) · 与 `origin/main` VERSION 一致 | 3 |

## 源码缺口汇总

下列 **正文章节 PDF** 在 `books/*/VERSION` 提交历史与 `v2026.11.03` Release zip 中未能核对到一一对应源码快照（多早于 2026-11-03 monorepo 导入）：

| 编号 | slug | 版本 | PDF 文件名 |
|---|---|---|---|
| `XW-EB-01` | `it-history` | `v4.6` | `从机柜到算力中心-图解IT演进史-v4.6.pdf` |
| `XW-EB-01` | `it-history` | `v4.7` | `从机柜到算力中心-图解IT演进史-v4.7.pdf` |
| `XW-EB-01` | `it-history` | `v4.8` | `图解IT简史-合订本-v4.8.pdf` |
| `XW-EB-01` | `it-history` | `v4.9` | `图解IT简史-合订本-v4.9.pdf` |
| `XW-EB-01` | `it-history` | `v2` | `图解IT简史-合集-v2.pdf` |
| `XW-EB-01` | `it-history` | `v3` | `图解IT简史-合集-v3.pdf` |
| `XW-EB-01` | `it-history` | `v3.1` | `图解IT简史-合集-v3.1.pdf` |
| `XW-EB-01` | `it-history` | `v4` | `图解IT简史-合集-v4.pdf` |
| `XW-EB-01` | `it-history` | `v4.1` | `图解IT简史-合集-v4.1.pdf` |
| `XW-EB-01` | `it-history` | `v4.2` | `图解IT简史-合集-v4.2.pdf` |
| `XW-EB-01` | `it-history` | `v4.3` | `图解IT简史-合集-v4.3.pdf` |
| `XW-EB-01` | `it-history` | `v4.4` | `从机房到AI-图解IT-合集-v4.4.pdf` |
| `XW-EB-01` | `it-history` | `v4.5` | `从机房到AI-图解IT-合集-v4.5.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.1` | `图解平台工程-云中立实践-v0.1.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.2` | `图解平台工程-云中立实践-v0.2.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.3` | `图解平台工程-云中立实践-v0.3.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.4` | `图解平台工程-云中立实践-v0.4.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.5` | `图解平台工程-云中立实践-v0.5.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.6` | `图解平台工程-云中立实践-v0.6.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.7` | `图解平台工程-云中立实践-v0.7.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.8` | `图解平台工程-云中立实践-v0.8.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.8.1` | `图解平台工程-云中立实践-v0.8.1.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.8.2` | `图解平台工程-云中立实践-v0.8.2.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.8.3` | `图解平台工程-云中立实践-v0.8.3.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.8.4` | `图解平台工程-云中立实践-v0.8.4.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.8.5` | `图解平台工程-云中立实践-v0.8.5.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.9.13` | `图解平台工程-云中立实践-v0.9.13.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.9.14` | `图解平台工程-云中立实践-v0.9.14.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.9.15` | `图解平台工程-云中立实践-v0.9.15.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.9.16` | `图解平台工程-云中立实践-v0.9.16.pdf` |
| `XW-EB-02` | `platform-engineering` | `v0.9.17` | `图解平台工程-云中立实践-v0.9.17.pdf` |
| `XW-EB-03` | `data-infra` | `v2` | `数据基础设施-AI前后-合订本-v2.pdf` |
| `XW-EB-03` | `data-infra` | `v3` | `数据基础设施-AI前后-合订本-v3.pdf` |
| `XW-EB-03` | `data-infra` | `v4` | `数据基础设施-AI前后-合订本-v4.pdf` |
| `XW-EB-03` | `data-infra` | `v5` | `趣谈数据基础设施-AI时代-合订本-v5.pdf` |
| `XW-EB-04` | `chuhai-first-step` | `v1.1` | `出海第一步-一人公司合规全流程-v1.1.pdf` |
| `XW-EB-05` | `ai-tools-overseas` | `v0.1` | `AI工具出海通关-注册与订阅全流程-v0.1.pdf` |
| `XW-EB-05` | `ai-tools-overseas` | `v0.2` | `AI工具出海通关-注册与订阅全流程-v0.2.pdf` |
| `XW-EB-05` | `ai-tools-overseas` | `v0.2.1` | `AI工具出海通关-注册与订阅全流程-v0.2.1.pdf` |
| `XW-EB-05` | `ai-tools-overseas` | `v0.2.2` | `AI工具出海通关-注册与订阅全流程-v0.2.2.pdf` |
| `XW-EB-05` | `ai-tools-overseas` | `v0.2.3` | `AI工具出海通关-注册与订阅全流程-v0.2.3.pdf` |
| `XW-EB-05` | `ai-tools-overseas` | `v0.2.4` | `AI工具出海通关-注册与订阅全流程-v0.2.4.pdf` |
| `XW-EB-06` | `ai-native` | `v0.2` | `AI-Native超级个体-新时代游戏-v0.2.pdf` |
| `XW-EB-06` | `ai-native` | `v0.3` | `AI-Native超级个体-新时代游戏-v0.3.pdf` |
| `XW-EB-06` | `ai-native` | `v0.4` | `AI-Native超级个体-新时代游戏-v0.4.pdf` |
| `XW-EB-06` | `ai-native` | `v0.5` | `AI-Native超级个体-新时代游戏-v0.5.pdf` |
| `XW-EB-06` | `ai-native` | `v0.6` | `AI-Native超级个体-新时代游戏-v0.6.pdf` |
| `XW-EB-06` | `ai-native` | `v0.7` | `AI-Native超级个体-新时代游戏-v0.7.pdf` |
| `XW-EB-06` | `ai-native` | `v0.7.1` | `AI-Native超级个体-新时代游戏-v0.7.1.pdf` |
| `XW-EB-06` | `ai-native` | `v0.7.2` | `AI-Native超级个体-新时代游戏-v0.7.2.pdf` |
| `XW-EB-06` | `ai-native` | `v0.8` | `AI-Native超级个体-新时代游戏-v0.8.pdf` |
| `XW-EB-06` | `ai-native` | `v0.9` | `AI-Native超级个体-新时代游戏-v0.9.pdf` |
| `XW-EB-06` | `ai-native` | `v0.9.1` | `AI-Native超级个体-新时代游戏-v0.9.1.pdf` |
| `XW-EB-06` | `ai-native` | `v0.9.2` | `AI-Native超级个体-新时代游戏-v0.9.2.pdf` |
| `XW-EB-06` | `ai-native` | `v0.9.3` | `AI-Native超级个体-新时代游戏-v0.9.3.pdf` |
| `XW-EB-06` | `ai-native` | `v0.9.4` | `AI-Native超级个体-新时代游戏-v0.9.4.pdf` |
| `XW-EB-06` | `ai-native` | `v0.9.5` | `AI-Native超级个体-新时代游戏-v0.9.5.pdf` |
| `XW-EB-07` | `agent-skills-spec` | `v0.1` | `XWorkspace-Agent工程规范包-开放方案-v0.1.pdf` |
| `XW-EB-08` | `cny-overseas-card-routes` | `v1.0` | `人民币海外卡三条路线攻略-v1.0.pdf` |
| `XW-EB-09` | `indie-observer` | `v0.1` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1.pdf` |
| `XW-EB-09` | `indie-observer` | `v0.1-r2` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1-r2.pdf` |
| `XW-EB-09` | `indie-observer` | `v0.1-r3` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1-r3.pdf` |
| `XW-EB-09` | `indie-observer` | `v0.1-r4` | `独立开发观察者计划-AI×可观测SaaS首季-v0.1-r4.pdf` |

## 说明

- monorepo 于 2026-11-03 `0caad32` Initial import 起才有统一 `VERSION` 追踪；更早 PDF 大多仅有 Drive 归档。
- 本地 `/workspace/it-history`、`platform-book`、`ai-native-book` 等历史工作区，未逐版本校验前不得当作某一旧 PDF 的精确源码。
- 构建脚本路径以当前 monorepo 为准。
