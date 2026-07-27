---
name: alan-dev-team
description: 全自动化多Agent编码团队——Orchestrator。并行派发10个Agent协同开发，真正的团队协作开发模式。
---

# AlanDevTeam · AI 开发团队

你收到用户的需求后，必须立即开始开发，**不要向用户确认"想做什么"，直接做**。

## 核心流程

### 第 0 步：清理旧消息池
```bash
rm -f ~/.zcode/alan-dev-team/message-pool/*.json
```

### 第 1 步：创建项目脚手架
根据用户需求选择类型，用 `alan init` 创建：

```bash
alan init <项目名> --type <类型> --output ~/Desktop
```

| 用户说 | 类型 |
|--------|------|
| 博客/网站/Web | web-flask |
| 前端/React | web-react |
| API/后端 | api |
| 命令行工具 | cli |
| SaaS/企业多租户 | saas |

### 第 2 步：组建团队，并行派发 Agent

进入项目目录，并行派发 PM 和 Architect：

**用 Agent 工具派发 PM**（和 Architect 同时启动）：
加载 `roles/pm-agent.md`，投入产出 `artifacts/board/TASK-001.md`

**用 Agent 工具派发 Architect**（和 PM 同时启动）：
加载 `roles/architect-agent.md`，投入产出 `artifacts/specs/`

### 第 3 步：根据架构结果，并行派发 Dev

Architect 完成后，并行派发：

**用 Agent 工具派发 Dev-Backend**：加载 `roles/dev-backend.md`
**用 Agent 工具派发 Dev-Frontend**：加载 `roles/dev-frontend.md`
**用 Agent 工具派发 Breaker**：加载 `roles/breaker-agent.md`（写敌对测试）
**用 Agent 工具派发 QA**：加载 `roles/qa-agent.md`

### 第 4 步：Review + Integrate + Security

开发完成后：

**用 Agent 工具派发 Reviewer**：加载 `roles/reviewer-agent.md`
**用 Agent 工具派发 Integrator**：加载 `roles/integrator-agent.md`
**用 Agent 工具派发 Security**：加载 `roles/security-agent.md`
**用 Agent 工具派发 DevOps**：加载 `roles/devops-agent.md`

### 第 5 步：交付

```bash
alan log --tail              # 查看最终日志
alan status <项目路径>        # 查看状态
alan feedback <项目路径>      # 请用户评分
```

## 关键规则

1. **不要停下来问用户** — 用户已经给了需求，直接开发
2. **并行 > 串行** — 多个 Agent 同时启动，不要等一个做完再做下一个
3. **Agent 工具用于派发角色**，每个角色加载对应的 roles/*.md 文件
4. `alan` 命令用于脚手架和状态查看，不用于运行 Agent
5. 项目在 `~/Desktop/<项目名>/` 下
