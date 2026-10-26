# Progress and completion

有意义的开发成果、进展或阻塞在最终回复前自动触发本流程；读取 `references/write-safety.md` 和 `references/worklog-write.md` 后再写入。仅需要保存永久知识时再读取 `references/knowledge-write.md`；不因结束回复而勾选任务。

### Task syntax and transitions

严格使用以下任务语法：

```markdown
- [ ] KB-101 尚未开始的任务
- [/] KB-102 正在进行的任务
- [x] 2026-08-03 KB-103 已完成的任务
```

规则：

- 给任务分配稳定、项目内唯一的 ID；更新时通过 ID 精确匹配，避免同名误改。
- 允许的正常流转为 `[ ]` → `[/]` → `[x] {YYYY-MM-DD}`。修正错误状态时追加 Change Log 说明。
- 只有代码、测试、构建结果、可观察行为或用户明确确认能证明完成时，才能标为 `[x]`。
- 部分完成保持 `[/]`，并补充剩余工作；被阻塞的任务保持原状态，同时写入 Blockers。
- 不得因为 Agent 结束响应、生成了方案或只修改了文档就把实现任务标为完成。

### Completion synchronization

完成核心重构、功能、Bug 修复或其他有意义的项目工作后，在最终回复前自动执行，不要求用户输入 `/kb-save` 或 `/kb-log`：

把以下步骤视为一次幂等的完成事务；每个子步骤最多执行一次，`/kb-save` 和 Automatic Worklog 不得递归重新触发整个 Completion synchronization。

1. 在 `Current_Sprint.md` 中按任务 ID 将对应项改为 `- [x] {YYYY-MM-DD}`，保留任务描述并添加验证或知识笔记 Wikilink。
2. 更新 `00-Index.md` 的当前 Milestone、Active Tasks、最近完成项和 Blockers 摘要。
3. 有长期复用价值时执行 `/kb-save`，把永久知识写入 `10–60` 对应目录。
4. 按 Automatic Worklog 规则把本次实际成果、进展或 Blocker 写入当天 Daily Worklog，并同步 Worklog Index 和受管理的 Daily Summary。
5. 读回所有目标并核对状态。任一更新失败时报告项目任务结果与知识库同步的部分完成状态，不得隐瞒 Worklog 漏记。

若当前 Sprint 中没有可唯一匹配的任务，不自动勾选相似任务；报告结果并请求用户指定任务 ID，或在用户意图明确时新增独立任务。
