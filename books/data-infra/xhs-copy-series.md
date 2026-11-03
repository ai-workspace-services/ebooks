# 《数据基础设施 AI 前后》v2 · 小红书 / 微信图文配文（13 篇）

每篇正文 300–500 字（不含标题与话题标签），年龄按 2026 年计，事实与年份均取自 v2 图稿与 series-copy.md。

## 00 SQL 52岁，Agent才2岁？

AI 再火，最底下撑着的还是 52 岁的 SQL。

AI 之前，数据基础设施是这么一路走来的：1970–1990 年代关系型数据库，1990 年代数据仓库与 BI，2006 年起 Hadoop 大数据，2010 年起云数仓，2020 年起湖仓一体与实时流。2022 年 11 月 ChatGPT 是分水岭，之后向量数据库与 RAG 普及，2024 年起出现 AI 原生数据平台、Agent 数据层和 MCP。用数据的人，也从分析师变成了“人 + 模型 / Agent”。

两张图里我最想让你记住的：
1️⃣ 6 层架构自下而上：存储、采集、计算、仓湖与 BI、治理、AI 数据层。
2️⃣ 查询方式变了：从 SQL 和报表，变成自然语言 + 语义检索。
3️⃣ 交付物变了：AI 之前交付报表、看板，AI 之后交付上下文、答案和自动化动作。
4️⃣ 年龄榜反差：Agent 2~4 岁、LLM 2~9 岁，天天喊着替人类打工；真正打江山的是 SQL 52 岁、C 语言 54 岁、NVIDIA 33 岁和 115 岁的 IBM。

选型小建议：先把口径、权限、质量这些老功课做扎实，再谈“AI 就绪”。数据本身不可信，模型只会更自信地答错。

你现在的数据栈最卡哪一层？A 存储 B 采集与计算 C 治理 D AI 数据层，评论区说说。

📌 共 2 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 00/12 · 数据基础设施概览
Haitao Pan · XWork Technologies LLC 服务支持

#数据基础设施 #AI #大数据 #数据库 #程序员 #技术科普 #独立开发


## 01 52岁的SQL，还在扛AI

做独立开发这些年，框架换了一茬又一茬，数据库却很少换。

AI 之前，这条线很清楚：1970 年 Codd 提出关系模型，1979 年 Oracle 推出商用 SQL 数据库，1995–96 年 MySQL、PostgreSQL 开源；2006 年 Amazon S3 上线、Hadoop/HDFS 诞生；2009 年 MongoDB、Redis 发布，NoSQL 兴起；2012 年 Spanner 论文发表，NewSQL 起步。2022 年 11 月 ChatGPT 之后，主流数据库陆续内置向量检索；2024 年 11 月 MCP 发布，数据库可以直接当 Agent 的工具。

图里的重点：
1️⃣ 四大子类各司其职：关系型 OLTP、NoSQL、分布式 SQL、对象存储与 HDFS。
2️⃣ PostgreSQL 借 pgvector（2021 年首个版本）做到“一库多用”，事务和语义检索放在同一个库里。
3️⃣ 对象存储成了训练语料、RAG 文档和模型文件的统一仓库。
4️⃣ Agent 直连数据库，催生了只读副本、查询限流和细粒度权限的需求。
5️⃣ 冷知识：SQL 最早叫 SEQUEL，1974 年诞生于 IBM，因为英国 Hawker Siddeley 公司持有这个商标，才去掉元音改名 SQL。

选型小建议：先看现有数据库的向量能力够不够，再决定要不要引入专用向量库；单机或主从真扩不动了，再上分布式 SQL。

你的项目主库是哪个？A PostgreSQL B MySQL C MongoDB D 其他，评论区聊聊。

📌 共 4 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 01/12 · 数据库与存储
Haitao Pan · XWork Technologies LLC 服务支持

#数据库 #SQL #PostgreSQL #AI #大数据 #程序员 #技术科普


## 02 Kafka才15岁，比SQL小37岁

数据进不来，后面的 AI 都是空谈。这一层管的就是数据怎么进来、怎么保持新鲜。

