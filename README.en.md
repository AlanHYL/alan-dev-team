# AlanDevTeam 🤖👥

[![CI](https://github.com/AlanHYL/alan-dev-team/actions/workflows/ci.yml/badge.svg)](https://github.com/AlanHYL/alan-dev-team/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/AlanHYL/alan-dev-team?style=social)](https://github.com/AlanHYL/alan-dev-team)

**Fully Automated Multi-Agent AI Coding Team** — One command spins up 10 AI agents (PM, Architect, Developers, QA, Security) that autonomously plan, code, test, review, and deliver production-grade software. Zero human intervention from requirements to deployment.

🇨🇳 [中文](./README.md) | 🌍 [English](./README.en.md)

```bash
alan init my-project && alan start ./my-project
```

---

## System Requirements

- **Python 3.12+** (required)
- **Git** (required)
- **Node.js** (required for some project types)
- Supports Windows / macOS / Linux

## Installation

For **first-time users**, Activate the `alan` command:

```bash
# Git Bash (Linux/macOS terminal)
source ~/.bashrc

# PowerShell
function alan { python "$env:USERPROFILE\.zcode\alan-dev-team\cli\alan.py" @args }
```

Verify it works:

```bash
alan doctor
```

You should see `✅ 系统健康` (System Healthy).

## Quick Start

```bash
# Create project scaffold
alan init my-blog --type web-flask

# Start full development (10 agents work in parallel)
alan start ./my-blog

# Check progress dashboard
alan status ./my-blog

# View agent logs
alan log --tail

# Rate the project (feedback loop, system learns from it)
alan feedback ./my-blog
```

## Architecture

10 AI agent roles working in parallel with Observe-Think-Act event-driven loop:

| Role | Responsibility |
|------|---------------|
| PM | Requirements, user stories, acceptance criteria |
| Architect | Tech selection, API design, file ownership matrix |
| Dev-Backend | API, data layer, business logic |
| Dev-Frontend | UI components, pages, interactions |
| Breaker | Adversarial testing - break code to verify quality |
| QA | Test plans, full regression, coverage >= 70% |
| Reviewer | 3-layer review: architecture + quality + business consistency |
| Integrator | Merge worktrees, resolve conflicts, per-step validation |
| Security | Security audit, vulnerability scanning |
| DevOps | Build verification, environment, deployment |

## Key Features

- **Parallel Development** — Each agent works in an isolated git worktree, no interference
- **File Ownership Matrix** — Each agent can only modify assigned files, preventing conflicts at source
- **Triple Review Gate** — Architecture compliance + Code quality + Business consistency (all must pass)
- **Auto-Fix Loop** — Issues found → auto-fix → re-verify (up to 3 attempts)
- **Cross-Project Memory** — Lessons learned automatically accumulate across projects
- **Message Pool** — Agents communicate asynchronously via event-driven message pool
- **Git Safety Net** — Test failures auto-rollback, never leave broken code
- **zcode / Claude Code Integration** — Built-in Skill with Hooks for event-driven agent responses

## Project Types

| Type | Stack | Command |
|------|-------|---------|
| Web App | Flask + SQLite | `alan init app --type web-flask` |
| Frontend App | React + Vite | `alan init app --type web-react` |
| API Service | FastAPI | `alan init app --type api` |
| CLI Tool | Python | `alan init app --type cli` |
| **SaaS Multi-Tenant** | **FastAPI + React + PostgreSQL + Docker** | `alan init app --type saas` |

## CLI Commands

```bash
alan init <name>       Create project scaffold (5 types)
alan start <path>      Start automated development pipeline
alan status [path]     View real-time progress dashboard
alan log [--tail]      View centralized agent logs
alan preview <path>    Sandbox preview pending changes
alan team              View team roster (10 agents)
alan tutorial          Interactive beginner tutorial
alan doctor            Full health check + auto-repair
alan feedback <path>   Rate project quality (1-5)
```

## zcode / Claude Code Integration

AlanDevTeam is pre-installed as a built-in zcode Skill:
- **Trigger in zcode**: `@alan-dev-team build me a blog`
- **Auto Message Pool**: Write/Edit operations automatically trigger PostToolUse Hook
- **Observe-Think-Act Loop**: Code changes → event-driven agent responses

## Inspiration

This project builds upon ideas from state-of-the-art multi-agent AI systems:

- [MetaGPT](https://github.com/geekan/MetaGPT) — SOP-driven role specialization (69k ⭐)
- [AgentGrid](https://github.com/ishanavasthi/agentgrid) — Parallel worktree + adversarial testing
- [Agent-Collab](https://github.com/egesabanci/agent-collab) — Structured handoff protocol
- [Merge Orchestrator](https://github.com/krzemienski/multi-agent-merge-orchestrator) — File ownership matrix
- [SWE-AF](https://github.com/Agent-Field/swe-af) — Autonomous engineering fleet

## License

MIT — Free to use, modify, and distribute.
