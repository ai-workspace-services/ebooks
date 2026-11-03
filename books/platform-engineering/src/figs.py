# Simple SVG 图解 for the sample chapter. Palette: bright tech-blue.
BG='#f8f9fa'; PANEL='#e8f0fb'; TITLE='#101c44'; ACC='#4b43e8'; PRI='#0058bd'
F="font-family:'Noto Sans CJK SC',sans-serif"
def box(x,y,w,h,t,sub='',fill=PANEL,stroke=PRI,tc=TITLE):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
    cy=y+h/2+(-6 if sub else 5)
    s+=f'<text x="{x+w/2}" y="{cy}" text-anchor="middle" font-size="15" font-weight="700" fill="{tc}" style="{F}">{t}</text>'
    if sub: s+=f'<text x="{x+w/2}" y="{cy+19}" text-anchor="middle" font-size="11.5" fill="{"#e8f0fb" if tc=="#fff" else "#46506e"}" style="{F}">{sub}</text>'
    return s
def arrow(x1,y1,x2,y2,label='',c=ACC):
    s=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="2" marker-end="url(#ah)"/>'
    if label: s+=f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-7}" text-anchor="middle" font-size="11" fill="{c}" style="{F}">{label}</text>'
    return s
def svg(h,body):
    return (f'<svg viewBox="0 0 500 {h}" xmlns="http://www.w3.org/2000/svg"><defs>'
     f'<marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{ACC}"/></marker>'
     f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#075ecc"/><stop offset="1" stop-color="#4338ca"/></linearGradient></defs>'
     f'<rect width="500" height="{h}" rx="14" fill="{BG}"/>{body}</svg>')
FIGS={}
FIGS['fig1']=('图 5-1 安全层三件套：各管一件事', svg(250,
  box(20,30,140,80,'Vault','秘密 · 策略 · 短期令牌')+box(180,30,140,80,'OIDC / JWT','机器身份交换')+box(340,30,140,80,'Zitadel','人的统一身份')+
  box(20,160,140,56,'CI 流水线','不存密码',fill='#fff')+box(180,160,140,56,'服务 / 主机','运行时读凭据',fill='#fff')+box(340,160,140,56,'工程师','统一登录',fill='#fff')+
  arrow(90,160,90,112,'换令牌')+arrow(250,160,250,112)+arrow(410,160,410,112,'登录')+arrow(160,70,178,70)))
FIGS['fig2']=('图 5-2 CI 怎样不碰密码：一次运行的凭据旅程', svg(330,
  box(20,24,200,56,'Gitea Actions','自建 · 开发版签发 OIDC')+box(280,24,200,56,'GitHub Actions','托管 · 原生签发 OIDC')+
  box(130,120,240,56,'JWT 身份令牌','repository · ref · job_workflow_ref')+
  box(130,210,240,56,'Vault JWT 角色','核对声明 → 绑定策略',fill='url(#g)',stroke=ACC,tc='#fff')+
  box(130,290-10,240,40,'batch 令牌 · 1 小时 · 只读','',fill='#fff')+
  arrow(120,80,200,118)+arrow(380,80,300,118)+arrow(250,176,250,208)+arrow(250,266,250,278)).replace('fill="#46506e" style','fill="#46506e" style',1))
rows=[('portal 构建','prod','v* / release/v* / prod-v2-*'),('Platform-Orchestrator','sit / uat / prod','每环境一份角色'),('gcp-oidc（runtime）','uat / prod','只读本环境联合配置'),('aws-bootstrap','uat / prod','main + GitHub Environment')]
b=''.join(f'<rect x="20" y="{70+i*48}" width="460" height="40" rx="8" fill="{PANEL if i%2==0 else "#fff"}"/>'
  f'<text x="34" y="{95+i*48}" font-size="13" font-weight="700" fill="{TITLE}" style="{F}">{a}</text>'
  f'<text x="215" y="{95+i*48}" font-size="12.5" fill="{PRI}" style="{F}">{e}</text>'
  f'<text x="318" y="{95+i*48}" font-size="12" fill="#46506e" style="{F}">{c}</text>' for i,(a,e,c) in enumerate(rows))
FIGS['fig3']=('图 5-3 角色即代码：58 份角色声明按服务 × 环境拆开（示例）', svg(280,
  f'<text x="34" y="50" font-size="12" fill="{ACC}" font-weight="700" style="{F}">角色（roles/*.json）</text><text x="215" y="50" font-size="12" fill="{ACC}" font-weight="700" style="{F}">环境</text><text x="318" y="50" font-size="12" fill="{ACC}" font-weight="700" style="{F}">信任条件</text>'+b))