AI 之前：1993 年 Informatica 成立，企业 ETL 兴起；2011 年 Kafka 开源；2012 年 Fivetran 成立；2016 年 Debezium 0.1 带来开源 CDC；2018–19 年 Census、Hightouch 开创反向 ETL；2020 年 Airbyte 开源连接器平台；2021 年 6 月 Sqoop 退役，进了 Apache Attic。AI 之后：2023 年起“文档解析 → 切块 → Embedding”管道普及；2024 年 11 月 MCP 发布，Agent 可以按需拉取数据。

图里的重点：
1️⃣ 四种进数方式：批量 ETL/ELT、CDC 变更捕获、消息队列与流平台、反向 ETL。
2️⃣ PDF、网页、工单这些非结构化数据成了一等公民，管道里多了解析、切块、嵌入三步。
3️⃣ CDC 让向量索引和源数据保持同步，AI 才不会读到过期内容。
4️⃣ 反向 ETL 正在走向“动作回写”：Agent 不只读数据，还要把结果写回业务系统。
5️⃣ 冷知识：本章最年长的 Informatica 和 R 语言同岁，都是 33 岁。

选型小建议：先定延迟需求——小时级用批量，分钟级用 ELT，秒级再上 CDC；敏感字段在采集环节就做脱敏或分级，别留到下游。

你们现在怎么同步数据？A 定时批量 B CDC 实时 C 手动导表，评论区见。

📌 共 4 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 02/12 · 数据采集与集成
Haitao Pan · XWork Technologies LLC 服务支持

#数据集成 #ETL #Kafka #AI #大数据 #程序员 #技术科普


## 03 Python比Java还大4岁

很多人以为 Python 是“新语言”，其实它 1991 年就发布了，比 Java（1995）还大 4 岁。计算层就是数据的“加工厂”，Python 数据栈和深度学习框架都在这里干活。

AI 之前，计算层是“大数据”的主场：2004 年 Google 发表 MapReduce 论文，2006 年 Hadoop 诞生，2008 年 Hive 开源，2011 年 Storm 开源，2014 年 Spark、Flink 成为 Apache 顶级项目，2015 年 Airflow 开源，2016 年 dbt 发布。AI 之后，2023 年起 Embedding 和 LLM 批量推理进入数据管道，2024 年起用 LLM 辅助写 SQL、dbt 模型和排错成了趋势。

图里的重点：
1️⃣ 四个子类：批处理、流处理、编排与转换、AI 计算。
2️⃣ 管道里的新任务：Embedding、批量推理、数据标注、合成数据。
3️⃣ CPU 与 GPU 混合调度，Ray 这类框架进了数据团队。
4️⃣ 编排对象从“表”扩展到模型、提示词和评测集。
5️⃣ 新陈代谢很快：MapReduce 已成 LEGACY，Oozie 2025 年 2 月退役。顺带一提，Jupyter 的名字致敬 Julia、Python 和 R。

选型小建议：先定延迟，分钟级用批处理、秒级用流处理，别为实时而实时；能用托管版本就别自建，省下的运维时间拿去写业务；SQL 优先还是代码优先，取决于团队技能。

你的数据加工主力是？A SQL + dbt B Spark C Pandas / Polars D Excel 公式。

📌 共 5 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 03/12 · 计算与处理
Haitao Pan · XWork Technologies LLC 服务支持

#大数据 #Spark #Python #数据工程 #AI #程序员 #技术科普


## 04 Excel 41岁，最早只在Mac上

先来个冷知识：Excel 1985 年首发在 Mac 上，Windows 版 1987 年才来。这一层再怎么变，最终结论往往还是要回到 SQL 和表格。

AI 之前：1979 年 Teradata 成立，MPP 数仓起步；1990 年代有了 Inmon / Kimball 建模方法；2003 年 Tableau 成立；BigQuery（2010）、Redshift（2012）发布；2012 年 Snowflake 成立、Druid 开源；2015 年 Power BI 正式发布；2016 年 ClickHouse 开源；2017–19 年 Hudi、Iceberg、Delta Lake 相继开源；2020 年提出湖仓一体。AI 之后：2023 年起出现仓内 LLM 函数和 BI Copilot，2024 年 Unity Catalog 开源、Polaris 发布。

