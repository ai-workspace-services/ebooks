# 《图解 IT 简史》v4 → v4.1 事实核查

> 2026-10-20。年份口径按 2026 年；图片未改，图文不一致见附录 A「v4.1 图文不一致说明」。

| 章节 | 原句 | 结论 | 依据链接 | 处理 |
|---|---|---|---|---|
| 全书 | IBM System/360 1964 | 正确 | https://en.wikipedia.org/wiki/IBM_System/360 | 保留 |
| 01 | UNIX 1969 贝尔实验室 | 正确 | https://en.wikipedia.org/wiki/Unix | 保留 |
| 01 | IBM PC 1981 | 正确 | https://en.wikipedia.org/wiki/IBM_Personal_Computer | 保留 |
| 01 | Linux 0.01 与万维网 1991 | 正确 | https://en.wikipedia.org/wiki/History_of_Linux | 保留 |
| 01 | System/360“押上整个公司”的豪赌 | 改为泛指 | https://en.wikipedia.org/wiki/IBM_System/360 | 写成“常被形容为”，不给金额 |
| 01 | 99.9% ≈ 每年 8.76 小时停机 | 正确（计算） | — | 保留 |
| 01（新增） | 1947 Mark II 飞蛾，日志藏于史密森尼 | 正确 | https://americanhistory.si.edu/collections/object/nmah_334663 | 新增；注明 bug 一词早已存在 |
| 02 | IBM VM/370 1972 | 正确 | https://en.wikipedia.org/wiki/VM_(operating_system) | 保留 |
| 02（新增） | Popek & Goldberg 1974 虚拟化条件 | 正确 | https://en.wikipedia.org/wiki/Popek_and_Goldberg_virtualization_requirements | 新增 |
| 02（新增） | x86 敏感指令不可直接陷入；VMware 二进制翻译；VT-x/AMD-V | 正确 | https://en.wikipedia.org/wiki/X86_virtualization | 新增，未写年份 |
| 02 | VMware 1998 成立；ESX 2001 | 正确 | https://en.wikipedia.org/wiki/VMware | 保留 |
| 02 | Xen 首个公开版 2003 | 正确 | https://en.wikipedia.org/wiki/Xen | 保留 |
| 02 | KVM 并入 Linux 2.6.20（2007） | 正确 | https://en.wikipedia.org/wiki/Kernel-based_Virtual_Machine | 保留 |
| 02 | “Xen 始终没能成为 Linux 虚拟化底座” | 修正 | https://en.wikipedia.org/wiki/Xen | 改为“在主流发行版中逐渐让位于 KVM”；图片冲突记入附录 A |
| 02 | chroot 1979 V7 Unix；FreeBSD Jail 2000 | 正确 | https://en.wikipedia.org/wiki/Chroot | 保留 |
| 02 | Docker 2013 开源 | 正确 | https://en.wikipedia.org/wiki/Docker_(software) | 保留 |
| 02 | AWS Nitro 2017 | 正确 | https://aws.amazon.com/ec2/nitro/ | 保留 |
| 02 | 博通 2023 完成收购 VMware | 正确 | https://investors.broadcom.com/news-releases/news-release-details/broadcom-completes-acquisition-vmware | 保留 |
| 02 | AI 训练“很多场景又开始偏爱物理机” | 改为泛指 | — | 改为“不少场景” |
| 03 | S3 2006-03 上线，AWS 首个正式商用服务 | 正确 | https://en.wikipedia.org/wiki/Amazon_S3 | 保留 |
| 03（新增） | S3 3 月 14 日上线，每 GB 每月 15 美分 | 正确 | https://aws.amazon.com/blogs/aws/amazon_s3/ | 新增 |
| 03 | EC2 2006-08 公测（8 月 25 日） | 正确 | https://techcrunch.com/2021/08/28/how-amazon-ec2-grew-from-a-notion-into-a-foundational-element-of-cloud-computing/ | 保留 |
| 03（新增） | EC2 由开普敦 Chris Pinkham 团队开发；笔记本模拟机架 | 正确 | https://en.wikipedia.org/wiki/Amazon_Elastic_Compute_Cloud | 新增，注明“据团队成员回忆” |
| 03 | cgroups 2008 并入 2.6.24；LXC 2008 | 正确 | https://en.wikipedia.org/wiki/Cgroups | 保留 |
| 03 | Amazon VPC 2009 | 正确 | https://aws.amazon.com/vpc/ | 保留 |
| 03 | OpenStack 2010 | 正确 | https://en.wikipedia.org/wiki/OpenStack | 保留 |
| 03 | eBPF 2014 新系统调用 | 正确 | https://en.wikipedia.org/wiki/EBPF | 保留 |
| 03 | Kubernetes 2014 开源；CNCF 2015 | 正确 | https://en.wikipedia.org/wiki/Kubernetes | 保留 |
| 03 | “绝大多数云主机跑 Linux” | 改为泛指 | — | 改为“大多数” |
| 04 | Heroku 2007；GAE 2008 | 正确 | https://en.wikipedia.org/wiki/Heroku | 保留 |
| 04 | EC2 Auto Scaling 2009 | 正确 | https://aws.amazon.com/ec2/autoscaling/ | 保留 |
| 04 | Lambda 2014-11（re:Invent） | 正确 | https://en.wikipedia.org/wiki/AWS_Lambda | 保留 |
| 04 | K8s 源自 Google 内部集群管理；1.0 2015 | 正确 | https://en.wikipedia.org/wiki/Kubernetes | 保留 |
| 04 | OpenStack Nova/Neutron/Cinder | 正确 | https://en.wikipedia.org/wiki/OpenStack | 保留 |
| 04 | Proxmox VE 2008 首版即 KVM+LXC+Ceph | 修正 | https://proxmox.com/en/about/press-releases/proxmox-ve-turns-10 | 改为 2008-04 首版 KVM+OpenVZ，2015 4.0 换 LXC，后集成 Ceph |
| 04 | Harvester 1.0 GA 2021 | 正确 | https://www.suse.com/c/rancher_blog/harvester-1-0-0/ | 保留 |
| 04（新增） | Netflix 2008-08 数据库损坏约三天无法寄 DVD，转向 AWS，2016 初完成 | 正确 | https://about.netflix.com/news/completing-the-netflix-cloud-migration | 新增 |
| 05 | BGP 首个 RFC 1989 | 正确 | https://www.rfc-editor.org/rfc/rfc1105 | 保留 |
| 05（新增） | BGP“三张餐巾纸”，1989-01 奥斯汀 IETF，Lougheed & Rekhter | 正确 | http://web.cs.ucla.edu/~lixia/papers/BGP_at_18.pdf | 新增 |
| 05（新增） | 2021-10-04 Facebook 约 6 小时中断，BGP 撤回 | 正确 | https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/ | 新增 |
| 05 | AWS Direct Connect 2011 | 正确 | https://aws.amazon.com/directconnect/ | 保留 |
| 05 | OIDC 1.0 2014 | 正确 | https://openid.net/specs/openid-connect-core-1_0.html | 保留 |
| 05 | AWS Landing Zone 2018；Control Tower GA 2019 | 正确 | https://aws.amazon.com/controltower/ | 保留 |
| 05 | FinOps 基金会 2019 | 正确 | https://www.finops.org/ | 保留 |
| 06 | Puppet 2005；Chef 2009；Ansible 2012 | 正确 | https://en.wikipedia.org/wiki/Ansible_(software) | 保留 |
| 06 | DevOpsDays 2009（根特，Patrick Debois） | 正确 | https://en.wikipedia.org/wiki/DevOps | 补充人名地点 |
| 06 | Jenkins 2011 自 Hudson 分出 | 正确 | https://en.wikipedia.org/wiki/Jenkins_(software) | 保留 |
| 06 | Terraform 0.1 2014 | 正确 | https://en.wikipedia.org/wiki/Terraform_(software) | 保留 |
| 06 | Weaveworks 2017 提出 GitOps | 正确 | https://www.weave.works/blog/gitops-operations-by-pull-request | 保留 |
| 06 | Backstage 2020 由 Spotify 开源 | 正确 | https://backstage.io/ | 保留 |
| 06 | OpenTofu 2023 分叉 | 正确 | https://opentofu.org/ | 保留 |
| 06（新增） | Knight Capital 2012-08-01，约 45 分钟，损失超 4.6 亿美元，漏部署 1/8 服务器 | 正确 | https://www.sec.gov/newsroom/press-releases/2013-222 | 新增（v4 备注中的 4.4 亿说法不用） |
| 07 | Inmon 1992；Kimball 1996 | 正确 | https://en.wikipedia.org/wiki/Bill_Inmon | 保留 |
| 07 | MPP：Teradata/Netezza/Greenplum/Vertica | 正确 | https://en.wikipedia.org/wiki/Massively_parallel | 保留 |
| 07 | Hadoop 2006；名字来自玩具象 | 正确 | https://en.wikipedia.org/wiki/Apache_Hadoop | 新增来历 |
| 07 | 云原生数仓 2015–2020 成主流 | 修正 | https://en.wikipedia.org/wiki/Snowflake_Inc. | 补充“诞生于 2010 年代初”；图片冲突记入附录 A |
| 07（新增） | 啤酒与尿布 | 存疑 | https://www.dssresources.com/newsletters/66.php | 明写“经不起细究、无可靠出处” |
| 08 | Kerberos v5 RFC 1510（1993）；LDAP 1993 | 正确 | https://www.rfc-editor.org/rfc/rfc1510 | 保留 |
| 08 | Check Point FireWall-1 1994 | 正确 | https://en.wikipedia.org/wiki/Check_Point | 保留 |
| 08 | Active Directory 2000；SAML 2.0 2005 | 正确 | https://en.wikipedia.org/wiki/Active_Directory | 保留 |
| 08 | OAuth 2.0 RFC 6749（2012）；JWT RFC 7519（2015） | 正确 | https://www.rfc-editor.org/rfc/rfc6749 | 保留 |
| 08 | Forrester 2010 零信任（Kindervag） | 正确 | https://en.wikipedia.org/wiki/Zero_trust_architecture | 补充人名 |
| 08 | BeyondCorp 2014；源于 Aurora 之后 | 正确 | https://research.google/pubs/beyondcorp-a-new-approach-to-enterprise-security/ | 新增因果，按 Google 公开说法 |
| 08 | NIST SP 800-207（2020） | 正确 | https://csrc.nist.gov/pubs/sp/800/207/final | 保留 |
| 08（新增） | Morris 蠕虫 1988-11-02，约 6000 台、约 10%；CFAA 首例定罪；CERT 成立 | 正确 | https://www.fbi.gov/history/cases-and-criminals/morris-worm | 新增 |
| 08 | “模型蒸馏窃取能力” | 改为泛指 | — | 保留为一般描述，无具体指控 |
| 09 | “开源”一词与 OSI 1998 | 正确 | https://opensource.org/history | 措辞改为“说法被正式提出，同年 OSI 成立” |
| 09 | OpenCost 2022 CNCF 沙箱 | 正确 | https://www.cncf.io/projects/opencost/ | 保留 |
| 09 | HashiCorp 2023-08 BSL；OpenTofu 1.6 GA 2024 | 正确 | https://www.hashicorp.com/blog/hashicorp-adopts-business-source-license | 保留 |
| 09（新增） | Elastic 2021 SSPL→OpenSearch；Redis 2024-03→Valkey；后均加 AGPL | 正确 | https://www.linuxfoundation.org/press/linux-foundation-launches-open-source-valkey-community | 新增 |
| 09 | 去 IOE = IBM/Oracle/EMC | 正确 | — | 保留（通行说法） |
| 10 | Transformer 2017《Attention Is All You Need》 | 正确 | https://arxiv.org/abs/1706.03762 | 保留 |
| 10 | GPT-3 2020；Copilot 预览 2021；ChatGPT 2022-11 | 正确 | https://en.wikipedia.org/wiki/ChatGPT | 保留 |
| 10 | AutoGPT 2023；MCP 2024-11 | 正确 | https://www.anthropic.com/news/model-context-protocol | 保留 |
| 10 | DeepSeek-R1 2025；Claude Code 2025 | 正确 | https://en.wikipedia.org/wiki/DeepSeek | 保留 |
| 10（新增） | AlexNet 2012，两块 GTX 580 | 正确 | https://en.wikipedia.org/wiki/AlexNet | 新增 |
| 10（新增） | ChatGPT 约两个月 1 亿月活（UBS 援引估算） | 存疑→注明来源 | https://en.wikipedia.org/wiki/ChatGPT | 写成“据瑞银援引的第三方估算” |
| 专题一 | Codd 1970；SEQUEL 1974；1986 ANSI | 正确 | https://dl.acm.org/doi/10.1145/362384.362685 | 保留 |
| 专题一（新增） | SEQUEL 因商标冲突改名 SQL | 正确 | https://en.wikipedia.org/wiki/SQL | 新增，不点公司名 |
| 专题一 | Kafka 2011 LinkedIn 开源；15 岁 | 正确 | https://en.wikipedia.org/wiki/Apache_Kafka | 保留 |
| 专题一（新增） | Kafka 名字来自作家卡夫卡（Jay Kreps） | 正确 | https://en.wikipedia.org/wiki/Apache_Kafka | 新增 |
| 专题一（新增） | Python 名字来自 Monty Python | 正确 | https://docs.python.org/3/faq/general.html | 新增 |
| 专题一 | Spark 2009 AMPLab | 正确 | https://en.wikipedia.org/wiki/Apache_Spark | 保留 |
| 专题一 | SAS 1976/1966；Excel 1985；Pandas 2008；NumPy 2005 | 正确 | 附录 A 年份口径表 | 保留 |
| 专题一 | 感知机 1958；k-NN 1967；ID3 1986；SVM 1995；RF 2001；sklearn 2007 | 正确 | 附录 A 年份口径表 | 保留 |
| 专题一 | Caffe 2013；PyTorch 2016；JAX 2018（8 岁）；Word2Vec 2013 | 正确 | https://en.wikipedia.org/wiki/JAX_(software) | 保留 |
| 专题一 | DeepSeek V3 2024-12、R1 2025-01（2 岁） | 正确 | 附录 A | 保留 |
| 专题一 | BabyAGI 2023-03-28，约 140 行 | 正确 | 附录 A | 保留 |
| 专题一 | LangChain 2022；Codex CLI 2025 | 正确 | https://en.wikipedia.org/wiki/LangChain | 保留 |
| 专题一 | IBM 1911（115）；NVIDIA 1993（33）；Meta 2004；Mistral 2023-04（3） | 正确 | https://en.wikipedia.org/wiki/Nvidia | 保留 |
| 序言 | 2006 S3/EC2；2014 K8s；2022-11 ChatGPT | 正确 | 见上 | 保留 |
| 关于出品方 | 产品名称与业务描述 | 正确（沿用公司简介） | https://xworktech.com/ | 保留，删邮箱 |