FIGS['fig4']=('图 5-4 交付端 fail closed：解析不到凭据就停', svg(300,
  box(150,20,200,50,'部署开始','Ansible playbook')+box(150,100,200,50,'从 Vault 解析规范凭据')+
  box(20,200,190,60,'解析到：写入','保留受保护备份 · diff 隐藏')+box(290,200,190,60,'解析不到：停止','不写空值 · 报错退出',fill='#fff',stroke=ACC)+
  arrow(250,70,250,98)+arrow(220,150,130,198,'有')+arrow(280,150,375,198,'无')))
def T(x,y,t,sz=12,c=TITLE,w='400',a='middle'): return f'<text x="{x}" y="{y}" text-anchor="{a}" font-size="{sz}" font-weight="{w}" fill="{c}" style="{F}">{t}</text>'
FIGS['fig61']=('图 6-1 一条实践线：多环境 → 不可变环境 → 滚动升级', svg(170,
  box(15,40,145,70,'多环境','SIT / UAT / PROD')+box(178,40,145,70,'不可变环境','同一构件 · 声明替换')+box(341,40,145,70,'滚动升级','分批替换 · 可回滚',fill='url(#g)',stroke=ACC,tc='#fff')+
  arrow(160,75,176,75)+arrow(323,75,339,75)+T(250,145,'GitOps · 环境副本 · Kubernetes · Argo CD / Flux CD 都在实践它',11.5,PRI)))
FIGS['fig62']=('图 6-2 漂移 vs 收敛：手工改动让现实偏离，控制器把现实拉回声明', svg(230,
  box(20,30,200,55,'Git 声明','唯一的真相')+box(280,30,200,55,'真实环境','运行中的状态')+
  arrow(220,50,278,50,'收敛 (pull)')+f'<line x1="278" y1="72" x2="222" y2="72" stroke="#c0392b" stroke-width="2" stroke-dasharray="5 4"/>'+T(250,95,'对比差异',11,'#c0392b')+
  box(280,140,200,55,'手工登录改参数','漂移来源',fill='#fff',stroke='#c0392b')+arrow(380,140,380,88,'',c='#c0392b')+
  box(20,140,200,55,'改声明 → PR 评审','唯一的变更入口',fill='#fff')+arrow(120,140,120,88)))
FIGS['fig63']=('图 6-3 构建一次、晋级同一构件：CI 只读验证，CD 消费唯一快照', svg(250,
  box(15,30,140,55,'commit / PR','Gitea ≡ GitHub')+box(180,30,140,55,'CI 只读验证','构建一次')+box(345,30,140,55,'不可变快照','uat-daily-build-…')+
  arrow(155,57,178,57)+arrow(320,57,343,57)+
  ''.join(box(15+i*165,160,140,55,e,'同一 tag · 同一摘要') for i,e in enumerate(['SIT','UAT','PROD']))+
  arrow(415,85,85,158,'晋级同一个产物')+arrow(155,187,178,187)+arrow(320,187,343,187)))
FIGS['fig64']=('图 6-4 滚动升级：maxSurge 多起一个，就绪后再停一个旧的（示意，4 副本）', svg(260,
  ''.join(T(30,55+r*52,lab,11.5,PRI,'700','start')+''.join(f'<rect x="{130+i*62}" y="{35+r*52}" width="50" height="32" rx="7" fill="{("url(#g)" if c=="n" else (PANEL if c=="o" else "#fff"))}" stroke="{PRI}" stroke-dasharray="{"4 3" if c=="w" else "0"}"/>'+T(155+i*62,56+r*52,{"n":"v2","o":"v1","w":"v2…"}[c],11,"#fff" if c=="n" else TITLE) for i,c in enumerate(row))
  for r,(lab,row) in enumerate([('开始',['o','o','o','o']),('起新 Pod',['o','o','o','o','w']),('就绪 → 停旧',['n','o','o','o']),('完成',['n','n','n','n'])]))+
  T(250,248,'未就绪的 Pod 不进 Service 后端 · 出问题 kubectl rollout undo',11,ACC)))