图里的重点：
1️⃣ 五个子类：传统数仓、云数仓、湖仓表格式、OLAP 引擎、BI。
2️⃣ 自然语言问数（Text-to-SQL、BI Copilot）让非技术同事也能直接提问。
3️⃣ 仓湖不再只服务报表，也成了模型训练和 RAG 的数据底座。
4️⃣ 开放表格式让 SQL 引擎和 AI 引擎读同一份数据，少做复制。
5️⃣ 指标口径不统一，AI 会算出“自信的错答案”，所以语义层更重要了。

选型小建议：Copilot 类功能一定要能看到它生成的 SQL，可审计、可纠错；计费模型别只看报价，拿真实负载跑一遍再算账；BI 要看语义层、权限继承和嵌入能力。

你们看数主要靠？A Excel B Tableau / Power BI C 开源 BI D 直接问 AI。

📌 共 5 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 04/12 · 分析、仓湖与 BI
Haitao Pan · XWork Technologies LLC 服务支持

#数据仓库 #BI #湖仓一体 #Excel #AI #大数据 #技术科普


## 05 治理工具大多不到10岁

有个反差挺好玩：治理工具大多不到 10 岁，它们要管的 SQL 已经 52 岁了。

AI 之前：2015 年 Apache Atlas 进入孵化，2016 年 LinkedIn 开源 WhereHows，2017 年 Great Expectations 开源，2018 年 5 月欧盟 GDPR 生效，2019 年 Lyft 开源 Amundsen，2020 年 DataHub 开源、CCPA 生效，2021 年 OpenMetadata 发布，中国《数据安全法》《个人信息保护法》施行。AI 之后：2024 年 6 月 Unity Catalog 开源，主打数据与 AI 统一目录；2024 年 8 月欧盟《人工智能法》生效；2025 年 9 月 Apache Griffin 退役。

图里的重点：
1️⃣ 四块拼图：元数据 / 目录 / 血缘、数据质量、权限与隐私合规、数据可观测。
2️⃣ 治理对象从表扩展到模型、特征、提示词和向量索引。
3️⃣ AI 反过来帮治理：自动打标签、生成数据文档、识别敏感字段。
4️⃣ Agent 访问需要行列级权限，每一次工具调用都要记入审计。
5️⃣ AI 法规要求训练与检索数据可追溯、来源说得清。

选型小建议：质量规则写进管道（左移），别靠事后巡检；权限先用 RBAC 起步，敏感场景再上 ABAC 和动态脱敏；合规地域要求要先于工具选型。

你们的数据有血缘图吗？A 有，自动采集 B 有，手工维护 C 没有，全靠记忆。

📌 共 4 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 05/12 · 数据治理与安全
Haitao Pan · XWork Technologies LLC 服务支持

#数据治理 #数据安全 #合规 #AI #大数据 #程序员 #技术科普


## 06 千万级向量，先用pgvector

做 RAG 之前，我也纠结过要不要上专用向量库，后来发现很多场景一个 PostgreSQL 就够了。

AI 之前：2017 年 Uber Michelangelo 让特征平台概念成型，Kubeflow 发布；2018 年 MLflow 发布；2019 年 Feast、Milvus 开源；2020 年 RAG 论文发表；2021 年 Pinecone 公开发布、pgvector 0.1；2022 年 10–11 月 LangChain、GPT Index（LlamaIndex）发布。AI 之后：2023 年向量检索成为数据库标配，语义层产品化；2024 年 11 月 Anthropic 开源 MCP；2025 年起 Text-to-SQL Agent 与 MCP Server 生态成为趋势。

图里的重点：
1️⃣ 五个子类：特征平台与 MLOps、向量数据库、RAG 与索引、语义层与 Text-to-SQL、Agent 数据接入（MCP）。
2️⃣ 数据从“给人看”变成“给模型用”，交付物从报表变成上下文。
3️⃣ 新瓶颈是检索质量、数据新鲜度和权限过滤，召回率、幻觉率进了数据团队 KPI。
4️⃣ 冷知识：Hugging Face 2016 年起家时，是一款陪青少年聊天的机器人 App。

