# Lightweight migration check

在开发启动、恢复/切换项目时读取；先完成配置验证与本轮适用规则筛选。本流程只读、不联网、不创建目录、锁、状态、备份或日志；不是完整升级，也不扫描其他仓库。纯日报查询不触发此检查。

## Machine-local record

本机状态文件为 `manage-obsidian-project-kb/installations.json`：POSIX 放在有效绝对路径 XDG_STATE_HOME 下，未设置或为相对路径时使用用户主目录 `.local/state/`；Windows 放在已解析的 LOCALAPPDATA 下。路径无法确定则报告 Pending，不改放到项目或 Vault。

读取 JSON：`schema_version` 必须为整数 1，`installations` 为记录数组。以解析软链接后的当前 Skill 安装绝对路径匹配 `installed_path`，同一物理安装必须恰好匹配一条；其他安装的记录不能借用。匹配记录仅当 `auto_migrate: OnUse` 且字符串数组 `authorized_migrations` 含 `bridge-v6-rule-loading-v1` 时有效。Disabled、无记录、不支持的 schema、歧义或损坏均不视为启用，不猜测或覆盖。source/revision 可作为已验证来源线索，不是授权依据。

协议 ID 沿用 v6：v7 仅重排指令与瘦身桥接，不改变该协议的行为或授权范围；不能据此授权未来其他迁移。授权状态不替代项目 `.ai/obsidian-kb.json`。

## Check, then route

1. 无项目配置或绑定非法时报告 UNCONFIGURED/DEGRADED，不自动初始化。当前任务明确只读时永不进入执行分支。
2. 无有效授权时只保留常规规则加载已发现的问题；有需求时简短提示一次启用方式，不预读完整迁移流程。用户明确要求启用/关闭时才加载 `references/auto-migration.md`。
3. 有效授权下复用本轮配置、规则元数据和 Catalog 比对，找 Schema/加载字段缺项、索引遗漏/过期。元数据不明确不得当作已升级；正常合法且未命中的规则不为迁移复读全文。不依赖“迁移完成”标记省略来源发现。
4. 比较已配置桥接与 `assets/AGENTS-bridge.md` 的期望区块（version 7），包括标记唯一和完整内容，不仅比较版本号。内置 Codex/ZCode 使用根级 AGENTS.md；启用 Codex 且存在非空 AGENTS.override.md 时也检查。Claude Code 还检查 CLAUDE.md 的 @AGENTS.md 导入，按 `assets/agent-import-bridge.md` 对比；独立且无托管标记的相同导入保持 Satisfied (unmanaged)。仅存在自定义适配器或目标不明时读取 `references/agent-adapters.md` 解析目标；验证相对路径/真实路径边界后才访问。非法/高于支持版本的协议保留原状，不降级。
5. 无差异直接结束，不加载初始化、升级执行、写入或模板流程，不生成“已检查”工作事件。只读任务或无授权有差异时集中报告 Pending，不写入。标记损坏/路径冲突不自动修复；仅报告受影响目标。
6. 有可迁移差异、有效授权且允许写入时才读取 `references/auto-migration.md` 执行本项目兼容迁移；相关规则在计划变化后补读。旧桥接要求更多读取时先遵守，更新后需宿主刷新才能解除的限制应明确报告。

同一会话已完成检查且配置、授权、桥接及来源未变化时不反复对账；恢复会话、切换项目、有关文件变化或上下文丢失后重查。不得缓存“不需要加载规则”来跳过任务范围变化后的规则筛选。