FIGS['fig65']=('图 6-5 从单机到集群：同一套 Git 仓库布局，只换收敛控制器', svg(270,
  box(150,20,200,55,'Git 仓库（Gitea ≡ GitHub）','environments/&lt;env&gt; · services/')+
  box(15,150,145,75,'阶段一','Compose + Doco CD')+box(178,150,145,75,'阶段二','K3s/K8s + Argo CD')+box(341,150,145,75,'阶段二（并列）','K3s/K8s + Flux CD')+
  arrow(210,75,90,148,'pull')+arrow(250,75,250,148,'pull')+arrow(290,75,410,148,'pull')+
  T(250,258,'单机 VPS  →  集群：先跑通，再扩展',11,PRI)))
FIGS['fig66']=('图 6-6 制品仓库在云中立流水线里的位置：构建一次，推送、签名、扫描，再按摘要拉取', svg(300,
  box(15,25,140,58,'CI 构建一次','Gitea ≡ GitHub Actions')+box(180,25,140,58,'Harbor','推送 · 签名 · 扫描',fill='url(#g)',stroke=ACC,tc='#fff')+box(345,25,140,58,'GitOps 声明','按摘要引用镜像')+
  arrow(155,54,178,54,'robot 推送')+arrow(320,54,343,54)+
  box(180,130,140,52,'项目 · RBAC','保留策略 · 代理缓存',fill='#fff')+arrow(250,83,250,128)+
  box(345,130,140,52,'Doco / Argo / Flux','从 Harbor 拉取',fill='#fff')+arrow(415,83,415,128)+
  box(15,215,140,52,'Harbor 副本 A','任意云 / 机房',fill='#fff')+box(180,215,140,52,'Harbor 副本 B','另一个环境',fill='#fff')+box(345,215,140,52,'其他 OCI 仓库','兼容即可复制',fill='#fff')+
  arrow(230,182,90,213,'复制')+arrow(250,182,250,213)+arrow(270,182,410,213)))
FIGS['figP2']=('图 P2-1 经典回路 vs 现代闭环：四类代码化事实源经向量化成为可观测的平台状态，再交给 Agent 在约束内控制（类比示意）', svg(470,
  T(20,26,'经典回路（上篇）：单输入单输出，负反馈',12.5,PRI,'700','start')+
  box(15,40,105,50,'commit','设定值')+box(140,40,105,50,'GitOps','流水线 · 控制器')+box(265,40,105,50,'环境','被控对象')+box(390,40,95,50,'实际状态','输出',fill='#fff')+
  arrow(120,65,138,65)+arrow(245,65,263,65)+arrow(370,65,388,65)+
  f'<path d="M437,90 L437,112 L192,112 L192,92" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ah)"/>'+T(315,126,'对比差异 → 拉回声明',11,ACC)+
  f'<line x1="15" y1="146" x2="485" y2="146" stroke="#c9d3e6"/>'+
  T(20,170,'现代闭环（下篇）：多输入多输出，以平台状态为中心',12.5,PRI,'700','start')+
  ''.join(box(15+i*118,182,108,44,t,s,fill='#fff') for i,(t,s) in enumerate([('GitOps','部署期望状态'),('IaC','资源'),('CaC','Config as Code'),('CMDB','资产与关系')]))+
  ''.join(arrow(69+i*118,226,250,256) for i in range(4))+
  box(130,258,240,52,'向量化 · 平台状态空间','资源 · 发布 · 配置 · 成本 · 告警',fill='url(#g)',stroke=ACC,tc='#fff')+
  box(15,268,100,40,'可观测','状态观测器',fill='#fff')+arrow(115,288,128,288)+
  box(160,340,180,50,'AI Agent','控制器：建议 / 执行')+arrow(250,310,250,338)+
  box(385,268,100,40,'21 项规范','约束条件',fill='#fff')+arrow(385,288,372,288)+
  box(15,340,120,50,'黄金路径','推荐轨迹',fill='#fff')+arrow(135,365,158,365)+
  box(365,340,120,50,'熔断 · 审批','安全边界',fill='#fff',stroke='#c0392b')+arrow(363,365,342,365,'',c='#c0392b')+
  box(160,412,180,44,'复盘写回规范与测试','自适应控制',fill='#fff')+arrow(250,390,250,410)+
  f'<path d="M340,434 L470,434 L470,312" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ah)"/>'))

def _row(y,items,w=88,gap=10,x0=15,fill='#fff'):
    return ''.join(box(x0+i*(w+gap),y,w,46,t,s,fill=fill) for i,(t,s) in enumerate(items))+''.join(arrow(x0+i*(w+gap)+w,y+23,x0+(i+1)*(w+gap)-2,y+23) for i in range(len(items)-1))
