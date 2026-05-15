# Git Workflow (April 2026)

## Branch Roles

- `main`: canonical integration and release baseline for this repository.
- Additional long-lived branches are opt-in. Do not assume `dev` exists unless the repository actually introduces it.

## Branch Types

- `feat/<scope>-<slug>`
- `fix/<scope>-<slug>`
- `docs/<scope>-<slug>`
- `refactor/<scope>-<slug>`
- `chore/<scope>-<slug>`
- `ci/<scope>-<slug>`
- `release/<version-or-slug>`
- `hotfix/<scope>-<slug>`
- `codex/<scope>-<slug>`
- `dependabot/<ecosystem-or-scope>`

## Rules

- Start normal work from `main`.
- Start hotfix work from `main`.
- Use Conventional Commit messages.
- Keep commits atomic and traceable to spec/task IDs.
- Do not force-push protected branches.
- Keep local guidance aligned with the active GitHub branch protection or ruleset configuration. If repository defaults change, update this file in the same change window.
- Do not bypass the commit-msg hook with `--no-verify`. Commitizen enforces Conventional Commit format; bypassing it leaves malformed messages in the permanent history.

## Pull Requests

- Default PR target: `main`.
- Require verification evidence before merge (tests, checks, or runbook validation).
- Required checks must match the active GitHub branch protection or ruleset, not stale local assumptions.
- Keep PR scope aligned to one plan/task slice where possible.
