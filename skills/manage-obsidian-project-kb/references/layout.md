# Vault layout and routing

仅在初始化目录、保存永久笔记或诊断目录布局时读取；检索使用已有配置和真实路径，无需先加载整棵目录规范。

## Folder Structure Rules

在 Vault 中同时维护共享层、项目层和跨项目工作日志层：

```text
{Vault_Path}/
├── {Shared_KB}/                 # 默认 Shared/
│   ├── 00-Index.md
│   ├── 05-Governance_&_Rules/
│   ├── 10-Domain_&_Contracts/
│   ├── 20-Architecture_&_Patterns/
│   ├── 30-Engineering_&_Standards/
│   ├── 40-Infra_&_Platforms/
│   ├── 50-Troubleshooting_&_Lessons/
│   └── 60-AI_&_Automation/
├── Projects/
│   └── {Project_Name}/
│       ├── 00-Index.md
│       ├── 05-Roadmap_&_Tasks/
│       │   ├── Current_Sprint.md
│       │   └── Archive/
│       ├── 10-Domain_&_Business/
│       ├── 20-Architecture_&_ADR/
│       ├── 30-Engineering_&_Tuning/
│       ├── 40-Infra_&_DevOps/
│       ├── 50-Troubleshooting/
│       └── 60-AI_&_Automation/
└── {Worklog_KB}/               # 默认 Worklog/
    ├── 00-Index.md
    ├── Daily/{YYYY}/{YYYY-MM}/
    └── Reports/{Weekly,Monthly,Custom}/
```

### Project routing rules

| Directory | Store here | Do not store here |
|---|---|---|
| `05-Roadmap_&_Tasks/` | 当前 Sprint、Milestone、任务、Blocker、路线图和历史 Sprint | 架构或排错正文 |
| `10-Domain_&_Business/` | 业务术语、聚合、领域模型、状态机、业务规则和 API 契约 | 框架调优细节 |
| `20-Architecture_&_ADR/` | 系统边界、拓扑、数据流、接口、租户隔离、安全模型和 ADR | 临时任务清单 |
| `30-Engineering_&_Tuning/` | 语言/框架机制、版本实践、并发模型、性能调优和工程规范 | 基础设施拓扑 |
| `40-Infra_&_DevOps/` | IaC、K8s、CI/CD、部署、数据库/缓存/日志拓扑和生命周期 | 应用层 Bug 复盘 |
| `50-Troubleshooting/` | 症状、诊断、根因、修复、验证、回归风险和复盘 | 未验证猜测 |
| `60-AI_&_Automation/` | 可复用提示词、Agent/CLI 配置、自动化脚本和 AI 工作流 | 密钥或机器私有凭据 |

内容同时涉及多个分类时，选择“主要知识价值”对应目录，拆成原子笔记，并用 Wikilinks 连接；不要复制相同正文到多个目录。

### Shared routing and precedence

| Shared directory | Store here |
|---|---|
| `05-Governance_&_Rules/` | 跨项目强制规则、安全/合规基线、命名和协作规范 |
| `10-Domain_&_Contracts/` | 共享术语、跨服务协议、公共事件和 API 契约 |
| `20-Architecture_&_Patterns/` | 可复用架构模式、参考拓扑和设计原则 |
| `30-Engineering_&_Standards/` | 编码、测试、版本、并发、性能和可观测性标准 |
| `40-Infra_&_Platforms/` | 公共平台、K8s、网络、数据库、缓存和 CI/CD 基线 |
| `50-Troubleshooting_&_Lessons/` | 已在多个项目验证的故障模式和组织级复盘 |
| `60-AI_&_Automation/` | 公共提示词、Agent 规则、CLI 工作流和自动化资产 |

- 共享笔记使用 `applies_to` 声明明确项目名或 `"*"`。规则使用 `enforcement: Mandatory | Default | Advisory` 声明约束强度，使用 `load: Always | Conditional` 与 `triggers` 声明加载时机；跨项目适用不等于每次任务都适用。
- 命中适用条件的 `Mandatory` 必须遵守；例外须记录批准依据、范围和结束条件并反向链接，不改变全局规则。Active 项目决策可覆盖 `Default`，`Advisory` 仅供参考。冲突必须向用户展示，不得静默选择。
- 只对两个及以上项目稳定复用的知识、公共契约或明确的组织规则使用共享层。单项目事实继续保存于项目层；不得复制共享正文到各项目。
