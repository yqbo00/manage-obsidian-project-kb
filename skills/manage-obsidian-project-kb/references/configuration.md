# Project configuration

访问项目知识库前读取；只定义绑定与验证，不触发初始化。存在自定义适配器或执行完整桥接维护/诊断时才读取 `references/agent-adapters.md`；内置客户端的轻量检查按 `references/migration-check.md`。

### Configuration is the source of truth

任何 Agent 启动、恢复会话、切换项目或收到知识库指令时，首先重新读取：

```text
{Project_Root}/.ai/obsidian-kb.json
```

当前配置 Schema 为：

```json
{
  "Schema_Version": 2,
  "Vault_Path": "/absolute/path/to/obsidian-vault",
  "Project_Name": "example-project",
  "Current_Sprint": "05-Roadmap_&_Tasks/Current_Sprint.md",
  "Shared_KB": "Shared",
  "Worklog_KB": "Worklog",
  "Agent_Clients": ["codex", "zcode"],
  "Custom_Agent_Bridges": []
}
```

验证要求：

- `Schema_Version` 是整数 `2`。缺失时视为旧版 Schema 0；Schema 0/1 读取仍有效，普通 `/kb-init` 可在创建本地备份后一次性迁移。Schema 1 迁移时默认 `Agent_Clients` 为 `["codex", "zcode"]`，`Custom_Agent_Bridges` 为空，以保持旧行为。高于当前支持版本时进入 `DEGRADED`，不得降级或猜测字段语义。
- `Vault_Path` 是规范化绝对目录路径。
- `Project_Name` 非空，且不含 `/`、`\\`、`..` 路径段、控制字符或目录穿越内容。
- `Current_Sprint` 是相对于 `Projects/{Project_Name}/` 且位于 `05-Roadmap_&_Tasks/` 内的 `.md` 路径，不得是绝对路径，不得包含 `..`；规范化后仍必须位于 `Project_KB` 内。默认值为 `05-Roadmap_&_Tasks/Current_Sprint.md`。
- `Shared_KB` 与 `Worklog_KB` 是相对于 `Vault_Path` 的安全目录路径，默认值分别为 `Shared` 和 `Worklog`；规范化后仍必须位于 Vault 内，且不得互相重叠或与 `{Vault_Path}/Projects` 重叠。旧配置缺少任一字段时保持有效并使用默认值，下次 `/kb-init` 可在备份配置后补齐。
- `Agent_Clients` 是去重后的内置适配器 ID 数组，只允许 `codex`、`zcode`、`claude-code`；顺序按此固定次序规范化。`Custom_Agent_Bridges` 是自定义适配器数组。完整字段、模式和边界见 `references/agent-adapters.md`；存在自定义适配器或处理 `/kb-init`、`/kb-doctor`、`/kb-status`、客户端变更时读取该文件；普通内置客户端配置读取无需加载桥接写入算法。
- 配置不得包含密钥、令牌、密码、个人敏感信息或 Agent 私有会话状态。
- 不得只依赖对话中缓存的配置；每次读写前重新读取文件。
- `.ai/obsidian-kb.json` 是机器本地配置，不是可移植项目资产。Git 仓库中必须确认它未被跟踪且已被忽略；不得把真实绝对路径写进提交、知识笔记或示例。

配置不存在时进入 `UNCONFIGURED` 状态并提供 `/kb-init` 向导；只读任务或自动迁移检查不得据此创建配置。配置非法或路径不可访问时进入 `DEGRADED` 状态：指出具体字段和原因，不猜测或覆盖，并建议 `/kb-init --reconfigure`。

从配置派生：

```text
Project_KB    = {Vault_Path}/Projects/{Project_Name}
SharedRoot    = {Vault_Path}/{Shared_KB}
WorklogRoot   = {Vault_Path}/{Worklog_KB}
Dashboard     = {Project_KB}/00-Index.md
CurrentSprint = {Project_KB}/{Current_Sprint}
WorklogIndex  = {WorklogRoot}/00-Index.md
DailyWorklog  = {WorklogRoot}/Daily/{YYYY}/{YYYY-MM}/{YYYY-MM-DD}.md
```
