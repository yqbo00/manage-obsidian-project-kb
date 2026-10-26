# Rule templates

用于规则笔记与 Catalog 写入；通用规则见 `references/markdown-templates.md`。创建空索引使用 `references/templates/initialization.md`，已有索引只局部更新，不为目录维护重新加载初始化流程。

## Rule note

项目规则使用项目 Dashboard 与 `project: "{Project_Name}"`；共享规则使用 `project: "Shared"`、`scope: Shared` 并链接 Shared Index。以下 load/强度/范围必须依据实际需求填写，不能照抄选项串；Always 时省略 triggers。旧 Mandatory 兼容策略见 `references/rule-loading.md`。

```markdown
---
title: "{规则标题}"
date: {YYYY-MM-DD}
project: "{Project_Name 或 Shared}"
category: "{实际主题目录名}"
tags: ["{适用领域}"]
status: {Active | Draft | Deprecated}
aliases: []
kind: Rule
applies_to: ["{已确认的项目范围}"]
enforcement: {Mandatory | Default | Advisory}
load: {Always | Conditional}
triggers:
  - "{一条完整适用条件；多个条目为 OR，条目内的 AND 明确写出}"
---

# {规则标题}

> Index: [[{实际项目或共享索引路径}]]

## Applicability

{适用操作、模块、路径或环境，与 Frontmatter triggers 一致；说明不适用情形。}

## Required Behavior

{具体、可执行的要求。}

## Verification

{检查方法、验收证据、已有技术控制及未验证项。}

## Exceptions

{允许例外的条件与批准依据；没有已批准例外时明确说明。}

## Evidence

{用户确认、实际问题、已有规则来源或其他可核查依据。}

## Change Log

- {YYYY-MM-DD}: {创建或修改的范围、依据和验证结果}
```

## Rule Catalog

`references/templates/initialization.md` 中 Project Dashboard 和 Shared Index 模板的 `kb:rule-catalog` 区块是目录格式；每个目标文件只保留一组标记。已存在的 Index 只在授权规则维护时局部补齐该区块，保留其他内容。

每行使用实际来源的 Vault 相对 Wikilink，不复制行为正文：

```markdown
| [[{来源路径}]] | Active | {项目范围} | Mandatory | Conditional | {完整条件摘要} |
```

行按来源路径去重。旧 Mandatory 缺少 load 时显示 `Legacy/Always`；Always 的 Triggers 写 `—`。多条件保留 OR/AND 语义；转义表格中的竖线。Catalog 是派生摘要，读取时核对来源元数据，保存时同步，不能只改表格来改变规则。
