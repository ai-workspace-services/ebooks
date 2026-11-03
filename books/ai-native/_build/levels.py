# 第 05 章 副本：我的 AI 工作流（来源：workflow-videos episodes 01–04 + out/v2 静帧）
LV=[
('01-docs','副本 1','我的AI工作流-一份底稿五个平台','Agent 写稿 · 脚本出版 · 人最后定稿','选题 / 大纲',
 'Grok Bot 写作 · 多平台分发 · 人工闸门',
 ['章节草稿 + 插图 → build.sh 生成整本 PDF → v0.x 版本号递增','风格预设：微信 / 小红书 / X / 领英 / 兔子论坛，每个平台出一份草稿','能自动发？Yes → X · Buffer 自动发布；No → 草稿待人工发'],
 '人工闸门「要改吗？」：Yes 回写作重来；No 开链接分享 · 上架',
 ['页脚 / 许可不对 → 重建','封面不对 → 重出图','快速开始页以仓库为准','Drive：源码 + PDF 作为新文件上传'],
 '一份底稿，五个平台各拿到自己风格的版本，人工确认后分享上架。'),
('02-coding','副本 2','我的AI工作流-代码AI写合并我来按','Codex / OpenCode 写码 · CI 把关 · 人决定合并','目标 prompt / issue',
 'Agent 实现 · CI · 人工闸门',
 ['Agent 开分支 → 写代码 + 测试 → 开 PR','GitHub Actions 自动运行','全绿？No → 修复再推（回到写代码）'],
 '人工闸门「合并？」：Yes → 合入 main → Mac 同步（ff-only）',
 ['案例：xconnect-app #127–129 · qmd #9 · 快速开始脚本 9/9','执行器口径同第 02 章：OpenCode + DSH 为主运行时，Codex 以适配器 Worker 接入'],
 'CI 全绿 + 人按下合并，代码进 main，本机 ff-only 同步。'),
('03-execution','副本 3','我的AI工作流-几个AI并行我只看一张表','定时任务驱动 · 多 Agent 并行 · 每晚汇总','定时任务到点',
 '执行层 · 汇总 · 人工闸门 + 发布',
 ['并行出战：Codex 21:36 Inbox 处理；Gemini · Antigravity 整理协作规范；Grok Bot 每 3 小时修 CI','21:00 每日汇总表：按 Agent 统计 完成 / 进行中 / 等用户 / 阻塞','Drive .md 每日存档'],
 '人工闸门：看 Top 待办 → 「发 X？」Yes → Buffer 每天两条',
 ['每日 Loop · 一直在转','人只看一张表，不盯每个 Agent'],
 '当天的汇总表与 .md 存档生成，Top 待办有人看过。'),
('04-chuhai-compliance','副本 4','我的AI工作流-一人公司出海合规先行','美国 LLC · 只谈合规 · 三地独立循环','决定出海做产品',
 '美国 · 公司主体 / 香港 · 个人 / 大陆 · 红线',
 ['注册美国 LLC（选州 · 注册代理）→ 申请 EIN（税号到手，妥善保管）','Mercury 企业账户：公司收支独立核算 → 应用商店开发者号：以公司主体上架收款','年报 / 报税：按期申报，每年复核；香港 · 个人独立循环，留存凭证'],
 '大陆红线「个人 ↔ 海外公户？」：禁止，双向都不做；个人境外投资依法依规',
 ['美国 · 香港各自独立循环','大陆个人 ↔ 海外公户 严禁','每年年报报税 · 合规优先','出自《出海第一步 · 一人公司合规全流程》；仅为流程梳理，不构成法律或税务意见'],
 '合规先行 · 每年一轮：主体、税号、账户、开发者号、年报全部到位且不碰红线。'),
]
entry(5,'05','副本：我的 AI 工作流','4 条作者自己的 AI 工作流，一集一个副本。')
add(f'''<div class="kicker">第 05 章 · 副本</div><h1>副本：我的 AI 工作流</h1>
<div class="lead">主城建好、装备配齐，就该刷副本了。这 4 个副本是作者每天在跑的真实工作流，各配一张泳道图静帧作关卡插画。</div>
{''.join(f'<div class="it"><b>{E(x[1])}</b><span><b>{E(x[2])}</b><br>{E(x[3])}</span></div>' for x in LV)}
<div class="map"><div class="mt">通用规则</div><div class="mi">每个副本都有入口（触发）、队伍（泳道）、Boss（人工闸门或红线）和通关条件</div><div class="mi">Agent 负责刷怪，人只守最后一道门：定稿、合并、看表、守红线</div><div class="mi">回路（红线箭头）= 失败重开，不算掉档</div></div>
<div class="note">道具鉴定：本章内容来自作者的工作流脚本（E1 · 用户提供的流程），不代表已通过 4.2 验收。</div>''','05 副本')
for d,no,t,sub,trig,team,steps,boss,notes,clear in LV:
    add(f'''<div class="kicker">第 05 章 · {E(no)}</div><h1 style="font-size:44px">{E(t)} {tag("E1 作者工作流")}</h1>
<div style="display:flex;gap:30px"><img src="{(ROOT/'assets'/f'lv-{d}.png').as_uri()}" style="width:400px;height:711px;border-radius:14px;border:1px solid #dde5f0;flex:0 0 auto">
<div style="flex:1;font-size:22px;line-height:1.55"><div class="src">{E(sub)}</div>
<div class="it"><b style="flex-basis:96px">入口</b><span>{E(trig)}</span></div><div class="it"><b style="flex-basis:96px">队伍</b><span>{E(team)}</span></div>
<h2 style="font-size:26px">攻略步骤</h2>{''.join(f'<div class="mi" style="font-size:21px">{i+1}. {E(s)}</div>' for i,s in enumerate(steps))}
<h2 style="font-size:26px">Boss</h2><div style="font-size:21px">{E(boss)}</div></div></div>
<div class="map" style="padding:16px 26px;margin-top:16px"><div class="mt">回路 / 备注</div>{''.join(f'<div class="mi" style="font-size:20px;padding:3px 0">{E(n)}</div>' for n in notes)}</div>
<div class="note" style="margin:14px 0;font-size:22px"><b>通关条件</b>：{E(clear)}</div>''',f'05 {no}',bm=f'　{no} · {t}')
