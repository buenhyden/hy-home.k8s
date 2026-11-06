---
title: "Hook-Delivered Folder Agent Rules"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0149"
---

# Hook-Delivered Folder Agent Rules Technical Specification (Spec)

## Overview

On 2026-11-06 the operator required that both Claude and Codex read the
`AGENTS.md` of each folder they work in. Claude Code 2.1.319 loads no
`AGENTS.md` while a `CLAUDE.md` exists, and its setting to load both is
ignored in project settings; Codex 0.166.0 loads only the root-to-cwd chain at
session start. The shared pre-action guard already sees every structured
write for both providers, but it reports through `systemMessage`, which
Claude shows to the user and not to the model (AUD-0001 F-08). A provider
hook change needs this package. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-agents-md-hook-context.md) records it.

## Strategic Boundaries & Non-goals

- In scope: `scripts/provider_write_guard.py` output, its tests in
  `tests/test_k8s_pre_edit_hook.py`, the AGENTS.md loading statements in
  `.claude/provider.md`, `.codex/provider.md` and
  `.agents/governance/agent-execution.md`, and an AUD-0001 addendum.
- Non-goals:
  - hook registrations in `.claude/settings.json` and `.codex/hooks.json`,
    so read-only tools stay uncovered and no hook re-review is triggered;
  - the root `AGENTS.md`, which is the Codex gateway: Claude gets its common
    core through `CLAUDE.md` and Codex loads it natively;
  - nested `CLAUDE.md` files or user-level settings;
  - any change to what the guard allows or blocks.
- Open questions: none that change a criterion. Codex delivery of the new
  field is unobserved until the Codex usage limit resets (2026-11-09).

## Contracts

- For each structured, patch or shell write target, the guard adds every
  existing `AGENTS.md` from the first folder below the repository root down
  to the target's folder, each with its repository path and full text.
- Model context is emitted as `hookSpecificOutput` with
  `hookEventName: "PreToolUse"` and `additionalContext`; the existing
  `systemMessage` stays as it is.
- Within one `session_id` a file is supplied once, and again only after its
  content changes. Without a `session_id` every call supplies the chain.
- Supplied text is bounded; any file beyond the bound is named with an
  instruction to read it explicitly.
- Allow and block decisions, exit codes and stderr reasons are unchanged.

## Core Design

The guard already resolves every target to a repository-relative path under
one root. It walks each target's parent folders, reads each `AGENTS.md`
through the existing symlink-safe file check, and records the supplied path
and content hash in a per-session state file under the system temporary
directory (folder mode 0700). A state-file failure only disables
deduplication; it never blocks a write. Constraining architecture:
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) keeps provider adapters thin and shared controls in one owner, which
this change keeps by staying in the shared guard.

## Data Modeling & Storage Strategy

One JSON state file per session and repository root, named by a SHA-256 of
both, holding `{"supplied": {"<path>": "<sha256>"}}`. It is temporary,
secret-free and safe to delete.

## Interfaces & Data Structures

Hook stdout gains `{"hookSpecificOutput": {"hookEventName": "PreToolUse",
"additionalContext": "..."}}` beside `systemMessage`. Hook stdin keeps its
current fields; `session_id` is read when present.

## Edge Cases & Error Handling

- Normal: a first write under `docs/03.specs/` supplies `docs/AGENTS.md` and
  `docs/03.specs/AGENTS.md`; a second write in the same session supplies none.
- Boundary: a target at the repository root supplies no folder file; a
  changed `AGENTS.md` is supplied again.
- Error: an unreadable or symlinked `AGENTS.md` is named, not read, and the
  write decision is unchanged.

## Failure Modes & Fallback / Human Escalation

If a provider rejects the new field, the hook fails and its write is
refused; revert the implementing commit. Explicit `AGENTS.md` reads remain
required by policy for read-only work.

## Verification Commands

- `python3 -m unittest tests.test_k8s_pre_edit_hook`
- the strict registry, Markdown-profile, link and lifecycle checks
- `python3 scripts/qa.py staged` on each commit
- an observed Claude write in this session after the change

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-HOOK-001 | Focused tests fail before and pass after: the chain, root exclusion, once-per-session supply, re-supply after change and the unchanged decisions |
| VAL-HOOK-002 | A Claude write after the change shows the supplied `AGENTS.md` text in the model context |
| VAL-HOOK-003 | Both provider notes and `agent-execution.md` state the new loading contract; an AUD-0001 addendum records F-08; strict checks PASS |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HOOK-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Focused tests red then green |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HOOK-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Observed provider-runtime evidence |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HOOK-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict document checks and review |
