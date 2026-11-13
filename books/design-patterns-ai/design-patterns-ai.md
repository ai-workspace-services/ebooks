# 序章 到了 AI 时代，我们反而更需要思考设计模式

AI 写代码的速度，已经把“能不能写出来”变成了次要问题。更常见的局面是：一次对话之后，仓库里多出了整整齐齐的接口、实现类、管理器、仓储和外观。缩进对齐，命名对称，目录看起来像教科书的参考答案。可是你只想改一个校验条件，却要同时打开七个文件，而且其中四个除了把参数原样传下去，什么也没做。

这不是传统意义上的烂代码。它更像一本正经、整整齐齐的屎山：结构很工整，层次很完整，就是经不起真实变化。AI 特别擅长生产这类东西，因为它在训练语料里见过太多“先把架构搭整齐”的示例，尤其是从类继承和接口族谱里长出来的写法。

所以到了 AI 时代，我们反而更需要思考设计模式。不是为了把模式贴得更多，而是为了在生成速度被放大之后，仍然能判断：这里到底有没有一个值得认真对待的变化点，或一个必须守住的一致性问题。没有，就直接写。有，再用合适的形状把它说清楚，并落回当前技术栈里已经存在的原语。

本书不谈 Java 的类继承教条，也不把 UML 里的箭头当成目标形态。立足的是今天已经在用的工程范式：Linux 容器原生，Node.js / Next.js 的 Portal，Go / Gin 的服务，以及 PostgreSQL 的约束与事务。需要时再辅以 Python CLI、GitHub Actions，以及 HCL 模块和 Ansible Playbook。模式的名字用来沟通，代码则用函数、结构体、模块和框架原语实现。

全书覆盖十八个经典模式。每一个都讲清五件事：适用信号、现代技术栈中的落点、AI 容易写出的过度设计反例、一段轻量实现，以及选型边界和验证方法。读完之后，希望你面对 AI 交出来的“完整方案”时，第一反应不再是“看起来好规范”，而是：“这里的变化点到底在哪？”

<!-- diagram:diagram-ai-slop-vs-signal -->

# 第 1 章 先找变化点，再决定要不要模式

## 变化点先于模式名字

引入一个模式之前，先问两件事。第一，这里要处理的是哪一种变化，或哪一种必须守住的一致性？第二，如果不引入这个模式，现有的函数、模块或框架原语是否已经够用？

表里的“适用信号”不是装饰，而是门槛。同一用例需要按确定规则在多种算法里选择，才考虑 Strategy；外部接口的数据形状与内部契约不同，才考虑 Adapter；一个用例里的多步写入必须共同成功，才考虑显式事务，也就是 Unit of Work。信号不成立，就不要为了“看起来可扩展”提前铺层。

代价同样要算。每多一个接口，每多一个包装类型，阅读路径就长一截，修改时要同步的地方就多一处。AI 不会替你付这笔代价，因为它可以在几秒内再生成对称的一层。付账的是之后每一个要改规则的人。

## 命名是沟通手段

模式的名字适合出现在设计讨论和评审里：“这里是适配器，不是新的业务规则。”“这里要用条件更新守住状态转换。”它不适合变成类型名和文件名的主角。`startSubscription`、`qualifyPlan`、`invoiceFromStripe` 能对上用例；`SubscriptionManagerFacade`、`IBillingStrategyFactory` 只对上教材目录。

名称表达业务含义，不表达设计模式身份。文件、函数、类型和配置键应当能互相指认，一个名字只代表一种东西。写清楚，而不是写得短。先在现有模块上做最小扩展，只有出现真实的复用、替换或所有权边界时再拆层。

## 实现落回当前技术栈的原语

在本书使用的技术栈里，很多模式早就有现成落点：

- Next.js 的 Route Handler 和 BFF 转发，常常就是 Proxy 或 Adapter。
- Gin 的 middleware 就是 Decorator 或责任链。
- pgx 的事务就是 Unit of Work 的句柄。
- `UPDATE ... WHERE status = $from` 就是 State 转换的守卫。
- Python 的 callable 和生成器，往往就是 Strategy 与 Iterator。
- GitHub Actions 的 reusable workflow，常常已经是 Template Method。

不必先发明一套平行于框架的对象模型，再把框架当作“底层细节”藏起来。先用原语把变化点写清楚，只有原语不够用时，再补最小的一层。

## 十八个模式的信号总表

后文会按四个变化点把每个模式展开。这里先给出一张压缩总表，方便对照。落点按当前技术栈书写：Next.js Portal、Go / Gin、PostgreSQL，以及 Python CLI、GitHub Actions、HCL 与 Playbook。