合计 92 条：正确 83，改为泛指 4，修正 3，存疑 2。


## v4.3 新增事实核查（2026-10-20）

| 章节 | 新增内容 | 结论 | 依据链接 | 实时核验 |
|---|---|---|---|---|
| 01 | 摩尔 1965 年提出、1975 年修正为约两年翻番 | 正确 | https://en.wikipedia.org/wiki/Moore%27s_law | 否（参考资料） |
| 01 | Brooks《没有银弹》1986，本质/偶然复杂度 | 正确 | https://en.wikipedia.org/wiki/No_Silver_Bullet | 否（参考资料） |
| 01 | Slashdot 效应 | 正确（通行说法） | https://en.wikipedia.org/wiki/Slashdot_effect | 否（参考资料） |
| 01 | 无责复盘做法 | 泛指 | https://sre.google/sre-book/postmortem-culture/ | 否（参考资料） |
| 01 | 可观测性三支柱：指标/日志/链路 | 泛指 | https://opentelemetry.io/docs/concepts/signals/ | 否（参考资料） |
| 02 | 一型/二型 Hypervisor；KVM 使 Linux 成为一型 | 正确 | https://en.wikipedia.org/wiki/Hypervisor | 否（参考资料） |
| 02 | VMotion/VirtualCenter 2003；演示用 3D 弹珠台 | 正确 | https://virtualizationreview.com/articles/2016/09/14/evolution-of-vmware-vmotion.aspx | 是（WebSearch） |
| 02 | 热迁移原理：预复制内存、短暂停机切换 | 正确 | https://www.eweek.com/networking/vmware-combo-drives-large-scale-virtualization/ | 是（WebSearch） |
| 02 | Xen 出自剑桥，论文《Xen and the Art of Virtualization》2003 | 正确 | https://dl.acm.org/doi/10.1145/945445.945462 | 否（参考资料） |
| 02 | KVM 作者 Avi Kivity / Qumranet，2008 被 Red Hat 收购 | 正确 | https://en.wikipedia.org/wiki/Qumranet | 否（参考资料） |
| 02 | 内存超卖、虚拟交换机 | 泛指 | — | 否（参考资料） |
| 03 | S3 设计持久性 11 个 9 | 正确 | https://aws.amazon.com/s3/storage-classes/ | 否（参考资料） |
| 03 | 2017-02-28 S3 us-east-1 故障：命令参数输错，约 4 小时，健康仪表盘受影响 | 正确 | https://aws.amazon.com/message/41926/ | 是（WebSearch） |
| 03 | 麦克莱恩 1956 集装箱运输 | 正确 | https://en.wikipedia.org/wiki/Malcom_McLean | 否（参考资料） |
| 03 | Docker 2013-03 PyCon 五分钟闪电演讲《The future of Linux Containers》 | 正确 | https://www.youtube.com/watch?v=wW9CAH9nSLs | 是（WebSearch） |
| 03 | SDN 控制面与数据面分离 | 泛指 | https://en.wikipedia.org/wiki/Software-defined_networking | 否（参考资料） |
| 03 | cgroups 由 Google 工程师提出，原名 process containers | 正确 | https://en.wikipedia.org/wiki/Cgroups | 否（参考资料） |
| 04 | Borg 论文 2015 | 正确 | https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/ | 否（参考资料） |
| 04 | Kubernetes=希腊语舵手；七辐条源自代号 Seven of Nine | 正确 | https://cloud.google.com/blog/products/containers-kubernetes/from-google-to-the-world-the-kubernetes-origin-story | 是（WebSearch） |
| 04 | 声明式管理/控制循环 | 泛指 | https://kubernetes.io/docs/concepts/architecture/controller/ | 否（参考资料） |
| 04 | Heroku git push 部署 | 正确 | https://devcenter.heroku.com/articles/git | 否（参考资料） |
| 04 | Serverless 冷启动 | 泛指 | — | 否（参考资料） |
| 04 | 博通收购后 VMware 转向订阅与产品打包 | 改为泛指 | https://news.vmware.com/company/vmware-by-broadcom-business-transformation | 否（参考资料） |
| 04 | OpenStack 2010 由 Rackspace 与 NASA 发起 | 正确 | https://en.wikipedia.org/wiki/OpenStack | 否（参考资料） |
| 05 | Capital One 2019：WAF 配置错误+权限过大，约 1 亿美国人、600 万加拿大人 | 正确 | https://www.justice.gov/usao-wdwa/united-states-v-paige-thompson | 是（WebSearch） |
| 05 | 数据引力，Dave McCrory 2010 | 正确 | https://en.wikipedia.org/wiki/Data_gravity | 否（参考资料） |
| 05 | 认证 vs 授权；RBAC | 泛指 | — | 否（参考资料） |
| 06 | Flickr《10+ Deploys Per Day》Velocity 2009；Debois 看直播后办 DevOpsDays | 正确 | https://devops.com/the-origins-of-devops-whats-in-a-name/ | 是（WebSearch） |
| 06 | Git 2005 由 Torvalds 编写（BitKeeper 停止免费）；“几周” | 正确（时长写“据说”） | https://en.wikipedia.org/wiki/Git | 否（参考资料） |
| 06 | 宠物与牲口比喻 | 泛指（未归属作者） | — | 否（参考资料） |
| 06 | RPO/RTO；配置漂移；GitOps 拉模式 | 泛指 | https://opengitops.dev/ | 否（参考资料） |
| 07 | OLTP/OLAP；列存 | 泛指 | — | 否（参考资料） |
| 07 | GFS 2003、MapReduce 2004；Cutting & Cafarella（Nutch）实现 Hadoop | 正确 | https://en.wikipedia.org/wiki/Apache_Hadoop | 否（参考资料） |
| 07 | Iceberg 源自 Netflix；Delta/Hudi 开放表格式 | 正确 | https://iceberg.apache.org/ | 否（参考资料） |
| 07 | Tableau 源自斯坦福，2003 成立 | 正确 | https://en.wikipedia.org/wiki/Tableau_Software | 否（参考资料） |
| 07 | Excel 数据透视表“也许是用得最多的 BI 工具” | 改为泛指（“也许”） | — | 否（参考资料） |
| 07 | Kimball 星型模型 | 正确 | https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/star-schema-olap-cube/ | 否（参考资料） |
| 08 | CTSS 1961 起，被普遍认为最早使用密码 | 正确 | https://history.computer.org/pubs/2011-06-ctss.pdf | 是（WebSearch） |
| 08 | Kerberos 名称来自三头犬；MIT Athena | 正确 | https://web.mit.edu/kerberos/ | 否（参考资料） |
| 08 | SQL 注入原理；长期位列常见风险榜 | 正确 | https://owasp.org/www-project-top-ten/ | 否（参考资料） |
| 08 | Target 2013：供应商凭证，约 4000 万张卡 | 正确 | https://corporate.target.com/press/release/2013/12/target-confirms-unauthorized-access-to-payment-card-data-in-u-s-stores | 是（WebSearch） |
| 08 | 提示词注入 | 泛指 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | 否（参考资料） |
| 08 | OAuth 授权示例；蒸馏是正当技术亦可被滥用 | 泛指 | https://www.rfc-editor.org/rfc/rfc6749 | 否（参考资料） |
| 09 | Log4Shell 2021-12 披露，远程代码执行 | 正确 | https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-356a | 是（WebSearch） |
| 09 | SBOM 随之受重视 | 泛指 | https://www.cisa.gov/sbom | 否（参考资料） |
| 09 | 改许可证的理由（云厂商托管） | 改为泛指（“说法大同小异”） | — | 否（参考资料） |
| 09 | Christine Peterson 1998-02 提出 open source；网景开源 | 正确 | https://opensource.com/article/18/2/coining-term-open-source-software | 是（WebSearch） |
| 09 | S3 API 成事实标准 | 泛指 | — | 否（参考资料） |
| 10 | CUDA 2006-11 发布架构、2007 公开 SDK | 正确 | https://en.wikipedia.org/wiki/CUDA | 是（WebSearch） |
| 10 | ImageNet 李飞飞团队，上百万张标注图片 | 正确 | https://en.wikipedia.org/wiki/ImageNet | 否（参考资料） |
| 10 | AI 数据中心选址看电力 | 改为泛指（“不少”） | — | 否（参考资料） |
| 10 | 大模型=下一词预测；幻觉；Agent 工具调用；MCP 统一插头 | 泛指 | https://modelcontextprotocol.io/ | 否（参考资料） |
| 专题一 | Codd 论文标题；Oracle 1979 首个商用 SQL 数据库 | 正确 | https://en.wikipedia.org/wiki/Oracle_Database | 否（参考资料） |
| 专题一 | 1958-07《纽约时报》感知机“胚胎”报道；演示为左右标记分辨 | 正确 | https://www.nytimes.com/1958/07/08/archives/new-navy-device-learns-by-doing-psychologist-shows-embryo-of.html | 是（WebSearch） |
| 专题一 | Word2Vec 国王-男人+女人≈女王 | 正确 | https://arxiv.org/abs/1301.3781 | 否（参考资料） |
| 专题一 | Transformer 八位作者（Google） | 正确 | https://arxiv.org/abs/1706.03762 | 否（参考资料） |
| 专题一 | Kafka 追加日志；Spark 内存计算 | 泛指 | https://kafka.apache.org/documentation/ | 否（参考资料） |

