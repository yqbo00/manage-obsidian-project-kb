# Markdown Templates

## Contents

- [Template rules](#template-rules)
- [Project Dashboard](#project-dashboard)
- [Current Sprint](#current-sprint)
- [Permanent atomic note](#permanent-atomic-note)
- [Shared index](#shared-index)
- [Shared atomic note](#shared-atomic-note)
- [Worklog index](#worklog-index)
- [Daily Worklog](#daily-worklog)
- [Saved Worklog report](#saved-worklog-report)

## Template rules

- 替换所有占位符；没有真实别名时使用 `aliases: []`，没有真实关联时删除对应占位行。
- 永久笔记必须包含 `title`、`date`、`project`、`category`、`tags`、`status` 和 `aliases`。共享笔记还必须包含 `scope`、`applies_to` 和 `enforcement`。
- 知识状态只使用 `Active`、`Deprecated`、`Draft`；日期使用当前本地日期 `YYYY-MM-DD`。
- `00-Index.md`、Sprint 和 Worklog 是可变状态文档；`10–60` 的永久笔记必须使用实际目录名作为 `category`。
- Worklog 的 `Completed`、`In Progress`、`Blocked` 是工作进度，不是知识状态。不要推断工时、工作量或生产率。

## Project Dashboard

```markdown
---
title: "{Project_Name} Project Dashboard"
date: {YYYY-MM-DD}
project: "{Project_Name}"
category: "00-Index"
tags: ["project-dashboard", "knowledge-base"]
status: Active
aliases: ["{Project_Name} MOC"]
---

# {Project_Name} Project Dashboard

## 🚀 Current Progress & Active Status

<!-- kb:progress:start -->
- Current Sprint: [[05-Roadmap_&_Tasks/Current_Sprint]]
- Current Milestone: {Milestone}
- Active Tasks:
  - {Task ID and concise status}
- Blockers:
  - {Blocker or None}
- Recently Completed:
  - {YYYY-MM-DD — Task ID — verified outcome}
<!-- kb:progress:end -->

## 🧭 Knowledge Map

### Domain & Business

### Architecture & ADR

### Engineering & Tuning

### Infra & DevOps

### Troubleshooting

### AI & Automation

## 🌐 Shared Knowledge

- [[{Shared_KB}/00-Index|Shared Knowledge Index]]
- {当前项目适用的核心共享规则链接}

## 🗓 Worklog

- [[{Worklog_KB}/00-Index|Cross-Project Worklog]]
```

## Current Sprint

```markdown
---
title: "{Project_Name} Current Sprint"
date: {YYYY-MM-DD}
project: "{Project_Name}"
category: "05-Roadmap_&_Tasks"
tags: ["sprint", "roadmap", "tasks"]
status: Active
aliases: ["Current Sprint"]
---

# Current Sprint — {Sprint_Name}

> Dashboard: [[Projects/{Project_Name}/00-Index|Project Dashboard]]

## Sprint Goal

{可验证的 Sprint 目标}

## Current Milestone

{当前里程碑及完成条件}

## Tasks

- [ ] KB-101 {未开始任务}
- [/] KB-102 {进行中任务}
- [x] {YYYY-MM-DD} KB-103 {已完成任务} — [[{Verification-or-Knowledge-Note}]]

## Blockers

- {Blocker、影响、负责人或解除条件；没有则写 None}

## Change Log

- {YYYY-MM-DD}: {任务或范围变化及原因}
```

## Permanent atomic note

````markdown
---
title: "{精准简要的主题}"
date: {YYYY-MM-DD}
project: "{Project_Name}"
category: "{10-60 的实际目录名}"
tags: ["{技术/框架标签}", "{业务或组件标签}"]
status: {Active | Draft | Deprecated}
aliases: ["{真实别名}"]
---

# {Title}

> Dashboard: [[Projects/{Project_Name}/00-Index|Project Dashboard]]

## Summary

{一段可独立理解的结论}

## Context & Constraints

- {适用场景、版本、边界和约束}

## Decision / Knowledge

{工程事实、决策、机制或可复用方案}

## Evidence & Verification

```{language}
{最小、脱敏、可复现的代码、配置、命令或证据}
```

## Consequences & Risks

- {收益、代价、兼容性或回归风险}

## Related

- [[{真实存在的相关文档}]] — {关系}

## Change Log

- {YYYY-MM-DD}: {创建或状态变化、证据与原因}
````

## Shared index

```markdown
---
title: "Shared Knowledge Index"
date: {YYYY-MM-DD}
project: "Shared"
category: "00-Index"
tags: ["shared", "knowledge-base"]
status: Active
aliases: ["Shared MOC"]
scope: Shared
---

# Shared Knowledge Index

## Governance & Rules
## Domain & Contracts
## Architecture & Patterns
## Engineering & Standards
## Infra & Platforms
## Troubleshooting & Lessons
## AI & Automation
```

## Shared atomic note

共享笔记复用 Permanent atomic note 正文，把 Dashboard 链接改为 `[[{Shared_KB}/00-Index|Shared Knowledge Index]]`，并使用：

```yaml
---
title: "{Title}"
date: {YYYY-MM-DD}
project: "Shared"
category: "{Shared 中的实际目录名}"
tags: ["{共享标签}"]
status: {Active | Draft | Deprecated}
aliases: []
scope: Shared
applies_to: ["*"]
enforcement: {Mandatory | Default | Advisory}
---
```

## Worklog index

```markdown
---
title: "Cross-Project Worklog"
date: {YYYY-MM-DD}
project: "Cross-Project"
category: "Worklog"
tags: ["worklog", "index"]
status: Active
aliases: ["Worklog MOC"]
scope: Vault
---

# Cross-Project Worklog

## Recent Daily Logs

## Saved Reports
```

## Daily Worklog

```markdown
---
title: "Daily Worklog — {YYYY-MM-DD}"
date: {YYYY-MM-DD}
project: "Cross-Project"
category: "Worklog"
tags: ["worklog", "daily"]
status: Active
aliases: []
scope: Vault
---

# Daily Worklog — {YYYY-MM-DD}

> Index: [[{Worklog_KB}/00-Index|Cross-Project Worklog]]

## Summary

<!-- kb:daily-summary:start -->
- Projects: 0
- Completed Outcomes: 0
- In Progress: 0
- Blockers: 0
<!-- kb:daily-summary:end -->

## By Project

### {Project_Name}

<!-- kb:worklog:event:start id="{Event_ID}" -->
#### {HH:mm} · {Completed | In Progress | Blocked} · {Outcome_Title}

- Timestamp: {RFC3339 timestamp with UTC offset}
- Task: {Task_ID or None}
- Outcome: {可独立理解的实际结果或进展}
- Verification: {测试、运行结果、配置核对、用户确认或未验证项}
- Knowledge: [[{真实存在的知识笔记}]]
- Knowledge Status: {Active | Draft | Deprecated | None}
- Next: {下一步或 None}
- Origin: {Automatic | Manual | Reconstructed}
<!-- kb:worklog:event:end -->
```

如果没有知识链接，删除 `Knowledge` 行并保留 `Knowledge Status: None`。更正历史记录时追加一个新事件并写 `Corrects: {Event_ID}`，不要修改旧事件正文。

## Saved Worklog report

```markdown
---
title: "Worklog Report — {Range}"
date: {YYYY-MM-DD}
project: "Cross-Project"
category: "Worklog Report"
tags: ["worklog", "report"]
status: Active
aliases: []
scope: Vault
source_range: "{Start_Date}..{End_Date}"
---

# Worklog Report — {Range}

## Summary

- Projects: {count}
- Completed Outcomes: {count}
- In Progress: {count}
- Blockers: {count}

## By Project

### {Project_Name}

#### Completed

- {Outcome} — [[{Worklog_KB}/Daily/{YYYY}/{YYYY-MM}/{YYYY-MM-DD}|{YYYY-MM-DD}]]

#### In Progress

- {Progress and next step}

#### Blockers

- {Blocker and impact}

## Knowledge Changes

- [[{Knowledge_Note}]] — {Active | Draft | Deprecated}

## Source Daily Logs

- [[{Worklog_KB}/Daily/{YYYY}/{YYYY-MM}/{YYYY-MM-DD}|{YYYY-MM-DD}]]
```
