# manage-obsidian-project-kb

一个面向 Codex CLI、ZCode、Claude Code 和自定义 AI 编程终端的跨 Agent 项目记忆与 Obsidian 知识库管理 Skill。它通过项目本地配置、声明式 Agent Adapter 桥接和统一 Vault 目录，让不同 Agent 共享项目进度、架构决策、公共规则、排错经验及按日期汇总的工作记录。

## 核心能力

- 在一个 Obsidian Vault 中隔离多个项目，同时维护 Shared 公共知识和跨项目 Worklog。
- 初始化项目配置、目录、Dashboard、Current Sprint，以及 Codex/ZCode/Claude Code/自定义客户端的幂等指令桥接。
- 启动时加载精简常驻规则与当前进度，按任务条件加载共享/项目规则；范围变化时补读新命中的规则。
- 完成有意义的工作后自动同步任务、Dashboard、永久笔记和当天 Worklog。
- 使用 `Active`、`Draft`、`Deprecated` 管理知识有效性，不覆盖或删除历史记录。
- 提供 `/kb-doctor` 检查配置、索引、桥接、锁、Git 忽略状态和有限范围断链。

## 仓库结构

```text
.
├── README.md
├── LICENSE
├── docs/upgrades/rule-loading-v5.md
├── .github/workflows/validate.yml
├── skills/
│   └── manage-obsidian-project-kb/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── assets/{AGENTS-bridge.md,agent-import-bridge.md}
│       └── references/{agent-adapters.md,rule-loading.md,upgrade.md,markdown-templates.md}
├── tests/
└── tools/validate_skill.py
```

`skills/manage-obsidian-project-kb/` 是可分发的完整 Skill 包。安装或导入时必须使用整个目录，不能只复制 `SKILL.md`。

## 安装

### Codex CLI

把完整 Skill 目录复制或软链接到 Codex 当前配置所使用的 Skills 根目录。以下示例使用 `~/.codex/skills`：

```bash
mkdir -p ~/.codex/skills
ln -s /absolute/path/to/this-repository/skills/manage-obsidian-project-kb \
  ~/.codex/skills/manage-obsidian-project-kb
```

