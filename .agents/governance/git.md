---
title: "Git Policy"
version: "2.2.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-10-09"
---

# Git Policy

## Overview

Keep local changes small, reviewable, and traceable to the active Spec and
Task. `main` is the default integration base unless repository evidence or the
approved Plan specifies another base.

## Authority Boundary

The user owns push, publication, merge, discard, and history recovery decisions.
Remote branch protection owns any required hosted metadata checks and cannot
be inferred from local evidence. [Approval and safety](approval-and-safety.md)
governs protected actions and exceptions.

## Governance Context

Inspect whether work is in a checkout, linked worktree, or detached HEAD.
Preserve user changes and host-managed workspaces. Use the active provider's
branch convention; Codex-created branches normally use `codex/`.

## Current Contract

- Before staging, inspect status and the relevant unstaged diff. Stage only
  the logical change and inspect `git diff --cached`.
- Use Conventional Commits with an imperative, specific summary; include the
  reason when it is not obvious. Keep commits aligned to Plan/Task units.
- Validate the exact index with the selected staged profile before each logical
  commit, including required lint and format checks immediately before the
  commit. Local QA owns selected repository-static quality evidence. A feature
  push, PR or main merge does not itself select a retired full/ci sweep. Follow the
  [quality sequence](quality.md#canonical-completion-sequence) and do not repeat
  identical leaves across hook, command or delivery phases. Never use
  `--no-verify`.
- For a prose-only authored document or README router commit, keep the common
  diff, applicable style and Commitizen message checks and the selected
  document-content checks. Follow
  [ordinary document selection](quality.md#ordinary-document-selection); a
  governance, provider, native, schema, registry or executable change needs
  the focused contract checks its actual consumer selects. Preserve active
  hooks, and do not replay their identical result on push.
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

### Branch and integration routing

Develop each independently reviewable Spec package on an owned feature branch
and linked worktree when needed. Run changed-behavior and affected checks while
editing, exact-index and message checks at logical commits, then applicable
named purpose and unit checks on the bounded final branch snapshot. Push and PR
creation carry that evidence without re-executing the same leaf. Compare the
integrated main tree and history with what was checked; a changed merge input
gets only its invalidated checks, and an identical fast-forward does not replay
them. The hosted `ci-summary` job owns the PR branch-metadata verdict directly;
the hosted PR style job owns only its selected style verdict. Each observed
result has its own SHA and trust boundary and never stands in for local purpose,
unit or document-content checks. A deployment style result requires an actual
deployment workflow and run; absent that input, keep it unobserved. Observe
actual ruleset requirements before calling an integration accepted.

### Release ownership

Use one producer for a `v`-prefixed strict SemVer tag and its matching GitHub
Release, bound to an exact reviewed main commit. A development push or merge
does not create a release or move an existing tag. The producer verifies the
version, tag collision, main ancestry and canonical changelog before any
publication; an invalid or mismatched input fails closed. The current
release-preparation PR targeting `main` updates the tracked `CHANGELOG.md`
from integrated changes. The committed main file is the release history; a
temporary generated artifact is only review input and is never its owner.
Publication verifies changelog bytes captured from the exact main commit,
not a later working-tree edit. The remote draft and published Release must
match the reviewed tag, target, prerelease state, release notes and required
assets before
the operation counts as complete; the tag and prior changelog sections are
immutable history.
If immutable Releases are enabled, attach every required asset to the draft
before publication. Actual tag/Release publication, remote immutable-release
settings and rulesets require direct observation and their operator approval
route; a local script or workflow declaration is not such evidence. Keep
release procedure with the Stage 05 operations owner and execution evidence
with the Task and Git.

### Commit-message validation

[`.cz.toml`](../../.cz.toml) is the single Commitizen grammar owner for
supported types, optional scope, subject and body/footer syntax of ordinary
authored messages. [`.gitmessage`](../../.gitmessage) explains that grammar to
authors; a second commitlint grammar must not duplicate it. The configured
commit-msg hook is the local enforcement point. Exact generated Git `Merge` and
`Revert` syntax exceptions grant no merge or
history rewrite authority. The pinned Commitizen hook accepts these two prefixes;
the paired `scripts/commit-message-exceptions.py` hook narrows that acceptance
using the generated patterns in `.cz.toml`. These checks validate syntax only:
a manually authored message with the same shape also passes. They authenticate
neither Git generation, an actual merge/revert, nor its provenance or authority.
A prefix alone, `Pull request`,
`fixup!`, `squash!`, or `amend!` does not receive an exception. The configured
commit-msg stage permits an empty message so Git can abort the commit.

New authored messages require a supported type, an optional nonempty scope and
a nonblank subject. Unicode, type capitalization and final punctuation are
permitted. The grammar excludes embedded header line breaks and requires a blank
line before an optional body/footer. `type!:` and `type(scope)!:` mark breaking
changes, as do `BREAKING CHANGE:` and `BREAKING-CHANGE:` footers. Git-cliff's
case-consistent grouping consumes its native parsed breaking result, rather than
arbitrary prose elsewhere in a body. Generated Git `Revert` messages remain
non-conventional and are filtered from the changelog; use `revert(scope): subject`
when changelog inclusion is intended. Prefer an imperative, specific subject
under 72 characters; length, capitalization and body wrapping are guidance.
History is read without rewriting older messages.

The hosted PR title metadata route uses the trusted base's `.cz.toml` authored
schema, with no generated-message exceptions. Its tracked configuration does not
establish execution; the hosted result remains `NOT_RUN` until the actual PR SHA
and run are observed. A title result and selected PR style result do not validate
an authored squash message. If an operator chooses squash, validate the exact
proposed final commit message against both local message checks before that remote
merge. A successful title check does not authorize the merge.

Selected local file checks do not validate a commit message. Inspect the
effective `core.hooksPath` source and
hook connection, and preserve active hooks and private settings. If an active
hook has already run an identical leaf on the checked index, record that result
without manually replaying it; a different mode, tool or input is separate.

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
pre-commit run commit-message-exceptions --hook-stage commit-msg --commit-msg-filename "$MESSAGE_FILE"
```

Both checks must succeed on that same file; do not replay a leaf already
observed through an active hook on identical input/configuration. Use that file
for the real commit. When unrelated unstaged configuration would
make pre-commit stash or refuse, use an isolated temporary Git repository with
the index's Commitizen pin, `.cz.toml`, exception guard and both hook registrations,
and the same candidate message. This
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