| 模式 | 适用信号 | 落点与边界 |
| --- | --- | --- |
| Strategy 策略 | 同一用例要按确定规则选择多种算法 | Go 函数或小接口，TS 映射，Python callable。一种行为就直接调用。 |
| Adapter 适配器 | 外部接口、协议或数据形状与内部契约不同 | Next.js 上游客户端，Go Provider 客户端，Python CLI 包装。须明确错误与取消语义。 |
| Facade 外观 | 多个调用方需要同一高层用例，内部涉及多个能力 | Gin 服务入口，Next.js 服务端模块。以业务动词命名，保留可定位的失败原因。 |
| Factory 工厂 | 构造确有多种配置或依赖组合 | 启动入口按配置选择实现。简单初始化用构造函数，配置无效时明确失败。 |
| Builder 构建器 | 分步组装，且存在组合约束或可选参数交叉 | 复杂配置生成、请求组装。普通参数对象可直接传入，须验证缺项与非法组合。 |
| Decorator 装饰器 | 多个调用点需要一致的日志、计时等横切处理 | Gin middleware，Go HTTP transport，Python decorator。核对顺序、错误传播和身份边界。 |
| Chain of Responsibility 责任链 | 步骤按顺序检查且可终止请求 | Gin 鉴权链，CLI 校验链。拒绝后后续步骤必须停止。 |
| Template Method 模板方法 | 总体顺序固定，少数步骤有明确变化点 | reusable workflow，或函数接收步骤函数。调用方只注入允许变化的步骤。 |
| Command 命令 | 同一操作由 HTTP、CLI 或任务入口触发，或需要排队 | Gin 与 CLI 共用用例。明确各入口的授权、幂等范围和结果。 |
| State 状态 | 允许的动作由当前状态决定，转换需受控 | 订阅、工单、交付阶段；显式转换加 PostgreSQL 条件更新。验证非法转换、重入与并发。 |
| Observer 观察者 | 一个变化要通知多个相互独立的接收者 | UI 订阅、进程内事件、异步消费者。须明确同步性、顺序、失败传播和清理。 |
| Composite 组合 | 叶节点与分组需要相同的递归处理 | React 树形菜单，Python 分组配置。平面列表直接遍历。验证空分组与终止条件。 |
| Proxy 代理 | 需透明转发，并集中实施访问控制、超时或缓存 | Next.js BFF，Go HTTP 客户端代理。保持协议契约，明确凭据、缓存身份和失败传播。 |
| Iterator 迭代器 | 数据量大或分批获取，调用方要逐条处理 | Python 生成器，Go 逐行读取，TS 异步迭代。检查提前退出、资源释放和分页边界。 |
| Repository 仓储 | 同一数据访问契约被多个用例依赖，或查询细节需要隔离 | Go 的 store / repository，实现用 pgx 或 GORM。避免按表生成通用 CRUD。 |
| Unit of Work 工作单元 | 一个用例中的多步写入必须共同成功 | 用例内显式 PostgreSQL 事务，共享同一事务句柄。验证提交、回滚和重复调用。 |
| Transactional Outbox 事务性发件箱 | 提交后必须可靠地产生跨系统事件 | 同事务写业务记录和 outbox，worker 投递。接收方按事件标识幂等。 |
| Ports and Adapters 端口与适配器 | 业务规则需隔离外部依赖，或同一用例有多个协议入口 | Gin、CLI 和数据库适配同一个 Go 用例。先确定真实边界，再引入端口。 |

# 第 2 章 十八个模式的全景图：四个变化点

把十八个名字平铺在桌上，最容易重新掉进“收集模式”的陷阱。更有用的做法是先问：眼前这个问题，属于哪一类变化？

本书把它们归成四个变化点。

**入口与协议边界**：外部系统的形状和我们内部契约不一样，或同一个用例要从页面、HTTP 和命令行进来。这一类里是 Adapter、Facade、Proxy，以及 Ports and Adapters。

**构造与组合**：对象或配置的创建本身就有分叉，或树形结构需要统一处理。这一类里是 Factory、Builder、Composite。

**请求链与行为控制**：选择算法、加横切、按顺序把关、固定流程里留变化点、跨入口发出同一操作、按状态允许动作、通知多个接收者，或逐条消费大批数据。这一类里是 Strategy、Decorator、责任链、Template Method、Command、State、Observer、Iterator。

**数据一致性与可靠事件**：查询细节需要隔离，多步写入必须同生同灭，或提交之后还要把事件可靠地送出进程。这一类里是 Repository、Unit of Work、Transactional Outbox。

<!-- diagram:diagram-18-patterns-map -->

这四类很少单独出现。后面会反复回到一个完整现场：Portal、Gin 和 PostgreSQL 共同实现订阅。Portal 负责交互和结果呈现；资格规则由 Gin 用例维护；数据库用约束和条件更新保护可表达的持久化不变量；多步原子写入采用显式事务；只有真正需要可靠的跨系统事件时，才在同一事务里写入 Outbox，再由幂等的 Worker 投递。那不是把十八个模式塞进一个功能，而是让每一种变化都待在该待的地方。

# 第 3 章 入口与协议边界

外部世界不会按我们的结构体来。支付渠道有自己的事件名，上游 API 有自己的错误码，浏览器页面也不能直接持有数据库句柄。这一章处理的就是这些边界：把外来的形状收成内部契约，给多个调用方一个清楚的入口，在转发时守住访问控制和超时，并让同一段业务规则既服务 HTTP，也服务 CLI。

<!-- diagram:diagram-boundary-layers -->

## Adapter 适配器

**适用信号**：外部接口、协议或数据形状与内部契约不同。

**技术栈落点**：Next.js 里访问上游 API 的客户端，Go 里对接账单或身份 Provider 的客户端，以及把外部命令行输出收成内部结构的 Python 包装。适配器要做的是转换，不是重新发明一套业务规则。

**AI 常见反例**：为每一个上游字段生成一对一的 `XxxDTO`、`XxxMapper`、`XxxAdapterImpl`，再加一个空的 `AdapterFactory`。更糟的是把 SDK 类型直接泄漏进用例，或者在适配层里偷偷加入资格判断。看起来层次完整，实际是把变化点藏进了翻译过程。

**轻量实现**：只收内部真正需要的字段，并明确失败语义。

