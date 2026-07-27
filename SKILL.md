---
name: alan-dev-team
description: 全自动化多Agent编码团队——Orchestrator。并行派发10个Agent协同开发，真正的团队协作开发模式。
---

# AlanDevTeam · AI 开发团队

你收到用户的需求后，必须立即开始执行以下步骤。**不要停下来问用户，直接做。**

## 第 0 步：清理并预检

```bash
rm -f ~/.zcode/alan-dev-team/message-pool/*.json
alan doctor
```

## 第 1 步：创建项目 + 定义文件所有权矩阵

根据用户需求创建脚手架，然后 Architect 定义每个 Agent 能改什么文件：

```bash
alan init <项目名> --type <类型> --output ~/Desktop
```

建好后，立即用 **Agent 工具派发 Architect**（加载 `roles/architect-agent.md`），让其产出：
- `artifacts/specs/api-spec.yaml` — API规范
- `artifacts/specs/db-schema.sql` — 数据库设计  
- **`OWNERSHIP.json`** — 文件所有权矩阵（这是关键：明确每个Agent能改什么文件）

**与 Architect 同时，派发 PM**（加载 `roles/pm-agent.md`），产出任务卡片。

**与 Architect 同时，派发 QA**（加载 `roles/qa-agent.md`），产出测试计划。

## 第 2 步：创建隔离 Worktree + 并行派发 Dev

Architect 完成后，运行：

```bash
python ~/.zcode/alan-dev-team/scripts/worktree-manager.py init --project <项目路径>
python ~/.zcode/alan-dev-team/scripts/worktree-manager.py assign --agent Dev-Backend --files "app.py,models.py"
python ~/.zcode/alan-dev-team/scripts/worktree-manager.py assign --agent Dev-Frontend --files "static/**,templates/**"
python ~/.zcode/alan-dev-team/scripts/worktree-manager.py assign --agent Breaker --files "tests/test_adversarial.py"
python ~/.zcode/alan-dev-team/scripts/worktree-manager.py create-worktrees
```

然后在各隔离 worktree 中并行派发 Agent：

**用 Agent 工具派发 Dev-Backend**（在 `../<项目名>-dev-backend/` 中工作）：
加载 `roles/dev-backend.md`，只允许修改 `app.py, models.py`

**用 Agent 工具派发 Dev-Frontend**（在 `../<项目名>-dev-frontend/` 中工作）：
加载 `roles/dev-frontend.md`，只允许修改 `static/**, templates/**`

**用 Agent 工具派发 Breaker**（在 `../<项目名>-breaker/` 中工作）：
加载 `roles/breaker-agent.md`，写敌对测试试图攻破代码

**用 Agent 工具派发 QA**：
加载 `roles/qa-agent.md`，执行测试

## 第 3 步：Integrator 合并 Worktree

并行开发完成后：

```bash
python ~/.zcode/alan-dev-team/scripts/worktree-manager.py merge
```

然后用 **Agent 工具派发 Integrator**（加载 `roles/integrator-agent.md`）：
- 检查每个 Agent 的文件所有权合规
- 按依赖顺序合并（后端→前端）
- 每步运行测试验证
- 产生集成报告

## 第 4 步：Review Gate + Security + DevOps

**用 Agent 工具派发 Reviewer**（加载 `roles/reviewer-agent.md`）：
- 三重审查：架构合规 + 代码质量 + 业务一致
- 输出审查报告

**用 Agent 工具派发 Security**（加载 `roles/security-agent.md`）

**用 Agent 工具派发 DevOps**（加载 `roles/devops-agent.md`）

## 第 5 步：记录经验 + 交付

```bash
# 记录项目经验到长期记忆
python ~/.zcode/alan-dev-team/scripts/lesson-learner.py \
  --project <项目名> --dir <项目路径> \
  --learn "<总结的经验教训>" \
  --agent "Dev-Backend:<改进建议>" \
  --agent "Dev-Frontend:<改进建议>"

alan log --tail              # 查看日志
alan status <项目路径>        # 查看最终状态
```

向用户交付最终项目路径和启动方式。

## 关键规则

1. **不要停下来问用户** — 直接做
2. **Worktree 隔离** — 每个 Dev 在自己的 worktree 中工作，互不干扰
3. **所有权矩阵** — Agent 只能修改分配给它的文件
4. **Integrator 合并** — 按依赖顺序合并，每步测试验证
5. **经验记录** — 项目完成后必须记录经验教训
