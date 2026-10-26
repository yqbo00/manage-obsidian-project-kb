# Knowledge templates

用于非 Rule 的永久笔记；通用规则见 `references/markdown-templates.md`。

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
kind: {Contract | ADR | Runbook | Knowledge | Asset}
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
kind: {Contract | ADR | Runbook | Knowledge | Asset}
scope: Shared
applies_to: ["{明确项目名；经授权全局适用时才使用 *}"]
---
```

### Type-specific body

`kind` 描述内容性质，`category` 仍描述主题目录。ADR 明确决策、备选与代价；Contract 明确接口/领域约定及兼容性验证，强制行为链接对应 Rule；Runbook 明确前提、步骤、验证与回滚；Asset 链接真实脚本或 Skill 及其适用条件。不要把这些内容都强制套成规则正文。