```go
type Invoice struct {
    ID     string
    Amount int64 // 最小货币单位
    Status string
}

func invoiceFromStripe(raw stripeEvent) (Invoice, error) {
    if raw.Type != "invoice.paid" {
        return Invoice{}, fmt.Errorf("unsupported event %s", raw.Type)
    }
    inv, err := raw.invoice()
    if err != nil {
        return Invoice{}, err
    }
    return Invoice{
        ID:     inv.ID,
        Amount: inv.AmountPaid,
        Status: "paid",
    }, nil
}
```

**选型边界与验证**：没有形状差异时，不必为“统一风格”包一层。验证时要覆盖格式错误、未知事件、调用取消和超时，确认这些失败不会被吞掉，也不会被解释成业务拒绝。

## Facade 外观

**适用信号**：多个调用方需要相同的高层用例，而这个用例内部会牵动多个能力。

**技术栈落点**：Gin 的服务入口，或 Next.js 服务端的功能模块。外观的价值是提供一个以业务动词命名的入口，而不是再发明一个“总管对象”。

**AI 常见反例**：`SubscriptionManagerFacade` 里堆上二十个方法，再把每个方法转发到另一个 `Service`，`Service` 再转发到 `Impl`。调用方仍然要理解内部步骤，失败时只得到一句 `internal error`。名字很像外观，实际既不外观，也不诚实。

**轻量实现**：入口负责绑定、鉴权和响应映射，业务规则交给用例，失败原因可定位。

```go
func (s *Server) startSubscription(c *gin.Context) {
    var req startSubReq
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{
            "error":  "invalid_request",
            "detail": err.Error(),
        })
        return
    }
    view, err := s.subs.Start(c.Request.Context(), req.toInput())
    if err != nil {
        writeAPIError(c, err) // 保留可定位的失败原因
        return
    }
    c.JSON(201, view)
}
```

**选型边界与验证**：只有一个调用方、内部也只有一步时，直接写处理函数即可。验证时看入口名称能否对上业务动词，以及每一种业务失败是否都能被调用方区分。

## Proxy 代理

**适用信号**：需要透明转发，并在转发点集中实施访问控制、超时或缓存。

**技术栈落点**：Next.js 的 BFF 转发，Go 的 HTTP 客户端代理。Proxy 必须保持协议契约：路径、状态码和错误含义不能被随便改写。凭据放在哪一侧、缓存键是否包含身份、失败如何传播，都要说清楚。

**AI 常见反例**：BFF 里既转发，又改写请求，还顺手做资格判断和数据聚合，最后变成一个隐形的第二套业务层。或者把上游的访问令牌缓存在与用户无关的公共键下，造成串用。

**轻量实现**：Portal 的 BFF 只做会话校验、超时和透明转发。

```ts
// app/api/billing/[...path]/route.ts
export async function POST(req: Request, ctx: Ctx) {
  const session = await requireSession(req);
  const path = ctx.params.path.join("/");
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 8_000);
  try {
    const res = await fetch(`${API_BASE}/v1/${path}`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${session.accessToken}`,
      },
      body: await req.text(),
      signal: ctl.signal,
      cache: "no-store",
    });
    return new Response(res.body, {
      status: res.status,
      headers: via(res),
    });
  } finally {
    clearTimeout(timer);
  }
}
```

**选型边界与验证**：如果调用方可以直接、安全地访问上游，就不要多一跳。验证超时是否终止请求，未登录是否进不去，缓存是否按身份隔离，以及上游 4xx / 5xx 是否原样可识别。

## Ports and Adapters 端口与适配器

**适用信号**：业务规则需要隔离外部依赖，或同一用例存在多个协议入口。

**技术栈落点**：Gin、CLI 和数据库适配同一个 Go 用例。先确定真实的依赖边界，再引入端口。不要为每个包预先准备一套接口。

**AI 常见反例**：每个目录都先写 `interface.go`，每个结构体都先抽 `IXxx`，测试里再配上二十个 mock。看起来“完全可替换”，其实没有一个替换是真实发生的。边界被接口数量掩盖，业务规则反而散落在各处。

**轻量实现**：用例只依赖自己真正需要的能力；HTTP 与 CLI 都只做适配。

```go
type Qualifier interface {
    Qualify(ctx context.Context, accountID, plan string) error
}

