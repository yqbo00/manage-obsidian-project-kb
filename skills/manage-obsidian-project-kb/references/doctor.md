# Read-only diagnostics

仅 `/kb-doctor`、明确诊断或实际迁移后的验收时读取。加载 `references/configuration.md`、`references/agent-adapters.md`、`references/layout.md`、`references/rule-loading.md` 和 `references/write-safety.md` 检查对应不变量，不默认读取安装、升级、写日志流程。检查 Markdown 结构时按 `references/markdown-templates.md` 选择有关模板；不为“检查完整性”重写所有文件。

### `/kb-doctor [--clear-lock project|shared|worklog]`

默认只读诊断，不隐式修复：

1. 检查配置 Schema、路径边界、Vault 可访问性，以及本地配置是否被 Git 跟踪或遗漏忽略。
2. 检查项目、Shared、Worklog 目录与索引、Current Sprint、必要 Frontmatter 和受管理区块。
3. 按配置检查所有内置与自定义适配器目标，报告模式、桥接版本、重复/破损标记、目标冲突和期望内容差异；只检查启用 Codex 时适用的非空 `AGENTS.override.md`。未配置客户端不得误报为故障。
4. 检查三个锁目录和 `owner.json`，报告 scope、operation ID、创建时间与可能的孤儿锁，但不按年龄推断无人使用。
5. 对索引链接执行有界存在性检查并汇总断链；不递归读取整个 Vault 正文。
6. 按 `references/rule-loading.md` 检查 Rule Catalog 遗漏/过期、非法加载字段、旧 Mandatory 兼容项和重复/冲突候选。只读报告，文本相似或日期较旧不足以自动合并、废弃或改变适用范围。

只有用户显式指定 `--clear-lock` 并确认对应范围没有活跃写入时，才可再次核对锁路径、展示 owner 信息并删除该锁目录；目录包含非锁元数据文件、路径逃逸预期根目录或确认不明确时拒绝操作。其他修复通过 `/kb-init` 或精确命令完成。
