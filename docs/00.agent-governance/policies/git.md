---
title: 'Git Policy'
version: "1.0.0"
type: governance/rule
status: active
owner: platform
updated: 2026-08-28
---

# Git Policy

## Overview

Keep local changes small, reviewable, and traceable to the active Spec and
Task. `main` is the default integration base unless repository evidence or the
approved Plan specifies another base.

## Authority Boundary

The user owns push, publication, merge, discard, and history recovery decisions.
Remote branch protection owns required hosted checks; local evidence cannot
waive them. [Approval and safety](approval-and-safety.md) governs exceptions.

## Governance Context

Inspect whether work is in a checkout, linked worktree, or detached HEAD.
Preserve user changes and host-managed workspaces. Use the active provider's
branch convention; Codex-created branches normally use `codex/`.

## Current Contract

- Before staging, inspect status and the relevant unstaged diff. Stage only
  the logical change and inspect `git diff --cached`.
- Use Conventional Commits with an imperative, specific summary; include the
  reason when it is not obvious. Keep commits aligned to Plan/Task units.
- Complete the [quality sequence](quality.md#canonical-completion-sequence)
  before each logical commit and branch finish. Never use `--no-verify`.
- Do not reset, restore away edits, clean, amend, rebase, force-push, delete
  branches, or remove worktrees without explicit approval for that operation.
  Prefer a forward corrective commit to rewriting shared history.
- Determine the PR base and inspect its diff. State scope, motivation, risk,
  validation, rollback, and limitations. Creating a PR or merging it requires
  the user's selection; a passing check is not permission.
- After verified implementation, offer the applicable merge, PR, keep, or
  discard choices without performing one implicitly.
- Before destructive discard, identify the branch, commits, and worktree and
  obtain exact confirmation. Clean only workflow-owned worktrees, never the
  user's main or host-managed workspace.

## Validation and Refresh

Inspect both staged and unstaged diffs after formatters. Rerun the affected
checks against final bytes. Keep branch protection assumptions evidence-backed;
do not claim a remote check ran from a local workflow-syntax result.

## Related Documents

- [Quality Policy](quality.md)
- [Approval and Safety](approval-and-safety.md)
- [Work Lifecycle](../skills/work-lifecycle.md)
