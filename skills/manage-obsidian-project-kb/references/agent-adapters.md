# Agent Adapter Protocol

在执行 `/kb-init`、`/kb-init --agents`、`/kb-doctor`、`/kb-status` 或修改 Agent 客户端配置时完整读取本文件。

## Configuration

内置客户端只在 `Agent_Clients` 保存稳定 ID。未知客户端保存在 `Custom_Agent_Bridges`：

```json
{
  "Agent_Clients": ["codex", "zcode", "claude-code"],
  "Custom_Agent_Bridges": [
    {
      "Id": "example-agent",
      "Instruction_File": ".example/PROJECT.md",
      "Bridge_Mode": "ManagedBlock"
    }
  ]
}
```

规则：

- `Id` 必须匹配 `^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$`；不得与内置 ID 重名，忽略大小写后必须唯一。
- `Instruction_File` 必须是从 `{Project_Root}` 起算的 UTF-8 项目相对文件路径，不得为空、为绝对路径、含 `..`、控制字符或逃逸项目根；规范化后重新检查父目录和最终目标。目标是符号链接时，解析后的真实路径必须仍在项目根内。
- `Bridge_Mode` 只允许 `CanonicalAGENTS`、`ManagedBlock`、`ImportAGENTS`。
- `CanonicalAGENTS` 的 `Instruction_File` 必须规范化为 `AGENTS.md`，不得包含 `Import_Line`。
- `ManagedBlock` 不得包含 `Import_Line`，把 `assets/AGENTS-bridge.md` 的同一权威区块安装到目标。
- `ImportAGENTS` 必须包含 `Import_Line`。它必须是单行、非空、不含控制字符的静态文本；仅作为文件内容写入，永远不得传给 Shell、解释器或模板求值。该模式只在用户确认客户端确实支持该导入语法后使用。
- 拒绝未知字段，避免拼写错误被静默忽略。数组按 `Id` 排序后持久化；语义比较不依赖用户原始数组顺序。

## Built-in adapters

| ID | Canonical target | Behavior |
|---|---|---|
| `codex` | `AGENTS.md` | 安装标准受管理区块；已存在且非空的 `AGENTS.override.md` 同步相同区块，不创建空 override。 |
| `zcode` | `AGENTS.md` | 与 Codex 共用一个标准受管理区块。 |
| `claude-code` | `CLAUDE.md` | 使用导入模板和适配器 ID `claude-code` 安装单行 `@AGENTS.md`。标准区块仍安装到 `AGENTS.md`。 |

启用 `claude-code` 或任何 `ImportAGENTS` 时，必须同时把 `AGENTS.md` 加入目标清单，确保导入目标存在。多个适配器要求 `AGENTS.md` 时只写一次。

自动检测仅生成建议：存在相关项目指令文件/配置目录或宿主可识别客户端时可建议对应 ID，但首次写入前必须让用户确认。普通 `/kb-init` 对已有 Schema 2 配置不重新询问；使用 `/kb-init --agents` 才调整集合。

## Import bridge rendering

从 `assets/agent-import-bridge.md` 渲染：

- `{{Adapter_Id}}` 替换为已验证的内置或自定义 ID。
- `{{Import_Line}}` 替换为已验证的单行静态文本。
- 开始与结束标记中的 ID 必须相同，且目标文件中该 ID 各只出现一次。
- 不展开环境变量、反斜杠转义、命令替换或其他占位符。

## Idempotent reconciliation

对配置、索引和每个桥接目标执行以下状态机：

1. 完整读取文件并记录原始字节、换行风格和权限；验证路径边界与标记结构。
2. 由规范化配置生成确定性的期望区块。按规范化绝对路径合并目标，并按目标路径排序执行。
3. 文件缺失时创建一次。文件存在且无相关标记时，仅追加一个区块；先确保原文结尾恰有一个换行，再用一个空行分隔。
   - 对 `ImportAGENTS`，若目标中已经存在完全相同的独立导入行但没有本 Skill 标记，将其报告为 `Satisfied (unmanaged)` 并保持 no-op，避免制造重复导入；只有用户明确要求接管时才在备份后把该行包入标记。
4. 恰有一组标记时，把从开始标记到结束标记的完整区间与期望区块比较；相同则 no-op，不相同才替换该区间。
5. 任一标记只有一端、重复、嵌套、ID 不一致，或同一目标收到互斥期望时，停止该目标且不写入。
6. 只有最终字节确实不同才创建一次不覆盖备份，并以同目录临时文件加原子重命名写入；尽量保留权限与原换行风格。失败时保留原文件和备份。
7. 写后读回并验证期望区块恰好一份、非托管前后缀字节不变。重复运行时再次计算结果，必须得到零变更、零备份。

配置迁移也遵循相同原则：Schema 0/1 只迁移一次；规范化后的 Schema 2 内容已经相同时不得因格式偏好重复写入。索引链接、Git exclude 行和目录创建都必须先检查存在性再补齐，不得盲目追加。

## Safe removal

从配置移除客户端默认只停止维护，不删除文件或历史区块。用户明确要求移除时：

1. 再次读取配置和目标，确认该区块不再被其他客户端需要。
2. 只删除精确匹配的一组托管标记及其内部内容，保留其他文本。
3. 修改前备份，写后验证；标记异常时拒绝删除。
4. `AGENTS.md` 的标准区块仍被任一客户端、导入桥接或项目工作流依赖时不得移除。
