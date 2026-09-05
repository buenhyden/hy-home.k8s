---
title: "Agent Governance and Quality Gate Consolidation Implementation Plan"
version: "2.0.1"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0072-PLAN-0001"
---

# Agent Governance and Quality Gate Consolidation Implementation Plan

## Overview

Revise SPEC-0072 around the latest user-authorized common `.agents/` authority.
Use Superpowers executing-plans and its review checkpoints. The original
Stage 00 consolidation is baseline history, not the implementation target.
The owning Task records execution evidence; this plan owns ordered work only.

## Context

The verified local and remote main baseline is
`eb4fcfe3283115388d6eb1f31d56780b3e578f77`. The clean checkout was branched as
`codex/common-agents-authority`; no user changes were staged or moved. Two
existing stashes remain untouched. Main already contains QA consolidation.
The old hub has 53 tracked files; an ignored Python cache is a separate local
artifact. Provider local settings and notes are private excluded content.

The authority-location request supersedes earlier instructions to remove
`.agents/`. The subsequent user request authorizes local staging, commits and
review of remaining work. Merge, push, PR, deployment, credentials, global
configuration, paid provider calls and new trust grants remain unauthorized.
Protected-path writes must use the normal scoped sandbox approval mechanism.

## Goals & In-Scope

- Dispose of every old-hub source with purpose, incoming/outgoing references,
  destination, retained meaning, provenance and verification in the Task.
- Migrate policies and normative SDLC to `.agents/governance/`, neutral roles
  and registry/schema to `.agents/roles/`, callable packages to
  `.agents/skills/`, and two ordinary procedures to `.agents/workflows/`.
- Rehome provider differences to `.claude/provider.md` and `.codex/provider.md`.
  Preserve native role paths and update explicit reads and Claude skill links.
- Include the hidden authority in document, language, formatting, ownership,
  secret and QA scope. Reject the old root and invalid new role/skill graphs.
- Preserve GitOps boundaries, bounded QA, immutable historical source evidence,
  memory retirement and all current permission restrictions.

## Non-Goals & Out-of-Scope

No cluster/manifests/Helm/Argo CD/Vault changes, global installation, model
upgrades, native hooks activation, general generator, duplicate registry,
new memory directory or remote integration. Native/provider and
hosted checks requiring absent authority remain NOT_RUN with reasons.

## Work Breakdown

### WP-001: Reconcile design and protect source evidence

- [ ] Read every source; attach the complete per-file disposition and folder
  decision tables to the existing Task, including ignored cache disposition.
- [ ] Update Spec criteria and add a narrowly superseding ADR for the authority
  location and skill discovery decision. Preserve ADR-0034 QA/CD decisions.
- [ ] Obtain a separate read-only review of this plan and source disposition;
  resolve missing consumers, history handling and unsafe skill instructions.

Read-only reviewer `migration_plan_review` confirmed all 53 source hashes and
unique destinations. Its required corrections are part of WP-002/003: closed
package/link/sidecar sets, explicit memory retirement, corrected unsafe skill
steps, destination-first writes and sealed-record preservation. No external
review approval or runtime success is inferred.

### WP-002: Transition the authority and native consumers together

- [ ] Add failing tests in `tests/test_agent_governance.py` for the new root,
  old-root rejection including dangling links, role/skill references, duplicate
  skill names, metadata, external symlinks and unchanged permission denial.
- [ ] Move only mapped files after checking their baseline bytes. Update
  `REGISTRY_PATH`, `REGISTRY_SCHEMA_PATH`, `REGISTRY_PROJECTION_ROOTS`, schema,
  role references and provider adapters as one atomic transition.
- [ ] Replace Codex `@` pseudo-imports with explicit reads. Claude imports
  only shared instructions and Claude guidance, never the Codex entrypoint.
  Expose Claude skills through individually validated relative links.
- [ ] Preserve any existing SKILL IDs/status in string-valued `metadata` (none existed in the baseline packages); require native
  name and description. Use explicit-only invocation metadata for skills
  newly exposed by Codex and correct instructions that request secrets,
  unapproved communications, persistent scratch state or unauthorized writes.
- [ ] Preserve `.claude/settings.json` permissions and write-hook behavior;
  update path roots only. No Codex hook/config directory is created.

