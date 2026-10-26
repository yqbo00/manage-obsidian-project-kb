# Initialization templates

仅创建/诊断项目 Dashboard、Sprint、Shared Index、Worklog Index 时读取。通用规则见 `references/markdown-templates.md`。

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

## Rule Catalog

<!-- kb:rule-catalog:start -->
| Source | Status | Applies to | Enforcement | Load | Triggers |
|---|---|---|---|---|---|
<!-- kb:rule-catalog:end -->

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

## Rule Catalog

<!-- kb:rule-catalog:start -->
| Source | Status | Applies to | Enforcement | Load | Triggers |
|---|---|---|---|---|---|
<!-- kb:rule-catalog:end -->

## Governance & Rules
## Domain & Contracts
## Architecture & Patterns
## Engineering & Standards
## Infra & Platforms
## Troubleshooting & Lessons
## AI & Automation
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
