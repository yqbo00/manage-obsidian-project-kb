# Rule maintenance

仅保存/整理规则、维护 Rule Catalog 或迁移规则时读取；写前读取 `references/write-safety.md`，适用规则仍按 `references/rule-loading.md` 加载。

## Catalog and source of truth

使用 `references/markdown-templates.md` 的 Rule Catalog 模板，在 Shared Index 或项目 Dashboard 内维护一份来源摘要。每行投影来源链接、status、applies_to、enforcement、load、triggers；旧 Mandatory 的缺省 load 显示 `Legacy/Always`，但不回写来源。

Catalog 不复制规则行为正文，不作为第二个权威副本。修改规则时获对应锁，局部更新来源、Change Log 与 Catalog，读回验证；相同路径只出现一次，摘要未变化则零写入。标记重复/破损时报告，不重建整个 Index。初始化只给新索引使用模板；既有索引可在授权规则维护时补齐 Catalog，缺失 Catalog 不阻止旧规则发现。

## Saving and promotion

- 先判断类型和适用范围，再使用现有主题目录。规则使用专用正文：适用条件、必须行为、验证方式、例外条件、证据与 Change Log；ADR/Runbook 等保留各自结构。
- 检查规则是否长期稳定、能指导具体行为、可验证，是否已有同义规则，以及是否只是本次范围或临时例外。单次推测保留为 Draft 候选，不能自动升级为全局 Mandatory；用户明确制定的长期规则可用其确认作为依据，无需等待重复事故。
- 新规则优先选择明确的 Conditional；只有跨任务稳定成立且用户已认可的少量要求才用 Always。`applies_to: ["*"]`、Always 和 Mandatory 都不得成为模板自动填充的默认值。用户个人语言偏好不写入可分发 Skill 默认规则。
- 扩大到全局范围、改成 Always 或提升强度须有用户授权；已有授权直接执行，不重复索要。维护旧规则时缩小范围或由 Always 改 Conditional 也需用户已授权的整理任务支持，不能在普通初始化中静默修改。
- 阶段例外记录批准依据、适用任务和结束条件，留在事项文档或 Sprint 并链接原规则；Worklog 记录结果，不反向成为全局规则。
- 合并重复规则时先核对适用条件和实际行为。经授权以原规则追加替代说明、标为 Deprecated、链接后继规则的方式保留历史；不得因标题相似或日期较旧自动合并/废弃。
- 验证方式应引用可执行检查或已有技术控制，并如实记录未验证项。仅记录 CI、账号权限或 Hook 不代表它已部署，也不授权自动修改这些控制。

## Migration

先升级 Skill 与桥接（当前 version 7），让旧 Mandatory 继续走兼容加载。推荐一次 `/kb-upgrade --auto-migrate`，随后由 `references/auto-migration.md` 在使用已有项目时幂等对账桥接并迁移明确条件的规则，无需逐项目执行命令。未启用自动迁移时仍可显式升级，或用 `/kb-init` 仅对账桥接。在已授权范围内逐条补齐 kind/load/triggers，核对正文适用条件并同步 Catalog；每次只改变有依据的规则，既有目录、配置和历史记录保持有效。