FIGS['figV11']=('图 11-0 平台状态向量化：只取进 Git 的事实源，按 commit 增量刷新，秘密在入库前过滤，检索按身份过滤', svg(250,
  _row(20,[('Git 事实源','声明·模块·规范'),('过滤秘密','Vault 值不入库'),('语义切分','module / role'),('向量化','带 commit 元数据'),('索引','有版本')])+
  T(250,100,'合入 main → CI 只处理变更文件 → 索引记录 commit',11,ACC)+
  box(140,120,220,50,'检索（按 OIDC 身份过滤）','开发者 / Agent 只见授权范围',fill='url(#g)',stroke=ACC,tc='#fff')+arrow(449,66,360,140)+
  box(15,195,140,40,'回答带出处','仓库 · 路径 · commit',fill='#fff')+box(345,195,140,40,'Agent 观测器','11.5 MCP 工具',fill='#fff')+arrow(180,170,120,193)+arrow(320,170,400,193)))
FIGS['figS12']=('图 12-1 规范的版本化绑定：本机只引用固定 SHA 的快照，升级与回退都是换一个 SHA', svg(230,
  _row(20,[('规范仓库','PR 审查后合入'),('完整 SHA','不接受分支'),('预览','默认不改本机'),('--apply','worktree 快照'),('--check','漂移即停止')])+
  box(60,110,170,50,'current → versions/<SHA>','活动版本指针',fill='url(#g)',stroke=ACC,tc='#fff')+box(270,110,170,50,'lock.json + history/','受管清单 · 显式回退')+
  arrow(400,66,150,108)+arrow(230,135,268,135)+
  T(250,190,'只做本地 worktree 与链接操作：不部署、不调云 API、不碰 DNS / 主机 / 数据库',11,ACC)+
  T(250,212,'遇到非本工具管理的同名目录 → 停止，不覆盖',11,PRI)))
FIGS['figS13']=('图 13-1 黄金路径：把规范预先串进模板，新项目第一天就满足规范；偏离写进合同', svg(220,
  box(15,20,120,60,'21 项规范','第 12 章')+arrow(135,50,163,50)+
  box(165,20,170,60,'黄金路径模板','PR 规则·CI·Harbor·GitOps·观测·备份',fill='url(#g)',stroke=ACC,tc='#fff')+arrow(335,50,363,50)+
  box(365,20,120,60,'新项目','SIT → UAT → PROD')+
  _row(120,[('静态站点',''),('Web 服务',''),('数据库',''),('AI 应用','')],w=108,gap=10)+arrow(250,80,250,118)+
  T(250,200,'不适合任何路径？→ 偏离写成合同（5.5）：哪条、为什么、谁批准、何时复查',11,ACC)))
FIGS['figS14']=('图 14-1 自助链路：每一步都是代码，凭据由 Vault 下发，结果回到门户', svg(160,
  _row(20,[('申请','门户 / Agent → PR'),('策略 / 审批','自助·审批·只读'),('交付','OpenTofu + Ansible'),('凭据','Vault 动态下发'),('门户','Cloud Hub / Ops')])+
  T(250,100,'外部集成同样进 Git：DNS · 告警规则 · 存储策略 · 通知路由 · OIDC 客户端',11,ACC)+
  T(250,126,'结果写回 CMDB（4.4）并被向量索引收录（11.1）',11,PRI)))
FIGS['figS15']=('图 15-1 AI 辅助维护闭环：AI 值守前四步，人审批变更，复盘写回规则只经 PR', svg(250,
  _row(20,[('观测','告警·巡检'),('诊断','指标+索引'),('建议/执行','plan·白名单'),('验证','SLO 复查'),('复盘写回','Runbook·测试')])+
  f'<path d="M449,66 L449,100 L59,100 L59,68" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ah)"/>'+T(250,116,'自适应：规则经 PR 更新后进入下一轮',11,ACC)+
  box(15,140,150,50,'熔断','破坏性动作默认禁止',fill='#fff',stroke='#c0392b')+box(175,140,150,50,'审批','写操作先出 plan',fill='#fff',stroke='#c0392b')+box(335,140,150,50,'回滚','制品·快照·GitOps',fill='#fff',stroke='#c0392b')+
  T(250,220,'人在 Operations / Releases 上做决定',11.5,PRI,'700')))
