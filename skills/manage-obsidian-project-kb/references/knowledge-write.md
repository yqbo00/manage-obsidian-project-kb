# Save and maintain knowledge

仅永久知识保存、状态变更、废弃及相关索引维护时读取。写前读取 `references/write-safety.md`、`references/layout.md`，按 `references/markdown-templates.md` 选择笔记/规则模板。规则提炼与修改额外读取 `references/rule-maintenance.md`；普通 ADR/Runbook 不加载规则提炼流程。

先按 kind 区分 Rule、Contract、ADR、Runbook、Knowledge、Asset，再按主题归档。临时范围、待办、阶段例外与阻塞留在事项文档/Sprint/Worklog，非 Rule 不强套规则正文；旧笔记无需批量补字段。

### Knowledge quality and security

- 只保存工程级事实、约束、决策、原因、替代方案、验证证据、复现步骤、关键配置和后续影响。
- 删除寒暄、重复说明、无结论思考过程、无关日志和临时输出。
- 把永久笔记的 `status` 视为知识有效性而非任务进度；普通流程由 Agent 自动维护，不要求用户手动选择或同步状态。
- 根据当前任务证据自动判定：未验证、证据不足或仍待确认时使用 `Draft` 并列出验证条件；经代码、测试、运行结果、配置核对或用户确认充分验证后使用 `Active`；被新知识明确替代或已不适用时使用 `Deprecated`，不得再作为当前方案引用。
- 状态变化时，在同一次受锁写入中局部更新 Frontmatter、追加带日期且包含证据或原因的 Change Log，并同步对应 Index 条目的状态标注；读回全部目标后才报告完成。
- 不要仅为状态选择打断用户。现有证据无法区分 `Draft`/`Active` 或“替代”/“并行适用”，且判断会影响使用时才询问；用户未回答时保守使用 `Draft` 并报告待验证项。不得自动把 `Deprecated` 恢复为 `Active`，应创建后继笔记，或取得用户明确确认并留下审计记录。
- 不写入密码、令牌、私钥、Cookie、个人数据或完整生产数据。代码、日志和命令必须脱敏。
- 永远先读再写；没有找到历史记录时明确说明未命中，不得伪造知识库上下文。

### File and Wikilink rules

- 使用 UTF-8 Markdown。文件名表达单一稳定主题，并替换 `/`、`\\`、`:`、`*`、`?`、`"`、`<`、`>`、`|`、`#`、`^`、`[`、`]` 等不安全字符。
- 每篇永久笔记只解决一个主要问题。过长或跨主题内容拆成独立卡片。
- 项目内链接使用路径明确的 Wikilink，例如 `[[20-Architecture_&_ADR/核心路由机制]]`。
- 多项目可能重名时使用 Vault 根相对链接，例如 `[[Projects/{Project_Name}/20-Architecture_&_ADR/核心路由机制|核心路由机制]]`。
- 每篇永久笔记链接回 `[[Projects/{Project_Name}/00-Index|Project Dashboard]]`，Dashboard 也链接到核心笔记。
- 共享笔记链接回 `[[{Shared_KB}/00-Index|Shared Knowledge Index]]`；项目 Dashboard 链接相关共享规则，而不是复制正文。
- 只链接真实存在或将在同次写入中创建的文档。不存在关联时省略模板占位行，不生成虚假孤链。

### `/kb-save [--shared] [可选标题] [可选分类]`

完成重要工作后自动视为触发；用户只说 `/kb-save` 即可，能够从上下文推断时不得要求其补充标题、分类、状态或 Index 同步步骤。临时讨论、原始日志和敏感数据不自动保存；具有长期价值但尚未验证的结论可保存为 `Draft`。

1. 重新读取配置、Project/Shared/Worklog 索引、今日 Daily Worklog、Current Sprint 和潜在重复笔记。默认写入项目层；只有用户显式使用 `--shared` 或确认提升为共享知识时才写入 Shared。
2. 先按 `kind: Rule | Contract | ADR | Runbook | Knowledge | Asset` 判断内容类型；临时状态只更新事项文档/Sprint/Worklog。将永久内容提炼为单一可复用主题，填写 `kind` 并路由到 `10–60`：
   - 领域模型、业务规则、状态机、API 契约 → `10-Domain_&_Business`
   - 架构、拓扑、边界、接口、ADR → `20-Architecture_&_ADR`
   - 框架机制、并发、性能、工程实践 → `30-Engineering_&_Tuning`
   - K8s、CI/CD、IaC、数据库/缓存/日志基础设施 → `40-Infra_&_DevOps`
   - Bug、异常、根因、修复、验证、复盘 → `50-Troubleshooting`
   - AI 提示词、CLI 工作流、Agent 配置、自动化脚本 → `60-AI_&_Automation`
3. `--shared` 按 Shared routing 保存，填写 `applies_to`；Rule 还须填写 `enforcement`、`load` 和 Conditional 的非空 `triggers`，使用规则模板。其他新笔记不默认赋予规则强度。按 `references/rule-maintenance.md` 检查规则稳定性、可执行性、重复来源与阶段例外；单次经验先作为候选，用户明确制定的长期规则不要求重复出现。全局提升须有用户明确授权，已有明确授权无需再次询问。
4. 先从代码、测试、运行结果、配置核对、用户确认和既有笔记自动判定状态，再判断是追加同一事件、创建新原子笔记，还是在证据明确时新建替代方案并废弃旧笔记；仅按上述知识状态歧义规则询问用户。
5. 获得对应锁后最小写入；状态变化时同步 Frontmatter、Change Log 和对应 Index 状态。项目使用共享知识时在 Dashboard 建立链接；若关联当前任务，只补齐 `references/progress.md` 的 Completion synchronization 中尚未执行的任务/Dashboard 子步骤，不得递归进入 `/kb-save` 或重复落账。
6. 读回所有修改文件并释放锁；随后读取 `references/worklog-write.md`，按 Automatic Worklog 对本次知识成果去重落账。报告保存路径、分类、状态、任务/索引/Worklog 同步；只有验证成功后才声称已保存。

### `/kb-deprecate [文档] [替代文档]`

精确定位目标，获锁后把 Frontmatter `status` 改为 `Deprecated`，追加日期、原因和替代 Wikilink；在替代文档与 Dashboard 中添加反向说明。保留原文件和索引项，读回验证后释放锁。匹配不唯一时先询问，不得猜测。

## Wikilink & Dashboard Maintenance

- Project Dashboard 与项目笔记互链；Shared Index 与共享笔记互链；项目只链接共享笔记，不复制内容。
- Worklog Index 链接 Daily 和显式保存的 Reports；Daily 事件链接项目任务或知识证据，但项目文档不反向维护每日事件清单。
- 原子笔记之间只建立有语义的链接，例如“依赖”“实现”“取代”“故障表现”或“验证”。
- Dashboard 的任务状态只来自 Current Sprint；永久知识入口只来自真实文件。
- 项目 Index 条目格式为 `- [[路径|标题]] — 摘要（Status）`；Shared Index 额外标注 `applies_to`，Rule Catalog 按规则协议投影强度、加载条件与来源。非规则知识不默认标记为 Mandatory。
- 修改规则时，在同一次受锁写入中同步来源 Frontmatter、正文、Change Log 与对应 Rule Catalog；目录缺失时只添加一次托管区块，内容不变时 no-op。部分失败须报告，读取时回到来源核对。
- 新增前按规范化路径去重。笔记废弃时保留条目并标记替代链接，不删除历史入口。
- 保护用户手写说明、Dataview 和自定义区块；只修改目标标题下的必要内容，不整体重新生成 Dashboard。
