---
title: 'Git Workflow (April 2026)'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Git Workflow (April 2026)

## Overview

### Branch Roles

- `main`: canonical integration and release baseline for this repository.
- Additional long-lived branches are opt-in. Do not assume `dev` exists unless the repository actually introduces it.

### Branch Types

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

## Authority Boundary

### Rules

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

## Governance Context

This rule applies bootstrap approval boundaries and quality evidence to local
Git history. It owns branch and finish behavior, while the active Task owns the
requested scope and evidence, GitHub controls own remote branch protection, and
the human owns merge, push, publish, discard, and history-recovery decisions.

## Current Contract

### Pull Requests

- Default PR target: `main`.
- Draft or WIP PRs may be opened for early CI feedback, but they are not ready for review or merge until required checks pass and verification evidence is complete.
- Require verification evidence before merge (tests, checks, or runbook validation).
- Required checks must match the active GitHub branch protection or ruleset, not stale local assumptions.
- Keep PR scope aligned to one plan/task slice where possible.

## Validation and Refresh

### Branch Completion Strategy

Use this sequence before presenting merge, PR, keep, or discard options.

1. Verify the relevant local checks for the changed scope. At minimum, run
   `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .` for
   governance/docs/runtime changes.
2. Detect whether the workspace is a normal checkout, linked worktree, or
   detached HEAD before deciding cleanup behavior.
3. Determine the base branch from repository evidence. The default base is
   `main` unless the active task/plan explicitly states otherwise.
4. Present explicit finish options:
   - merge locally to the base branch,
   - push and create a pull request,
   - keep the branch as-is,
   - discard the work.
5. Do not merge, push, delete, reset, clean, or remove a worktree unless the
   human explicitly selects that option.
6. Discard is destructive. Before any discard action, list the branch, commits,
   and affected worktree path, then require exact typed confirmation such as
   `discard`.
7. For PR creation, preserve the working branch/worktree for review iteration.
8. For local merge or discard, clean only worktrees created and owned by the
   active workflow; do not remove host-managed workspaces.

## Related Documents

- [Harness Approval Boundaries](approval-boundaries.md)
- [Agent Quality Standards](quality-standards.md)
- [Postflight Checklist](postflight-checklist.md)
- [Agentic Execution Rules](agentic.md)