FIGS['figS16']=('图 16-1 全书结构：上篇七层是经典回路，下篇在其上加以平台状态为中心的闭环', svg(240,
  T(250,22,'下篇：现代闭环',12,PRI,'700')+
  _row(34,[('11 状态',''),('12 规范',''),('13 路径',''),('14 自助',''),('15 值守','')])+
  box(15,105,470,36,'平台状态（代码化 + 向量化）','',fill='url(#g)',stroke=ACC,tc='#fff')+
  T(250,165,'上篇：七层经典回路 → 第 10 章 Open Platform',12,PRI,'700')+
  ''.join(box(15+i*67,177,60,40,t,'',fill='#fff') for i,t in enumerate(['Git/CI','资源','交付','身份','环境','云中立','观测']))))
FIGS['figW9']=('图 9-4 八阶段升级：UAT 演练产出晋级资格，PROD 消费同一构件并重新预检', svg(230,
  _row(20,[('preflight',''),('backup',''),('migration',''),('promotion',''),('verification','')])+
  _row(100,[('rollback','只回退应用'),('repromotion','同一 digest'),('终验','')],w=120,gap=20,x0=40)+
  arrow(449,66,420,98)+
  box(140,170,220,46,'晋级资格 → PROD','重新预检，不做演练',fill='url(#g)',stroke=ACC,tc='#fff')+arrow(400,146,330,168)))

FIGS['figW3']=('图 3-4 资源交接：声明与密钥引用经控制面校验后交给 IaC，产出 CMDB，playbook 只读 CMDB，最后汇总验收', svg(240,
  box(15,15,140,40,'GitOps 声明','资源 · 拓扑 · 版本',fill='#fff')+box(15,70,140,40,'密钥服务','只给最小范围',fill='#fff')+
  box(185,40,130,46,'控制面校验','输入 · 版本 · 身份')+arrow(155,35,185,55)+arrow(155,90,185,72)+
  box(345,40,140,46,'IaC','render · plan · apply')+arrow(315,63,343,63)+
  box(345,130,140,46,'CMDB','本次资源事实')+arrow(415,86,415,128)+
  box(185,130,130,46,'playbook','主机 · 服务 · 数据')+arrow(345,153,317,153)+
  box(15,130,140,46,'服务 CI','tag · digest',fill='#fff')+arrow(155,153,183,153)+
  box(150,190,200,40,'控制面汇总验收','回执齐全才放行',fill='url(#g)',stroke=ACC,tc='#fff')+arrow(250,176,250,188)))
FIGS['figW10']=('图 10-4 五层分工：入口只派发，控制面只校验与放行，执行归 IaC 与 playbook role，回执回到控制面', svg(250,
  box(15,20,110,46,'CI 入口','审批 · 派发')+box(150,20,130,46,'控制面','校验 · 放行',fill='url(#g)',stroke=ACC,tc='#fff')+arrow(125,43,148,43)+
  box(320,20,165,46,'GitOps','期望状态',fill='#fff')+arrow(280,43,318,43)+
  box(150,110,130,46,'IaC','资源 · DNS · state')+box(320,110,165,46,'playbook','主机 · 服务 · 数据')+arrow(215,66,215,108)+arrow(260,66,360,108)+
  box(150,190,130,40,'CMDB','资源事实',fill='#fff')+arrow(215,156,215,188)+arrow(280,210,400,158)+
  f'<path d="M400,156 L400,175 L470,175 L470,90 L265,90 L265,68" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ah)"/>'+
  T(70,200,'回执空 / 失败',10.5,ACC)+T(70,216,'不匹配即停止',10.5,ACC)))
FIGS['figW6']=('图 6-7 发布主链：快照打不可变 tag，UAT 混合编排按矩阵分发子运行；共享平台另走独立入口', svg(250,
  box(15,15,150,40,'每日快照','')+box(15,80,150,40,'不可变 tag / 构建','')+arrow(90,55,90,78)+
  box(15,145,150,40,'UAT 混合编排','按资源矩阵逐行分发',fill='url(#g)',stroke=ACC,tc='#fff')+arrow(90,120,90,143)+
  box(330,15,155,40,'共享平台入口','独立生命周期',fill='#fff')+box(330,80,155,40,'密钥 · 可观测','身份',fill='#fff')+arrow(407,55,407,78)+
  ''.join(box(15+i*120,205,110,36,t,'',fill='#fff') for i,t in enumerate(['Selfhost','Serverless','外部主机','子运行']))+
  ''.join(arrow(90,185,70+i*120,203) for i in range(4))))
