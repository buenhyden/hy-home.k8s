---
title: "Git Policy"
version: "1.4.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-09-10"
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
- Validate the exact index with the staged profile before each logical commit,
  and run the full profile once before branch finish or handoff. Both belong to
  the same [quality sequence](quality.md#canonical-completion-sequence); neither
  substitutes for the other, and neither is repeated on unchanged bytes.
  Never use `--no-verify`.
- Do not reset, restore away edits, clean, amend, rebase, force-push, delete
  branches, or remove worktrees without explicit approval for that operation.
  Prefer a forward corrective commit to rewriting shared history.
- Determine the PR base and inspect its diff. State scope, motivation, risk,
  validation, rollback, and limitations. Creating a PR or merging it requires
  the user's selection; a passing check is not permission.
- After verified implementation, honor the user's already selected finish action.
  If none is selected, ask; no passing check grants integration or cleanup authority.
- Before destructive discard, identify the branch, commits, and worktree and
  obtain exact confirmation. Clean only workflow-owned worktrees, never the
  user's main or host-managed workspace.

### Commit-message validation

[`.cz.toml`](../../.cz.toml) owns supported types, optional scope, subject and
body/footer syntax for ordinary authored messages. Its explicit generated-message
prefix exceptions retain Git/tool compatibility and grant no merge or history
rewrite authority. Git-cliff filters non-conventional history, including a
native `Revert` prefix; use `revert(scope): subject` when changelog inclusion is
intended. The hook permits an empty message only so Git can abort the commit.
A final ordinary subject period is rejected; breaking changes use
`BREAKING CHANGE:` in the footer because `type(scope)!` syntax is unsupported. Use an
imperative, specific subject, preferably under 72 characters. Length, case and
body wrapping are guidance, not extra validator rules. Historical parsers may
retain prior punctuation without permitting it in new messages.

Full QA checks files through the manual stage and does not validate a commit
message. Inspect the effective `core.hooksPath` source and hook connection, and
preserve active hooks and private settings.

Git honours one hook directory, so a user-global `core.hooksPath` makes this
repository's own hooks unreachable and silently drops the commit-message check
and every staged formatter. The supported repair is to widen what runs, never
to choose one side: this repository's `core.hooksPath` points at
`scripts/githooks`, whose entries run the user's global hook first and then the
workspace hook, returning the first non-zero status unchanged. Enable it once
per clone with `git config core.hooksPath scripts/githooks`; it is local
configuration, not tracked state, so a fresh clone runs whatever the user's
global configuration alone provides until it is set.

The chain reaches exactly the hooks that directory has an entry for. A global
hook of any other name stops running the moment this repository's
`core.hooksPath` is set, which is the same silent loss the repair exists to
prevent, so widening it to a new hook means adding the matching entry rather
than assuming the chain already covers the name.

If the same message is not checked by an active commit-msg hook, validate the
actual UTF-8 message file in the pinned pre-commit environment before
committing:

```bash
pre-commit run commitizen --hook-stage commit-msg --commit-msg-filename "$MESSAGE_FILE"
```

Use that file for the real commit. When unrelated unstaged configuration would
make pre-commit stash or refuse, use an isolated temporary Git repository with
the index's Commitizen pin/configuration and the same candidate message. This
is explicit message evidence, not proof of hook installation or delivery in
the source repository. Never change hooksPath, disable a hook, or set a skip
variable in order to make a failing check pass or to leave a check unrun;
widening the set of hooks that run is the only supported change.

## Validation and Refresh

Inspect both staged and unstaged diffs after formatters. Rerun the affected
checks against final bytes. Keep branch protection assumptions evidence-backed;
do not claim a remote check ran from a local workflow-syntax result.

## Related Documents

- [Quality Policy](quality.md)
- [Approval and Safety](approval-and-safety.md)
- [Work Lifecycle](../workflows/work-lifecycle.md)