合计新增 57 条；实时核验 13 条；改为泛指/机制说明 20 条；未发现需修正的新增事实。


## v4.5 文案融合核查（来自「自媒体文案备份」改写，2026-10-20）

| 章节 | 新增内容 | 结论 | 依据链接 | 实时核验 |
|---|---|---|---|---|
| 02 | Xen 早期架构优势、KVM 合入内核后的生态优势；OpenVZ 为轻量隔离/容器前史；ESXi 企业平台路线 | 正确（叙事改写，未新增争议数字） | https://en.wikipedia.org/wiki/Xen ; https://en.wikipedia.org/wiki/Kernel-based_Virtual_Machine | 否（与 v4.3 已核事实一致） |
| 03 | 云卖控制面/API/计量；容器与虚拟机不同抽象层、容器常跑在 VM 上 | 泛指（机制说明） | — | 否 |
| 04 | 弹性=供给节奏；标签/账单治理；容器未替代 VM 商品形态 | 泛指 | — | 否 |
| 05 | 上云求速度、下云重新算账；Landing Zone 四柱；FinOps；身份新边界 | 泛指（Capital One 等旧事实未改） | — | 否 |
| 08 | 人/工作负载/云资源/CI 四类身份；密钥需轮换审计 | 泛指 | https://www.nist.gov/publications/zero-trust-architecture | 否 |
| 09 | 云中立≠反云；可观测开放格式；企业自有控制面 | 泛指 | — | 否 |
| 专题一 | Kafka 可回放日志、页缓存/顺序写；Redis 热状态层、antirez/LLOOGG | 正确（软化“内核红利”表述） | https://en.wikipedia.org/wiki/Apache_Kafka ; https://en.wikipedia.org/wiki/Redis | 否 |