### WP-003: Transition document, QA and historical consumers

- [ ] Change Stage 99 path profiles and `scripts/document_contracts.py` scope
  together; keep English-only and native-format exceptions precise.
- [ ] Update `scripts/validation/registry.json`, repository-quality path rules,
  narrow pre-commit selectors, README/ownership/navigation and tests so hidden
  governance participates in all corresponding existing gates.
- [ ] Preserve historical source commit/blob/hash fields. Update current
  replacement endpoints through the existing archive contract, not a second
  ledger or fallback to the retired tree. Repair active historical executable
  instructions with an explicit supersession note; do not alter past results.
- [ ] Diagnose baseline full-QA failures at their owners: unavailable historical
  replacement, workflow responsibility inventory, unittest package discovery
  and required pre-commit executable resolution. Keep execution limits and
  trusted executable resolution; missing prerequisites remain failures.

### WP-004: Verify final bytes and record limits

- [ ] Run focused tests after each changed contract; use temporary repositories
  for denial/error/path tests without reverting user files.
- [ ] Run `python3 scripts/validate-agent-governance.py --root .`, document and
  link validators, then `python3 scripts/qa.py full` over final bytes.
  Do not separately repeat the full suite or its pre-commit gate unchanged.
- [ ] Verify old-root lstat absence, zero functional old consumers, all residual
  historical/negative-test strings classified, exact permission parity, no
  manifest changes, and preservation of unrelated index content. Re-run deterministic
  synchronization only if an actual generator is introduced; none is planned.
- [ ] Record syntax/contracts separately from native discovery/invocation,
  permissions/hooks, hosted CI and live infrastructure. Keep branch/worktree.
- [ ] Stage only the reviewed transition paths using a NUL-delimited manifest;
  run `python3 scripts/qa.py staged`, repository pre-commit and commit-message
  validation, inspect the cached diff, and commit with active hooks enabled.
- [ ] Review WORK-004 next: inspect installed native discovery interfaces
  without paid calls, authentication access or trust changes. Record actual
  native evidence separately and retain hosted/runtime blockers that remain.

## Verification Plan

The baseline direct governance command exits 1 at the retired-path rule because
of the sandbox's empty `.agents/` directory. Baseline full QA exits 1 after
219.932 seconds with six failing gates; full details belong to the Task.

Focused tests must first reject the unmodified old topology for the expected
reason, then pass the migrated tree and continue rejecting permissions widened
to broad shell access, external links, malformed metadata and old-root revival.

`full` remains the final repository-static entrypoint; `ci` gate membership
stays equal without a redundant local execution. Staged validation is now
required for the user-authorized local commits; it reads the index snapshot.
The current session loaded old gateways; re-reading cannot prove new-session
native loading. No authenticated provider call is authorized.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Protected `.agents/` write is denied | Request only mapped paths through normal approval; keep source until the transition can be completed |
| Auto-discovery exposes dangerous steps | Explicit-only metadata plus role/user approval preconditions; never grant tools through skill metadata |
| Historic evidence loses provenance | Keep source commits and hashes; distinguish current link endpoints from past observations |
| QA omits hidden paths | Negative scope tests and shared registry/profile updates |
| Migration interrupted | Byte-checked per-file mapping and no overwriting unknown files; no compatibility authority |
| Rollback requested | Reverse only the reviewed mapped transition as a new change after checking later user edits and dependent commits; no blanket restore/reset or history rewrite |

## Completion Criteria

- `.agents/` is the single common authority and every one of the 53 source files
  has an explicit disposition; the old root has no file, directory or link.
- All active functional references resolve to current owners; residual source
  evidence and denial-test mentions are classified instead of concealed.
- Role IDs, permissions, models and handoffs retain their original meanings.
- Native skill metadata and loader paths are valid; actual runtime levels are
  reported only when observed, otherwise NOT_RUN with a reason.
- Required focused and full static checks pass. A failure remains incomplete.
- Only reviewed transition paths enter local commits; private local state and
  existing stashes remain unchanged. No remote integration is performed.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AGQ-001](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-002](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-003](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-004](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-005](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-006](spec.md#success-criteria--verification-plan) | WP-004 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-007](spec.md#success-criteria--verification-plan) | WP-004 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-008](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
