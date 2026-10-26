# Read context and status

用于 `/kb-read`、`/kb-status` 与开发中的相关知识检索。先按 `references/configuration.md` 验证配置，按 `references/rule-loading.md` 筛选规则；status 还读取 `references/agent-adapters.md` 检查已配置桥接，不运行初始化、升级或自动修复。

### `/kb-status`

以只读方式读取配置、Shared Index、Project Dashboard、Current Sprint、Worklog Index 和今日 Daily Worklog，输出：

- 当前 Sprint Goal 与 Milestone。
- 所有进行中任务、最高优先级未开始任务和 Blockers。
- 最近完成项及其验证或知识链接。
- Dashboard/Sprint 不一致、缺失链接或配置异常。
- 当前常驻/命中规则、旧 Mandatory 兼容项和共享层健康状态；没有开发任务时不假设部署等条件已触发，也不加载所有条件规则全文。
- 今日当前项目的 Worklog 成果、进展、Blocker、待补录项和 Worklog 层健康状态。
- 每个已配置 Agent 适配器的模式、目标、桥接版本、标记完整性和同步状态；合并报告共享同一物理目标的客户端。
- 基于依赖、优先级和 Blockers 给出的下一步建议，并明确标注为建议而非既定任务。

不得在 `/kb-status` 中静默修改文件；需要同步时先说明并在用户任务授权范围内执行进度更新。

### `/kb-read [关键词/目录]`

1. 重新读取配置，并先读取 Shared Index、Dashboard 进度区和 Current Sprint。
2. 默认同时搜索项目层与共享层。参数 `shared` 或 `project` 可限定范围；目录编号/名称把搜索限制在对应范围，否则作为字面关键词。
3. 使用内置搜索工具，或使用通用回退：

   ```bash
   find "{Search_Root}" -type f -name '*.md' \
     -exec grep -nHiF -- "{Keyword}" {} +
   ```

4. 读取候选 Frontmatter、命中上下文和必要正文，按 Wikilink 最多扩展一跳。普通知识默认最多注入 5 篇最相关文档；该限制及一跳限制不适用于已命中规则和其执行所必需的引用。规则按 Rule loading 协议单独加载，不能用 top-k 检索代替规则筛选。
5. 优先使用 `status: Active` 且 `applies_to` 匹配的共享知识；按 Mandatory、项目显式覆盖、Default、Advisory 的顺序处理。把 Draft 标为未验证，Deprecated 仅作历史背景。
6. 注入摘要必须包含结论、适用条件、状态和项目相对来源路径。未命中时明确说明。

参数为空时从当前任务提取 2–6 个高辨识度关键词；没有任务上下文时只展示 Dashboard 与目录入口。
