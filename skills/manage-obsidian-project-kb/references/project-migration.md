# Project compatibility migration

仅实际升级/迁移项目或明确预览迁移影响时读取。配置与路径先按 `references/configuration.md` 验证；已绑定项目按 `references/rule-loading.md` 加载适用规则。实际写入前读取 `references/write-safety.md`，规则迁移读取 `references/rule-maintenance.md`。--check 全程只读；自动迁移不走新项目初始化向导，也不创建项目来源记录。

## 3. Reconcile the current project

若请求启用自动迁移，在完整新版包核验成功后先按 `references/auto-migration.md` 持久化授权并报告结果。项目迁移失败不撤销已成功保存的授权；后续按实际文件恢复。仅安装更新但授权未保存成功时，不声称其他项目将自动迁移。

读取 `references/initialization.md`，按 `/kb-init` 运行已有配置校验、Git 本地忽略、目录及桥接对账。保持 Vault、Project_Name 和 Agent_Clients 选择；Schema 0/1 按协议备份后迁移，Schema 2 无需改写。适用标准区块更新至当前模板版本；导入桥接验证其导入目标，不能要求所有导入文件都有同一个版本标记。

配置缺失时先进行初始化向导取得必要的 Vault/项目选择，不猜测绑定。如果某个目标失败，报告部分状态并只继续无依赖的步骤。

成功确定来源且完成 Git 本地忽略检查后，可将已验证的 `source`、`installed_path`、`revision` 保存到项目本地 `.ai/kb-backups/upgrades/source.json`，供后续升级复用；值相同时不写入。该记录不替代实际文件校验，不保存凭据或带认证参数的 URL，不打包进可分发 Skill。--check 不创建记录。

## 4. Migrate rules conservatively

在已有锁顺序下处理 Shared，然后处理当前项目。修改前把来源笔记与索引保存为不覆盖的私有备份，核对内容未被其他 Agent 改动后再打补丁。

- 从现有规则正文提取已经明确的操作、模块、路径和环境条件，补齐 kind/load/triggers；条件明确时可将旧兼容加载迁移为 Conditional。这是本命令已授权的兼容性整理，不需每条重新确认。
- 保持实际适用范围、行为要求、enforcement 和 status 不变。始终适用的规则标记 Always；无法确定的旧 Mandatory 不写猜测的 triggers，继续兼容加载并列入待确认项。
- 已经有合法加载元数据且正文一致的来源保持不变，Catalog 独立对账；中断后来源已更新、索引未更新时仍须修复索引。保留原文历史，必要时局部补充验证/例外/证据说明；未知证据写未验证，不能编造。
- 类型判断明确时补 kind，但不得通过改类型移除原有强制要求。非规则知识只在整理必需时补类型，不重写全部 ADR、Runbook 或故障笔记。
- 同步来源、Change Log 与对应 Rule Catalog。对每个文件比较实际与期望内容，只有内容无差异才不写入或备份；即使业务语义不变，实际元数据迁移仍须备份并记录一次 Change Log。已记录的同一迁移不重复追加，Catalog 按来源去重。
- 不自动合并/废弃、降低强度、扩大项目范围、清除锁或执行知识笔记中的运维命令。这些不属于兼容升级。

Shared 在另一个项目升级时若已迁移且内容一致，自动 no-op，无需用户记住“共享层做过没有”。只看当前文件实际内容，不能依赖某个项目的升级成功标记来跳过检查。

## 5. Verify and report once

读取 `references/doctor.md` 并执行 `/kb-doctor`，读回配置、所有桥接和本次修改的规则/Catalog。检查标记唯一、未托管内容保留、条件与正文一致。再次计算同一升级的预期变更，确认已完成部分无差异；不要为了证明幂等性反复下载包、写备份或日志。

进行只读加载场景核对：文档任务跳过明确无关的条件规则，新增构建/迁移计划触发补读，旧 Mandatory 保持兼容，Catalog 漏项及超过 5 篇的命中规则不被截断。报告这是场景核对，不把它说成实际部署或完整客户端端到端测试。

仅实际持久变更时读取 `references/worklog-write.md`，按 Automatic Worklog 的稳定事件 ID 去重记录一次；完全无变化或 --check 不产生工作事件。中断后再次 `/kb-upgrade` 时重新检查实际内容并完成剩余项，已完成文件保持 no-op，失败项不能被整体成功标记掩盖。

若上次已完成持久变更但漏记日志，仅在 Change Log 等证据明确原日期、结果且事件尚不存在时，复用 `/kb-log --reconcile` 规则补录并标记 Reconstructed；不改成今天的新成果。证据不足时只报告待补录，不能凭现有版本推断曾经发生的升级事件。--check 始终只报告，不补录。

最终只给一份简短结果：包来源/实际版本、自动迁移启用状态及本机记录位置、项目桥接、Shared、项目规则、验证、备份位置，以及需用户处理的少量剩余项。区分 `Completed`、`Already current`、`Pending`；存在未完成项时使用“升级部分完成”，不能仅因桥接成功而说知识库全部迁移完毕。尚未使用的其他项目标为“使用时迁移”，不是“已升级”。