FIGS['figW7']=('图 7-4 边缘入口：稳定域名经边缘网关按模式选择后端；数据单写者，两库之间单向只读复制', svg(300,
  box(15,15,140,40,'品牌主页','静态托管',fill='#fff')+box(180,15,140,40,'控制台','静态资源走 CDN',fill='#fff')+
  box(345,15,140,40,'API 稳定域名','账户 · 账单')+arrow(320,35,343,35)+
  box(300,80,185,44,'边缘网关','按模式选后端；仅安全方法回退',fill='url(#g)',stroke=ACC,tc='#fff')+arrow(415,55,415,78)+
  box(230,150,120,40,'Serverless','')+box(380,150,105,40,'Selfhost','')+arrow(360,124,300,148)+arrow(440,124,432,148)+
  box(230,225,120,44,'托管 PG','单写者',fill='#fff')+box(380,225,105,44,'自建 PG','只读副本',fill='#fff')+
  arrow(290,190,290,223)+arrow(432,190,432,223)+
  f'<path d="M350,247 L378,247" stroke="{ACC}" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#ah)"/>'+
  T(110,150,'换后端不连带',10.5,PRI)+T(110,166,'更换品牌主页',10.5,PRI)+T(110,290,'路由切换与数据一致性分开验收',11,ACC,'700')))

FIGS['figL1']=('图 6-8 功能泳道：功能 ID 关联多仓库 PR，固定候选先过 SIT、再过 UAT，组合验证后才合并', svg(390,
  box(15,15,470,44,'功能 ID：billing-refund','关联 Console / Accounts / Billing 三个 PR',fill='url(#g)',stroke=ACC,tc='#fff')+
  box(15,85,145,44,'CI 构建','固定 commit + digest')+box(178,85,145,44,'候选清单','revision-3')+box(340,85,145,44,'K3s Namespace','feature-billing-refund')+
  arrow(250,59,88,83)+arrow(160,107,176,107)+arrow(323,107,338,107)+
  box(340,160,145,44,'SIT','契约 · 集成 · 回归')+arrow(412,129,412,158)+
  box(178,160,145,44,'固定候选','不跟随分支',fill='#fff')+arrow(340,182,325,182)+
  box(15,160,145,44,'UAT','登录 · 业务 · 对账')+arrow(178,182,162,182)+
  box(15,235,145,44,'组合验证','候选 vs 最新 main',fill='#fff')+arrow(88,204,88,233)+
  box(178,235,145,44,'合并 PR','验收通过后',fill='url(#g)',stroke=ACC,tc='#fff')+arrow(160,257,176,257)+
  f'<path d="M478,204 L478,300 L340,300" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="5 4"/>'+
  T(400,226,'PR 新提交',10.5,ACC)+T(400,242,'→ 新 revision 重建',10.5,ACC)+
  T(250,330,'旧 UAT 结果不能放行新 revision',11.5,ACC,'700')+T(250,355,'SIT 与 UAT 共用一套物理资源，区别只在阶段与候选状态',11,PRI)))
FIGS['figL2']=('图 6-9 全链路泳道与 Flux 部署链路：构建、编排、收敛分开，泳道内写入只进独立测试库', svg(380,
  T(125,25,'部署链路（main 合并前）',12.5,TITLE,'700')+T(375,25,'泳道调用链',12.5,TITLE,'700')+
  box(15,40,220,40,'业务 PR 固定 SHA','不持有凭据',fill='#fff')+box(15,105,220,40,'CI 构建镜像 digest','')+
  box(15,170,220,44,'受信任的非生产编排','凭据由 Vault 下发',fill='url(#g)',stroke=ACC,tc='#fff')+
  box(15,240,220,44,'功能泳道 GitOps 声明','受保护的非生产分支')+box(15,310,220,40,'Flux / Helm 部署','HelmRelease values',fill='#fff')+
  arrow(125,80,125,103)+arrow(125,145,125,168)+arrow(125,214,125,238)+arrow(125,284,125,308)+
  box(265,40,220,40,'billing-refund.preview','.example.com',fill='#fff')+box(265,105,220,40,'Next.js-feature','')+
  box(265,170,220,40,'Accounts-feature','')+box(265,235,220,40,'Billing-feature','')+
  box(265,300,220,44,'PG：billing_refund','独立 database 与角色',fill='url(#g)',stroke=ACC,tc='#fff')+
  arrow(375,80,375,103)+arrow(375,145,375,168)+arrow(375,210,375,233)+arrow(375,275,375,298)+
  arrow(235,330,263,322)+T(250,372,'Service DNS 固定依赖地址；不做逐跳 Header 染色',11,ACC,'700')))
