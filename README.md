# manage-obsidian-project-kb

一个面向 Codex CLI、ZCode 等 AI 编程终端的跨 Agent 项目记忆与 Obsidian 知识库管理 Skill。它通过项目本地配置、根级 `AGENTS.md` 桥接和统一 Vault 目录，让不同 Agent 共享项目进度、架构决策、公共规则、排错经验及按日期汇总的工作记录。

## 核心能力

- 在一个 Obsidian Vault 中隔离多个项目，同时维护 Shared 公共知识和跨项目 Worklog。
- 初始化项目配置、目录、Dashboard、Current Sprint 和 Codex/ZCode 兼容的指令桥接。
- 启动开发任务前加载 Mandatory 公共规则、当前进度及相关历史知识。
- 完成有意义的工作后自动同步任务、Dashboard、永久笔记和当天 Worklog。
- 使用 `Active`、`Draft`、`Deprecated` 管理知识有效性，不覆盖或删除历史记录。
- 提供 `/kb-doctor` 检查配置、索引、桥接、锁、Git 忽略状态和有限范围断链。

## 仓库结构

```text
.
├── README.md
├── LICENSE
├── .github/workflows/validate.yml
├── skills/
│   └── manage-obsidian-project-kb/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── assets/AGENTS-bridge.md
│       └── references/markdown-templates.md
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

## 初始化项目

在目标代码仓库根目录启动 Agent，然后执行：

```text
$manage-obsidian-project-kb 请执行 /kb-init
```

Agent 会询问 Obsidian Vault 路径和项目名称，并在项目根目录创建机器本地配置：

```json
{
  "Schema_Version": 1,
  "Vault_Path": "/absolute/path/to/obsidian-vault",
  "Project_Name": "example-project",
  "Current_Sprint": "05-Roadmap_&_Tasks/Current_Sprint.md",
  "Shared_KB": "Shared",
  "Worklog_KB": "Worklog"
}
```

`.ai/obsidian-kb.json` 含本机绝对路径。`/kb-init` 会检查它未被 Git 跟踪，并将其加入仓库本地 exclude；不要提交该文件。

初始化还会始终维护根目录 `AGENTS.md`，以便 ZCode 和 Codex 都能加载知识库桥接。项目已经存在非空 `AGENTS.override.md` 时，会同步维护相同受管理区块，满足 Codex 的 override 优先级。ZCode 只读取当前 Workspace 根级 `AGENTS.md`，不会递归合并子目录规则；参见 [ZCode Agent 文档](https://zcode.z.ai/en/docs/agents)。

## 命令

这些是跨 CLI 的逻辑协议；即使终端没有注册原生 Slash Command，也应在 Skill 激活后按相同语义执行。

| Command | Purpose |
|---|---|
| `/kb-init` | 初始化或升级配置、Vault 目录和双 Agent 桥接 |
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
- Vault 不可访问或 Mandatory 规则无法加载时，允许明确警告后的只读分析，但暂停代码和配置修改。

## License

本项目采用 [MIT License](LICENSE)。Copyright (c) 2026 manage-obsidian-project-kb contributors。
