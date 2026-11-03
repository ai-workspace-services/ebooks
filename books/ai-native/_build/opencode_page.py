CASES=[('Zcode 事件：曾被公开报道的代码与环境信息收集争议',
 '据开发者 ferstar（2026-09-18，个人博客与 X）首次披露，并经 V2EX 社区讨论与 vonng.com 分析：事件曝光前，ZCode 3.12.3 桌面端在登录状态下即会把整个工作区（含完整 .git 历史、LFS 缓存、reflog 与本地配置）打包，AES 加密后直传阿里云 OSS；解密私钥仅在服务端，用户本地无法解密，设置中也未找到关闭开关。',
 '厂商回应：据 ZCode 官方 X 账号与界面新闻（2026-09-21），官方致歉并开源；据金融界报道，ZCode 于 2026-09-18 发布情况说明，称问题源于「代码库索引」功能，已修复并致歉；据界面新闻，2026-09-21 官方宣布开源客户端，称 v3.14.0 已移除 Repo Wiki 与快照上传链路，第三方审计确认相关云端存储已删除，并承诺代码未用于训练。<br>据 GitHub 仓库页面（2026-10-23 查看，组织名 Z.ai，简介注明 Zhipu.ai）：仓库创建于 2026-09-20，Apache-2.0 许可；共 6 个提交（「Initial commit」后即「feat: open source」），此前开发历史不在仓库中，后续为「sync ZCode source」式同步；Issues 与 Discussions 均已关闭；README 未见致歉声明。据作者观察，厂商此前删除了原有提交历史（待核实）。'),
('Trae 遥测争议：关闭开关后仍被报告持续上报',
 '据 The Register（2025-07-28）与 Cybernews 报道，开发者 segmentationf4u1t 在 GitHub 发布分析称：在设置中关闭遥测后，Trae 约 7 分钟内仍有约 500 次请求、约 26 MB 数据发往字节跳动服务器，含设备标识与使用行为数据。',
 '厂商回应：据上述报道，字节跳动更新了设置说明，称该开关只控制 VS Code 框架层的遥测，其他 Trae 组件的遥测不受影响；之后官方文档提供了「隐私模式」。')]
cs=''.join(f'<div class="mi" style="line-height:1.45;font-size:20px"><span style="font-weight:800">{E(h)}</span><br>{E(a)}<br><span style="color:#5a6b78">{E(r).replace('&lt;br&gt;','<br>')}</span></div>' for h,a,r in CASES)
add(f'''<div class="kicker">3.6 · 附 · 作者推荐</div><h1>作者推荐：编程工具统一用 OpenCode</h1>
<div class="gbox win" style="font-size:21px;line-height:1.5"><b>我的选择（个人观点）</b>开源阵营的模型我都接，但编程工具我只装一把：<span style="font-weight:800;color:#1d6b3a">OpenCode</span>。理由有四条：
<br>① 闭源的 IDE / Agent 工具会上传哪些代码和环境信息，用户自己没法验证；
<br>② 「免费」往往是拿隐私数据换的——不花钱的装备，账单可能记在你的仓库上；
<br>③ 有的工具是封闭生态，进去容易，带着存档出来难；
<br>④ 开源代码由全球开发者一起审计，国际上的信任度更高。
<br>更实际的是：OpenCode 经我们的网关（New API / LiteLLM）能接任何模型，正好是主城 OpenCode + DSH + DS-Bot 主运行时的一部分，换阵营不换武器。</div>
<div class="map"><div class="mt">真实案例：踩坑记录（据公开报道整理，表述以报道与厂商回应为准）</div>{cs}
<div class="mc">教训：装备上手前先看它会把什么发出去；仓库里别留密钥，历史里出现过的凭据要轮换。</div></div>
<div class="src">来源清单见源码包 sources/ch03-sources-20261023.md</div>''','03 装备库 · 3.6 作者推荐',bm='　3.6 附 作者推荐：编程工具统一用 OpenCode')