FIGS['figR1']=('图 5-5 主机与集群的三角色：同名 Linux 用户，各自独立的集群身份', svg(270,
  box(20,24,140,64,'root','初始化 · 恢复 · 管理')+box(180,24,140,64,'operator','日常业务运维')+box(340,24,140,64,'auditor','只读审计 · 迁移核对')+
  box(20,140,140,56,'受限管理主体','独立 kubeconfig',fill='#fff')+box(180,140,140,56,'业务运维主体','独立 kubeconfig',fill='#fff')+box(340,140,140,56,'只读审计主体','独立 kubeconfig',fill='#fff')+
  arrow(90,88,90,138,'SSH 公钥')+arrow(250,88,250,138,'SSH 公钥')+arrow(410,88,410,138,'SSH 公钥')+
  T(250,228,'Linux 用户名 ≠ 集群身份隔离；不用 sudo kubectl 冒充身份',12,ACC,'700')+
  T(250,252,'OS root 仍可触达集群 CA：保留恢复入口，不宣称强制隔离',11,'#46506e')))
FIGS['figR2']=('图 5-6 声明与执行分开：GitOps 说「给谁什么」，Playbooks 交付凭据并用真实身份验收', svg(290,
  box(20,24,200,64,'GitOps（声明源）','映射 · RBAC · 准入 · 凭据引用')+box(280,24,200,64,'Vault KV（规划）','kv/&lt;env&gt;/&lt;cluster&gt;/&lt;role&gt;')+
  box(20,130,200,64,'Flux 调谐','RBAC 范围按 revision 收敛')+box(280,130,200,64,'Playbooks role','运行时读 · 交付 kubeconfig',fill='url(#g)',stroke=ACC,tc='#fff')+
  box(150,226,200,48,'真实身份验收','允许 / 拒绝 · 脱敏证据',fill='#fff')+
  arrow(120,88,120,128)+arrow(220,56,278,56,'只存路径')+arrow(380,88,380,128)+arrow(120,194,200,224)+arrow(380,194,300,224)))
FIGS['figR3']=('图 5-7 权限边界：能看、能缩放、能管，各停在自己那一格（初期，规划）', svg(300,
  f'<text x="180" y="40" font-size="12" fill="{ACC}" font-weight="700" style="{F}">root</text><text x="285" y="40" font-size="12" fill="{ACC}" font-weight="700" style="{F}">operator</text><text x="395" y="40" font-size="12" fill="{ACC}" font-weight="700" style="{F}">auditor</text>'+
  ''.join(f'<rect x="20" y="{52+i*40}" width="460" height="34" rx="8" fill="{PANEL if i%2==0 else "#fff"}"/><text x="32" y="{74+i*40}" font-size="12.5" font-weight="700" fill="{TITLE}" style="{F}">{a}</text>'+
   ''.join(f'<text x="{x}" y="{74+i*40}" font-size="12" fill="{PRI if v!="✗" else "#b42318"}" style="{F}">{v}</text>' for x,v in zip((180,285,395),vs))
   for i,(a,vs) in enumerate([('授权范围状态读取',('✓','✓','✓ 需评审')),('点名无状态服务缩放',('✓','✓','✗')),('发布：经 GitOps PR',('审查','提交','✗')),('Secret / exec / proxy',('逐项审查','✗','✗')),('RBAC / 准入 / 扩权',('审查发布','✗','✗')),('有状态与数据变更',('受控恢复','✗','✗'))]))))
FIGS['figE1']=('图 5-8 默认引用链：Vault KV 存值，GitOps 只写路径，ESO 同步成 Secret，chart 只认 Secret 名', svg(300,
  box(20,24,140,64,'Vault KV','kv/env/cluster/role')+box(180,24,140,64,'GitOps 声明','ExternalSecret 引用')+box(340,24,140,64,'Flux 调谐','按 revision 收敛')+
  box(100,140,140,64,'ESO 控制器','唯一持 Vault 读权限',fill='url(#g)',stroke=ACC,tc='#fff')+box(260,140,160,64,'K8s Secret','admin · operator · auditor')+
  box(20,232,140,48,'chart root','← admin',fill='#fff')+box(180,232,140,48,'chart operator','← operator',fill='#fff')+box(340,232,140,48,'chart auditor','← auditor',fill='#fff')+
  arrow(160,56,178,56)+arrow(320,56,338,56)+arrow(410,88,200,138)+arrow(90,88,150,138,'读取')+arrow(240,172,258,172)+
  arrow(330,204,90,230)+arrow(330,204,250,230)+arrow(330,204,410,230)))
