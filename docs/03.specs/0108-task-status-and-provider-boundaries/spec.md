---
title: "Task Status Derivation and Provider Boundaries"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0108"
---

# Task Status Derivation and Provider Boundaries Technical Specification (Spec)

## Overview

This package applies the v9 execution prompt findings K-P1 (F03, F29), K-P2
(F22, F40, F42) and F25 that the operator selected on 2026-10-13. A
multi-row Task stops carrying a hand-synchronized frontmatter summary,
README files under the provider roots follow their Korean-first navigation
profile, and requested push, merge and pull-request commands move from a
blanket Claude denial to a per-call prompt. Consumers are the Stage 99
Registry, the Markdown, link and lifecycle validators, the Task template and
the Claude native settings.
The [Plan](plan.md) orders three work units, and
[Task 0001](tasks/tsk-0001-task-status-and-provider-boundaries.md) records
their execution and acceptance.

## Strategic Boundaries & Non-goals

- In scope: Task summary derivation and the retirement of
  `scripts/sync-task-status.py`; the README exception to the English-only
  roots and the Korean body of `.agents/roles/README.md`; the Claude
  `ask` list for the plain remote publish, local merge and pull-request
  create and merge commands named in `.claude/settings.json`.
- Non-goals: rewriting historical Task status, translating the other eight
  provider-root READMEs in this package, the shared memory store (its design
  belongs to [SPEC-0109](../0109-shared-workspace-memory/spec.md)), Codex
  configuration, K-P0, K-P3 beyond F25, K-P4 and K-P5.
- Protected surfaces: force, delete and mirror pushes, release creation,
  workflow dispatch, live Kubernetes, Argo CD and Vault commands stay denied.

## Contracts

- A single-row Task keeps the literal `frontmatter` Status marker and a
  required frontmatter `status`.
- A multi-row Task may omit frontmatter `status`. Every reader derives the
  summary from the rows with `derive_task_summary`. A present value must
  still equal the derivation, so recorded history stays valid.
- An unreadable current Task table yields no derived status and fails as a
  missing status rather than passing.
- A `README.md` under `.agents/`, `.claude/` or `.codex/` follows its
  navigation profile language; every other file under those roots remains
  English only. Untranslated READMEs are listed in the language contract's
  `pending_paths` until they pass.
- Claude permissions are exactly the validated allow, ask and deny lists.
  The ask entries grant no approval; the user still answers each prompt.

## Core Design

`document_contracts.task_status(metadata, text, profile)` is the single
reader helper. It returns the frontmatter value when present, otherwise the
row derivation for a multi-row current Task table, otherwise an empty
string. `document_lifecycle.document_from_text`, the Markdown profile,
cancellation and terminal-language checks and the link validator's body
and reciprocal enforcement all call it, so an omitted summary never
disables a check. `DocumentLanguage.english_only(path)` is the single
English-only predicate shared by language classification and tracked-file
collection.

## Data Modeling & Storage Strategy

The `sdlc/task` and `common/template-sdlc-task` profiles list `status` as
optional; the shared frontmatter schema no longer requires it globally,
while every other profile still requires it through its Registry key set.
No stored document is migrated.

## Interfaces & Data Structures

- `task_status(metadata: Mapping, text: str, profile: DocumentProfile) -> str`
- `task_execution_issues(rows, status, binding)` treats `status == ""` on a
  multi-row Task as an omitted summary and on a single-row Task as an
  invalid status.
- `DocumentLanguage.english_only(path: PurePosixPath) -> bool`
- `.claude/settings.json` `permissions` keys: `allow`, `ask`, `deny`.

## Edge Cases & Error Handling

Incompatible superseded row mixtures, unknown row states and malformed
tables derive no status. A single-row Task without status reports
`TASK-EXECUTION-STATUS`. A pending README that starts passing reports
`LANG-PENDING` until it is removed from the list.

## Failure Modes & Fallback / Human Escalation

Rollback is a forward revert of the package commits. A Claude client that
does not honor `ask` falls back to its default permission mode; the deny
list still blocks the protected variants.

## Verification Commands

- `python3 -m unittest tests.test_task_execution_contract tests.test_task_summary_derivation tests.test_document_language tests.test_document_scope_selection tests.test_agent_governance`
- `python3 scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`, `scripts/validate-document-contract-registry.py`, `scripts/validate-agent-governance.py`
- `python3 scripts/qa.py staged` on each logical commit's exact index.

These are repository-static checks. They do not show that a Claude client
actually prompts for an `ask` entry.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-TSKSUM-001 | Focused tests show an omitted multi-row summary is derived identically by lifecycle, profile and link readers, a mismatched present summary and a status-less single row still fail, and the writer, its CLI tests and registrations are removed with derivation coverage kept. |
| VAL-TSKSUM-002 | Language tests and the profile validator show provider-root READMEs follow their profile, non-README files stay English only, `.agents/roles/README.md` passes Korean-first and the remaining READMEs are pending (point-in-time; SPEC-0110 later translated them and emptied `pending_paths`). |
| VAL-TSKSUM-003 | The governance validator requires the exact allow, ask and deny lists and rejects a lost or widened ask entry; protected push variants remain denied. Native prompting stays unobserved. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TSKSUM-001 | Task execution owns state once; [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) writer retirement after consumer-zero; focused regression. |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TSKSUM-002 | README purpose and language; [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) single language owner; language tests. |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TSKSUM-003 | Explicit approval boundary for remote writes; [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) repository-declared versus runtime evidence; governance validator tests. |