选型小建议：千万级向量以内先用 pgvector，规模和 QPS 上来再换专用库；默认用关键词 + 向量的混合检索再加重排；保留原文，换 Embedding 模型时才能重建索引；MCP 接入只读优先。

你的 RAG 向量存在哪？A pgvector B 专用向量库 C 托管服务 D 还没开始做。

📌 共 5 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 06/12 · AI 数据层
Haitao Pan · XWork Technologies LLC 服务支持

#RAG #向量数据库 #AI #大模型 #MCP #程序员 #技术科普


## 07 DuckDB的名字来自一只鸭

大模型再强，最后还得查 SQL、看表格。这组工具里最老的 SPSS 58 岁，最年轻的 Polars 也 6 岁了。

AI 之前：1968 年 SPSS 发布，1974 年 SEQUEL（SQL）论文，1976 年 SAS Institute 成立，1985 年 Excel 首发 Mac，1993 年 R 语言发布，2003 年 Tableau 成立，2008 年 Pandas 起步，2009 年 Spark 诞生于伯克利，2014 年 Project Jupyter，2019 年 DuckDB 0.1，2020 年 Polars 起步。AI 之后：2023 年 7 月 ChatGPT Code Interpreter 上线，上传表格就能直接分析；2023 年 8 月 Python in Excel 公测，单元格里能写 =PY。

图里的重点：
1️⃣ 四组工具：统计软件老前辈、表格与可视化、Python 数据栈、新一代引擎。
2️⃣ SQL 和 Pandas 代码越来越多由 AI 生成，人负责审核口径和结果。
3️⃣ DuckDB、Polars 让笔记本也能分析大数据，AI 工具常把它们当执行后端。
4️⃣ Pandas 2008 年诞生于对冲基金 AQR，是 Wes McKinney 为金融数据分析写的。
5️⃣ DuckDB 的名字来自创始人养过的宠物鸭 Wilbur：鸭子能飞、能走、能游，象征多面手。

选型小建议：工具再新，结论最终要能回到可复核的 SQL 和表格。让 AI 写分析代码可以，但口径和结果一定自己过一遍。能在笔记本上用单机引擎跑完的分析，就没必要先开集群。

你日常分析用哪个？A Excel B SQL C Pandas D DuckDB / Polars。

📌 共 6 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 07/12 · 数据分析工具
Haitao Pan · XWork Technologies LLC 服务支持

#数据分析 #SQL #Excel #Python #AI #程序员 #技术科普


## 08 感知机68岁，还在教科书第一章

LLM 很火，但在表格数据上，梯度提升树依然是强基线。

AI 之前：1958 年感知机，1967 年 k-NN（Cover & Hart），1986 年 ID3 决策树，1993 年 Weka 立项，1995 年 SVM 软间隔，2001 年随机森林，2007 年 Scikit-learn 立项，2014 年 XGBoost，2016 年 LightGBM，2017 年 CatBoost；2022 年 7 月还有论文指出，表格数据上树模型仍强于深度学习。AI 之后：2023 年起 LLM 辅助写特征工程和建模代码，2025 年 1 月 TabPFN 登上 Nature，表格基础模型来了。

图里的重点：
1️⃣ 梯度提升三剑客：XGBoost 12 岁（陈天奇）、LightGBM 10 岁（微软）、CatBoost 9 岁（Yandex）。
2️⃣ LLM 帮忙写特征工程、调参与评估代码，建模门槛进一步降低。
3️⃣ 经典模型更容易解释和审计，合规场景依然常用。
4️⃣ 冷知识：1958 年《纽约时报》报道感知机时说，海军预计它将来能“走路、说话、看、写、自我复制”。
5️⃣ Weka 是新西兰一种不会飞的鸟；XGBoost 在 2014 年 Kaggle 希格斯玻色子挑战赛（1785 支队伍参赛）中走红。

