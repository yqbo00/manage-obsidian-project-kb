# Initialization and bridge reconciliation

仅初始化、重配置或已授权的项目兼容迁移时读取。先加载 `references/configuration.md`、`references/write-safety.md`、`references/layout.md`，有已有规则时按 `references/rule-loading.md` 核对适用要求。目标配置 Schema 2，标准桥接 version 7；高于支持版本时报告，不降级。

### `/kb-init [--agents | --reconfigure]`

1. 解析 `{Project_Root}` 并检查 `.ai/obsidian-kb.json`。
2. 完整读取 `references/agent-adapters.md`。配置不存在时，询问 `Vault_Path`；把项目根目录名作为 `Project_Name` 默认值。`Current_Sprint`、`Shared_KB` 和 `Worklog_KB` 分别使用默认值，并让用户确认自动检测建议的客户端集合；检测只能提供建议，不得静默启用客户端。允许选择内置 `codex`、`zcode`、`claude-code`，以及登记一个或多个 `custom` 适配器。写入当前 Schema。
3. 将相对 Vault 路径或 `~` 解析成宿主平台的绝对路径并确认。Vault 不存在时先询问是否创建；需要额外权限时走宿主审批。
4. 若属于 Git 仓库，在任何真实路径写入前检查 `.ai/obsidian-kb.json` 是否已被跟踪或忽略。已跟踪时警告并停止初始化，交由用户决定如何从索引移除；未跟踪且未忽略时，通过 `git rev-parse --git-path info/exclude` 定位仓库本地 exclude，先读后局部追加 `/.ai/obsidian-kb.json` 与 `/.ai/kb-backups/`，不得擅自改写项目 `.gitignore`。
5. 使用内置写入工具创建配置；回退 Shell 仅用于标准目录和文件操作。所有路径都必须引用，例如 `mkdir -p "{Project_Root}/.ai"`。先规范化数组、字段顺序和默认值，再进行语义比较。只有升级、重配置或修复确实会改变内容时，才把原文件保存到不覆盖的 `.ai/kb-backups/{config|agents}/` 时间戳文件；内容不变时不得重写或备份。
6. 读取 `references/markdown-templates.md` 并仅加载其中的初始化模板包，幂等创建项目树、Shared 树、Worklog 的 `Daily/`、`Reports/Weekly/`、`Reports/Monthly/`、`Reports/Custom/` 和项目 `Archive/`；按固定锁顺序只创建缺失的 Project Dashboard、Shared Index、Current Sprint 与 Worklog Index，并在项目 Dashboard 缺少 Worklog 入口时局部补充链接。
7. 完整读取 `assets/AGENTS-bridge.md` 和 `assets/agent-import-bridge.md`，根据已配置适配器生成去重后的目标清单并按 `references/agent-adapters.md` 对账。Codex/ZCode 和 `CanonicalAGENTS` 共用 `{Project_Root}/AGENTS.md`；仅在启用 Codex 且非空 `AGENTS.override.md` 已存在时同步它；Claude Code 使用根级 `CLAUDE.md` 中受管理的 `@AGENTS.md` 导入；Custom 按其模式处理。不得创建无用途的 override 文件。
8. 对每个目标独立执行：不存在则创建；存在且无本 Skill 标记时仅在末尾追加一个分隔良好的区块；恰有一组匹配标记时只在区块内容过期时替换整个标记区间。完全一致时 no-op。修改既有文件前才创建一次本地时间戳备份；标记缺失一端、嵌套、重复、ID 不匹配、目标冲突或符号链接逃逸项目根时停止该目标并报告。任何失败都不得被其他目标的成功掩盖。
9. 读回配置、三个索引、Current Sprint、目录树、Git 本地忽略状态、Dashboard Worklog 链接和所有已配置适配器目标；逐项验证唯一标记、期望内容、未触碰区内容及 no-op 结论，只在全部必要目标成功后报告初始化完成。

普通 `/kb-init` 不改变既有合法配置选择，但可幂等迁移旧 Schema、补齐目录树及缺失/过期的受管理区块。`/kb-init --agents` 只重新选择和对账 Agent 适配器，不改变 Vault、项目名或知识目录；移除客户端只停止维护其桥接，默认保留历史文件和区块，除非用户明确要求非破坏性移除对应托管区块。只有 `/kb-init --reconfigure` 才可改变其他配置值。发现旧目录时只报告，不自动迁移。

规则加载升级不改变配置 Schema 2。更新桥接后仍按旧 Mandatory 兼容策略运行；普通初始化不批量改写历史规则的 `kind`、`load`、`triggers` 或强度。仅在用户授权整理规则时，逐条核对并更新笔记与 Catalog，不能只改索引来缩小规则范围。
