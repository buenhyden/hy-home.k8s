# Git Workflow (April 2026)

## Branch Roles

- `main`: canonical integration and release baseline for this repository.
- Additional long-lived branches are opt-in. Do not assume `dev` exists unless the repository actually introduces it.

## Branch Types

- `feat/<scope>-<slug>`
- `fix/<scope>-<slug>`
- `docs/<scope>-<slug>`
- `refactor/<scope>-<slug>`
- `test/<scope>-<slug>`
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
- When a human requests commits, split them by logical task unit; stage only the
  files for that unit and review `git diff --cached` before each commit.
- If a broad commit has already been published to a shared branch, do not
  rewrite it for cleanup without explicit approval. Record the exception in the
  active SDD task/plan and use a forward-only corrective commit instead.
- Do not force-push protected branches.
- Do not run destructive or history-rewriting Git commands from the default
  agent path. Shared Claude permissions deny `git reset --hard`,
  `git checkout --`, `git restore`, `git clean`, `git rebase`,
  `git commit --amend`, `git branch -D`, `git push --force`, `git push -f`,
  `git push --delete`, and `git push --mirror`.
- If a human explicitly approves one of those command classes for recovery,
  record the approval scope, target branch, rollback or backup expectation,
  and verification evidence in the active SDD task/plan before taking action.
- Every pull request targeting `main` must run the required CI and branch-policy checks with no bypass exceptions.
- Keep local guidance aligned with the active GitHub branch protection or ruleset configuration. If repository defaults change, update this file in the same change window.
- Do not bypass the commit-msg hook with `--no-verify`. Commitizen enforces Conventional Commit format; bypassing it leaves malformed messages in the permanent history.
- Apply the coverage policy in `quality-standards.md`: future testable application code targets 90% coverage where applicable, while current infra-only Bash/YAML/Markdown work uses validation-matrix coverage.

## Pull Requests

- Default PR target: `main`.
- Draft or WIP PRs may be opened for early CI feedback, but they are not ready for review or merge until required checks pass and verification evidence is complete.
- Require verification evidence before merge (tests, checks, or runbook validation).
- Required checks must match the active GitHub branch protection or ruleset, not stale local assumptions.
- Keep PR scope aligned to one plan/task slice where possible.
