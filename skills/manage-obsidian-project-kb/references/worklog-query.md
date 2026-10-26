# Worklog queries

纯日报/报表查询只需已验证的项目配置和目标日期日志，不默认读取 Sprint、项目规则全文、桥接或迁移协议。输出真实来源，缺失日期不是零成果。用户要求写报表时，先加载 `references/rule-loading.md` 核对适用的写入规则，再读取 `references/write-safety.md` 和 `references/worklog-write.md`，按 `references/markdown-templates.md` 选择 Worklog 模板；没有保存请求时全程只读。

### `/kb-today [YYYY-MM-DD]`

默认使用宿主本地今天，以只读方式读取对应 Daily Worklog，按项目汇总 Completed、In Progress、Blocked、知识变化和下一步，并列出来源 Event ID。日期文件缺失表示“无记录”，不得声称“没有工作”；不得扫描所有项目或静默补录。

### `/kb-report [YYYY-MM-DD | week | month | START..END] [--save]`

从 Worklog Daily 文件聚合日期范围；`week` 使用本地当前自然周，`month` 使用本地当前自然月。输出按项目和工作进度分组的结果、Blocker、知识变化与源日期链接；缺失日期明确标为无记录，不以事件数量衡量生产率。默认只读；仅显式 `--save` 时读取 `references/markdown-templates.md` 的 Saved Worklog report 模板，把自然周、自然月和其他范围分别保存到 `Reports/Weekly`、`Reports/Monthly`、`Reports/Custom` 的不覆盖快照并更新 Worklog Index。
