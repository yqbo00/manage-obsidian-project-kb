# Worklog writes and recovery

仅有实际成果需自动落账、用户要求 `/kb-log` 或有证据需补录时读取；写前加载 `references/write-safety.md`。创建事件/日报时按 `references/markdown-templates.md` 加载 Worklog 模板，不加载初始化与笔记模板。

## Cross-Project Worklog

Worklog 是 Vault 级、按日期组织的追加式成果账本。自动记录已验证的功能、修复、重构、架构/调研产物、测试、部署、知识变化、任务进展以及新发现或解除的 Blocker；不记录文件浏览、搜索、普通命令、无结论讨论、原始日志和重复的过程噪音。只读问答和未产生持久成果的状态查询不得写入。

### Automatic Worklog

1. 在最终回复前，从实际变更、测试/运行结果、Sprint 变化、知识笔记和用户确认中提炼本次 `Completed | In Progress | Blocked` 结果；不要推断工时、工作量或生产率。
2. 使用宿主本地日期和带时区的当前时间。按 `日期 + Project_Name + Task_ID（缺失时用 no-task）+ 主要证据路径或结果 slug` 生成安全、稳定的 Event ID；写入前按 ID 及“项目、任务、结果、证据”元组查重。相同事件不重复写；同一任务的新进展使用新结果 ID；碰撞时追加数字后缀。
3. 获得 Worklog 锁后，只创建缺失的年月目录和当天文件；在 `## By Project` 的当前项目区追加完整事件。不得修改历史事件正文；更正时追加带 `Corrects` 的新事件。
4. 从全部事件块重新计算受管理的 Daily Summary，只在 Worklog Index 缺少当天链接时添加一次。事件正文只保留结果、验证、知识链接、下一步和来源，不复制知识笔记内容。
5. 读回 Event ID、Daily Summary 和 Index 链接后释放锁。若 Vault、权限或锁阻止写入，项目工作仍可报告完成，但必须明确标记 `Worklog: Pending`；不得写入未约定的替代位置或声称已记录。

### Recovery and boundaries

- 下次启动时只用当天 Current Sprint 完成项、Dashboard 最近完成项及其直接链接笔记的 Change Log 检测当前项目漏记；不要无界扫描知识树。只有日期、结果和证据均明确时才能补录，并标记 `Origin: Reconstructed`。无法确定时报告而不猜测。
- Agent 被强制终止时无法保证执行最终同步；`/kb-log --reconcile` 用于显式恢复。Agent 未观察到的会议、手工发布或线下工作只能依据用户说明通过 `/kb-log` 补录，并标记 `Origin: Manual`。
- Worklog 工作进度与知识状态相互独立：`Completed/In Progress/Blocked` 不改变 `Active/Draft/Deprecated`，只投影关联笔记的真实状态。

### `/kb-log [说明]` or `/kb-log --reconcile [YYYY-MM-DD]`

- 普通形式用于补录 Agent 未观察到的外部工作；根据用户说明和可用证据生成 `Origin: Manual` 事件，不把未确认内容写成已验证事实。
- `--reconcile` 仅检查当前项目在指定日期（默认今天）的 Sprint 完成项、Dashboard 最近完成项及其直接链接笔记的 Change Log；只补录结果与证据均明确且 Worklog 未命中的事件，标记 `Origin: Reconstructed`，并报告无法恢复的空白。
- 两种形式都复用 Automatic Worklog 的锁、去重、摘要、Index 和读回规则；能够推断时不要求用户填写模板字段。
