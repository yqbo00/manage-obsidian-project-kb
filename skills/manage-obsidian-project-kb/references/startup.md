# Development startup

用于新的项目开发任务、恢复会话或切换项目；纯 Worklog 汇总按 `references/worklog-query.md`，不触发整套项目启动。

### Sources of truth

- `Current_Sprint.md` 是任务粒度状态的唯一事实源。
- `00-Index.md` 是高频 Dashboard，只投影当前 Milestone、Active Tasks、Blockers 和核心知识入口，不维护第二份完整任务清单。
- `00-Index.md` 必须包含标题完全一致的 `## 🚀 Current Progress & Active Status` 区块。
- `{SharedRoot}/00-Index.md` 是共享规则与跨项目知识的 MOC，不保存任何项目的 Sprint 状态。
- `DailyWorklog` 是“某天实际做了什么”的跨项目派生账本，只保存结果摘要和证据链接；不得反向覆盖 Sprint 或永久笔记中的权威状态。
- Dashboard 与 Sprint 不一致时，以 `Current_Sprint.md` 为准，并在获得写权限后同步修复 Dashboard 摘要。

### Startup alignment

处理任何项目开发任务前：

1. 读取并验证配置。
2. 读取 `references/rule-loading.md`，按协议读取 Shared Index 与项目 Rule Catalog，核对候选元数据，加载适用的 Active 常驻规则、任务命中的条件规则及缺少加载条件的旧 Mandatory。筛选同时考虑项目、模块路径、任务与计划操作；普通知识按需检索。
3. 读取项目 `00-Index.md` 的进度区、配置指定的 `Current_Sprint`，以及今日 Daily Worklog 中当前项目的条目；提取目标、Milestone、所有 `- [/]`、Blockers、相关 `- [ ]` 和今日已记录成果。
4. 对照今天已完成的 Sprint 条目、Dashboard 最近完成项及其直接链接的永久笔记 Change Log 与 Worklog Event ID，识别上次会话可能漏记的确定性成果；不要无界扫描项目知识树。只读任务仅报告待补录项；获得项目写入授权的开发任务在发现确定漏项时读取 `references/worklog-write.md`，按 `/kb-log --reconcile` 补录；未发现漏项不加载写日志流程。
5. 向当前对话注入精炼状态：当前目标、进行中任务、阻塞项、今日成果和相关知识链接。
6. 任务涉及领域规则、架构、工程机制、基础设施、历史故障或自动化时，从任务提取 2–6 个关键词，读取 `references/retrieval.md` 并隐式执行 `/kb-read`。
7. 若文件缺失或互相冲突，明确报告；不得凭空推断进度或工作记录。

在上述配置与适用规则核对后、业务修改前，按 `references/migration-check.md` 检查当前安装的本机自动迁移授权。已启用时自动对账当前已初始化项目的桥接和规则；不联网、不重装全局包、不访问其他项目。只读任务只报告待迁移项，无变化零写入。不得把普通任务授权当作启用跨项目自动迁移的授权。

执行设计或修改前简要说明会影响本次工作的规则及来源、例外或未解决条件，不逐轮重复整份规则清单。由查询转向修改、构建、部署、迁移或其他新范围时，在行动前补读新命中的规则。
