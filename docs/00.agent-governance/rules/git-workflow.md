# Git Workflow (March 2026)

## Branch Roles

- `main`: production baseline.
- `dev`: integration baseline.

## Branch Types

- `feat/<scope>-<slug>`
- `fix/<scope>-<slug>`
- `docs/<scope>-<slug>`
- `refactor/<scope>-<slug>`
- `chore/<scope>-<slug>`
- `release/<version-or-slug>`
- `hotfix/<scope>-<slug>`

## Rules

- Start feature work from `dev`.
- Start hotfix work from `main`, then merge back to `main` and `dev`.
- Use Conventional Commit messages.
- Keep commits atomic and traceable to spec/task IDs.
- Do not force-push protected branches.

## Pull Requests

- Default PR target: `dev`.
- Require verification evidence before merge (tests, checks, or runbook validation).
- Keep PR scope aligned to one plan/task slice where possible.