选型小建议：表格数据先跑一个梯度提升树当基线，再决定要不要试深度学习或 TabPFN 这类表格基础模型。

你做表格预测首选？A XGBoost / LightGBM B 随机森林 C 深度学习 D 直接问 LLM。

📌 共 5 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 08/12 · 机器学习算法与库
Haitao Pan · XWork Technologies LLC 服务支持

#机器学习 #XGBoost #算法 #AI #数据科学 #程序员 #技术科普


## 09 AlexNet只用两块3GB显卡

今天训练大模型拼的是编译、分布式和显存效率，可 2012 年的 AlexNet 只用了两块 3GB 显存的 GTX 580，训练了约 5–6 天。

AI 之前：1986 年反向传播推广，1997 年 LSTM，1998 年 LeNet-5，2007 年 Theano，2012 年 AlexNet，2013 年 Caffe，2015 年 Keras、TensorFlow、ResNet 扎堆出现，2016 年 PyTorch，2018 年 JAX。AI 之后：2023 年 3 月 PyTorch 2.0 带来 torch.compile，把编译优化带进日常训练；2023 年 11 月 Keras 3 支持 JAX / TF / PyTorch 多后端。

图里的重点：
1️⃣ 年龄 8–40 岁：最年轻的 JAX 8 岁，BP 推广 40 岁，正是挑大梁的青壮年。
2️⃣ 从学术框架到工业级平台，接口越来越高层，几行代码就能搭出网络。
3️⃣ Keras 3 回归多后端，同一份代码能跑在三个框架上。
4️⃣ LeNet-5 曾用于美国银行的支票识别，据估计一度每天读取全美约 10% 的支票。
5️⃣ Keras 的名字来自希腊语“角”，典出《奥德赛》的“角之门”：从那里来的梦会成真。

选型小建议：新项目先看团队熟悉度和部署链路；想给自己留切换余地，可以考虑 Keras 3 这类多后端接口。说到底，AI 时代的底层依然是 1986 年推广开的反向传播。

你的主力框架是？A PyTorch B TensorFlow / Keras C JAX。

📌 共 5 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 09/12 · 深度学习框架与里程碑
Haitao Pan · XWork Technologies LLC 服务支持

#深度学习 #PyTorch #TensorFlow #AI #神经网络 #程序员 #技术科普


## 10 Transformer今年才9岁

整个 LLM 时代满打满算不到 10 岁，Transformer 今年才 9 岁。从注意力机制奠基到现在，这个时代其实才刚读小学。

AI 之前：2013 年 Word2Vec，2017 年 Transformer，2018 年 GPT-1、BERT，2019 年 GPT-2、T5，2020 年 GPT-3，2022 年 1 月 InstructGPT。分水岭是 2022 年 11 月的 ChatGPT，之后 2023 年 2–3 月 LLaMA、GPT-4 登场，2024 年 3 月 Claude 3，2024 年 12 月和 2025 年 1 月 DeepSeek-V3 / R1。

图里的重点：
1️⃣ 预训练前夜，Word2Vec 把词变成向量，Transformer 用注意力机制取代循环网络；到了预训练时代，“先预训练、再微调”成了范式，参数从 1 亿涨到 GPT-3 的 1750 亿。
2️⃣ 分水岭之后，模型从研究成果变成人人可用的产品：ChatGPT 上线 5 天用户破百万，约两个月月活过亿。
3️⃣ 开源模型（LLaMA、DeepSeek 等）让企业可以私有化部署。
4️⃣ 推理模型（R1 等）把“先思考再回答”带进主流。
5️⃣ 冷知识：《Attention Is All You Need》共 8 位作者；GPT-2 曾因担心被滥用而分阶段放出，2019 年 11 月才发布 15 亿参数完整版。

选型小建议：先想清楚数据能不能离开自己的环境——能，就用 API 快速验证；不能，就评估开源模型私有化部署。

你现在用得最多的是？A 闭源 API B 开源模型自部署 C 两者混用。

📌 共 4 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 10/12 · 大语言模型
Haitao Pan · XWork Technologies LLC 服务支持

