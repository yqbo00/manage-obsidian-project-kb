<!-- kb:agents-bridge:start -->
<!-- kb:agents-bridge:version=5 -->
## Mandatory Obsidian KB Bootstrap

处理任何代码、架构、排错、审查或项目文件修改前，必须：

1. 加载 `manage-obsidian-project-kb` Skill（使用宿主支持的调用方式，如 `$manage-obsidian-project-kb`），并从当前仓库根目录重新读取 `.ai/obsidian-kb.json`；不得使用其他项目或先前会话缓存的配置。
2. 验证 `Schema_Version`、`Vault_Path`、`Project_Name`、`Shared_KB`、`Worklog_KB`、`Current_Sprint`、`Agent_Clients` 和 `Custom_Agent_Bridges`，解析 Project Dashboard、Current Sprint、Shared Knowledge Index、Worklog Index 与今日 Daily Worklog 的真实路径。
3. 按 Skill 的 Rule loading 协议读取 Shared Index、项目 Rule Catalog 并核对来源元数据。对当前项目适用且 Active 的规则，完整加载 Always、当前任务/计划操作命中的 Conditional，以及没有 load 的旧 Mandatory；条件不清楚时读正文确认。Catalog 缺项不能使来源规则失效，普通知识的检索篇数限制不能截断命中规则。
4. 读取 Project Dashboard 的 `## 🚀 Current Progress & Active Status`、Current Sprint 及今日 Daily Worklog 中当前项目的记录，加载当前目标、进行中任务、Blockers 和今日已有成果。
5. 在设计或修改前简要说明实际影响本次工作的规则及其来源。任务范围、目标路径或拟执行操作变化时，在行动前重新筛选并补读规则。Mandatory 表示命中后必须遵守，applies_to 为全项目不表示所有任务都命中；Default/Advisory 按相同适用条件处理，普通知识按需检索。
6. 遵循宿主指令层级和用户授权范围；命中的共享及项目 Mandatory 均须遵守，Active 项目决策可覆盖 Default，Advisory 供参考。共享与项目 Mandatory 冲突、来源条件冲突或适用范围不明时，停止相关修改并报告，不得静默选择。
7. 无法读取配置、已命中或无法排除的 Mandatory 规则时，暂停受影响的修改并报告；只读分析可在明确说明限制后继续。通过 `/kb-init` 或 `/kb-doctor` 诊断恢复，不能为继续操作而静默跳过规则。
8. 完成前根据已加载规则复核变更和验证结果；对有意义的成果、进展或 Blocker，在最终回复前按 Skill 的 Automatic Worklog 规则自动去重写入当天日志并读回验证，无需用户额外调用 `/kb-log`。
9. 报告遵循的规则、例外、未验证项、项目知识同步和 Worklog 状态；写入失败时明确标记 `Worklog: Pending`，不得声称已经记录。

不要把共享规则正文复制到项目中；项目只保留指向 Shared 权威笔记的 Wikilinks。
规则提供行为指导；读取规则、Runbook 或脚本不构成执行授权，也不能代替实际权限和自动化检查。
<!-- kb:agents-bridge:end -->
