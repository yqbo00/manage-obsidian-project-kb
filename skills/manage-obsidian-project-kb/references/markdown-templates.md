# Markdown template routing

创建 Markdown 前读取本页，再完整读取需要的模板包；不要一次加载所有模板。已有文件的局部修改若不涉及模板结构，不为形式一致重读或重建模板。

## Template rules

- 替换所有占位符；没有真实别名时使用 `aliases: []`，没有真实关联时删除对应占位行。
- 新永久笔记必须包含 `title`、`date`、`project`、`category`、`tags`、`status`、`aliases` 和 `kind`。共享笔记还必须包含 `scope`、`applies_to`；Rule 必须包含 `enforcement`、`load`，Conditional 必须有非空 `triggers`。旧笔记不批量补字段，按 `references/rule-loading.md` 兼容读取。
- 知识状态只使用 `Active`、`Deprecated`、`Draft`；日期使用当前本地日期 `YYYY-MM-DD`。
- `00-Index.md`、Sprint 和 Worklog 是可变状态文档；`10–60` 的永久笔记必须使用实际目录名作为 `category`。
- Worklog 的 `Completed`、`In Progress`、`Blocked` 是工作进度，不是知识状态。不要推断工时、工作量或生产率。

## Select one or more packs

| 当前操作 | 资源 |
|---|---|
| 初始化 Dashboard、Sprint、Shared/Worklog Index，或检查这些结构 | `references/templates/initialization.md` |
| 普通永久/共享笔记（Contract、ADR、Runbook、Knowledge、Asset） | `references/templates/knowledge.md` |
| Rule 笔记或 Rule Catalog 写入/诊断 | `references/templates/rules.md` |
| Daily Worklog 事件、日报、Saved Worklog report | `references/templates/worklog.md` |

只组合本次真实需要的包。初始化不写规则或日报时，不读取规则、普通笔记、日报模板；写日志不加载整个 Vault 初始化规范。