重新启动 Codex 会话后，通过 `$manage-obsidian-project-kb` 显式调用。Codex 的 Skill 与项目指令机制说明见 [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) 和 [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。

### ZCode

推荐直接复用 Codex 中的同一个目录：

1. 打开 `Settings → Skills → Import`。
2. 选择 Codex 来源中的 `manage-obsidian-project-kb`。
3. 选择 `Symlink` 和 `Global`，完成后启用并点击 `Refresh`。

也可以把完整目录放到 `~/.zcode/skills/manage-obsidian-project-kb/`。ZCode 支持 `$skill-name` 调用，并能以软链接或复制方式导入 Codex Skill；参见 [ZCode Skill 文档](https://zcode.z.ai/en/docs/skill)。

### Claude Code

把完整 Skill 目录复制或软链接到项目级 `.claude/skills/manage-obsidian-project-kb/`，或用户级 `~/.claude/skills/manage-obsidian-project-kb/`。重新启动会话后可用 `/manage-obsidian-project-kb` 调用；Claude Code 也可依据 Skill description 自动加载。`/kb-init` 为其维护根级 `CLAUDE.md` 中的 `@AGENTS.md` 导入，让公共启动协议只有一个权威副本。参见 [Claude Code Skills](https://code.claude.com/docs/en/slash-commands) 和 [Claude Code Memory](https://code.claude.com/docs/en/memory)。

## 初始化项目

在目标代码仓库根目录启动 Agent，然后执行：

```text
$manage-obsidian-project-kb 请执行 /kb-init
```

Agent 会询问 Obsidian Vault 路径和项目名称，并在项目根目录创建机器本地配置：

```json
{
  "Schema_Version": 2,
  "Vault_Path": "/absolute/path/to/obsidian-vault",
  "Project_Name": "example-project",
  "Current_Sprint": "05-Roadmap_&_Tasks/Current_Sprint.md",
  "Shared_KB": "Shared",
  "Worklog_KB": "Worklog",
  "Agent_Clients": ["codex", "zcode", "claude-code"],
  "Custom_Agent_Bridges": []
}
```

`.ai/obsidian-kb.json` 含本机绝对路径。`/kb-init` 会检查它未被 Git 跟踪，并将其加入仓库本地 exclude；不要提交该文件。

首次初始化会让你确认自动检测到的客户端；检测结果只作为建议。Codex 与 ZCode 共用根级 `AGENTS.md`，Claude Code 通过 `CLAUDE.md` 导入它。自定义客户端可直接读取 `AGENTS.md`、接收标准托管区块，或使用经确认的静态导入行。使用 `/kb-init --agents` 可单独调整客户端，不改变 Vault 配置。

初始化采用声明式对账：只有期望内容和现状确实不同时才备份并修改单一托管区块。重复执行 `/kb-init` 时，已经一致的配置、目录、索引和桥接保持零写入、零备份，用户在标记区块之外的内容不会被改动。Schema 1 项目会一次性迁移为 Schema 2，并默认保留原 Codex/ZCode 行为。

## 规则按需加载与升级

已有项目与知识库的用户请按 [本次版本升级手册：规则按需加载（桥接协议 v5）](docs/upgrades/rule-loading-v5.md) 操作，包含客户端更新、项目桥接升级、共享/项目规则整理、验收与回退。

**旧用户请直接复制下面这段提示词。旧版还没有 `/kb-upgrade`，需要先由 Agent 安装新版，再继续升级项目：**

```text
请从 https://github.com/yqbo00/manage-obsidian-project-kb
的 master 分支获取最新版完整 Skill，更新当前客户端实际使用的
manage-obsidian-project-kb 安装副本。修改前备份，保留本地定制。

随后重新读取安装后的 SKILL.md 和 references/upgrade.md，
确认新版已定义 /kb-upgrade，再继续完成当前项目桥接、关联 Shared
和项目知识库规则的升级，并验证结果。

不要仅执行旧版 /kb-init，也不要在下载安装新版后停止。
无法确定的规则保留原状，最后报告实际加载路径、获取的提交 ID、
桥接版本、已完成的迁移和剩余事项。
```

已安装支持升级命令的新版后，后续才可简写为 `使用 manage-obsidian-project-kb 执行 /kb-upgrade`；`/kb-upgrade --check` 只检查不修改。Agent 连续完成版本检查、安装、桥接、规则整理和验收，不需要用户逐步发送命令。不明确的规则保留兼容状态，最后汇总；网络和写入权限仍由客户端控制。

`Mandatory` 表示命中适用条件后必须遵守；`applies_to: ["*"]` 仅表示跨项目适用。规则用 `load: Always | Conditional` 表示加载时机，Conditional 用 `triggers` 写完整适用条件。启动先读 Rule Catalog 并核对来源元数据，再读常驻/命中规则正文；由查询转为修改、构建、部署等操作前重新筛选。一般知识的 5 篇检索限制不适用于命中规则。

新笔记通过 `kind` 区分规则、契约、ADR、Runbook、知识和执行资产，仍使用现有主题目录。规则正文包含适用条件、行为要求、验证、例外与证据；临时状态继续保存在事项文档、Sprint、Worklog。规则目录只投影来源元数据，正文是权威副本。

升级不改变配置 Schema 2：

1. 更新客户端安装的完整 Skill 包，在已有项目执行 `/kb-init`，将已配置的桥接区块幂等更新至 version 5。
2. 旧 Mandatory 缺少 load 时继续全文加载，避免静默漏读；旧 Index 缺少 Rule Catalog 时从笔记头部发现规则。
3. 授权 Agent 整理规则时，再逐条明确 kind/load/triggers 并同步 Catalog；普通初始化不会批量改变历史规则范围或强度。

重复初始化仍须零无效写入。Markdown 只能指导行为，权限和兼容性等要求应配合实际账号限制、CI 检查或其他执行控制。

## 命令

这些是跨 CLI 的逻辑协议；即使终端没有注册原生 Slash Command，也应在 Skill 激活后按相同语义执行。

| Command | Purpose |
|---|---|
| `/kb-upgrade [--check]` | 一次请求完成当前安装、项目桥接与知识规则升级；可只读预检 |
| `/kb-init` | 初始化或幂等升级配置、Vault 目录和 Agent Adapter 桥接 |
| `/kb-init --agents` | 仅选择和对账 Agent 客户端，不修改 Vault 设置 |
| `/kb-doctor` | 只读检查配置、桥接、锁、索引和本地路径安全 |
| `/kb-status` | 汇总当前 Sprint、任务、阻塞、共享规则和今日成果 |
| `/kb-read [关键词/目录]` | 检索项目层和 Shared 层知识 |
| `/kb-save [--shared]` | 保存项目永久笔记或经确认的共享知识 |
| `/kb-log [说明]` | 补录 Agent 未观察到的工作 |
| `/kb-today [日期]` | 按项目查看某日工作汇总 |
| `/kb-report [范围] [--save]` | 聚合日、周、月或自定义范围报告 |
| `/kb-deprecate [文档] [替代文档]` | 非破坏性废弃知识并连接后继文档 |

## 开发与验证

项目校验不依赖第三方 Python 包：

```bash
python3 tools/validate_skill.py skills/manage-obsidian-project-kb
python3 -m unittest discover -s tests -v
```

校验包含 Skill 名称与目录一致性、Frontmatter、ZCode 大小限制、Codex UI 元数据、资源引用、桥接标记和关键模板。Pull Request 和主分支推送会运行同样的 GitHub Actions 检查。

## 安全边界

- 不保存密钥、Cookie、个人数据或完整生产数据。
- 不覆盖或直接删除历史知识；废弃方案通过 `status: Deprecated` 保留。
- 不自动清理归属不明的写锁；必须先执行 `/kb-doctor` 并由用户确认没有活跃写入。
- Vault 不可访问，或命中/无法排除的 Mandatory 规则无法加载时，允许说明限制后的只读分析，并暂停受影响的修改。

## License

本项目采用 [MIT License](LICENSE)。Copyright (c) 2026 manage-obsidian-project-kb contributors。
