---
title: "Folder CLAUDE.md Imports"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0151"
---

# Folder CLAUDE.md Imports Technical Specification (Spec)

## Overview

SPEC-0149 gave Claude folder `AGENTS.md` rules through the write hook only,
so reads were uncovered and rules supplied before a context compaction were
not supplied again. Claude Code loads a folder `CLAUDE.md` once Claude reads,
writes or edits a file in that folder, reloads it on demand after a
compaction, and resolves its `@path` imports relative to the file (memory
documentation, read 2026-11-06). On 2026-11-06 the operator asked to adopt a
folder `CLAUDE.md` holding `@AGENTS.md`. A Stage 99 profile, validator and
provider change needs this package. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-folder-claude-imports.md) records it.

## Strategic Boundaries & Non-goals

- In scope: one `CLAUDE.md` beside each of the 15 folder `AGENTS.md` files;
  a `common/folder-claude-import` profile in `docs/99.templates/registry.json`;
  a pairing and content check in `scripts/validation/repository/quality.py`;
  the guard's folder chain limited to Codex; the `AGENTS.md` statements in
  `.claude/provider.md`, `.codex/provider.md` and
  `.agents/governance/agent-execution.md`; the AUD-0001 m0002 draft row.
- Non-goals:
  - the root `CLAUDE.md` and root `AGENTS.md` (the Codex gateway);
  - `.claude/CLAUDE.md` and anything below `docs/98.archive/`;
  - user-level settings and hook registrations.
- Open questions: none that change a criterion. Whether an `AGENTS.md` edited
  mid-session is picked up is undocumented and left unclaimed.

## Contracts

- Every tracked folder `AGENTS.md` outside `docs/98.archive/` has a sibling
  `CLAUDE.md` whose whole content is `@AGENTS.md` and a newline, and every
  folder `CLAUDE.md` other than `.claude/CLAUDE.md` has a sibling
  `AGENTS.md`; the repository quality check refuses any gap.
- Each folder `CLAUDE.md` maps to exactly one registry profile.
- The shared guard supplies the folder `AGENTS.md` chain only to Codex; both
  providers keep its model-visible guidance.

## Core Design

Claude's native nested loading replaces the hook path for Claude, which
covers reads and compaction reloads without repository code. Codex ignores
`CLAUDE.md` and keeps the hook path. Constraining architecture: [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
keeps provider adapters thin and document forms in the Stage 99 registry;
this change adds one native profile and keeps the shared guard as the only
cross-provider control.

## Data Modeling & Storage Strategy

No data changes beyond one registry profile.

## Interfaces & Data Structures

One registry profile; one quality diagnostic family for missing or
malformed folder `CLAUDE.md` files.

## Edge Cases & Error Handling

- Normal: a read in `docs/05.operations/` loads that folder's `AGENTS.md`.
- Error: a folder `AGENTS.md` without its `CLAUDE.md`, a `CLAUDE.md` with
  other content, or one without an `AGENTS.md` is refused.
- Boundary: `.claude/CLAUDE.md` and the root files are untouched.

## Failure Modes & Fallback / Human Escalation

If Claude does not load a folder `CLAUDE.md`, explicit reads remain
required by policy; revert the guard change to restore hook delivery.

## Verification Commands

- `python3 -m unittest tests.test_repository_quality_rules tests.test_k8s_pre_edit_hook`
- the strict registry, Markdown-profile, link and lifecycle checks
- `python3 scripts/qa.py staged` on each commit
- a new Claude session that only reads a file in an untouched folder

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-CLI-001 | Focused tests fail before and pass after: pairing and content gaps refused, Codex alone gets the guard's folder chain |
| VAL-CLI-002 | The 15 files, the profile, provider notes and policy are in place; strict checks and staged QA PASS |
| VAL-CLI-003 | A new Claude session that only reads a file in an untouched folder shows that folder's `AGENTS.md` text in its context |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CLI-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Focused tests red then green |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CLI-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict checks and staged QA |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CLI-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Observed provider-runtime evidence |
