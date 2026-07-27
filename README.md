# AlanDevTeam 🤖👥

[![CI](https://github.com/AlanHYL/alan-dev-team/actions/workflows/ci.yml/badge.svg)](https://github.com/AlanHYL/alan-dev-team/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/AlanHYL/alan-dev-team?style=social)](https://github.com/AlanHYL/alan-dev-team)

**全自动多 Agent 编码团队** — 一个命令启动 10 人虚拟开发团队，从需求到交付全自动。

🇨🇳 [中文](./README.md) | 🌍 [English](./README.en.md)

```
alan init my-project && alan start ./my-project
```

## 架构

10 个 Agent 角色并行协作，Observe-Think-Act 事件驱动循环：

| 角色 | 职责 |
|------|------|
| PM | 需求分析、用户故事、验收条件 |
| Architect | 技术选型、API设计、文件所有权矩阵 |
| Dev-Backend | 后端 API、数据层、业务逻辑 |
| Dev-Frontend | UI 组件、页面、交互逻辑 |
| Breaker | 敌对测试——攻破代码验证质量 |
| QA | 测试计划、全量回归、覆盖率 |
| Reviewer | 架构合规 + 代码质量 + 业务一致审查 |
| Integrator | 合并 worktree、解决冲突、每步验证 |
| Security | 安全审计、漏洞扫描 |
| DevOps | 构建验证、环境配置、部署 |

## 核心特性

- **并行开发** — 每个 Agent 在隔离的 git worktree 中工作，互不干扰
- **文件所有权矩阵** — 每个 Agent 只能修改分配的文件，从源头防冲突
- **三重审查门禁** — 架构合规 + 代码质量 + 业务一致
- **自动修复循环** — 发现问题 → 自动修复 → 再验证（最多 3 次）
- **跨项目记忆** — 每个项目的经验教训自动积累，下次项目自动优化
- **消息池通信** — Agent 通过消息池异步通信，Observe-Think-Act 事件驱动
- **Git 安全网** — 测试失败自动回滚，绝不留下破损代码

## 快速开始

```bash
# 安装（已安装则跳过）
source ~/.bashrc

# 创建项目脚手架
alan init my-blog --type web-flask

# 启动全自动开发
alan start ./my-blog

# 查看进度
alan status ./my-blog

# 查看日志
alan log --tail

# 项目评分（反馈闭环）
alan feedback ./my-blog
```

### 项目类型

| 类型 | 技术栈 | 命令 |
|------|--------|------|
| Web 应用 | Flask + SQLite | `alan init app --type web-flask` |
| 前端应用 | React + Vite | `alan init app --type web-react` |
| API 服务 | FastAPI | `alan init app --type api` |
| CLI 工具 | Python | `alan init app --type cli` |
| **SaaS 多租户** | **FastAPI + React + PostgreSQL + Docker** | `alan init app --type saas` |

## 系统命令

```bash
alan init <name>       创建项目脚手架
alan start <path>      启动全自动开发
alan status [path]     查看进度仪表盘
alan log [--tail]      查看日志
alan preview <path>    沙箱模式预览变更
alan team              查看团队阵容
alan tutorial          新手引导
alan doctor            系统健康检查 + 自愈
alan feedback <path>   给项目评分反馈
```

## 与 zcode 集成

AlanDevTeam 作为 zcode Skill 已预装，支持：
- **zcode 中触发**：`@alan-dev-team 帮我创建一个博客`
- **自动消息池**：Write/Edit 操作自动触发 PostToolUse Hook
- **Observe-Think-Act 循环**：代码变更 → 事件驱动 Agent 响应

## 架构设计

本项目参考了以下业界领先的多 Agent 系统：

- [MetaGPT](https://github.com/geekan/MetaGPT) — SOP 驱动角色分工
- [AgentGrid](https://github.com/ishanavasthi/agentgrid) — 并行 Worktree + 敌对测试
- [Agent-Collab](https://github.com/egesabanci/agent-collab) — 结构化交接协议
- [Merge Orchestrator](https://github.com/krzemienski/multi-agent-merge-orchestrator) — 文件所有权矩阵
- [SWE-AF](https://github.com/Agent-Field/swe-af) — 自治工程舰队

## 许可证

MIT