func (u *Subscription) Start(
    ctx context.Context, in StartInput,
) (*Sub, error) {
    if err := u.qualify.Qualify(ctx, in.AccountID, in.Plan); err != nil {
        return nil, err
    }
    return u.commitStart(ctx, in)
}
```

Gin 处理函数和 CLI 子命令都调用 `u.Start`。数据库访问通过已有的 store 端口完成，而不是让用例直接依赖某个驱动细节。若当前只有一种资格规则实现，也不必再包一层工厂。

**选型边界与验证**：只有一个入口、依赖也不需要在测试中替换时，直接传入具体类型即可。引入端口之后，验证 HTTP 与 CLI 是否真的走到同一用例，以及替换测试替身时是否只替换了那个真实边界。

# 第 4 章 构造与组合

这一章关注对象和配置是怎么被造出来的。如果构造只有一种方式，就用普通的构造函数或字面量。只有配置分叉、参数相互约束，或树形结构需要统一处理时，才值得把“怎么造”单独说清楚。

## Factory 工厂

**适用信号**：对象构造确有多种配置或依赖组合。

**技术栈落点**：Go 服务的启动入口按配置选择实现，Python 根据参数创建 CLI 客户端。工厂应当在配置无效时明确失败，而不是返回一个半初始化对象，把错误推迟到第一次调用。

**AI 常见反例**：即便只有 PostgreSQL 一种存储，也为 `Store`、`Cache`、`Logger` 各写一个抽象工厂家族，再加 `FactoryProvider`。启动代码读起来像框架，运行时却没有任何分叉。

**轻量实现**：分叉写在一个函数里，未知配置直接失败。

```go
func newStore(cfg Config) (Store, error) {
    switch cfg.Driver {
    case "postgres":
        return newPGStore(cfg.DSN)
    default:
        return nil, fmt.Errorf("unsupported driver %q", cfg.Driver)
    }
}
```

**选型边界与验证**：简单初始化用构造函数或 `NewXxx(cfg)` 即可。验证未知驱动、错误的数据源和缺项配置都会在启动时失败，而不是在第一个请求里才暴露。

## Builder 构建器

**适用信号**：对象需要分步组装，并且存在组合约束，或可选参数会交叉影响。

**技术栈落点**：Python 里生成复杂的渲染配置，Go 里组装有约束的请求。如果只是一串普通字段，直接传入参数对象，不要为了链式调用去写 Builder。

**AI 常见反例**：为只有三个字段的结构体生成 `WithX` / `WithY` / `Build` 长链，却不校验字段组合。`prod` 环境可以关掉 TLS，缺 `region` 也能 `Build()` 成功，问题被留到部署时。

**轻量实现**：用一个配置对象收集字段，在出口统一校验。

```python
@dataclass
class RenderOpts:
    env: str
    region: str
    replicas: int
    enable_tls: bool = True

    def validate(self) -> None:
        if self.replicas < 1:
            raise ValueError("replicas must be >= 1")
        if self.env == "prod" and not self.enable_tls:
            raise ValueError("prod requires tls")

def build_render_opts(data: dict) -> RenderOpts:
    opts = RenderOpts(
        env=data["env"],
        region=data.get("region", "default"),
        replicas=int(data.get("replicas", 1)),
        enable_tls=bool(data.get("enable_tls", True)),
    )
    opts.validate()
    return opts
```

**选型边界与验证**：没有交叉约束时，不必上构建器。验证要覆盖缺项、类型错误、以及像“生产环境关闭 TLS”这样的非法组合。

## Composite 组合

**适用信号**：树形对象的叶节点与分组需要相同的递归处理。

**技术栈落点**：React 里的树形菜单，Python 里分组配置的校验。如果数据其实是平面列表，直接遍历即可，不要先把它上升成组件树。

**AI 常见反例**：为两层菜单引入 `MenuComponent`、`MenuLeaf`、`MenuComposite` 和访问者。或者递归没有终止条件，空分组被静默跳过，错误要到运行时才出现。

**轻量实现**：用同一种函数处理节点和分组，显式对待空分组。

```python
def validate_group(node: dict) -> list[str]:
    errors: list[str] = []
    name = node.get("name", "?")
    if "children" in node:
        if not node["children"]:
            errors.append(f"{name}: empty group")
        for child in node["children"]:
            errors.extend(validate_group(child))
        return errors
    if "path" not in node:
        errors.append(f"{name}: leaf missing path")
    return errors
```

**选型边界与验证**：平面列表用直接循环。验证空分组、过深嵌套、缺字段的叶节点，以及递归能够终止。

# 第 5 章 请求链与行为控制

请求从进入系统到产生结果，中间会经过选择、过滤、排列和通知。这一章的模式都在回答：这一步能不能换，能不能停，能不能复用，以及状态变了之后谁有权继续往下走。

<!-- diagram:diagram-state-and-chain -->

## Strategy 策略

**适用信号**：同一用例需要按确定规则选择多个算法。

**技术栈落点**：Go 里的函数值或小接口，TypeScript 里的函数映射，Python 里的 callable。选择规则应当是明确的，而不是藏在一长串 `if` 与隐式默认值里。

**AI 常见反例**：为两种计价方式准备 `IPricingStrategy`、`AbstractPricingStrategy`、`MonthlyPricingStrategy`、`AnnualPricingStrategy` 和 `PricingStrategyFactory`。调用处仍然写死了套餐名，只是多绕了一圈类型。若当前其实只有一种算法，这些类型就是单纯的膨胀。

**轻量实现**：用函数表表达可替换的算法，未知规则明确失败。

```go
type priceFunc func(qty int) (int64, error)

var priceByPlan = map[string]priceFunc{
    "monthly": priceMonthly,
    "annual":  priceAnnual,
}