#大语言模型 #LLM #ChatGPT #DeepSeek #AI #程序员 #技术科普


## 11 Agent全家最大的才4岁

Agent 天天说要接管人类工作，可全家最大的 LangChain 才 4 岁，人均还在“喝奶、读幼儿园”的年纪。

AI 之前只有两位“前辈”：2022 年 10 月 LangChain、2022 年 11 月 GPT Index（LlamaIndex）。AI 之后一下子热闹了：2023 年 3 月 AutoGPT、BabyAGI，6 月 MetaGPT 开源，10 月 AutoGen 独立仓库，11 月 CrewAI 0.1；2024 年 3 月 Devin，11 月 MCP 开源；2025 年 2–6 月 Claude Code、Codex CLI、Gemini CLI 相继出现，12 月 MCP 捐给 Linux 基金会 AAIF；2026 年 2 月 Xcode 26.3 集成编码 Agent 与 MCP。

图里的重点：
1️⃣ 三大类：编排与数据框架，把模型、工具和私有数据串起来；自主与多智能体，给个目标就自己拆任务、分角色协作；AI 软件工程师，从写代码片段到独立修 Bug、提交 PR。
2️⃣ 2025 年起编码 Agent 进入终端和 IDE，成了开发者的日常工具。
3️⃣ MCP 让 Agent 用统一协议接入数据库、文件和 SaaS。
4️⃣ BabyAGI 原版只有约 140 行 Python，作者说代码由 GPT-4 写成，用了约 50 个提示词。
5️⃣ Devin 2024 年在 SWE-bench 570 题子集上独立解决 13.86%，此前无辅助的最好成绩只有 1.96%。

选型小建议：能力越强越要管住权限——只读优先、最小授权、全程审计，敏感操作留给人来确认。

你让 Agent 干过最大的活是？A 写代码 B 查数据 C 跑自动化流程 D 还不敢放手。

📌 共 4 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 11/12 · AI Agent
Haitao Pan · XWork Technologies LLC 服务支持

#AIAgent #智能体 #MCP #AI编程 #大模型 #程序员 #技术科普


## 12 IBM 115岁，AI新秀才3岁

最年轻的 AI 新秀 3 岁，最年长的 IBM 115 岁，差了整整 112 岁。从打孔卡到大模型，整部计算机史都在这张榜上。

AI 之前的公司年表：1911 年 CTR 成立（1924 年改名 IBM），1975 年 Microsoft，1976 年 Apple，1993 年 NVIDIA，1998 年 Google，2004 年 Facebook，2010 年 DeepMind，2015 年 OpenAI，2016 年 Hugging Face，2019 年智谱、Cohere，2021 年 Anthropic，2022 年 8 月 Perplexity。ChatGPT 之后成立的新秀：2023 年 3 月月之暗面、4 月 Mistral AI、7 月 DeepSeek。

图里的重点：
1️⃣ 四组公司：百年与半百巨头、互联网与算力、AI 研究与平台、AI 之后的新秀。
2️⃣ 老牌巨头靠算力、云和终端入口参与 AI 竞争。
3️⃣ 2021–2023 年成立的公司，几年内就成了大模型赛道的重要玩家。
4️⃣ 冷知识：NVIDIA 1993 年由黄仁勋等三人在圣何塞一家 Denny's 餐厅的卡座里谋划诞生；Google 1996 年在斯坦福时叫 BackRub，因为它分析的是网页的“反向链接”。
5️⃣ 趣味反差：Agent 还在幼儿园，SQL 已经 52 岁，C 语言 54 岁。

选型小建议：选模型或平台时别只看热度，优先选接口开放、方便迁移的方案，供应商换了也不至于推倒重来。

你觉得 10 年后还在牌桌上的是？A 百年老店 B 互联网巨头 C AI 新秀。

📌 共 5 张图，建议按顺序看
图解 IT 简史 · 数据基础设施 AI 前后 系列 12/12 · AI 与科技公司寿命
Haitao Pan · XWork Technologies LLC 服务支持

#科技公司 #AI #NVIDIA #OpenAI #科技史 #程序员 #技术科普
