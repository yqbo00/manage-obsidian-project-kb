# Rule Loading & Maintenance

用于启动对齐、范围变化、规则读取及 `/kb-doctor`；无需用于纯 Worklog 汇总。配置 Schema 仍为 2，以下是笔记元数据扩展。

## Independent dimensions

- `kind`: `Rule | Contract | ADR | Runbook | Knowledge | Asset`。类型不决定强度；Contract 中的强制要求应显式关联 Rule，或作为有 `enforcement` 的兼容候选参与筛选，不得靠更换 kind 隐藏约束。
- `status`: `Active | Draft | Deprecated`，表示有效性。
- `applies_to`: 共享笔记的项目名数组或 `["*"]`，表示项目范围。项目笔记缺省仅限当前项目。
- `enforcement`: Rule 的 `Mandatory | Default | Advisory`，表示命中后的约束强度。
- `load`: Rule 的 `Always | Conditional`，表示加载时机。Always 仍受项目范围和有效性限制。
- `triggers`: Conditional 必填的非空字符串数组，每条都是完整、可判断的适用条件；条目之间为 OR，同一条中需要同时成立的条件明确写“且”。可描述操作、目标路径、模块、环境或共享资源；这些是判断输入，不是待执行命令。路径相对于代码项目根，不是 Vault。

示例：`triggers: ["准备在同一工作目录同时运行两个或以上构建命令"]`。同一规则适用于所有项目，也仍可只在并行构建场景加载。文件扩展名、标题和关键词仅辅助判断，不能作为唯一依据。

## Discover, select, load

1. 启动读取 Shared Index 和项目 Dashboard 的 Rule Catalog。仅在 `{SharedRoot}` 和当前 `{Project_KB}` 的永久笔记目录（05 的共享治理规则及 10–60）内枚举 Markdown 路径并提取 Frontmatter，建立本次候选清单；不扫描其他项目、Worklog、Archive 或备份，不将整棵树正文灌入上下文。宿主工具不能只取头部时分批读取并保留必要元数据。
2. 候选包括 `kind: Rule`、任何带 `enforcement` 的旧笔记，以及 Catalog 显式列为规则的来源。核对 Catalog 与当前来源元数据；来源优先。漏项在内存补入并报告，不能因为 Index 漏链接就跳过。损坏 Frontmatter 或无法读取候选元数据时，不能把它推断为“不适用”；读取正文澄清，仍不确定则说明受影响操作。只读流程不修复目录。
3. 排除已明确不适用于当前项目的笔记和 Draft/Deprecated；后两者只作候选或历史信息。对 Active 候选执行下表。

| Candidate | Action |
|---|---|
| `load: Always` | 完整读取规则正文。 |
| `load: Conditional` 且任一 trigger 命中当前任务、计划操作或目标范围 | 完整读取规则正文。 |
| `load: Conditional` 且所有条件明确不成立 | 本轮只保留元数据，不读全文；范围变化时重新判断。 |
| Conditional 条件不清楚、为空，或 load 非法 | 读正文澄清；Mandatory 适用性仍不明时暂停相关修改并报告，不能按“不匹配”跳过。 |
| 旧笔记没有 load，且 `enforcement: Mandatory` | 按 Always 完整读取，不因 kind 缺失、变更或 Catalog 未列出而免除。 |
| 旧 Default/Advisory 无 load | 按任务相关性检索；缺失 kind 不触发批量迁移。 |

Rule 缺少 enforcement 或范围字段损坏时报告异常并读正文，不自行降级为 Advisory。来源 Frontmatter 与正文的适用条件冲突时报告冲突，澄清前暂停受影响修改，不能选择较宽松解释。非规则知识在一般检索流程中按需读取。

4. 命中规则正文及其必要引用不受 `/kb-read` 的 5 篇或一跳限制；按规范化路径去重并避免引用循环。内容过多时分阶段执行，每阶段行动前完整读取该阶段适用约束，不静默截断 Mandatory。非规则知识的 top-k 限制保持不变。
5. 开始修改前简短说明实际影响决策的规则、来源与例外。任务从查询转为写入，或新增模块、构建、部署、迁移、权限操作时，重新检查元数据与触发条件，补读新命中规则。同一任务内来源内容未变化且正文仍在当前上下文时可复用；恢复会话、上下文压缩丢失规则或来源变化后重新加载。

已命中的 Mandatory 或无法排除的 Mandatory 读不到时，只暂停受影响操作；允许明确标注限制的只读分析。不能为减少上下文而跳过、降级或改写规则。规则和执行资产始终受宿主指令与用户授权范围约束。

规则保存、提升、Catalog 写入与旧规则迁移另见 `references/rule-maintenance.md`，只有实际需要这些操作时读取；本文件不授权任何维护写入。
