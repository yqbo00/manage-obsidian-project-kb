# Safe writes

仅在实际写入配置、桥接、知识库或工作日志前读取；诊断锁时可读取本文件，但不据此创建锁。写入前重新核对配置与目标文件，使用最小补丁和既有协议，不从缓存直接覆盖。

### Non-destructive and cross-agent writes

- 不删除、清空、截断或整文件覆盖历史知识。只执行局部补丁、追加记录和明确的状态更新。
- 废弃永久笔记时保留文件，把 Frontmatter 的 `status` 改为 `Deprecated`，并追加原因和替代文档链接。
- 同名新主题使用唯一后缀；不得覆盖既有文件。更新同一知识事件时追加带日期的 Update 或 Change Log。
- `Current_Sprint.md` 是可变状态文件。切换 Sprint 前先在 `Archive/` 创建不可覆盖的完整快照并读回验证，再更新当前文件和配置。
- 项目、共享和工作日志写入分别使用 `{Project_KB}/.kb-write.lock/`、`{SharedRoot}/.kb-write.lock/`、`{WorklogRoot}/.kb-write.lock/`。同时更新多层时固定按“共享锁 → 项目锁 → Worklog 锁”获取，避免死锁。
- 使用原子目录创建获取锁，并立即在锁内写入 `owner.json`。使用以下 Schema，`operation_id` 必须是本次生成且不可预测的唯一值，时间使用带时区 RFC3339：

  ```json
  {
    "operation_id": "unique-random-id",
    "created_at": "2026-08-14T10:30:00+08:00",
    "scope": "project",
    "operation": "concise operation summary"
  }
  ```

  `scope` 只允许 `project`、`shared` 或 `worklog`。释放前核对 `operation_id`；只释放本次操作创建且仍由自己持有的锁。
- 锁已存在时读取并报告 owner 元数据，有限重试后停止写入。锁归属不明、元数据损坏或 Agent 异常退出时不得按时间自动删除；使用 `/kb-doctor` 诊断，并仅在用户显式确认没有活跃写入后执行指定范围的清锁。
- 首次初始化可在获锁前执行幂等 `mkdir`；任何 Markdown 写入必须在获锁后完成。
- 所有初始化都按“读取 → 验证 → 计算期望状态 → 比较 → 仅在有差异时写入 → 读回”的声明式对账执行。目录已存在、配置语义一致、桥接区块字节一致或索引链接已存在时必须是 no-op：不创建备份、不更新时间戳、不调整用户文本。不得通过盲目追加实现初始化。
- 同一物理目标文件只对账一次。多个客户端共享 `AGENTS.md` 时先按规范化绝对路径合并目标；同一自定义 `Id`、同一目标上的冲突模式或冲突导入行视为配置错误并停止相关目标，不得按数组顺序覆盖。
- 若发现旧版 `01-Architecture/`、`02-TechStack/` 或 `03-Troubleshooting/`，保留原目录和文件，只报告迁移建议。未获得用户明确指令时不得自动移动、复制或删除旧知识。
