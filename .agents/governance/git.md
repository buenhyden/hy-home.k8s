---
title: "Git Policy"
version: "2.6.1"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-13"
---

# Git Policy

## Purpose

### Objective

Keep local changes small, reviewable, and traceable to the active Spec and
Task. `main` is the default integration base unless repository evidence or the
approved Plan specifies another base.

### Authority

The user owns push, publication, merge, discard, and history recovery decisions.
Remote branch protection owns any required hosted metadata checks and cannot
be inferred from local evidence: observe it before reporting that an
integration met its required checks; Acceptance stays a criterion decision.
[Approval and safety](approval-and-safety.md)
governs protected actions and exceptions.

- [Quality Policy](quality.md)
- [Approval and Safety](approval-and-safety.md)
- [Work Lifecycle](../workflows/work-lifecycle.md)

## Scope

### Applies To

Inspect whether work is in a checkout, linked worktree, or detached HEAD.
Preserve user changes and host-managed workspaces. Use the active provider's
branch convention; Codex-created branches normally use `codex/`.

### Exclusions

This policy excludes no subject within its scope; if one is excluded, name it and its owner here.

## Rules

### Requirements

- Before staging, inspect status and the relevant unstaged diff. Stage only
  the logical change and inspect `git diff --cached`.
- Use Conventional Commits with an imperative, specific summary; include the
  reason when it is not obvious. Keep commits aligned to Plan/Task units.
