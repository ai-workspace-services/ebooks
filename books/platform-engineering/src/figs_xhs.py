"""Extra 图解 for unwritten chapters (XHS packs; can go into the book later). Generic facts only."""
from figs import *
def vflow(items):
    h=40+len(items)*80; b=''
    for i,(t,s) in enumerate(items):
        y=25+i*80; last=i==len(items)-1
        b+=box(90,y,320,56,t,s,**({'fill':'url(#g)','stroke':ACC,'tc':'#fff'} if last else {}))
        if not last: b+=arrow(250,y+56,250,y+78)
    return svg(h,b)
def grid(items):
    rows=(len(items)+1)//2; b=''
    for i,(t,s) in enumerate(items):
        b+=box(20+(i%2)*240,25+(i//2)*90,220,70,t,s)
    return svg(40+rows*90,b)
def cmp(head,rows):
    W=460/len(head); b=''
    for j,c in enumerate(head):
        b+=f'<rect x="{20+j*W}" y="20" width="{W}" height="36" fill="{PRI}"/><text x="{20+j*W+W/2}" y="43" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" style="{F}">{c}</text>'
    for i,r in enumerate(rows):
        for j,c in enumerate(r):
            b+=f'<rect x="{20+j*W}" y="{56+i*44}" width="{W}" height="44" fill="{PANEL if i%2==0 else "#fff"}" stroke="#c9d6ec"/><text x="{20+j*W+W/2}" y="{83+i*44}" text-anchor="middle" font-size="12" fill="{TITLE}" style="{F}">{c}</text>'
    return svg(76+len(rows)*44,b)
X={
'1':[('图 1-1 自由软件的四项自由',grid([('自由 0','任意目的运行'),('自由 1','研究并修改源码'),('自由 2','再分发副本'),('自由 3','分发修改后的版本')])),
     ('图 1-2 开源商业：代码免费，服务收费',vflow([('上游社区','代码开放、协作开发'),('发行版','打包、测试、集成'),('订阅与服务','长期支持 · 认证 · 安全更新')])),
     ('图 1-3 从中台到平台工程',vflow([('烟囱式系统','每个团队各搭一套'),('中台','共享业务与数据能力'),('技术平台','共享基础设施'),('平台工程','自助、可编程的内部平台')]))],
'2':[('图 2-1 一切变更走流水线',vflow([('commit / PR','评审 · 讨论'),('CI 只读验证','lint · test · build'),('不可变构件','镜像 · 包 · tag'),('交付','由 CD 消费')])),
     ('图 2-2 Gitea 与 GitHub 对等',cmp(['','Gitea','GitHub'],[['部署','自建','托管 / Enterprise 自建'],['CI','Gitea Actions','GitHub Actions'],['runner','act_runner 自建','托管或自托管'],['工作流语法','基本兼容 Actions','Actions 语法']])),
     ('图 2-3 Reusable Workflow：一处定义，处处调用',grid([('组织基线仓库','共享工作流'),('仓库 A','uses: 基线'),('仓库 B','uses: 基线'),('仓库 C','uses: 基线')]))],
'3':[('图 3-1 OpenTofu 工作流',vflow([('写 .tf 声明','资源期望状态'),('tofu plan','对比 state，列出变更'),('评审 plan','替换/删除要报警'),('tofu apply','收敛并写回 state')])),
     ('图 3-2 模块按版本钉住',grid([('模块仓库','打 tag / 提交 SHA'),('环境 SIT','source = …?ref=SHA'),('环境 UAT','同一 SHA'),('环境 PROD','评审后再升级')])),
     ('图 3-3 自建 Remote State',vflow([('多人 / 多流水线','同时运行'),('State 后端','S3 兼容存储 · 自建'),('状态锁','同一时刻只有一个 apply')]))],
'4':[('图 4-1 幂等：跑一次和跑十次结果一样',vflow([('期望状态','role 里声明'),('检查现状','已满足则跳过'),('只改差异','changed 才执行'),('结果一致','可重复执行')])),
     ('图 4-2 动态 inventory：不写死 IP',vflow([('CMDB','主机 · 分组 · 角色'),('inventory 插件','运行时生成'),('playbook','按分组执行')])),
     ('图 4-3 交付物对比',cmp(['交付物','适用','特点'],[['Ansible role','主机配置','幂等、可 check'],['Golden Image','虚拟机','预装、启动即用'],['Helm chart','Kubernetes','版本化、可回滚']]))],
'7':[('图 7-1 云中立：同一套配置，任意运行面',grid([('公有云','IaaS 虚机'),('VPS','多家运营商'),('裸金属','自有机房'),('K3s / K8s','统一运行面')])),
     ('图 7-2 三种编排模式',cmp(['模式','运行在','适合'],[['Selfhost','自建主机/集群','完全掌控'],['Serverless','托管运行时','弹性、免运维'],['Hybrid','两者组合','按服务取舍']])),
     ('图 7-3 退出成本：越开放越低',vflow([('专有托管服务','迁移成本高'),('开放标准 + 托管','可替换'),('开源自建','随时搬家')]))],
'8':[('图 8-1 可观测三根支柱',grid([('Metrics','数值随时间变化'),('Logs','离散事件记录'),('Traces','一次请求的全链路'),('Grafana','统一查询与看板')])),
     ('图 8-2 采集到展示',vflow([('采集端','exporter · Vector · OTel'),('存储','VictoriaMetrics · VictoriaLogs'),('查询与告警','Grafana · 告警规则'),('值班','通知到人')])),
     ('图 8-3 控制端与节点端分离',grid([('控制端','存储 · 看板 · 告警'),('节点端','只装采集'),('写入令牌','节点只能写'),('读权限','人经统一身份登录')]))],
'9':[('图 9-1 能恢复才算备份成功',vflow([('定时备份','全量 + 增量'),('异地存储','S3 兼容 · 自建'),('恢复演练','隔离实例上还原'),('校验','行数 · 校验和 · 应用自检')])),
     ('图 9-2 RPO 与 RTO',cmp(['指标','含义','由什么决定'],[['RPO','最多丢多少数据','备份频率'],['RTO','多久恢复服务','恢复流程与演练']])),
     ('图 9-3 回滚靠不可变快照',grid([('快照 N-1','可回退'),('快照 N','当前运行'),('快照 N+1','待晋级'),('回滚','切回上一个 tag')]))],
'10':[('图 10-1 AI 聚合网关',vflow([('应用 / Agent','统一 API 入口'),('New API','用户 · 额度 · 模型权限'),('LiteLLM','路由 · 重试 · 成本统计'),('多家模型','自建或第三方')])),
      ('图 10-2 MCP：把工具交给 Agent',grid([('Agent','发起调用'),('MCP Server','暴露工具'),('IaC / CMDB','受控操作'),('审计','每次调用可追溯')])),
      ('图 10-3 Agent 运维的边界',cmp(['操作','默认','条件'],[['只读查询','允许','有日志'],['变更 plan','允许','需人评审'],['apply / 删除','禁止','人批准后执行']]))],
}
X['11']=[('图 11-1 七层拧成一个平台',vflow([('Git 与 CI','入口'),('资源 · 交付','OpenTofu · Ansible'),('安全 · 环境','Vault · GitOps'),('云中立 · 可观测','K3s · Grafana'),('Open Platform','可恢复 · 可接入 AI')])),
 ('图 11-2 成熟度自评（每层打分）',cmp(['等级','状态','特征'],[['0','手工','靠人记、靠登录'],['1','脚本化','有脚本，无评审'],['2','声明式','Git 为真相，可重复'],['3','平台化','自助、合同测试、可审计']])),
 ('图 11-3 开放标准清单',grid([('Git','版本与评审'),('OCI','镜像与构件'),('OIDC','机器与人的身份'),('OpenTelemetry','遥测数据'),('MCP','Agent 调用工具'),('HCL / YAML','声明格式')]))]
