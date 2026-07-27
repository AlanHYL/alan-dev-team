# AlanDevTeam 🤖👥

**Fully Automated Multi-Agent Coding Team** — One command spins up a 10-role virtual development team, from requirements to delivery. Zero human intervention.

[![CI](https://github.com/AlanHYL/alan-dev-team/actions/workflows/ci.yml/badge.svg)](https://github.com/AlanHYL/alan-dev-team/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[中文](./README.md) | [English](./README.en.md)

```bash
alan init my-project && alan start ./my-project
```

## Architecture

10 Agent roles working in parallel with Observe-Think-Act event-driven loop:

| Role | Responsibility |
|------|---------------|
| PM | Requirements, user stories, acceptance criteria |
| Architect | Tech selection, API design, file ownership matrix |
| Dev-Backend | API, data layer, business logic |
| Dev-Frontend | UI components, pages, interactions |
| Breaker | Adversarial testing - break code to verify quality |
| QA | Test plans, full regression, coverage |
| Reviewer | Architecture compliance + code quality + business consistency |
| Integrator | Merge worktrees, resolve conflicts, per-step validation |
| Security | Security audit, vulnerability scanning |
| DevOps | Build verification, environment setup, deployment |

## Key Features

- **Parallel Development** — Each agent works in an isolated git worktree
- **File Ownership Matrix** — Each agent can only modify assigned files, preventing conflicts at the source
- **Triple Review Gate** — Architecture compliance + Code quality + Business consistency
- **Auto-Fix Loop** — Issues found → auto-fix → re-verify (up to 3 attempts)
- **Cross-Project Memory** — Lessons learned automatically accumulate and optimize future projects
- **Message Pool** — Agents communicate asynchronously via message pool (Observe-Think-Act)
- **Git Safety Net** — Test failures auto-rollback, never leave broken code
- **zcode Integration** — Built-in zcode Skill with PostToolUse Hook for event-driven agent responses

## Quick Start

```bash
# Create project scaffold
alan init my-blog --type web-flask

# Start full development
alan start ./my-blog

# Check progress
alan status ./my-blog

# View logs
alan log --tail

# Rate project (feedback loop)
alan feedback ./my-blog
```

### Project Types

| Type | Stack | Command |
|------|-------|---------|
| Web App | Flask + SQLite | `alan init app --type web-flask` |
| Frontend App | React + Vite | `alan init app --type web-react` |
| API Service | FastAPI | `alan init app --type api` |
| CLI Tool | Python | `alan init app --type cli` |
| **SaaS Multi-Tenant** | **FastAPI + React + PostgreSQL + Docker** | `alan init app --type saas` |

## CLI Commands

```bash
alan init <name>       Create project scaffold
alan start <path>      Start automated development
alan status [path]     View progress dashboard
alan log [--tail]      View logs
alan preview <path>    Sandbox preview changes
alan team              View team roster
alan tutorial          Interactive tutorial
alan doctor            System health check + self-heal
alan feedback <path>   Rate project (feedback loop)
```

## zcode Integration

AlanDevTeam is pre-installed as a zcode Skill:
- **Trigger in zcode**: `@alan-dev-team build me a blog`
- **Auto Message Pool**: Write/Edit operations automatically trigger PostToolUse Hook
- **Observe-Think-Act Loop**: Code changes → event-driven agent response

## Inspiration

This project builds upon ideas from state-of-the-art multi-agent systems:

- [MetaGPT](https://github.com/geekan/MetaGPT) — SOP-driven role specialization
- [AgentGrid](https://github.com/ishanavasthi/agentgrid) — Parallel worktree + adversarial testing
- [Agent-Collab](https://github.com/egesabanci/agent-collab) — Structured handoff protocol
- [Merge Orchestrator](https://github.com/krzemienski/multi-agent-merge-orchestrator) — File ownership matrix
- [SWE-AF](https://github.com/Agent-Field/swe-af) — Autonomous engineering fleet

## License

MIT