处理说明：Drive 原文多为 ChatGPT 对话与关键词/图文制作稿；已跳过关键词列表与制作说明，仅改写叙事段落融入书稿。未发明统计数字或第一人称经历。

## v4.9 新增事实核查
核查时间：2026-10-20（北京时间），全部用 WebSearch 实时检索官方文档/论文/发布公告。

共 48 条：核实 35，通识/观点 8，软化或更正 7。

| 章节 | 原句 | 结论 | 依据链接 | 处理 |
|---|---|---|---|---|
| 01 | 1999 年 Dan Kegel 写了《The C10K problem》 | 核实 | https://web.archive.org/web/19990508164301/http://www.kegel.com/c10k.html | 保留 |
| 01 | epoll 在 2.5.44 版内核首次出现，随 2.6 系列走向主流 | 核实（man epoll(7)：introduced in 2.5.44） | https://lwn.net/Articles/16026/ | 保留 |
| 01 | 1998 年 5 月章文嵩发起 LVS | 核实 | https://www.linuxvirtualserver.org/whatis.html | 保留 |
| 01 | 2004 年 10 月 Igor Sysoev 发布 Nginx 第一个公开版本 | 核实（0.1.0，2004-10-04） | https://blog.nginx.org/blog/celebrating-20-years-of-nginx | 保留 |
| 01 | 2016 年 9 月 Lyft 开源 Envoy | 核实（2016-09-14） | https://eng.lyft.com/announcing-envoy-c-l7-proxy-and-communication-bus-92520b6c8191 | 保留 |
| 01 | Intel 发起的 DPDK 绕过内核收发包 | 核实（Intel 2010 创建；2013 dpdk.org；2017 入 LF） | https://www.linuxfoundation.org/press/press-release/networking-industry-leaders-join-forces-to-expand-new-open-source-community-to-drive-development-of-the-dpdk-project | 保留，未写具体年份 |
| 01 | Google 2016 年出版《Site Reliability Engineering》，提出错误预算 | 核实（O'Reilly 2016-04；第 3 章 Embracing Risk） | https://sre.google/sre-book/embracing-risk/ | 删去中文版书名（未单独核实） |
| 01 | 2000 年 Brewer 在 PODC 主题演讲提出 CAP；2002 年 Gilbert、Lynch 证明 | 核实 | https://doi.org/10.1145/564585.564601 | 保留 |
| 01 | Lamport 的 Paxos 以“兼职议会”故事写成，1998 年发表 | 核实（ACM TOCS 16(2), 1998-05） | https://dl.acm.org/doi/10.1145/279227.279229 | 保留 |
| 01 | 2014 年 Ongaro、Ousterhout 发表 Raft，获 USENIX ATC 最佳论文 | 核实 | https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro | 保留 |
| 01 | Yahoo 开发的 ZooKeeper 2010 年成为 Apache 顶级项目 | 核实（2010-11-17 董事会批准） | https://www.apache.org/foundation/board/minutes/ZooKeeper.html | 保留 |
| 01 | etcd 用 Raft；Kubernetes 状态存于 etcd | 通识（etcd/K8s 官方文档） | https://etcd.io/docs/ | 保留 |
| 02 | 2005 年随 Solaris 10 正式发布的 Zones | 核实（2004 beta，2005-03 GA） | https://en.wikipedia.org/wiki/Solaris_Containers | 保留 |
| 02 | Virtuozzo 与 2005 年开源的 OpenVZ | 核实 | https://wiki.openvz.org/History | 保留，未写 Virtuozzo 年份（2000 开发/2002 商用，口径不一） |
| 02 | ESXi 是一型，Workstation 是二型 | 核实 | https://www.vmware.com/topics/hypervisor | 保留 |
| 02 | “吵闹的邻居”、利用率与稳定性拔河 | 观点/行业术语，非数据 | — | 保留，无数字 |
| 02 | 调度器决定资源归属 | 观点 | — | 保留 |
| 03 | 块/文件/对象存储比喻 | 通识 | — | 保留 |
| 03 | 数据比计算更难移动（数据引力） | 观点，无数字 | — | 保留，未引用具体搬迁数据 |
| 03 | 2008 年 McKeown 等发表 OpenFlow 论文 | 核实（SIGCOMM CCR 38(2)） | https://dl.acm.org/doi/10.1145/1355734.1355746 | 保留 |
| 03 | VLAN 编号 12 位，可用 4094；RFC 7348（2014）VXLAN 24 位约 1600 万 | 核实 | https://www.rfc-editor.org/rfc/rfc7348 | 保留 |
| 04 | 2013 年 Google 发表 Omega 论文；想法回流 Borg 与 Kubernetes | 核实（EuroSys 2013；ACM Queue 2016 “Borg, Omega, and Kubernetes”） | https://queue.acm.org/doi/full/10.1145/2898442.2898444 | 保留 |
| 04 | “Borg 管了十多年” | 未精确核实 | — | 软化为“早在 Kubernetes 之前就管着生产集群” |
| 04 | 2009 年伯克利做出 Mesos 前身，2013 年 Apache 顶级项目 | 核实（Nexus TR 2009-11） | https://news.apache.org/foundation/entry/the_apache_software_foundation_announces45 | 保留 |
| 04 | Twitter 等公司曾用 Mesos | 未逐条核实 | — | 软化为“一度是热门选择” |
| 04 | 2016 年 Docker 1.12 内置 Swarm 模式 | 核实 | https://www.docker.com/blog/docker-1-12-built-in-orchestration/ | 保留 |
| 04 | 2019 年 Docker 企业业务卖给 Mirantis | 核实（2019-11） | https://www.mirantis.com/company/press-center/company-news/mirantis-acquires-docker-enterprise/ | 保留 |
| 04 | 2025 年 Apache Mesos 移入 Attic | 核实（2025-08 退役，10 月完成） | https://attic.apache.org/projects/mesos.html | 保留 |
| 04 | 2015 年 12 月阿里提出“大中台、小前台” | 核实（2015-12-07 张勇内部信） | https://www.thepaper.cn/newsDetail_forward_1405922 | 保留 |
| 04 | 中台被 PaaS 吸收、“中台渐冷” | 观点，无统计 | — | 软化为“不少企业开始重新掂量” |
| 04 | CapEx→OpEx，按小时/秒计费 | 通识（AWS 按秒计费 2017） | https://aws.amazon.com/about-aws/whats-new/2017/10/announcing-amazon-ec2-per-second-billing/ | 保留 |
| 05 | 2018 年 11 月 AWS 推出 Transit Gateway | 核实（2018-11-26） | https://aws.amazon.com/about-aws/whats-new/2018/11/introducing-aws-transit-gateway/ | 保留 |
| 05 | 2017 年 11 月推出 PrivateLink | 核实 | https://press.aboutamazon.com/2017/11/aws-announces-aws-privatelink | 保留（原稿“再早一年”正确） |
| 05 | CMDB 记录资源、负责人、依赖 | 通识（ITIL） | — | 保留 |
| 06 | Terraform state 映射资源；plan 先刷新再比较、不改动 | 核实 | https://developer.hashicorp.com/terraform/cli/commands/plan | 保留 |
| 06 | 远程 state + 锁 | 核实（Terraform 文档 state locking） | https://developer.hashicorp.com/terraform/language/state/locking | 保留 |
| 08 | CISA 2023 零信任成熟度模型 2.0：四阶段、五支柱 | 核实 | https://www.cisa.gov/zero-trust-maturity-model | 保留；原稿“落地五阶段”无出处，改用 CISA 四阶段 |
| 08 | （去重）删除与上文重复的“零信任通常还意味着……”一段 | — | — | 已替换 |
| 09 | 2019 年 5 月 OpenTracing 与 OpenCensus 合并为 OpenTelemetry | 核实 | https://www.cncf.io/blog/2019/05/21/a-brief-history-of-opentelemetry-so-far/ | 保留 |
| 09 | Prometheus 2012 SoundCloud，2016 第二个加入 CNCF | 核实 | https://www.cncf.io/announcements/2018/08/09/prometheus-graduates/ | 保留 |
| 09 | Loki 2018、Tempo 2020（Grafana Labs） | 核实 | https://grafana.com/blog/announcing-grafana-tempo-a-massively-scalable-distributed-tracing-system/ | 保留 |
| 09 | BPF 上世纪 90 年代初；Linux 3.18（2014）引入 eBPF 系统调用 | 核实（McCanne/Jacobson 1992 论文、1993 发表） | https://docs.ebpf.io/linux/timeline/ | 年份软化为“90 年代初” |
| 09 | DeepFlow 等具体产品 | 未写名 | — | 避免软文，只说“一些开源项目” |
| 10 | All-Reduce / NCCL 组织 GPU 集体通信 | 核实 | https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html | 保留 |
| 10 | NVLink 2014 发布，2016 随 Tesla P100 落地 | 核实 | https://nvidianews.nvidia.com/news/nvidia-launches-world-s-first-high-speed-gpu-interconnect-helping-pave-the-way-to-exascale-computing | 保留 |
| 10 | RoCE v1 2010 仅二层；RoCE v2 2014 加 UDP/IP 可路由 | 核实 | https://infinibandta.org/ibta-announces-new-roce-specification/ | 保留 |
| 10 | 2023 年 SOSP vLLM/PagedAttention，借鉴分页减少 KV Cache 浪费 | 核实（arXiv 2309.06180） | https://arxiv.org/abs/2309.06180 | 保留；未引用 60–80% 浪费等数字 |
| 10 | “五十年前”发明分页 | 不准确（Atlas 约 1962） | — | 改为“几十年前” |