func quotePlan(plan string, qty int) (int64, error) {
    fn, ok := priceByPlan[plan]
    if !ok {
        return 0, fmt.Errorf("unknown plan %q", plan)
    }
    return fn(qty)
}
```

**选型边界与验证**：只有一种行为时直接调用。验证每种策略的计算结果，以及选择规则在未知输入上的失败方式。

## Decorator 装饰器

**适用信号**：多个调用点需要一致的日志、计时、追踪等横切处理。

**技术栈落点**：Gin middleware，Go 的 HTTP transport，Python decorator。装饰器应当把原请求的错误和身份原样传播下去，并让执行顺序可见。

**AI 常见反例**：为日志、计时、重试、熔断、鉴权各自生成包装类型，再嵌套成难以阅读的构造表达式。顺序只写在注释里，错误在某一层被吞掉，身份在另一层被替换。表面上“关注点分离”，排障时却找不到请求到底在哪一层改变了含义。

**轻量实现**：一个只做访问日志的 Gin middleware，明确放在链中的位置。

```go
func withAccessLog(next gin.HandlerFunc) gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        next(c)
        log.Info("http",
            "path", c.FullPath(),
            "status", c.Writer.Status(),
            "ms", time.Since(start).Milliseconds(),
        )
    }
}
```

**选型边界与验证**：只在一处出现的逻辑，直接写在处理函数里。验证装饰顺序、错误是否继续传播，以及身份不会在包装层被悄悄改写。

## Chain of Responsibility 责任链

**适用信号**：处理步骤按顺序检查，并且可能在中途终止请求。

**技术栈落点**：Gin 的鉴权 middleware 链，CLI 的输入校验链。顺序必须显式。验证的关键是：被拒绝之后，后续步骤不再执行。

**AI 常见反例**：实现一套可动态注册、可运行时排序的“通用责任链框架”，再为每个检查写 `Handler` 基类。实际顺序写在配置文件的远处，测试只能打到整条链的最终状态，无法证明中间某一步截断了请求。

**轻量实现**：用路由分组把顺序写在明处。

```go
func NewRouter(s *Server) *gin.Engine {
    r := gin.New()
    r.Use(withAccessLog)

    billing := r.Group("/v1")
    billing.Use(
        parseIdentity,
        requireScope("billing:write"),
        rateLimit,
    )
    billing.POST("/subscriptions", s.startSubscription)
    return r
}
```

**选型边界与验证**：只有一步检查时，不必叫责任链。测试要分别覆盖身份失败、权限失败和超额，并断言用例函数在这些情况下一次都不会被调用。

## Template Method 模板方法

**适用信号**：总体顺序固定，只有少数步骤存在明确的变化点。

**技术栈落点**：GitHub Actions 的 reusable workflow，或 Go / Python 函数接收步骤函数。调用方只应注入那些被允许变化的步骤，公共顺序由模板自己测试。

**AI 常见反例**：用很深的基类继承来表达“先检查再执行”，子类要覆盖一打钩子才能把一件事做完。或者把本已固定的顺序拆成到处可插拔的回调，结果每个调用方都可以把交付顺序改乱。

**轻量实现**：固定的交付顺序放进可复用工作流，环境作为唯一变化点。

```yaml
# .github/workflows/reusable-deliver.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
jobs:
  lint:
    uses: ./.github/workflows/lint.yml
  test:
    needs: lint
    uses: ./.github/workflows/test.yml
  deliver:
    needs: test
    uses: ./.github/workflows/deliver.yml
    with:
      environment: ${{ inputs.environment }}
```

若变化点在进程内，用函数参数同样清楚：

```go
func runDelivery(ctx context.Context, steps Steps) error {
    if err := steps.Lint(ctx); err != nil {
        return err
    }
    if err := steps.Test(ctx); err != nil {
        return err
    }
    return steps.Deliver(ctx)
}
```

**选型边界与验证**：每个调用点的顺序都不同时，这不是模板方法。验证公共顺序不会被调用方打乱，以及变化点之外的步骤保持一致。

## Command 命令

**适用信号**：同一种操作会由 HTTP、CLI 或任务入口触发，或需要进入队列后再执行。

**技术栈落点**：Gin 与 CLI 共用同一个业务用例，Python 的子命令作为另一入口。每个入口都要说清授权、幂等范围和返回结果，而不能假定“从网页进来才算正式请求”。

**AI 常见反例**：为 HTTP、CLI 和定时任务各写一套几乎相同的业务步骤，或引入庞大的命令总线、中间件和处理器注册表，却把真正的规则又复制了三份。表面是 Command，实际是三处逻辑。

**轻量实现**：操作本身成为用例方法，入口只负责翻译。

```go
type StartInput struct {
    AccountID string
    Plan      string
    RequestID string // 入口各自提供，用于幂等
}

func (u *Subscription) Start(
    ctx context.Context, in StartInput,
) (*Sub, error) {
    if err := u.authorizeStart(ctx, in); err != nil {
        return nil, err
    }
    return u.commitStart(ctx, in)
}
```

CLI 与 HTTP 都构造 `StartInput` 再调用 `Start`。需要排队时，入队的也是同一份输入，而不是另一种业务含义。

**选型边界与验证**：只有一个入口时，不必先抽 Command 类型。验证各入口的授权是否一致，重复的 `RequestID` 是否只生效一次，以及返回结果对调用方是否稳定。

## State 状态

**适用信号**：允许的动作由当前状态决定，并且转换必须受控。

**技术栈落点**：订阅、工单、交付阶段。Go 里用显式的状态转换表，配合 PostgreSQL 的条件更新。简单状态用枚举和函数即可，不必上完整的状态机框架。

**AI 常见反例**：把状态做成类层次，每个状态一个类型，转换靠多态“自己把自己换成下一个”。并发下会出现两次付款确认都以为自己成功，或已取消的订阅被静默改回 active。状态写在内存里，数据库只是最后被覆盖的缓存。

**轻量实现**：允许的转换写在表里，持久化用条件更新守住。

```go
var allowed = map[string]map[string]bool{
    "pending":  {"active": true, "canceled": true},
    "active":   {"past_due": true, "canceled": true},
    "past_due": {"active": true, "canceled": true},
}

