# Changelog

## [1.0.0] - 2026-07-28

### Added
- 10-role multi-agent team (PM, Architect, Dev-Backend, Dev-Frontend, Breaker, QA, Reviewer, Integrator, Security, DevOps)
- `alan` CLI with 9 commands (init, start, status, log, preview, team, tutorial, doctor, feedback)
- Parallel git worktree isolation for conflict-free multi-agent development
- File ownership matrix to prevent cross-agent file conflicts
- Observe-Think-Act event-driven loop via zcode PostToolUse Hooks
- Triple review gate (architecture compliance + code quality + business consistency)
- Auto-fix loop with 3-strike protocol
- Cross-project memory system (lesson-learner)
- Message pool for asynchronous agent communication
- Git safety net (test-fail-rollback)
- Project scaffolding for 5 types (web-flask, web-react, api, cli, saas)
- SaaS multi-tenant template (FastAPI + React + PostgreSQL + Docker)
- Sandbox preview mode
- System health check with auto-repair (`alan doctor`)
- New user tutorial (`alan tutorial`)
- Feedback loop for continuous improvement
- GitHub Actions CI/CD
- zcode native integration (Hooks + Skills)
