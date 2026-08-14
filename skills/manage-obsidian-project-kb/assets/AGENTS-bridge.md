<!-- kb:agents-bridge:start -->
<!-- kb:agents-bridge:version=3 -->
## Mandatory Obsidian KB Bootstrap

处理任何代码、架构、排错、审查或项目文件修改前，必须：

1. 使用 `$manage-obsidian-project-kb`，并从当前仓库根目录重新读取 `.ai/obsidian-kb.json`；不得使用其他项目或先前会话缓存的配置。
2. 验证 `Schema_Version`、`Vault_Path`、`Project_Name`、`Shared_KB`、`Worklog_KB` 和 `Current_Sprint`，解析 Project Dashboard、Current Sprint、Shared Knowledge Index、Worklog Index 与今日 Daily Worklog 的真实路径。
3. 读取 Shared Knowledge Index，并在 Shared 树内检索、完整读取所有同时满足以下条件的笔记：
   - `status: Active`
   - `scope: Shared`
   - `enforcement: Mandatory`
   - `applies_to` 包含 `"*"` 或当前 `Project_Name`
4. 读取 Project Dashboard 的 `## 🚀 Current Progress & Active Status`、Current Sprint 及今日 Daily Worklog 中当前项目的记录，加载当前目标、进行中任务、Blockers 和今日已有成果。
5. 在设计或修改前，列出本任务适用的 Mandatory 规则及其 Vault 相对来源；随后按需检索相关 `Default` 和 `Advisory` 知识。
6. 遵循优先级：更高层级系统/用户指令 > Mandatory 共享规则 > Active 项目决策 > Default > Advisory。发现冲突、过期链接或适用范围不明时，停止相关修改并向用户报告，不得静默选择。
7. 无法读取配置或适用的 Mandatory 规则时，只读分析可以在明确警告后继续；代码、配置和项目文件修改必须暂停，直到通过 `/kb-init` 或 `/kb-doctor` 恢复可读状态。
8. 完成前根据已加载规则复核变更和验证结果；对有意义的成果、进展或 Blocker，在最终回复前按 Skill 的 Automatic Worklog 规则自动去重写入当天日志并读回验证，无需用户额外调用 `/kb-log`。
9. 报告遵循的规则、例外、未验证项、项目知识同步和 Worklog 状态；写入失败时明确标记 `Worklog: Pending`，不得声称已经记录。

不要把共享规则正文复制到项目中；项目只保留指向 Shared 权威笔记的 Wikilinks。
<!-- kb:agents-bridge:end -->