func (u *Subscription) Transition(
    ctx context.Context, id, from, to string,
) error {
    if !allowed[from][to] {
        return fmt.Errorf("illegal transition %s -> %s", from, to)
    }
    tag, err := u.store.Exec(ctx, `
        UPDATE subscriptions
           SET status = $1, updated_at = now()
         WHERE id = $2 AND status = $3`,
        to, id, from)
    if err != nil {
        return err
    }
    if tag.RowsAffected() == 0 {
        return errConflict("subscription status changed")
    }
    return nil
}
```

**选型边界与验证**：若动作与状态无关，直接执行即可。必须验证非法转换被拒绝、重复提交不会双写，以及并发下只有一次条件更新成功。

## Observer 观察者

**适用信号**：一个变化需要通知多个相互独立的接收者。

**技术栈落点**：界面订阅、进程内事件、异步消费者。必须明确四件事：通知是同步还是异步，有没有顺序，失败如何传播，订阅如何清理。跨进程的通知需要独立的交付语义，不能假装进程内观察者已经把消息送出去了。

**AI 常见反例**：引入全局事件总线，所有模块靠字符串事件名松耦合，结果依赖关系被藏进发布订阅表。同步监听里做远程调用，一次失败让整个请求回滚到一半；或者只发布、不清理，测试和请求结束后仍有监听在跑。

**轻量实现**：进程内的同步通知，失败立即返回。

```go
type Listener func(ctx context.Context, ev Event) error

