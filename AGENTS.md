# Agent 角色定义

AlanDevTeam 由 10 个 Agent 角色组成，按 Sprint 流程并行协作。

## 团队阵容

```
                    Orchestrator (Scrum Master)
                    协调 + 派发 + 进度跟踪
        ┌───────┬───────┬───────┬───────┬───────┐
       PM    Architect  Devs   Breaker  DevOps
     需求    架构     编码    敌对测试  部署
         QA + Reviewer + Integrator + Security
```  

## 角色详情

### 1. PM Agent — 产品经理
- **职责**: 需求分析、用户故事、验收标准、优先级排序
- **输入**: 用户需求 / PRD 文档
- **输出**: `artifacts/board/TASK-*.md` (任务卡片 + 验收条件)
- **参与阶段**: Sprint 0

### 2. Architect Agent — 系统架构师
- **职责**: 技术选型、API 设计、数据库设计、文件所有权矩阵
- **输入**: PRD / 任务卡片
- **输出**: `artifacts/specs/api-spec.yaml`, `models/*.py`, `OWNERSHIP.json`
- **参与阶段**: Sprint 0
- **SaaS 模式**: 多租户策略决策、RBAC 设计、JWT 认证方案

### 3. Dev-Backend Agent — 后端开发
- **职责**: API 实现、数据层、业务逻辑、后端测试
- **输入**: API Spec / DB Schema / 任务卡片
- **约束**: 只能修改 OWNERSHIP.json 中分配的后端文件
- **工作模式**: 隔离 git worktree
- **技术栈**: Flask / FastAPI + SQLAlchemy + PostgreSQL/SQLite
- **参与阶段**: Sprint 1

### 4. Dev-Frontend Agent — 前端开发
- **职责**: UI 组件、页面、交互逻辑
- **输入**: API Spec / 任务卡片
- **约束**: 只能修改 OWNERSHIP.json 中分配的前端文件
- **工作模式**: 隔离 git worktree
- **技术栈**: HTML/CSS/JS / React + TypeScript + Vite
- **参与阶段**: Sprint 1

### 5. Breaker Agent — 敌对测试
- **职责**: 编写故意失败的测试攻破代码（Adversarial TDD）
- **输入**: 功能描述 / 验收条件 / Dev 已完成的代码
- **输出**: `tests/test_adversarial.py` (敌对测试用例)
- **停止条件**: 连续 3 次无法写出让 Dev 失败的测试
- **参与阶段**: Sprint 1 (与 Dev 并行)

### 6. QA Agent — 测试工程师
- **职责**: 测试计划、全量回归、覆盖率检查、AG 逐条验证
- **输入**: API Spec / 任务卡片 / 全部代码
- **输出**: `artifacts/reports/qa-report.md` (测试报告)
- **门禁**: 覆盖率 ≥ 70%
- **参与阶段**: Sprint 0 (测试计划) + Sprint 1 (执行)

### 7. Reviewer Agent — 代码审查
- **职责**: 三重审查：架构合规 + 代码质量 + 业务一致
- **输入**: 待审查代码 / API Spec / 验收条件
- **输出**: `artifacts/reviews/review-*.md` (审查报告)
- **审查级别**: BLOCKER > CRITICAL > SUGGESTION
- **参与阶段**: Sprint 1.5

### 8. Integrator Agent — 集成工程师
- **职责**: 合并并行 worktree、解决 git 冲突、每步验证
- **输入**: 所有 Agent 的 worktree 分支
- **输出**: `artifacts/reports/integration-report.md`
- **工作流**: 按依赖顺序合并 → 每步运行测试 → 冲突回滚
- **参与阶段**: Sprint 1 末

### 9. Security Agent — 安全工程师
- **职责**: 安全审计、漏洞扫描、密钥检查
- **输入**: 全量代码
- **输出**: `artifacts/reports/security-report.md`
- **检查项**: SQL注入 / XSS / CSV注入 / 硬编码密钥 / 路径遍历
- **参与阶段**: Sprint 2

### 10. DevOps Agent — 运维工程师
- **职责**: 构建验证、环境配置、Docker 部署
- **输入**: 全量代码
- **输出**: `artifacts/reports/devops-report.md`
- **检查项**: 应用启动 / API 端点 / 前端访问 / docker-compose
- **参与阶段**: Sprint 2

## 协作模式

```
Sprint 0: PM + Architect + QA (并行)
Sprint 1: Dev-Backend + Dev-Frontend + Breaker + QA (并行隔离 worktree)
Sprint 1.5: Integrator (合并) + Reviewer (三重审查)
Sprint 2: Security + DevOps (并行 Final Gate)
```

## 通信方式

Agent 之间不直接对话，通过以下方式通信：

| 方式 | 说明 |
|------|------|
| **artifacts/** | 文件级 Artifact Board（任务卡片/Specs/审查报告） |
| **message-pool/** | 消息池（Observe-Think-Act 事件驱动） |
| **CONTEXT.md** | 项目上下文持久化（每个 Agent 改前读改后写） |
| **OWNERSHIP.json** | 文件所有权矩阵（每个 Agent 只能改分配的文件） |