FIGS['figE2']=('图 5-9 一套身份模型两种接入：容器内应用与非容器 SaaS 都走 OIDC，换到的都是短期令牌', svg(290,
  box(160,20,180,56,'身份提供方','Zitadel · CI 签发方',fill='url(#g)',stroke=ACC,tc='#fff')+
  box(20,120,140,64,'集群内应用','OIDC 登录 · 校验 JWT')+box(180,120,140,64,'非容器 SaaS','门户 · 托管控制台')+box(340,120,140,64,'CI 流水线','OIDC → Vault JWT 角色')+
  box(20,220,300,48,'人：短期会话，按组映射角色',fill='#fff')+box(340,220,140,48,'机器：短期令牌',fill='#fff')+
  arrow(210,76,90,118)+arrow(250,76,250,118)+arrow(290,76,410,118)+arrow(170,184,170,218)+arrow(410,184,410,218)))
FIGS['figP1']=('图 16-1 Case A：环境级 Vault KV 公钥 → common → 三个 OS 用户（规划，待验收）', svg(240,
  box(20,24,200,60,'Vault KV v2','kv/&lt;env&gt;/security/{role}')+box(280,24,200,60,'bootstrap 脚本','cas=0 只建不覆盖',fill='#fff')+
  box(150,110,200,50,'vhosts/common','显式启用 · 先验证再 reload',fill='url(#g)',stroke=ACC,tc='#fff')+
  box(20,180,140,44,'root','prohibit-password')+box(180,180,140,44,'operator','受控 sudo')+box(340,180,140,44,'auditor','只读 · 无 sudo')+
  arrow(380,84,300,108,'写')+arrow(120,84,200,108,'读')+arrow(200,160,90,178)+arrow(250,160,250,178)+arrow(300,160,410,178)))
FIGS['figP2']=('图 16-2 Case B：K3s 冷启动依赖链（✅ 代码已合并 · ⏳ 目标集群验收）', svg(330,
  box(20,16,200,40,'IaC CMDB','节点 · 卷 · SHA')+box(280,16,200,40,'GitOps','source · RBAC 声明')+
  box(150,72,200,36,'common','hostname · OS 三账户')+box(150,120,200,36,'web_saas_data_volume','数据盘证据')+
  box(150,168,200,36,'k3s_platform_bootstrap','只编排',fill='url(#g)',stroke=ACC,tc='#fff')+
  box(10,222,115,40,'k3s-cluster-server','API 就绪')+box(132,222,75,40,'helm_cli','')+box(214,222,90,40,'flux_controllers','')+box(311,222,85,40,'flux_gitops','交接')+box(403,222,90,40,'k3s_identity','真实允许/拒绝')+
  box(100,282,300,36,'Flux 调谐','RBAC · ESO/TLS · Vault · DB · 业务',fill='#fff')+
  arrow(120,56,220,70)+arrow(380,56,280,70)+arrow(250,108,250,118)+arrow(250,156,250,166)+arrow(250,204,67,220)+arrow(250,204,448,220)+arrow(353,262,250,280)))
FIGS['figP3']=('图 16-3 Case C：发布解析链（目标草案，未全部实现）', svg(485,
  box(120,8,220,40,'A 选择不可变发布 tag','')+
  arrow(230,48,230,62)+
  box(120,64,220,40,'B 解析发布记录','环境 · 业务 · 制品版本',fill='url(#g)',stroke=ACC,tc='#fff')+
  arrow(230,104,230,118)+
  box(120,120,220,40,'D 固定 GitOps commit','选择目标声明')+
  arrow(230,160,230,174)+
  box(120,176,220,40,'E IaC 读取目标','节点 · 既有 state 身份')+
  arrow(230,216,230,230)+
  box(120,232,220,40,'F IaC 输出 CMDB','')+
  arrow(230,272,230,286)+
  box(120,288,220,40,'G Playbooks 消费','CMDB 与 GitOps 配置')+
  arrow(230,328,230,342)+
  box(120,344,220,40,'H 初始化','OS · K3s · Flux')+
  arrow(230,384,230,398)+
  box(120,400,220,40,'I Flux 按声明部署业务','')+
  box(370,64,125,40,'C 校验工作流 ref','与 Vault role')+arrow(340,84,368,84)+
  T(250,470,'tag 选内容 · 声明定目标 · 每次运行解析一次 SHA 向下游传递',11,ACC,'700')))
