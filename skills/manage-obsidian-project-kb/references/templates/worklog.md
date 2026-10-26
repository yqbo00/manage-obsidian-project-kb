# Worklog templates

用于日报事件和持久报表；通用规则见 `references/markdown-templates.md`。新建 Worklog Index 时才另读初始化模板包。

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