- Commit through the active hooks: the `staged-qa` hook validates the exact
  index with the selected staged profile, which includes the selected lint and
  format gate, as one run. Local QA owns selected repository-static quality
  evidence. Follow the
  [quality sequence](quality.md#canonical-completion-sequence) and do not repeat
  an identical leaf across hook, command, push or delivery phases. Never use
  `--no-verify`.
- For a prose-only authored document or README router commit, keep the common
  diff, applicable style and Commitizen message checks and the selected
  document-content checks. Follow
  [ordinary document selection](quality.md#ordinary-document-selection); a
  governance, provider, native, schema, registry or executable change needs
  the focused contract checks its actual consumer selects. Preserve active
  hooks.
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

#### Branch and integration routing

`main` is the only long-lived branch; feature branches and the
`release/<tag>` preparation branch are short-lived (ADR-0052 in the
[ADR log](../../docs/02.architecture/decisions/README.md)).
Develop each independently reviewable Spec package on an owned feature branch
and linked worktree when needed. Run changed-behavior and affected checks while
editing, exact-index and message checks at logical commits, then applicable
named purpose and unit checks on the bounded final branch snapshot. Compare the
integrated main tree and history with what was checked; a changed merge input
gets only its invalidated checks. The hosted `ci-summary` job owns the PR branch and commit-metadata verdict directly;
the hosted PR style job owns only its selected style verdict. Each observed
result has its own SHA and trust boundary and never stands in for local purpose,
unit or document-content checks. `ci-summary` accepts a pull request only
when its base is `main` and its head branch starts with one of `feat/`, `fix/`,
`docs/`, `refactor/`, `test/`, `chore/`, `ci/`, `release/`, `hotfix/`, `codex/`,
`claude/` or `dependabot/`. Every change to `main` arrives by pull
request; the intended protection blocks direct and force pushes. A pull
request completes only when the required checks pass, the review requirement
is met (no approving review is required, count 0, and no CODEOWNERS review,
because a sole owner cannot approve their own pull request) and the
core-diff checklist of the final diff records no unresolved `BLOCK` finding
([semantic review](quality.md#semantic-review)); an extra agent review is
optional and never required.
The repository owner (`@buenhyden`) merges the pull request, or explicitly
directs its merge, using a merge commit only, so the commits a Task cites stay
reachable; an administrator bypass (`--admin`) is never used. The intended
repository merge setting is recorded in `.github/rulesets/main-protection.md`.
Required checks, the checklist review and the owner's merge or explicit merge
direction together offset the missing second reviewer; no automated check, App
or signature replaces the owner's approval. A deployment style result requires
an actual deployment workflow and run; absent that input, keep it unobserved.

#### Release ownership

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

#### Commit-message validation

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

Hosted `ci-summary` checks a PR title only against the trusted base's
`.cz.toml` authoring schema; generated-message exceptions do not apply to
titles. It checks newly introduced commit messages in `base..head`, including
merge commits, against that base's grammar and generated `Merge` and `Revert`
patterns. It first binds the exact PR event base, head, and merge SHA and the
merge commit's parent relationship. The [CI workflow](../../.github/workflows/ci.yml)
and [its static validator](../../scripts/validate-ci-python-contract.py) own
the execution conditions; the [hosted surface](../../.github/repository-surface.md)
explains where results are consumed. Tracked configuration alone does not
prove execution. Hosted results remain `NOT_RUN` until an actual PR SHA and
run are observed. Grammar checks do not authenticate Git generation, origin,
approval, or merge authority. PR title and selected style results do not
validate a merge commit message, so check the merge message that would be
generated before remote merge with both local message checks.

Selected local file checks do not validate a commit message. Inspect the
effective `core.hooksPath` source and
hook connection, and preserve active hooks and private settings.

Git honours one hook directory, so a user-global `core.hooksPath` makes this
repository's own hooks unreachable and silently drops the commit-message checks
and mandatory selected staged QA and style checks. The supported repair widens
what runs: this repository's `core.hooksPath` points at
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

The workspace hook runs with one pinned validation environment first on
`PATH`, named by the Git option `hyhome.validationVenv`. Build it once per
account, outside every checkout, from the hashed lock:

```bash
umask 022 && python3 -m venv "$HOME/.venvs/hyhome-validation"
"$HOME/.venvs/hyhome-validation/bin/python" -m pip install --only-binary :all: \
  --require-hashes -r .github/requirements/ci-validation.txt
git config --global hyhome.validationVenv "$HOME/.venvs/hyhome-validation"
```

The chain refuses the workspace hook with `HOOK-ENV` when the option is unset
or empty, or when the environment lies inside a worktree. It also refuses an
environment that lacks an executable `bin/python3` or `bin/pre-commit`, or
whose files are writable by group or other, or owned by another account.
Git configuration is not tracked, so a commit under review cannot choose the
environment. Rebuild the environment when the lock changes; the chain does not
compare it with the lock. The pin covers the hook's interpreter, pre-commit,
the `language: system` Python entries, `scripts/qa.py` and the Python gates it
runs. It does not cover shell validators, which use the closed system `PATH`
`scripts/qa.py` builds, or `language: python` hooks, which use pre-commit's own
environments. Unsetting the option blocks the hook, so it is no way around a
check.

If the same message is not checked by an active commit-msg hook, validate the
actual UTF-8 message file in the pinned validation environment before
committing:

```bash
pre-commit run commitizen --hook-stage commit-msg --commit-msg-filename "$MESSAGE_FILE"
pre-commit run commit-message-exceptions --hook-stage commit-msg --commit-msg-filename "$MESSAGE_FILE"
```

Both checks must succeed on that same file. Use that file
for the real commit. When unrelated unstaged configuration would
make pre-commit stash or refuse, use an isolated temporary Git repository with
the index's Commitizen pin, `.cz.toml`, exception guard and both hook registrations,
and the same candidate message. This
is explicit message evidence, not proof of hook installation or delivery in
the source repository. Never change hooksPath, disable a hook, or set a skip
variable in order to make a failing check pass or to leave a check unrun;
widening the set of hooks that run is the only supported change.

### Enforcement

Inspect both staged and unstaged diffs after formatters. Rerun the affected
checks against final bytes. Do not claim a remote check ran from a local workflow-syntax result.

## Exceptions

### Exception Conditions

Exception and escalation conditions are stated under Requirements.

### Approval and Review

Approval and review conditions are stated under Requirements.

## Ownership

### Responsibilities

Responsibilities are stated under Authority and Requirements.

### Change and Adoption

This policy changes as a governed-document change under the work lifecycle and the document lifecycle policy, with no adoption step of its own; if it needs one, state it here.