func (b *Bus) Publish(ctx context.Context, ev Event) error {
    for _, fn := range b.listeners[ev.Name] {
        if err := fn(ctx, ev); err != nil {
            return err // 同步：失败立即传播
        }
    }
    return nil
}
```

若接收者在另一个进程里，应改用后文的 Outbox，而不是把 `Publish` 直接写成跨网络调用。

**选型边界与验证**：只有一个后续动作时，直接调用即可。验证监听顺序、失败是否按约定传播或隔离，以及取消订阅后不再被通知。

## Iterator 迭代器

**适用信号**：数据量大或需要分批获取，调用方必须逐条处理。

**技术栈落点**：Python 生成器，Go 的逐行读取，TypeScript 的异步迭代。小集合直接 `for range` 或数组循环即可。重点是提前退出、资源释放和分页边界。

**AI 常见反例**：先把全部行读进切片再返回，或实现一套可组合的迭代器框架来处理几百行配置。游标不关闭，取消上下文后仍继续翻页，分页令牌错误时静默跳过最后一页。

**轻量实现**：逐行扫描，允许回调提前返回，并用 `defer` 释放游标。

```go
func forEachInvoice(
    ctx context.Context, q Querier, fn func(Invoice) error,
) error {
    rows, err := q.Query(ctx,
        `SELECT id, amount, status FROM invoices ORDER BY id`)
    if err != nil {
        return err
    }
    defer rows.Close()
    for rows.Next() {
        var inv Invoice
        if err := rows.Scan(&inv.ID, &inv.Amount, &inv.Status); err != nil {
            return err
        }
        if err := fn(inv); err != nil {
            return err // 允许提前退出
        }
    }
    return rows.Err()
}
```

**选型边界与验证**：小集合不必上迭代器协议。验证中途退出时连接被释放，上下文取消能停止翻页，以及最后一页不会丢失。

# 第 6 章 数据一致性与可靠事件

前几章处理的是形状、入口和动作。这一章处理的是提交以后还必须成立的事实：读到的数据含义稳定，多步写入要么一起成功，跨系统的通知不能在进程崩溃后失踪。

<!-- diagram:diagram-tx-outbox -->

## Repository 仓储

**适用信号**：同一份业务数据访问契约被多个用例依赖，或查询细节需要被隔离。

**技术栈落点**：Go 里现有的 store 或 repository，具体实现用 pgx 或 GORM。仓储应当表达业务能问出的问题，例如“某个账户当前有效的订阅”，而不是对每张表提供一套通用的增删改查。

**AI 常见反例**：按表生成 `GenericCRUDRepository[T]`，再让用例去拼条件。查询意图消失了，所有“特殊查询”最后都漏到处理函数里写原始 SQL，仓储层变成了空转。也常见把事务、缓存和领域规则一股脑塞进仓储，使它既不像数据访问，也不像用例。

**轻量实现**：接口按用例需要的问题来命名，实现里写真实的 PostgreSQL 查询。

```go
type SubscriptionStore interface {
    GetByID(ctx context.Context, id string) (*Sub, error)
    GetActiveByAccount(ctx context.Context, accountID string) (*Sub, error)
    Insert(ctx context.Context, tx pgx.Tx, sub *Sub) error
    UpdateStatus(ctx context.Context, tx pgx.Tx, id, from, to string) error
}
```

**选型边界与验证**：只有一个用例、查询也很直接时，不必先抽仓储接口。验证必须对着真实的 PostgreSQL 查询，覆盖命中、未命中、唯一约束冲突，而不是只测内存替身。

## Unit of Work 工作单元

**适用信号**：一个用例中的多步写入必须共同成功。

**技术栈落点**：Go 用例内的显式 PostgreSQL 事务。参与这次用例的所有写入共享同一个事务句柄。不要用隐式的全局会话去“自动完成”这件事，否则回滚范围会变得难以解释。

**AI 常见反例**：引入沉重的工作单元框架，仓储自己开事务，用例再开一层，结果一次请求里套了多个提交点。或者在事务里发起远程调用，把外部系统的延迟和失败带进数据库锁。还有一种更隐蔽的写法：看起来调用了 `Commit`，却在错误路径上忘记 `Rollback`。

**轻量实现**：用例函数里显式开启、回滚和提交。

```go
func (u *Subscription) Start(
    ctx context.Context, in StartInput,
) (*Sub, error) {
    tx, err := u.pool.Begin(ctx)
    if err != nil {
        return nil, err
    }
    defer tx.Rollback(ctx)

    sub := newPending(in)
    if err := u.store.Insert(ctx, tx, sub); err != nil {
        return nil, err
    }
    if err := u.store.InsertEvent(ctx, tx, startedEvent(in)); err != nil {
        return nil, err
    }
    if err := tx.Commit(ctx); err != nil {
        return nil, err
    }
    return sub, nil
}
```

**选型边界与验证**：只有一步写入时，单条语句即可。验证成功路径只提交一次，任何一步失败都回滚，重复调用不会留下部分成功的数据。

## Transactional Outbox 事务性发件箱

**适用信号**：数据提交之后，必须可靠地产生跨系统事件。

**技术栈落点**：在 PostgreSQL 的同一事务里写入业务记录和 outbox 行，再由 Worker 投递。接收方按事件标识幂等。还要处理重投、积压和观测。如果同步调用已经能满足可靠性，就保持直接调用。

**AI 常见反例**：在事务提交后直接调用外部 HTTP，默认“发请求失败就回滚”——可是对方可能已经收到。或者上了消息队列，却没有稳定的事件标识，重试造成重复开通。还有一种是为每个内部函数调用都配 Outbox，把本地就能完成的步骤做成分布式问题。

**轻量实现**：同事务写入，Worker 扫描未投递事件，接收方以 `event_id` 去重。

```sql
CREATE TABLE outbox_events (
    event_id     uuid PRIMARY KEY,
    topic        text NOT NULL,
    payload      jsonb NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now(),
    published_at timestamptz
);
```

```go
func (w *OutboxWorker) Tick(ctx context.Context) error {
    ev, err := w.claimNext(ctx)
    if err != nil || ev == nil {
        return err
    }
    if err := w.publish(ctx, ev); err != nil {
        return err // 保留未标记，等待重投
    }
    return w.markPublished(ctx, ev.EventID)
}
```

**选型边界与验证**：同步流程足够时，不要上 Outbox。上了之后，必须验证：业务行回滚时事件不会被投递；重复投递时接收方只处理一次；积压可以被观测到。

# 第 7 章 三个真实工程选型现场

模式不是用来填满架构图的。下面三个现场都来自真实的工程选择：先看变化点，再决定用哪一种形状，以及明确不用哪一种。

## Portal、Gin 和 PostgreSQL 共同实现订阅

这是贯穿全书的主现场。三个角色的职责要先划清：

- Portal 负责交互和结果呈现。页面收集套餐和确认动作，BFF 作为 Proxy 转发，把成功、校验失败和冲突翻译成用户能理解的结果。资格规则不放在页面里。
- Gin 用例维护资格规则和写入边界。`qualifyPlan`、`quotePlan`、`Start`、`Transition` 都在这一侧。入口是 Facade，鉴权是责任链，计价若有多种套餐再落为 Strategy。
- PostgreSQL 通过约束保护可表达的持久化不变量，例如同一账户在同一时间只能有一份有效订阅。状态转换用条件更新守卫。多步原子写入采用显式事务。只有需要可靠发送外部事件时，才在同一事务里写入 Outbox。

一次开通的路径可以写成这样：Portal 确认支付并展示结果；Gin 先做资格判断，再开启事务，写入订阅行和可选的 outbox 事件，然后提交；Worker 投递事件，下游按 `event_id` 幂等处理。任一步业务写入失败，事件都不会单独逃出去。

这里没有把十八个模式全用上。没有树形结构，就不用 Composite；没有大批量逐条处理，就不用 Iterator；没有多种存储驱动，就不用 Factory。该用的那些，也尽量落在函数、middleware、事务和 SQL 上，而不是落在以模式命名的类型树上。

## GitHub Actions 与跨入口渲染

持续交付里最常见的诱惑，是把一段“看起来差不多”的步骤复制到每一个仓库、每一个作业。更好的问法是：重复的到底是顺序，是步骤，还是渲染逻辑？

- 多个作业共享固定的交付顺序时，先检查 reusable workflow。这就是 Template Method：公共顺序不变，调用方只传入环境或产物名这类被允许的变化点。
- 单作业内共享一组步骤时，先检查 composite action。不必为此再写一个工作流引擎。
- 多种入口要复用同一段渲染逻辑时，把它放进由所属仓维护的 Python 或 Shell CLI。CI、本地命令和必要的服务入口都调用它，这是 Command 的现场：同一操作，多个入口，授权和结果在同一实现里定义。

不要把渲染逻辑复制进 workflow 的 YAML 长篇里，也不要为了“统一抽象”先做一套通用流水线框架。先找到被复用的那一段，再选择最小的落点。

<!-- diagram:diagram-iac-ci-reuse -->

## HCL 模块与 Playbook Role

基础设施和配置管理更习惯声明，而不是对象模型。HCL 模块和 Playbook Role 应当优先用声明、参数和资源引用去组合想要的结构。扩展时先复用既有模块或 Role，而不是在环境目录里重写一份资源。

只有两类变化出现时，才值得增加一层：Provider 的接口确实不同，需要 Adapter 把外部形状收进来；或者某段策略确实会按确定规则切换，才抽出 Strategy。如果当前只有一种云资源和一种安置方式，直接写出模块调用即可。

在我们遵循的 HCL 约定里，可批量编排的环境保持扁平显式块，不在环境的 `.tf` 中使用会让键漂移的控制结构。循环和条件放在生成器一侧，使 HCL 可审计、diff 友好。这本身就是在拒绝一种常见的过度设计：把所有变化都藏进模板里，最后谁也读不清真实要创建什么。

# 第 8 章 命名、轻量扩展与验证

模式选对了，名字用错了，代码还是会重新长成屎山。下面几条是与模式选择配套的书写原则。

第一，名称表达业务含义，不表达设计模式身份。用 `load_cmdb`、`build_inventory`、`startSubscription` 这样能对上用例的名字，不要用 `XxxManagerFacade`。

第二，文件名、函数名、类型名、YAML 键和 HCL 资源名应能互相指认。一个名字只代表一种东西。

第三，写清楚，而不是写得短。避免把多层判断、隐式转换和副作用压进一行，或使用所在文件里并不常见的冷僻语法。AI 很喜欢把逻辑压缩成“巧妙”的一行，评审时要把它展开。

第四，先在现有模块、Role、脚本或函数上做最小扩展。只有出现真实的复用、替换或所有权边界时再拆层，不为“以后可能用到”预建框架。

第五，同一目录不要混入第三种文件名风格。历史仓库里同时存在不同风格时，新文件跟随最近邻文件。不要借一次重构把目录全部改名。

第六，公共 API、CLI 参数、退出码和配置键保持稳定；内部命名可在本目录惯例内整理。

这些原则落到各技术栈，会有更具体的形状。TypeScript 里组件文件用 PascalCase，函数用 camelCase，业务功能放在既有模块附近，不平行再造一套目录。Go 里包名短小全小写，文件名用 snake_case，Handler 负责绑定和映射，业务规则放在用例，持久化放在 store，接口只为真实替换或测试隔离而设。Python 与 Shell 里，结构化决策放进可测试的 Python 函数，Shell 只串联命令；YAML 描述结构，不把循环藏进难以阅读的模板。HCL 的资源名保持稳定，环境目录保持显式。

验证时问三个问题就够用。不熟悉这段代码的人，能否只靠名字找到入口和结果？新文件是否跟随了最近邻的命名，而不是借机改写整个目录？本次变更是否只在现有边界里增加了最小的一块，而不是多了一层抽象？

# 尾声 让 AI 写得快，但不让它写飞

AI 会继续加快代码的生产。它能在一次对话里交出整份目录、整组接口和整套测试替身。如果评审只看“齐不齐”，这些结果很容易被当成高质量。真正要看的是另一面：变化点有没有被说清楚，一致性有没有被守住，每一层抽象是不是付得起代价。

设计模式在这个时代的意义，不是给生成结果再盖一层教材封皮。它是一套共用的判断语言。当有人写出 `GenericCRUDRepository`，你可以指出：这里没有被多个用例共享的数据契约，查询意图被抹掉了。当有人把资格规则放进 Portal 页面，你可以指出：规则的变化点在 Gin 用例，页面只负责呈现。当有人在提交后直接通知外部系统，你可以指出：若必须可靠投递，应在同一事务里写下 Outbox。

工具会更快，规则会更多。只要还要把软件写到可修改、可验证，先找变化点、再落回原语，就仍然是最体面的写法。AI 可以带飞速度，但不能代替你决定哪里该留一层，哪里不该留。

# 附录 十八个模式速查

| 模式 | 所在章节 | 变化点 | 一句判断 |
| --- | --- | --- | --- |
| Strategy 策略 | 第 5 章 | 请求链与行为 | 多种算法、规则明确时再抽；一种行为直接调用。 |
| Adapter 适配器 | 第 3 章 | 入口与协议 | 只转换外部形状，不把业务规则藏进映射。 |
| Facade 外观 | 第 3 章 | 入口与协议 | 以业务动词提供入口，保留可定位的失败原因。 |
| Factory 工厂 | 第 4 章 | 构造与组合 | 构造确有分叉再用；无效配置必须当时失败。 |
| Builder 构建器 | 第 4 章 | 构造与组合 | 有组合约束才用；普通参数对象直接传入。 |
| Decorator 装饰器 | 第 5 章 | 请求链与行为 | 横切处理要顺序可见，错误和身份原样传播。 |
| Chain of Responsibility 责任链 | 第 5 章 | 请求链与行为 | 顺序显式；拒绝后后续步骤必须停止。 |
| Template Method 模板方法 | 第 5 章 | 请求链与行为 | 公共顺序固定，调用方只注入允许的变化点。 |
| Command 命令 | 第 5 章 | 请求链与行为 | 多个入口共享同一操作，授权与幂等要一致。 |
| State 状态 | 第 5 章 | 请求链与行为 | 允许的转换写明，用条件更新守卫并发。 |
| Observer 观察者 | 第 5 章 | 请求链与行为 | 先约定同步性、顺序、失败和清理；跨进程另谈交付。 |
| Composite 组合 | 第 4 章 | 构造与组合 | 叶与组需要相同递归时再用；平面列表直接遍历。 |
| Proxy 代理 | 第 3 章 | 入口与协议 | 透明转发，集中处理访问控制、超时和缓存身份。 |
| Iterator 迭代器 | 第 5 章 | 请求链与行为 | 大数据逐条处理；注意提前退出、释放和分页。 |
| Repository 仓储 | 第 6 章 | 数据一致性 | 按业务问题隔离查询，避免按表生成通用 CRUD。 |
| Unit of Work 工作单元 | 第 6 章 | 数据一致性 | 多步写入共享同一事务句柄，同生同灭。 |
| Transactional Outbox 事务性发件箱 | 第 6 章 | 数据一致性 | 同事务写事件，Worker 投递，接收方按标识幂等。 |
| Ports and Adapters 端口与适配器 | 第 3 章 | 入口与协议 | 先确定真实依赖边界，再引入端口。 |

# 许可

本书正文采用知识共享署名-相同方式共享 4.0 国际许可协议（[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)）发布。署名：Haitao Pan · XWork Technologies LLC 服务支持。

书中的构建脚本与示例代码采用 MIT 许可。示例只用于说明实现形状，不是可直接上线的完整服务。

版本：v0.1 ｜ 2026-11-13
